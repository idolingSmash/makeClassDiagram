#!/usr/bin/python
# -*- coding: utf-8 -*-


class Character:

	def __init__(self):
		self.attributeList = []
		self.operateList = []
	def setAttribute(self,attrStr):
		self.attributeList.append(attrStr)

	def setOperate(self,operStr):
		self.operateList.append(operStr)

	def getAttribute(self):
		return self.attributeList

	def getOperate(self):
		return self.operateList

	def getAttributeItem(self,index):
		if index < len(self.attributeList):
			return self.attributeList[index]
		else :
			return ""

	def getOperateItem(self,index):
		if index < len(self.operateList):
			return self.operateList[index]
		else :
			return ""
