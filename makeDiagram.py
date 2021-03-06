#!/usr/bin/python
# -*- coding: utf-8 -*-

import packageLib.constDictionary as dic
import packageLib.constList as lis
import packageLib.constClass as cls
import packageLib.commonFunction as comm
import packageLib.elementTreeFunction as etFunc
import packageLib.cabochaFunction as pump
import packageLib.networkFunction as barabasi

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

import networkx
import pylab
import matplotlib.font_manager
from matplotlib import font_manager
from itertools import combinations
from random import randint

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
	body部-ModelElement.namespaceを作成
"""
def makeModelElementNameSpace(cdTree, UUID ,access):
	modelNameSpaceTree = SubElement(cdTree, u"UML:ModelElement.namespace")
	nameSpaceTree = SubElement(modelNameSpaceTree, u"UML:Namespace")
	nameSpaceTree.set(u"xmi.idref", UUID)
	visibilityTree = SubElement(cdTree, u"UML:ModelElement.visibility")
	visibilityTree.set(u"xmi.value", access)	

"""
	body部-Feature.ownerを作成
"""
def makeFeatureOwner(cdTree, UUID ,access):
	modelNameSpaceTree = SubElement(cdTree, u"UML:Feature.owner")
	nameSpaceTree = SubElement(modelNameSpaceTree, u"UML:Classifier")
	nameSpaceTree.set(u"xmi.idref", UUID)
	visibilityTree = SubElement(cdTree, u"UML:Feature.visibility")
	visibilityTree.set(u"xmi.value", access)


"""
	body部-Feature.taggedValueを作成
"""
def makePartsTaggedValue(cdTree, UUID):
	tagValueUUID = uuid.uuid3(uuid.NAMESPACE_DNS, UUID.encode('utf-8'))
	tagValue = SubElement(cdTree, u"UML:ModelElement.taggedValue")
	childTagValue = SubElement(tagValue, u"UML:TaggedValue")
	childTagValue.set(u"xmi.id",str(tagValueUUID))
	childTagValue.set(u"version",u"0")
	childTagValue.set(u"tag",u"jude.type_modifier")
	gcTagValue = SubElement(childTagValue ,u"UML:TaggedValue.modelElement")
	ggcTagValue = SubElement(gcTagValue ,u"UML:ModelElement")
	ggcTagValue.set(u"xmi.idref", UUID)


"""
	body部-makeOwnedElement-Class部-Attributeを作成
	uuidは class: + [クラス名],attribute: + [属性名]　で生成
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
		makeModelElementNameSpace(attributeTree, str(uuidFromName), u"private")
		makeFeatureOwner(attributeTree, str(uuidFromName), u"private")
		attriStructure = SubElement(attributeTree, u"UML:StructuralFeature.type")
		attriSClassifier = SubElement(attriStructure, u"UML:Classifier")
		attriSClassifier.set(u"xmi.idref", dic.structureIntType[u"xmi.id"])

"""
	body部-makeOwnedElement-Class-Operate-BehavioralFeatureを作成
"""
def makeBehavioralFeature(cdTree, UUID1, UUID2):
	behaviorTree = SubElement(cdTree, u"UML:BehavioralFeature.parameter")
	behaviorUUID = uuid.uuid3(uuid.NAMESPACE_DNS, UUID2.encode('utf-8'))
	parameterTree = SubElement(behaviorTree, u"UML:Parameter")
	parameterTree.set(u"xmi.id", str(behaviorUUID))
	parameterTree.set(u"name", u"")
	parameterTree.set(u"version", u"0")
	parameterTree.set(u"unSolvedFlag", u"false")
	parameterTree.set(u"kind", u"return")
	makeModelElementNameSpace(parameterTree, UUID1, u"public")
	PBFTree = SubElement(parameterTree, u"UML:Parameter.behavioralFeature")
	childPBFTree = SubElement(PBFTree, u"UML:BehavioralFeature")
	childPBFTree.set(u"xmi.idref", UUID2)
	parameterTypeTree = SubElement(parameterTree, u"UML:Parameter.type")
	childParameterTypeTree = SubElement(parameterTypeTree, u"UML:Classifier")
	childParameterTypeTree.set(u"xmi.idref", dic.structureVoidType[u"xmi.id"])

