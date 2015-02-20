#!/usr/bin/python
# -*- coding: utf-8 -*-

import re
import CaboCha
from lxml import etree as lxml
from bs4 import BeautifulSoup

"""
	グローバル変数
"""
SRL = {u"SubjectHa":u"", u"SubjectGa":u"", u"ObjectNi":u"", u"ObjectWo":u""}

"""
	sentenceタグにIDを付与
"""
def addSentenceID(xmlStr, idx):
	parseXML = lxml.fromstring(xmlStr)
	parseXML.xpath('//sentence')[0].set('id', str(idx))
	return lxml.tostring(parseXML, encoding="utf-8")

"""
	sentenceタグに文章のタイプを付与
		ト書き(stageDirections)	「」なし
		台詞(speech)　			「」あり
"""
def addSentenceStructureType(xmlStr, sentStr):
	parseXML = lxml.fromstring(xmlStr)
	structType = ""
	if not re.search(u"「*.」" , sentStr) is None:
		structType = u"speech"
	else :
		structType = u"stageDirections"
	parseXML.xpath('//sentence')[0].set('structure', structType)
	return lxml.tostring(parseXML, encoding="utf-8")

"""
	係り受け解析をする
"""
def makePumpkinCake(sentList):
	plist = []
	c = CaboCha.Parser()
	for i, nimono in enumerate(sentList):
		tree = c.parse(nimono.encode('utf-8'))
		xmlData = addSentenceID(tree.toString(CaboCha.FORMAT_XML), i)
		a = addSentenceStructureType(xmlData, nimono)
		plist.append(a)
	return plist

"""
	・助詞[は][が]を判定
"""
def isWaGa(xmlStr):
	flag = False
	tokenList = xmlStr.find_all('tok')
	for tokenItem in tokenList:
		if tokenItem.attrs['feature'].split(',')[0] == u"助詞" and \
			tokenItem.attrs['feature'].split(',')[1] == u"係助詞" and \
		  	tokenItem.text == u"は":
			flag = True
		elif tokenItem.attrs['feature'].split(',')[0] == u"助詞" and \
			tokenItem.attrs['feature'].split(',')[1] == u"格助詞" and \
			tokenItem.text == u"が":
		  	flag = True
	return flag

"""
	・助詞[は]を判定
"""
def isWa(xmlStr):
	flag = False
	tokenList = xmlStr.find_all('tok')
	for tokenItem in tokenList:
		if tokenItem.attrs['feature'].split(',')[0] == u"助詞" and \
			tokenItem.attrs['feature'].split(',')[1] == u"係助詞" and \
		  	tokenItem.text == u"は":
			flag = True
	return flag

"""
	・助詞[が]を判定
"""
def isGa(xmlStr):
	flag = False
	tokenList = xmlStr.find_all('tok')
	for tokenItem in tokenList:
		if tokenItem.attrs['feature'].split(',')[0] == u"助詞" and \
			tokenItem.attrs['feature'].split(',')[1] == u"格助詞" and \
			tokenItem.text == u"が":
		  	flag = True
	return flag

"""
	・「、」であるか判別(chunk内)
"""
def isDokuten(xmlStr):
	flag = False
	for tokenItem in xmlStr:
		hinshiList = tokenItem.attrib['feature'].split(',')
		if hinshiList[1] == u"読点":
			flag = True
	return flag

"""
	・「。」であるか判別(chunk内)
"""
def isKuten(xmlStr):
	flag = False
	for tokenItem in xmlStr:
		hinshiList = tokenItem.attrib['feature'].split(',')
		if hinshiList[1] == u"句点":
			flag = True
	return flag

"""
	・接続助詞であるか判別(chunk内)
"""
def isSetsuzokuJoshi(xmlStr):
	flag = False
	for tokenItem in xmlStr:
		hinshiList = tokenItem.attrib['feature'].split(',')
		if hinshiList[1] == u"接続助詞":
			flag = True
	return flag

"""
	・並列助詞であるか判別(chunk内)
"""
def isHeiretsuJoshi(xmlStr):
	flag = False
	for tokenItem in xmlStr:
		hinshiList = tokenItem.attrib['feature'].split(',')
		if hinshiList[1] == u"接続助詞":
			flag = True
	return flag

"""
	・名詞-一般or名詞-固有名詞の単語が存在するか
"""
def isCharacter(xmlStr):
	flag = False
	tokenList = xmlStr.find_all('tok')
	for tokenItem in tokenList:
		if tokenItem.attrs['feature'].split(',')[0] == u"名詞" and \
			tokenItem.attrs['feature'].split(',')[1] == u"一般":
			flag = True
		elif tokenItem.attrs['feature'].split(',')[0] == u"名詞" and \
			tokenItem.attrs['feature'].split(',')[1] == u"固有名詞":
		  	flag = True
	return flag	

"""
	・名詞-一般or名詞-固有名詞の単語を取得する
"""
def __getCharacter(xmlStr):
	actor = ""
	tokenList = xmlStr.find_all('tok')
	for tokenItem in tokenList:
		if tokenItem.attrs['feature'].split(',')[0] == u"名詞" and \
			tokenItem.attrs['feature'].split(',')[1] == u"一般":
			actor = tokenItem.string
		elif tokenItem.attrs['feature'].split(',')[0] == u"名詞" and \
			tokenItem.attrs['feature'].split(',')[1] == u"固有名詞":
		  	actor = tokenItem.string
	return actor

