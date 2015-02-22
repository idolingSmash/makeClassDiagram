#!/usr/bin/python
# -*- coding: utf-8 -*-

import os.path
import re
import sys
import codecs
import urllib2

"""
	コマンドラインから文字列を抽出する
	.txt以外は強制終了
"""
def getTextPathInCommandLine():
	argvs = sys.argv  # コマンドライン引数を格納したリストの取得
	argc = len(argvs) # 引数の個数


	if argc != 2:   # 引数が２つじゃない場合は、その旨を表示
	    print 'Usage: # python %s filepath' % argvs[0]
	    quit()         # プログラムの終了
	else :
		root, ext = os.path.splitext(argvs[1])
		if ext != '.txt':
			print 'Usage: # %s is not text file. You should change into the ext of text.' % argvs[1]
			quit()

	return argvs[1]

"""
	読み込んだテキストファイルを改行単位にリスト化する
"""
def getReadLineList(path):

	if os.path.isfile(path) == False:
		print 'Usage: # %s does not exist.' % path
		quit()
	else :
		iStream = codecs.open(path, 'r', 'utf-8')
		lineList = iStream.readlines()
		iStream.close()
	return lineList

"""
	テキストファイルに書き込む
"""
def setWriteLineList(name,outstr):
	outFileName, ext = os.path.splitext(name)
	fout = codecs.open(outFileName + ext, 'w', 'utf-8' )
	fout.write(outstr) # 引数の文字列をファイルに書き込む
	fout.close() # ファイルを閉じる


"""
	全角判定
"""
def isZenkaku(sentence):
	bFlag = True
	regexp = re.compile('(?:\xEF\xBD[\xA1-\xBF]|\xEF\xBE[\x80-\x9F])|[\x20-\x7E]')
	result = regexp.search(sentence)
	if result != None :
		bFlag = False
	else :
		bFlag = True
	return bFlag

"""
	漢字かそれ以外かの判別
"""
def isKanji(word):
	regexp = re.compile(r'^(?:\xe4[\xb8-\xbf][\x80-\xbf]|[\xe5-\xe9][\x80-\xbf][\x80-\xbf]|\xef\xa4\xa9|\xef\xa7\x9c|\xef\xa8[\x8e-\xad])+$')
	result = regexp.search(word.encode('utf-8'))
	if result != None :
		return True
	else :
		return False

"""
	全角カタカナかそれ以外かの判別
"""
def isKatakana(word):
	regexp = re.compile(r'^(?:\xe3\x82[\xa1-\xbf]|\xe3\x83[\x80-\xb6]|\xe3\x83\xbc)+$')
	result = regexp.search(word.encode('utf-8'))
	if result != None :
		return True
	else :
		return False

"""
	全角ひらがなかそれ以外かの判別
"""
def isHiragana(word):
	regexp = re.compile(r'^(?:\xE3\x81[\x81-\xBF]|\xE3\x82[\x80-\x93])+$')
	result = regexp.search(word.encode('utf-8'))
	if result != None :
		return True
	else :
		return False

"""
	URLEncodeに変換する
"""
def convertURLEncode(str):
	return urllib2.quote(str.encode('utf-8'))

"""
	リスト一覧をコンソールに表示する
"""
def printListItem(Lists):
	for item in Lists:
		print item