#!/usr/bin/python
# -*- coding: utf-8 -*-

import constDictionary as dic
import commonFunction as comm
import elementTreeFunction as etFunc

import os.path
import re
import sys
import codecs
from xml.etree.ElementTree import Element, SubElement, Comment, tostring
from xml.etree import ElementTree
from xml.dom import minidom

def makeHeader(ptree):
	parentsTree = SubElement(ptree, u'XMI.header')
	docTree = SubElement(parentsTree, u"XMI.documentation")
	metaTree = SubElement(parentsTree, u"XMI.metamodel")
	attriMetaDoc = {"xmi.name":"UML", "xmi.version":"1.4"}
	for key, val in dic.tagXmiHeader.iteritems():
		valTree = SubElement(docTree, key)
		if isinstance(val, str):
			valTree.text = val
		elif isinstance(val, list):
			childTree = SubElement(valTree, val[0])
			for ckey, cval in val[1].iteritems():
				childTree.set(ckey, cval)

	for key, val in attriMetaDoc.iteritems():
		metaTree.set(key, val)

	return parentsTree

if __name__ == "__main__":
	parents = Element(u'XML')
	D = dic.attriXmiVersion
	for key,val in D.iteritems():
			parents.set(key, val)

	Header = makeHeader(parents)
	Body = SubElement(parents, u'XMI.content')
	print etFunc.prettify(parents)
  