"""
	body部-makeOwnedElement-Class-Operateを作成
	uuidは class: + [クラス名],operate: + [属性名]　で生成
"""
def makeOperateInPartsClass(cdTree, characterClass):
	uuidFromName = uuid.uuid3(uuid.NAMESPACE_DNS,(u"class:" + characterClass[1].getClassName()).encode('utf-8'))
	for operItem in characterClass[1].getOperate():
		uuidFromOperate = uuid.uuid3(uuid.NAMESPACE_DNS,(u"class:" + characterClass[1].getClassName() + u"," + u"operate:" + operItem).encode('utf-8'))
		operateTree = SubElement(cdTree, u"UML:Operation")
		operateTree.set(u"xmi.id", str(uuidFromOperate))
		operateTree.set(u"name", comm.convertURLEncode(operItem))
		for key,val in dic.attriOperateInPartsClass.iteritems():
			operateTree.set(key,val)
		makeModelElementNameSpace(operateTree, str(uuidFromName), u"public")
		makePartsTaggedValue(operateTree, str(uuidFromOperate))
		makeFeatureOwner(operateTree, str(uuidFromName), u"public")
#		makeBehavioralFeature(operateTree, str(uuidFromName), str(uuidFromOperate))

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
		makeModelElementNameSpace(classChildTree, dic.attriXmiModel[u"xmi.id"], u"public")
		classFeature = SubElement(classChildTree, u"UML:Classifier.feature")
		makeAttributeInPartsClass(classFeature, classItem)
		makeOperateInPartsClass(classFeature, classItem)


"""
	body部-AssociationEndを作成
"""

def makeAssociationEnd(cdTree, fromClass, toClass, UUIDEND, UUIDASS):
	uuidFromClass = uuid.uuid3(uuid.NAMESPACE_DNS, (u"class:" + fromClass).encode('utf-8'))
	uuidToClass = uuid.uuid3(uuid.NAMESPACE_DNS, (u"class:" + toClass).encode('utf-8'))
	associationEndTree = SubElement(cdTree, u"UML:AssociationEnd")
	associationEndTree.set(u"xmi.id", UUIDEND)
	associationEndTree.set(u"name", u"")
	for key, val in dic.attriAssociationEnd.iteritems(): associationEndTree.set(key, val)
	makeModelElementNameSpace(associationEndTree, dic.attriXmiModel[u"xmi.id"], u"private")
	featureOwnerTree = SubElement(associationEndTree, u"UML:Feature.owner")
	childFeatureOwnerTree = SubElement(featureOwnerTree, u"UML:Classifier")
	childFeatureOwnerTree.set(u"xmi.idref", str(uuidToClass))
	featureVisibility = SubElement(associationEndTree, u"UML:Feature.visibility")
	featureVisibility.set(u"xmi.value", u"private")
	participantTree = SubElement(associationEndTree, u"UML:AssociationEnd.participant")
	childParticipantTree = SubElement(participantTree, u"UML:Classifier")
	childParticipantTree.set(u"xmi.idref", str(uuidFromClass))
	associationStemTree = SubElement(associationEndTree, u"UML:AssociationEnd.association")
	childassociationStemTree = SubElement(associationStemTree, u"UML:Association")
	childassociationStemTree.set(u"xmi.idref", UUIDASS)
	associationStemVisibility = SubElement(associationEndTree, u"UML:AssociationEnd.visibility")
	associationStemVisibility.set(u"xmi.value", u"private")

