#!/usr/bin/python
# -*- coding: utf-8 -*-


class Character:

	def __init__(self):
		self.className = ""
		self.attributeList = []
		self.operateList = []
		self.relateList = []

	def setClassName(self, name):
		self.className = name

	def setAttribute(self,attrStr):
		self.attributeList.append(attrStr)

	def setOperate(self,operStr):
		self.operateList.append(operStr)

	def setRelateList(self, obj, verb):
		self.relateList.append([obj, verb])

	def getClassName(self):
		return self.className

	def getAttribute(self):
		return self.attributeList

	def getOperate(self):
		return self.operateList

	def getRelateList(self):
		return self.relateList

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

	def getRelateItem(self,index):
		if index < len(self.operateList):
			return self.relateList[index]
		else :
			return ""
