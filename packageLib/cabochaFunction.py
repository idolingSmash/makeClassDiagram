#!/usr/bin/python
# -*- coding: utf-8 -*-

import CaboCha
from lxml import etree as lxml
from bs4 import BeautifulSoup

"""
	sentenceタグにIDを付与
"""
def addSentenceID(xmlStr, idx):
	parseXML = lxml.fromstring(xmlStr)
	parseXML.xpath('//sentence')[0].set('id', str(idx))
	return lxml.tostring(parseXML, encoding="utf-8")

"""
	係り受け解析をする
"""
def makePumpkinCake(sentList):
	plist = []
	c = CaboCha.Parser()
	for i, nimono in enumerate(sentList):
		tree = c.parse(nimono.encode('utf-8'))
		plist.append(addSentenceID(tree.toString(CaboCha.FORMAT_XML), i))
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
def getCharacter(xmlStr):
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
	小説内の登場人物
	・助詞[は][が]を判定
	・名詞-一般or名詞-固有名詞の単語が存在するか
"""
def getActor(pumpList):
	actorList = []
	for sentItem in pumpList:
		soup = BeautifulSoup(sentItem)
 		chunkList = soup.find_all('chunk')
 		for chunkItem in chunkList:
			if isWaGa(chunkItem):
				if isCharacter(chunkItem):
					contents = getCharacter(chunkItem)
					if not contents in actorList:
						actorList.append(contents)
	return actorList


