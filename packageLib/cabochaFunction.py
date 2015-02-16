#!/usr/bin/python
# -*- coding: utf-8 -*-

import CaboCha

"""
	係り受け解析をする
"""
def makePumpkinCake(sentList):
	plist = []
	c = CaboCha.Parser()
	for nimono in sentList:
		tree = c.parse(nimono.encode('utf-8'))
		plist.append(tree.toString(CaboCha.FORMAT_XML))
	return plist

"""
	小説内の登場人物
"""
def getActor(pump):
	return pump
