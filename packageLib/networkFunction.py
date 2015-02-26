#!/usr/bin/python
# -*- coding: utf-8 -*-

import networkx
import pylab
import matplotlib.font_manager
from matplotlib import font_manager
from itertools import combinations
from random import randint

"""
	ネットワークを設定
		ノード、エッジの作成
"""
def setGraph(cList):
	vector = {}
	actor = []
	edges = []
	graph = networkx.Graph()  # 無向グラフ

	for key, val in cList.iteritems():
		actor.append(val.getClassName())
		for relateItem in val.getRelateList():
			edges.append((val.getClassName(), relateItem[1]))

	graph.add_nodes_from(actor)
	graph.add_edges_from(edges)
	return graph

"""
	ネットワークを表示
"""
def displayNetwork(cList):
	graph = setGraph(cList)

	pylab.figure(figsize=(3, 4))  # 横3inch 縦4inchのサイズにする
	pos = networkx.spring_layout(graph)  # いい感じにplotする
#	pos = networkx.spectral_layout(graph)
#	pos = networkx.random_layout(graph)  #とでもすれば高速にplot出来る

	# 見た目をいじる
	networkx.draw_networkx_nodes(graph, pos, node_size=100, node_color="w")
	networkx.draw_networkx_edges(graph, pos, width=1)
#	networkx.draw_networkx_edge_labels(graph, pos, edge_labels=edge_labels, font_family=u'Hiragino Kaku Gothic ProN')
	networkx.draw_networkx_labels(graph, pos, font_size=16, font_color="r", font_family=u'Hiragino Kaku Gothic ProN')

	pylab.xticks([])
	pylab.yticks([])

	pylab.show()

"""
	ノードの座標点を取得
"""
def getNodePosition(cList):
	graph = setGraph(cList)
	pos = networkx.spring_layout(graph)  # いい感じにplotする
	return pos