"""
	body部-Associationを作成
	uuid 
		association			association:[subjectName]-[verb]-[objectName]
		associationEndA		associationEnd:[subjectName]-[objectName]-[verb]
		associationEndB		associationEnd:[objectName]-[subjectName]-[verb]
"""
def makeAssociation(cdTree, cList):
	for classItem in cList.iteritems():
		for linkItem in classItem[1].getRelateList():
			subjectName = classItem[1].getClassName()
			verbName = comm.convertURLEncode(linkItem[0])
			objectName = linkItem[1]
			seedAssociation = u"association:" + subjectName + u"-" + linkItem[0] + u"-" + objectName
			seedAssociationEndA = u"associationEnd:" + subjectName + u"-" + objectName + u"-" + linkItem[0]
			seedAssociationEndB = u"associationEnd:" + objectName + u"-" + subjectName + u"-" + linkItem[0]
			uuidAssociation = uuid.uuid3(uuid.NAMESPACE_DNS, seedAssociation.encode('utf-8'))
			uuidAssociationEndA = uuid.uuid3(uuid.NAMESPACE_DNS, seedAssociationEndA.encode('utf-8'))
			uuidAssociationEndB = uuid.uuid3(uuid.NAMESPACE_DNS, seedAssociationEndB.encode('utf-8'))
			associationTree = SubElement(cdTree, u"UML:Association")
			associationTree.set(u"xmi.id", str(uuidAssociation))
			associationTree.set(u"name", verbName)
			associationTree.set(u"version",u"0")
			associationTree.set(u"unSolvedFlag",u"false")
			makeModelElementNameSpace(associationTree, dic.attriXmiModel[u"xmi.id"], u"public")
			associationConnectionTree = SubElement(associationTree , u"UML:Association.connection")
			makeAssociationEnd(associationConnectionTree, subjectName, objectName, str(uuidAssociationEndA), str(uuidAssociation))
			makeAssociationEnd(associationConnectionTree, objectName, subjectName, str(uuidAssociationEndB), str(uuidAssociation))
			associationEndA = SubElement(cdTree, u"UML:AssociationEnd")
			associationEndB = SubElement(cdTree, u"UML:AssociationEnd")
			associationEndA.set(u"xmi.idref", str(uuidAssociationEndA))
			associationEndB.set(u"xmi.idref", str(uuidAssociationEndB))

"""
	body部-makeOwnedElementを作成
"""
def makeOwnedElement(cdTree, cList):
	makePartsClass(cdTree, cList)
	makeAssociation(cdTree, cList)

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
	body部-Diagram-JUDE:UPresentation.clientsを作成
	関連線の一覧
	uuid 
		associationpresentation:[subjectName]-[verb]-[objectName]
"""
def makeDiagramRelateClients(cdTree, cList, keyword):
	clientsTree = SubElement(cdTree, u"JUDE:UPresentation.clients")
	
	#keywordが主語のとき
	for key, val in cList.iteritems():
		if val.getClassName() == keyword:
			for item in val.getRelateList():
				AssociationPresentation = SubElement(clientsTree, u"JUDE:AssociationPresentation")
				uuidAP = uuid.uuid3(uuid.NAMESPACE_DNS, (u"associationpresentation:" + val.getClassName() + u"-" + item[0] + u"-" + item[1]).encode('utf-8'))
				AssociationPresentation.set(u"xmi.idref", str(uuidAP))

	#keywordが目的語のとき
	for key, val in cList.iteritems():
		for item in val.getRelateList():
			if item[1] == keyword:
				AssociationPresentation = SubElement(clientsTree, u"JUDE:AssociationPresentation")
				uuidAP = uuid.uuid3(uuid.NAMESPACE_DNS, (u"associationpresentation:" + val.getClassName() + u"-" + item[0] + u"-" + item[1]).encode('utf-8'))
				AssociationPresentation.set(u"xmi.idref", str(uuidAP))			


"""
	body部-Diagram-LocationPointを作成
"""
def makeDiagramLocationPoint(cdTree, pointX, pointY):
	JomtPresentation = SubElement(cdTree, u"JUDE:JomtPresentation.location")
	locationX = SubElement(JomtPresentation, u"XMI.field")
	locationY = SubElement(JomtPresentation, u"XMI.field")
	locationX.text = pointX
	locationY.text = pointY

"""
	body部-Diagram-関連点(sourceEnd)を作成
"""
def makeDiagramRelateSourceEnd(cdTree, pointX, pointY):
	JomtPresentation = SubElement(cdTree, u"JUDE:BinaryRelationPresentation.sourceEnd")
	locationX = SubElement(JomtPresentation, u"XMI.field")
	locationY = SubElement(JomtPresentation, u"XMI.field")
	locationX.text = pointX
	locationY.text = pointY


"""
	body部-Diagram-関連点(targetEnd)を作成
