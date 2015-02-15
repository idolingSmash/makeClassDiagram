#!/usr/bin/python
# -*- coding: utf-8 -*-

import packageLib.constDictionary as dic
import packageLib.constList as lis
import packageLib.commonFunction as comm
import packageLib.elementTreeFunction as etFunc

import os.path
import re
import sys
import codecs
from xml.etree.ElementTree import Element, SubElement, Comment, tostring
from xml.etree import ElementTree
from xml.dom import minidom

"""
	header部を作成
"""
def makeHeader(ptree):
	parentsTree = SubElement(ptree, u'XMI.header')
	docTree = SubElement(parentsTree, u"XMI.documentation")
	metaTree = SubElement(parentsTree, u"XMI.metamodel")
	attriMetaDic = {u"xmi.name":u"UML", u"xmi.version":u"1.4"}
	for key, val in dic.tagXmiHeader.iteritems():
		valTree = SubElement(docTree, key)
		if isinstance(val, unicode):
			valTree.text = val
		elif isinstance(val, list):
			childTree = SubElement(valTree, val[0])
			for ckey, cval in val[1].iteritems():
				childTree.set(ckey, cval)
	etFunc.setAttributeInTag(metaTree, attriMetaDic)
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
"""
def makeBodyProperty(cdTree):
	umlModel = SubElement(cdTree, u'UML:Model')
	taggedValue = SubElement(cdTree, u"UML:ModelElement.taggedValue")
	etFunc.setAttributeInTag(umlModel, dic.attriXmiModel)
	extensionProperty = SubElement(umlModel, u'XMI.extension')
	customStyleMap = SubElement(extensionProperty, u'UML:Model.customStyleMap')
	for key, val in dic.modelCustomStyleMap.iteritems():	
		childTree = SubElement(customStyleMap, u"UML:Model.styleProperty")
		childTree.set(u"key",key)
		childTree.set(u"value",val)
	makeTaggedValue(taggedValue, lis.taggedValueModelElement)

"""
	body部を作成
"""
def makeBody(cdTree):
	Body = SubElement(cdTree, u'XMI.content')
	makeBodyProperty(Body)



"""
	クラス図ダイアグラムを作成
"""
def makeClassDiagram(cdTree):	
	etFunc.setAttributeInTag(cdTree, dic.attriXmiVersion)
	makeHeader(cdTree)
	makeBody(cdTree)	
	return cdTree

if __name__ == "__main__":
#	print comm.convertURLEncode(u"千葉真一")
	parents = Element(u'XML')
	comm.setWriteLineList("test.xml", etFunc.prettify(makeClassDiagram(parents)))