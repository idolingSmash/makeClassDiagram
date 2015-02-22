#!/usr/bin/python
# -*- coding: utf-8 -*-

import packageLib.constDictionary as dic
import packageLib.constList as lis
import packageLib.constClass as cls
import packageLib.commonFunction as comm
import packageLib.elementTreeFunction as etFunc
import packageLib.cabochaFunction as pump

import os.path
import re
import sys
import codecs
import uuid
from collections import OrderedDict
from xml.etree.ElementTree import Element, SubElement, Comment, tostring
from xml.etree import ElementTree
from xml.dom import minidom
from lxml import etree as lxml
import lxml.builder as builder
from bs4 import BeautifulSoup

xmlFilePath = u"test.xml"

"""
	header部を作成
"""
def makeHeader(ptree):
	parentsTree = SubElement(ptree, u'XMI.header')
	docTree = SubElement(parentsTree, u"XMI.documentation")
	metaTree = SubElement(parentsTree, u"XMI.metamodel")
	attriMetaDic = {u"xmi.name":u"UML", u"xmi.version":u"1.4"}
	etFunc.setAttributeInTag(metaTree, attriMetaDic)
	for lineItem in lis.tagXmiHeader:
		valTree = SubElement(docTree, lineItem[0])
		valTree.text = lineItem[1]
	verTree = SubElement(SubElement(docTree, u"XMI.sortedVersionHistories"), u"XMI.versionEntry")
	verTree.set(u"productVersion", u"professional 6.7.0")
	verTree.set(u"modelVersion",u"36")
	return parentsTree

"""
	header部を作成
"""
def _makeHeader(ptree):
	parentsTree = lxml.Element(u'XMI.header')
	ptree.extend([parentsTree])
	return ptree

"""
	body部-taggedValueを作成
"""
def makeTaggedValue(cdTree, splitList):
	listAttriKey = [u"xmi.id", u"version", u"tag", u"value"]
	for spItem in splitList:
		childTree = SubElement(cdTree, u"UML:TaggedValue")
		slists = spItem.split(",")
		for i,keyItem in enumerate(listAttriKey):
			if i == 0:
				childTree.set(keyItem, slists[i] + dic.attriXmiModel[u"xmi.id"][2:])
			else :
				childTree.set(keyItem, slists[i])
		gchildTree = SubElement(childTree, u"UML:TaggedValue.modelElement")
		g2childTree = SubElement(gchildTree, u"UML:ModelElement")
		g2childTree.set(u"xmi.idref", dic.attriXmiModel[u"xmi.id"])

"""
	body部-taggedValueを作成
"""
def makeOwnedElement(cdTree, cList):
	classChildTree = SubElement(cdTree, u"UML:Class")


"""
	body部を作成
		UML:Model
		UML:ModelElement.taggedValue
"""
def makeBodyProperty(cdTree, cList):
	umlModel = SubElement(cdTree, u'UML:Model')
	taggedValue = SubElement(umlModel, u"UML:ModelElement.taggedValue")
	ownedElement = SubElement(umlModel, u"UML:Namespace.ownedElement")
#	etFunc.setAttributeInTag(umlModel, dic.attriXmiModel)
	for item in lis.attriXmiModel : umlModel.set(item[0],item[1])
	extensionProperty = SubElement(umlModel, u'XMI.extension')
	customStyleMap = SubElement(extensionProperty, u'UML:Model.customStyleMap')
	for key, val in dic.modelCustomStyleMap.iteritems():	
		childTree = SubElement(customStyleMap, u"UML:Model.styleProperty")
		childTree.set(u"key",key)
		childTree.set(u"value",val)
	makeTaggedValue(taggedValue, lis.taggedValueModelElement)
	makeOwnedElement(ownedElement, cList)
		

"""
	body部-Diagramを作成
"""
def makeDiagram(cdTree, cList):
	ptree = SubElement(cdTree, u'XMI.extension')

"""
	body部を作成
"""
def makeBody(cdTree, cList):
	Body = SubElement(cdTree, u'XMI.content')
	makeBodyProperty(Body, cList)
	makeDiagram(Body, cList)


"""
	クラス図ダイアグラムを作成
"""
def makeClassDiagram(cList):
	parents = Element(u'XMI')
	attriXmiVersionTapple = ((u"xmi.version",u"1.1"),
							(u"xmlns:JUDE",u"http://objectclub.esm.co.jp/Jude/namespace/"),
							(u"xmlns:UML",u"org.omg.xmi.namespace.UML"))
	dd = OrderedDict(attriXmiVersionTapple)
	for item in dd:
		parents.set(item, dd[item])

#	NS = 'http://objectclub.esm.co.jp/Jude/namespace/'
#	location_attribute = '{%s}noNameSpaceSchemaLocation' % NS
#	NSMAP = { u"JUDE":u"http://objectclub.esm.co.jp/Jude/namespace/",
#						u"UML":u"org.omg.xmi.namespace.UML"}
#	parents = lxml.Element(u'XMI', OrderedDict([(u'xmi.version',u'1.1')]), nsmap = NSMAP )
#	parents.set(nsmap = NSMAP)
	makeHeader(parents)
#	makeBody(cdTree, cList)	
	return parents

"""
	xmlを出力
		lxmlでの出力
		属性がappendした順番でなかったため一時中止
"""
def _outputXML(cdTree):
	tree = lxml.fromstring(cdTree)
	with open(xmlFilePath, "w") as f:
		f.write(lxml.tostring(tree, pretty_print = True, xml_declaration = True, encoding='UTF-8', standalone="yes"))

"""
	xmlを出力
"""
def outputXML(cdTree):
	fout = codecs.open(xmlFilePath, 'w', 'utf-8' )
	firstSentence = u'<?xml version=\'1.0\' encoding=\'UTF-8\' standalone=\'yes\'?>'
	xmlSentence = etFunc.prettify(cdTree).replace(u'<?xml version="1.0" ?>', u'')
	for item in firstSentence:
		fout.write(item)
	for item in xmlSentence:
		fout.write(item)
	fout.close() # ファイルを閉じる


if __name__ == "__main__":
#	print comm.convertURLEncode(u"千葉真一")
	
	paramPath = comm.getTextPathInCommandLine()
	textList = [item.strip() for item in comm.getReadLineList(paramPath)]
	title = textList[0]
	sentenceList = textList[2:]

	pumpkinCake = pump.makePumpkinCake(sentenceList) #cabocha処理(XML形式で出力)
	supportSentenceList = pump.supportNoun(pumpkinCake, sentenceList) #主語を補う
	pumpkinCakeBySupportSubject = pump.makePumpkinCake(supportSentenceList) #cabocha処理(XML形式で出力)
	characterList = pump.makeCharacterPackage(pumpkinCakeBySupportSubject, supportSentenceList) #classにパッケージ化


#	for ids in cl.iteritems():
#		print u"【" + ids[1].getClassName() + u"】"
#		print u"『属性』"
#		for item in ids[1].getAttribute(): print item
#		print u"『操作』"
#		for item in ids[1].getOperate(): print item
#		print u""
	outputXML(makeClassDiagram(characterList))


#getActor
#	actorList = pump.getActor(pumpkinCake) #登場人物を抽出
#	comm.printListItem(pumpkinCake)