"""
def makeDiagramRelateTargetEnd(cdTree, pointX, pointY):
	JomtPresentation = SubElement(cdTree, u"JUDE:BinaryRelationPresentation.targetEnd")
	locationX = SubElement(JomtPresentation, u"XMI.field")
	locationY = SubElement(JomtPresentation, u"XMI.field")
	locationX.text = pointX
	locationY.text = pointY


"""
	body部-Diagram-JUDE:FramePresentationを作成
"""
def makeDiagramFramePresentation(cdTree):
	framePresentation = SubElement(cdTree , u"JUDE:FramePresentation")
	framePresentation.set(u"width", dic.diagramSize[u"width"])
	framePresentation.set(u"height", dic.diagramSize[u"height"])
	for key, val in dic.attriDiagramFramePresentation.iteritems():
		framePresentation.set(key, val)
	UPresentationTree = SubElement(framePresentation, u"JUDE:UPresentation.diagram")
	childUPresentationTree = SubElement(UPresentationTree, u"JUDE:Diagram")
	childUPresentationTree.set(u"xmi.idref", dic.attriDiagramBase[u"xmi.id"])
	makeDiagramLocationPoint(framePresentation,dic.diagramLocationPoint[u"pointX"], dic.diagramLocationPoint[u"pointY"])


"""
	body部-Diagram-JUDE:ClassifierPresentation-customStyleMapを作成
"""
def makeDiagramClassStyleMap(cdTree):
	styleMap = SubElement(cdTree, u"JUDE:UPresentation.customStyleMap")
	attrProperty = SubElement(styleMap, u"JUDE:UPresentation.styleProperty")
	colorProperty = SubElement(styleMap, u"JUDE:UPresentation.styleProperty")
	operProperty = SubElement(styleMap, u"JUDE:UPresentation.styleProperty")
	attrProperty.set(u"key",u"attribute.filter_by_visibility")
	attrProperty.set(u"value",u"")
	colorProperty.set(u"key",u"fill.color")
	colorProperty.set(u"value",u"#FFFFCC")
	operProperty.set(u"key",u"operation.filter_by_visibility")
	operProperty.set(u"value",u"")

"""
	クラス図に表示するクラスのサイズを設定
"""
def setDialogClassSize(cdTree, classData):
	nameLength = len(classData.getClassName())
	attributeMaxLength = 0
	operationMaxLength = 0
	
	maxName = 0
	maxAttribute = 0
	maxOperate = 0

	width = 0
	height = 0

	if 0 < len(classData.getAttribute()):
		for attritem in classData.getAttribute():
			if attributeMaxLength < len(attritem):
				attributeMaxLength = len(attritem)

	if 0 < len(classData.getOperate()):
		for opeitem in classData.getOperate():
			if operationMaxLength < len(opeitem):
				operationMaxLength = len(opeitem)

	if nameLength < 2: maxName = 40
	else : maxName = 46 + 13 * (nameLength - 2)
	
	maxAttribute = 79 + 12 * (attributeMaxLength - 1);
	maxOperate = 81 + 12 * (operationMaxLength - 1);
	
	width = max([maxName, maxAttribute, maxOperate])
	height = 42.09375 + 15.09375 * (len(classData.getAttribute()) + len(classData.getOperate()))

	cdTree.set(u"width", str(width))
	cdTree.set(u"height", str(height))

"""
	body部-Diagram-JUDE:ClassifierPresentationを作成
	uuid:diagramclass:[クラス名]
