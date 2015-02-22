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
	verTree.set(u"modelVersion",u"36")
	verTree.set(u"productVersion", u"professional 6.7.0")

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
	body部-makeOwnedElement-Class部-Attributeを作成
	uuidは class: + [クラス名] , attribute: + [属性名]　で生成
"""
def makeAttributeInPartsClass(cdTree, characterClass):
	uuidFromName = uuid.uuid3(uuid.NAMESPACE_DNS,(u"class:" + characterClass[1].getClassName()).encode('utf-8'))
	for attriItem in characterClass[1].getAttribute():
		uuidFromAttribute = uuid.uuid3(uuid.NAMESPACE_DNS,(u"class:" + characterClass[1].getClassName() + u"," + u"attribute:" + attriItem).encode('utf-8'))
		attributeTree = SubElement(cdTree, u"UML:Attribute")
		attributeTree.set(u"xmi.id", str(uuidFromAttribute))
		attributeTree.set(u"name", comm.convertURLEncode(attriItem))
		for key,val in dic.attriAttributeInPartsClass.iteritems():
			attributeTree.set(key,val)
		attriModelNameSpace = SubElement(attributeTree, u"UML:ModelElement.namespace")
		attriNameSpace = SubElement(attriModelNameSpace, u"UML:Namespace")
		attriNameSpace.set(u"xmi.idref", str(uuidFromName))
		attriVisibility = SubElement(attributeTree, u"UML:ModelElement.visibility")
		attriVisibility.set(u"xmi.value", u"private")

		attriFeature = SubElement(attributeTree, u"UML:Feature.owner")
		attriClassifier = SubElement(attriFeature, u"UML:Classifier")
		attriClassifier.set(u"xmi.idref", str(uuidFromName))
		attriFVisibility = SubElement(attributeTree, u"UML:Feature.visibility")
		attriFVisibility.set(u"xmi.value", u"private")

		attriStructure = SubElement(attributeTree, u"UML:StructuralFeature.type")
		attriSClassifier = SubElement(attriStructure, u"UML:Classifier")
		attriSClassifier.set(u"xmi.idref", dic.structureIntType[u"xmi.id"])


"""
	body部-makeOwnedElement-Class部を作成
	uuidは class: + [クラス名]　で生成
"""
def makePartsClass(cdTree, cList):
	for classItem in cList.iteritems():
		classChildTree = SubElement(cdTree, u"UML:Class")
		uuidFromName = uuid.uuid3(uuid.NAMESPACE_DNS, (u"class:" + classItem[1].getClassName()).encode('utf-8'))
		classChildTree.set(u"xmi.id", str(uuidFromName))
		classChildTree.set(u"name", comm.convertURLEncode(classItem[1].getClassName()))
		for key, val in dic.attriPartsClass.iteritems(): classChildTree.set(key, val)
		classModelNameSpace = SubElement(classChildTree, u"UML:ModelElement.namespace")
		classNameSpace = SubElement(classModelNameSpace, u"UML:Namespace")
		classNameSpace.set(u"xmi.idref", dic.attriXmiModel[u"xmi.id"])
		classVisibility = SubElement(classChildTree, u"UML:ModelElement.visibility")
		classVisibility.set(u"xmi.value", u"public")
		classFeature = SubElement(classChildTree, u"UML:Classifier.feature")
		makeAttributeInPartsClass(classFeature, classItem)

"""
	body部-makeOwnedElementを作成
"""
def makeOwnedElement(cdTree, cList):
	makePartsClass(cdTree, cList)


"""
	body部を作成
		UML:Model
		UML:ModelElement.taggedValue
"""
def makeBodyProperty(cdTree, cList):
	umlModel = SubElement(cdTree, u'UML:Model')
	taggedValue = SubElement(umlModel, u"UML:ModelElement.taggedValue")
	ownedElement = SubElement(umlModel, u"UML:Namespace.ownedElement")
	OD = OrderedDict(dic.attriXmiModelTapple)
	for item in OD:
		umlModel.set(item, OD[item])
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
	primitiveInt = SubElement(Body, u"UML:Primitive")
	primitiveVoid = SubElement(Body, u"UML:Primitive")
	for key, val in dic.structureIntType.iteritems(): primitiveInt.set(key, val)
	for key, val in dic.structureVoidType.iteritems(): primitiveVoid.set(key, val)
	makeDiagram(Body, cList)


"""
	クラス図ダイアグラムを作成
"""
def makeClassDiagram(cList):
	parents = Element(u'XMI')
	OD = OrderedDict(dic.attriXmiVersionTapple)
	for item in OD:
		parents.set(item, OD[item])
	makeHeader(parents)
	makeBody(parents, cList)	
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

