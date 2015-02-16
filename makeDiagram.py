#!/usr/bin/python
# -*- coding: utf-8 -*-

import packageLib.constDictionary as dic
import packageLib.constList as lis
import packageLib.commonFunction as comm
import packageLib.elementTreeFunction as etFunc
import packageLib.cabochaFunction as pump

import os.path
import re
import sys
import codecs
from xml.etree.ElementTree import Element, SubElement, Comment, tostring
from xml.etree import ElementTree
from xml.dom import minidom
from lxml import etree

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
	body部を作成
		UML:Model
		UML:ModelElement.taggedValue
"""
def makeBodyProperty(cdTree):
	umlModel = SubElement(cdTree, u'UML:Model')
	taggedValue = SubElement(umlModel, u"UML:ModelElement.taggedValue")
	etFunc.setAttributeInTag(umlModel, dic.attriXmiModel)
	extensionProperty = SubElement(umlModel, u'XMI.extension')
	customStyleMap = SubElement(extensionProperty, u'UML:Model.customStyleMap')
	for key, val in dic.modelCustomStyleMap.iteritems():	
		childTree = SubElement(customStyleMap, u"UML:Model.styleProperty")
		childTree.set(u"key",key)
		childTree.set(u"value",val)
	makeTaggedValue(taggedValue, lis.taggedValueModelElement)
	SubElement(umlModel, u"UML:Namespace.ownedElement")	

"""
	body部-Diagramを作成
"""
def makeDiagram(cdTree):
	ptree = SubElement(cdTree, u'XMI.extension')

"""
	body部を作成
"""
def makeBody(cdTree):
	Body = SubElement(cdTree, u'XMI.content')
	makeBodyProperty(Body)
	makeDiagram(Body)


"""
	クラス図ダイアグラムを作成
"""
def makeClassDiagram(cdTree):	
	etFunc.setAttributeInTag(cdTree, dic.attriXmiVersion)
	makeHeader(cdTree)
	makeBody(cdTree)	
	return cdTree

"""
	xmlを出力
"""
def outputXML(cdTree):
	tree = etree.fromstring(cdTree)
	with open("test.xml", "w") as f:
		f.write(etree.tostring(tree, pretty_print = True, xml_declaration = True, encoding='UTF-8', standalone="yes"))

if __name__ == "__main__":
#	print comm.convertURLEncode(u"千葉真一")
	
#	paramPath = comm.getTextPathInCommandLine()
#	textList = [item.strip() for item in comm.getReadLineList(paramPath)]
#	title = textList[0]
#	sentenceList = textList[2:10]

	#cabocha処理	
#	pumpkinCake = pump.makePumpkinCake(sentenceList)
#	for i,soup in enumerate(pumpkinCake):
#		print str(i) + u"行目"
#		print soup

	parents = Element(u'XMI')
	outputXML(etFunc.prettify(makeClassDiagram(parents)))

	