"""
def makeDiagramClassifierPresentation(cdTree, cList):
	for item in cList.iteritems():
		uuidDiagramClass = uuid.uuid3(uuid.NAMESPACE_DNS, (u"diagramclass:"+ item[1].getClassName()).encode('utf-8'))
		uuidClass = uuid.uuid3(uuid.NAMESPACE_DNS,  (u"class:"+ item[1].getClassName()) .encode('utf-8'))
		diagramClass = SubElement(cdTree, u"JUDE:ClassifierPresentation")
		diagramClass.set(u"xmi.id", str(uuidDiagramClass))
		for key, val in dic.dialogClassifierPresentation.iteritems():
			diagramClass.set(key, val)
		setDialogClassSize(diagramClass, item[1])
		semanticModel = SubElement(diagramClass, u"JUDE:UPresentation.semanticModel")
		childSemanticModel = SubElement(semanticModel, u"UML:Class")
		childSemanticModel.set(u"xmi.idref", str(uuidClass))
		UPresentation = SubElement(diagramClass, u"JUDE:UPresentation.diagram")
		childUPresentation = SubElement(UPresentation, u"UML:Diagram")
		childUPresentation.set(u"xmi.idref", dic.attriDiagramBase[u"xmi.id"])
		makeDiagramRelateClients(diagramClass, cList, item[1].getClassName())
		makeDiagramClassStyleMap(diagramClass)
		makeDiagramLocationPoint(diagramClass, str(item[1].getPosition()[0]), str(item[1].getPosition()[1]))


"""
	body部-Diagram-JUDE:AssociationPresentationを作成
	uuid:
	associationpresentation		associationpresentation:[subjectName]-[verb]-[objectName]
	association					association:[subjectName]-[verb]-[objectName]
	主語を走査

"""
def makeDiagramAssociationPresentation(cdTree, cList):
	for key, val in cList.iteritems():
		if 0 < len(val.getRelateList()):
			for item in val.getRelateList():
				dialogAssociationPresentation = SubElement(cdTree, u"JUDE:AssociationPresentation")
				uuidAP = uuid.uuid3(uuid.NAMESPACE_DNS, (u"associationpresentation:" + val.getClassName() + u"-" + item[0] + u"-" + item[1]).encode('utf-8'))
				dialogAssociationPresentation.set(u"xmi.id", str(uuidAP))
				for dkey, dval in dic.dialogAssociationPresentation.iteritems():
					dialogAssociationPresentation.set(dkey, dval)
				semanticModel = SubElement(dialogAssociationPresentation, u"JUDE:UPresentation.semanticModel")
				childSemanticModel = SubElement(semanticModel, u"UML:Association")
				uuidAss = uuid.uuid3(uuid.NAMESPACE_DNS, (u"association:" + val.getClassName() + u"-" + item[0] + u"-" + item[1]).encode('utf-8'))
				childSemanticModel.set(u"xmi.idref", str(uuidAss))
				diagramBase = SubElement(dialogAssociationPresentation, u"JUDE:UPresentation.diagram")
				childDiagramBase = SubElement(diagramBase, u"JUDE:Diagram")
				childDiagramBase.set(u"xmi.idref", dic.attriDiagramBase[u"xmi.id"])

				classPoint = SubElement(dialogAssociationPresentation, u"JUDE:UPresentation.servers")
				uuidCS = uuid.uuid3(uuid.NAMESPACE_DNS, (u"diagramclass:" + val.getClassName()).encode('utf-8'))
				childClassPointSubject = SubElement(classPoint, u"JUDE:ClassifierPresentation")
				childClassPointSubject.set(u"xmi.idref", str(uuidCS))

				uuidCO = uuid.uuid3(uuid.NAMESPACE_DNS, (u"diagramclass:" + item[1]).encode('utf-8'))
				childClassPointObject = SubElement(classPoint, u"JUDE:ClassifierPresentation")
				childClassPointObject.set(u"xmi.idref", str(uuidCO))

				customStyleMap = SubElement(dialogAssociationPresentation, u"JUDE:UPresentation.customStyleMap")
				childCustomStyleMap = SubElement(customStyleMap, u"JUDE:UPresentation.styleProperty")
				childCustomStyleMap.set(u"key",u"line.shape")
				childCustomStyleMap.set(u"value",u"line")

				makeDiagramLocationPoint(dialogAssociationPresentation, str(0.0), str(0.0))
				makeDiagramRelateSourceEnd(dialogAssociationPresentation, str(0.5), str(0.5))
				makeDiagramRelateTargetEnd(dialogAssociationPresentation, str(0.5), str(0.5))
				snakePath = SubElement(dialogAssociationPresentation, u"JUDE:PathPresentation.points")
#				terminalPartsA = SubElement(dialogAssociationPresentation, u"qualifierBoxAPresentation")
#				terminalPartsB = SubElement(dialogAssociationPresentation, u"qualifierBoxAPresentation")

"""
	body部-Diagram-CustomStyleMapを作成
