#!/usr/bin/python
# -*- coding: utf-8 -*-

from xml.etree.ElementTree import Element, SubElement, Comment, tostring
from xml.etree import ElementTree
from xml.dom import minidom

"""
	Return a pretty-printed XML string for the Element.
"""
def prettify(elem):
    rough_string = ElementTree.tostring(elem, 'utf-8')
    reparsed = minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent="  ")

"""
	タグ内に属性を一括で埋め込む
"""
def setAttributeInTag(tree, dic):
	for key,val in dic.iteritems():
		tree.set(key, val) 