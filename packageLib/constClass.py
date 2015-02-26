#!/usr/bin/python
# -*- coding: utf-8 -*-

import random

class Character:

	def __init__(self):
		self.className = ""
		self.attributeList = []
		self.operateList = []
		self.relateList = []
		self.position = [random.uniform(1, 1000), random.uniform(1, 1000)]

	def setClassName(self, name):
		self.className = name

	def setAttribute(self,attrStr):
		self.attributeList.append(attrStr)

	def setOperate(self,operStr):
		self.operateList.append(operStr)

	def setRelateList(self, obj, verb):
		self.relateList.append([obj, verb])

	def setPosition(self, positionX, positionY):
		self.position[0] = positionX
		self.position[1] = positionY

	def getClassName(self):
		return self.className

	def getAttribute(self):
		return self.attributeList

	def getOperate(self):
		return self.operateList

	def getRelateList(self):
		return self.relateList

	def getPosition(self):
		return self.position

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