"""
def makeDiagramCustomStyleMap(cdTree):
	customStyleMap = SubElement(cdTree, u"JUDE:Diagram.customStyleMap")
	for key, val in dic.diagramCustomStyleMap.iteritems():
		styleProperty = SubElement(customStyleMap, u"JUDE:Diagram.styleProperty")
		styleProperty.set(u"key",key)
		styleProperty.set(u"value",val)


"""
	body部-Diagramを作成
"""
def makeDiagram(cdTree, cList, title):
	ptree = SubElement(cdTree, u'XMI.extension')
	diagramTree = SubElement(ptree, u"JUDE:Diagram")
	diagramTree.set(u"name", title) 
	for key, val in dic.attriDiagramBase.iteritems(): diagramTree.set(key, val)
	diagramNamespace = SubElement(diagramTree, u"UML:ModelElement.namespace")
	childDiagramNamespace = SubElement(diagramNamespace, u"UML:Namespace")
	childDiagramNamespace.set(u"xmi.idref", dic.attriXmiModel[u"xmi.id"])
	diagramPresentations = SubElement(diagramTree, u"JUDE:Diagram.presentations")
	makeDiagramFramePresentation(diagramPresentations)
	makeDiagramClassifierPresentation(diagramPresentations, cList)
	makeDiagramAssociationPresentation(diagramPresentations, cList)
	makeDiagramCustomStyleMap(diagramTree)

"""
	body部を作成
"""
def makeBody(cdTree, cList, title):
	Body = SubElement(cdTree, u'XMI.content')
	makeBodyProperty(Body, cList)
	primitiveInt = SubElement(Body, u"UML:Primitive")
	primitiveVoid = SubElement(Body, u"UML:Primitive")
	for key, val in dic.structureIntType.iteritems(): primitiveInt.set(key, val)
	for key, val in dic.structureVoidType.iteritems(): primitiveVoid.set(key, val)
	makeDiagram(Body, cList, title)


"""
	クラス図ダイアグラムを作成
"""
def makeClassDiagram(cList, title):
	parents = Element(u'XMI')
	OD = OrderedDict(dic.attriXmiVersionTapple)
	for item in OD:
		parents.set(item, OD[item])
	makeHeader(parents)
	makeBody(parents, cList, title)	
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

"""
	デバッグ用
"""
def samplePrintCharacterList(cList):
	for ids in characterList.iteritems():
		print u"【" + ids[1].getClassName() + u"】"
		print u"『属性』"
		for item in ids[1].getAttribute(): print item
		print u"『操作』"
		for item in ids[1].getOperate(): print item
		print u"『関連』"
	
		for item in ids[1].getRelateList(): print item[0] + u"-" + item[1]
		print u""

"""
	端役も追加
"""
def addObjectSmallRole(cList):
	SubjectList = []
	ObjectList = []
	for ids in cList.iteritems():
		SubjectList.append(ids[1].getClassName())
	for ids in cList.iteritems():
		for item in ids[1].getRelateList():
			if not item[1] in SubjectList:
				ObjectList.append(item[1]) 
	ObjectList = list(set(ObjectList))
	for item in ObjectList: 
		actClass = cls.Character()
		actClass.setClassName(item)
		cList[item] = actClass


if __name__ == "__main__":
	paramPath = comm.getTextPathInCommandLine()
	textList = [item.strip() for item in comm.getReadLineList(paramPath)]
	title = textList[0]
	sentenceList = textList[2:]

	pumpkinCake = pump.makePumpkinCake(sentenceList) #cabocha処理(XML形式で出力)
	supportSentenceList = pump.supportNoun(pumpkinCake, sentenceList) #主語を補う
	pumpkinCakeBySupportSubject = pump.makePumpkinCake(supportSentenceList) #cabocha処理(XML形式で出力)
	characterList = pump.makeCharacterPackage(pumpkinCakeBySupportSubject, supportSentenceList) #classにパッケージ化
	addObjectSmallRole(characterList)
#	samplePrintCharacterList(characterList) #debug用
#	barabasi.displayNetwork(characterList)  #ネットワーク表示用

	positionDic = barabasi.getNodePosition(characterList)
	for key, val in positionDic.iteritems():
		characterList[key].setPosition(val[0]*1000, val[1]*1000)

	outputXML(makeClassDiagram(characterList, title))