"""
	単文分割の分岐点
	・接続助詞 + 「、」 or 並列助詞 + 「、」 or link="-1" + 「。」 であるchunkIDを取得する
	・sentence単位
"""
def divideSimpleSentenceCheckPoint(xmlStr):
	chunkID = []
	for chunkItem in xmlStr.xpath('//sentence/chunk'):
		xmlTokenData = lxml.fromstring(lxml.tostring(chunkItem)).xpath('//chunk/tok')
		if isDokuten(xmlTokenData) and isSetsuzokuJoshi(xmlTokenData):
			chunkID.append(int(chunkItem.attrib['id'])) 
		elif isDokuten(xmlTokenData) and isHeiretsuJoshi(xmlTokenData):
			chunkID.append(int(chunkItem.attrib['id']))
		elif isKuten(xmlTokenData) and int(chunkItem.attrib['link']) != -1:
			chunkID.append(int(chunkItem.attrib['id']))
	return chunkID

"""
	分割した単文をリスト化
"""
def divideSimpleSentenceList(xmlStr):
	prevIdx = 0
	simpleSentenceList = []
	pointList = divideSimpleSentenceCheckPoint(xmlStr) #分岐点を取得
	chunkSrcList = xmlStr.xpath('//sentence/chunk')
	for idx in pointList:
		simpleSentenceList.append(chunkSrcList[prevIdx:idx])
		prevIdx = idx
	simpleSentenceList.append(chunkSrcList[prevIdx:])
	return simpleSentenceList

"""
	・名詞-一般or名詞-固有名詞の単語を取得する
"""
def getCharacter(tokenList):
	character = ""
	for tokenItem in tokenList:
		hinshiList = tokenItem.attrib['feature'].split(',')
		if hinshiList[0] == u"名詞" and hinshiList[1] == u"一般":
			character = tokenItem.text
		elif hinshiList[0] == u"名詞" and hinshiList[1] == u"固有名詞":
			character = tokenItem.text
	return character
"""
	ハ格であるか？
"""
def isWa(tokenList):
	flag = False
	for tokenItem in tokenList:
		hinshiList = tokenItem.attrib['feature'].split(',')
		if hinshiList[0] == u"助詞" and hinshiList[1] == u"係助詞" and tokenItem.text == u"は":
			flag = True
	return flag

"""
	ハ格を取得
"""
def getWa(chunkList):
	waWord = ""
	for chunkUnit in chunkList:
		xmlTokenData = lxml.fromstring(lxml.tostring(chunkUnit)).xpath('//chunk/tok')
		if isWa(xmlTokenData):
			waWord = getCharacter(xmlTokenData)
	return waWord

#			elif hinshiList[0] == u"助詞" and hinshiList[1] == u"格助詞" and tokenItem.text == u"が":
#				print u"が格あるで"


"""
	小説内の登場人物
	・助詞[は][が]を判定
	・名詞-一般or名詞-固有名詞の単語が存在するか
	***(後ほど修正！！！)
"""
def getActor(pumpList):
	actorList = []
	for sentItem in pumpList:
		soup = BeautifulSoup(sentItem)
 		chunkList = soup.find_all('chunk')
 		for chunkItem in chunkList:
			if isWaGa(chunkItem):
				if isCharacter(chunkItem):
					contents = __getCharacter(chunkItem)
					if not contents in actorList:
						actorList.append(contents)
	return actorList

"""
	省略された主語・目的語を補う
"""
def supportNoun(pumpkinCake, sentenceList):
	outputList = []
	pointList = [] #単文の分割
	SRLInSentence = {u"SubjectHa":u"", u"SubjectGa":u"", u"ObjectNi":u"", u"ObjectWo":u""}
 	for nimono in pumpkinCake:
		parseXML = lxml.fromstring(nimono)
		if parseXML.xpath('//sentence')[0].attrib['structure'] == u"stageDirections":
			simpleSentenceList = divideSimpleSentenceList(parseXML)
			for sentenceUnit in simpleSentenceList:
				wa = getWa(sentenceUnit)
				print wa
#				for chunkUnit in sentenceUnit:
#					xmlTokenData = lxml.fromstring(lxml.tostring(chunkUnit)).xpath('//chunk/tok')
#					for tokenItem in xmlTokenData:
#						hinshiList = tokenItem.attrib['feature'].split(',')
#						if hinshiList[0] == u"助詞" and hinshiList[1] == u"係助詞" and tokenItem.text == u"は":
#							print u"は格あるで"
#						elif hinshiList[0] == u"助詞" and hinshiList[1] == u"格助詞" and tokenItem.text == u"が":
#							print u"が格あるで"

#			for chunkItem in parseXML.xpath('//sentence/chunk'):
#				xmlTokenData = lxml.fromstring(lxml.tostring(chunkItem)).xpath('//chunk/tok')
#				if i < pointList[0]:
					
#				else :
#					pass

#					print tokenItem.attrib['feature'] + u' ' + tokenItem.text
#			SRL

	return outputList