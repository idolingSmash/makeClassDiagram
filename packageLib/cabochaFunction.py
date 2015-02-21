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
def isHaGa(xmlStr):
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
def isHa(xmlStr):
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
		simpleSentenceList.append(chunkSrcList[prevIdx:idx + 1])
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
def isHa(tokenList):
	flag = False
	for tokenItem in tokenList:
		hinshiList = tokenItem.attrib['feature'].split(',')
		if hinshiList[0] == u"助詞" and hinshiList[1] == u"係助詞" and tokenItem.text == u"は":
			flag = True
	return flag

"""
	ハ格を取得
"""
def getHa(chunkList):
	haWord = ""
	for chunkUnit in chunkList:
		xmlTokenData = lxml.fromstring(lxml.tostring(chunkUnit)).xpath('//chunk/tok')
		if isHa(xmlTokenData):
			haWord = getCharacter(xmlTokenData)
	return haWord


"""
	ハ格であるか？
"""
def isGa(tokenList):
	flag = False
	for tokenItem in tokenList:
		hinshiList = tokenItem.attrib['feature'].split(',')
		if hinshiList[0] == u"助詞" and hinshiList[1] == u"格助詞" and tokenItem.text == u"が":
			flag = True
	return flag

"""
	ハ格を取得
"""
def getGa(chunkList):
	gaWord = ""
	for chunkUnit in chunkList:
		xmlTokenData = lxml.fromstring(lxml.tostring(chunkUnit)).xpath('//chunk/tok')
		if isGa(xmlTokenData):
			gaWord = getCharacter(xmlTokenData)
	return gaWord

"""
	二格であるか？
"""
def isNi(tokenList):
	flag = False
	for tokenItem in tokenList:
		hinshiList = tokenItem.attrib['feature'].split(',')
		if hinshiList[0] == u"助詞" and hinshiList[1] == u"格助詞" and tokenItem.text == u"に":
			flag = True
	return flag

"""
	二格を取得
"""
def getNi(chunkList):
	niWord = ""
	for chunkUnit in chunkList:
		xmlTokenData = lxml.fromstring(lxml.tostring(chunkUnit)).xpath('//chunk/tok')
		if isNi(xmlTokenData):
			niWord = getCharacter(xmlTokenData)
	return niWord

"""
	ヲ格であるか？
"""
def isWo(tokenList):
	flag = False
	for tokenItem in tokenList:
		hinshiList = tokenItem.attrib['feature'].split(',')
		if hinshiList[0] == u"助詞" and hinshiList[1] == u"格助詞" and tokenItem.text == u"を":
			flag = True
	return flag

"""
	ヲ格を取得
"""
def getWo(chunkList):
	woWord = ""
	for chunkUnit in chunkList:
		xmlTokenData = lxml.fromstring(lxml.tostring(chunkUnit)).xpath('//chunk/tok')
		if isWo(xmlTokenData):
			woWord = getCharacter(xmlTokenData)
	return woWord

"""
	動詞はあるか？
"""
def isVerb(chunkList):
	flag = False
	for chunkUnit in chunkList:
		tokenList = lxml.fromstring(lxml.tostring(chunkUnit)).xpath('//chunk/tok')
		for tokenItem in tokenList:
			hinshiList = tokenItem.attrib['feature'].split(',')
			if hinshiList[0] == u"動詞" and hinshiList[1] == u"自立":
				flag = True
	return flag

"""
	動詞を取得
"""
def getVerb(chunkList):
	verbWord = ""
	for chunkUnit in chunkList:
		tokenList = lxml.fromstring(lxml.tostring(chunkUnit)).xpath('//chunk/tok')
		for tokenItem in tokenList:
			hinshiList = tokenItem.attrib['feature'].split(',')
			if hinshiList[0] == u"動詞" and hinshiList[1] == u"自立":
				verbWord = tokenItem.text
	return verbWord

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
			if isHaGa(chunkItem):
				if isCharacter(chunkItem):
					contents = __getCharacter(chunkItem)
					if not contents in actorList:
						actorList.append(contents)
	return actorList

"""
	文章内照応解析用の辞書に保管
"""
def insertSRL(sentenceUnit):
	dictElement = {}
	dictElement[u"SubjectHa"] = getHa(sentenceUnit)
	dictElement[u"SubjectGa"] = getGa(sentenceUnit)
	dictElement[u"ObjectWo"] = getWo(sentenceUnit)
	dictElement[u"ObjectNi"] = getNi(sentenceUnit)
	return dictElement

"""
	文章内照応解析用の辞書から対象の主語を取得
	優先順位　ハ格　＞　ガ格　＞　二格　＞　ヲ格
"""
def getSubjectFromSRL(dictElement):
	subject = u""
	if dictElement[u"SubjectHa"] != "":
		subject = dictElement[u"SubjectHa"]
	elif dictElement[u"SubjectHa"] == "" and dictElement[u"SubjectGa"] != "":
		subject = dictElement[u"SubjectGa"]
	elif dictElement[u"SubjectHa"] == "" and dictElement[u"SubjectGa"] == "" and\
		dictElement[u"ObjectWo"] != "":
		subject = dictElement[u"ObjectWo"]
	else :
		subject = dictElement[u"ObjectNi"]
	return subject

"""
	SRLの更新
	新しい要素がある場合はマージして置換する
"""
def mergeSRL(prevDict, nextDict):
	if nextDict[u"SubjectHa"] != u"":
		prevDict[u"SubjectHa"] = nextDict[u"SubjectHa"]
	if nextDict[u"SubjectGa"] != u"":
		prevDict[u"SubjectGa"] = nextDict[u"SubjectGa"]
	if nextDict[u"ObjectNi"] != u"":
		prevDict[u"ObjectNi"] = nextDict[u"ObjectNi"]
	if nextDict[u"ObjectWo"] != u"":
		prevDict[u"ObjectWo"] = nextDict[u"ObjectWo"]
	return prevDict


"""
	省略された主語・目的語を補う
"""
def supportNoun(pumpkinCake, sentenceList):
	outputList = []
	pointList = [] #単文の分割
	iterVerbWord = ""
	prevSRL = {}
	nextSRL = {}
	SRLInSentence = {u"SubjectHa":u"", u"SubjectGa":u"", u"ObjectNi":u"", u"ObjectWo":u""}
 	for idx, nimono in enumerate(pumpkinCake):
		parseXML = lxml.fromstring(nimono)
		if parseXML.xpath('//sentence')[0].attrib['structure'] == u"stageDirections":
			simpleSentenceList = divideSimpleSentenceList(parseXML)
			for i,sentenceUnit in enumerate(simpleSentenceList):
				nextSRL = insertSRL(sentenceUnit)
				if i != 0 and isVerb(sentenceUnit):
					if nextSRL[u"SubjectHa"] == u"" and nextSRL[u"SubjectGa"] == u"":
						startIdx = sentenceList[idx].find(getVerb(sentenceUnit))
						insertSubject = getSubjectFromSRL(prevSRL)
						if insertSubject != u"":
							print sentenceList[idx][:startIdx] + u"『" + insertSubject + u"は』" + sentenceList[idx][startIdx:]
				prevSRL = mergeSRL(prevSRL,nextSRL)

	return outputList