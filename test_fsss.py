#  Copyright (c) 2019 Owen Siljander

from unittest import TestCase

from algs import fsss
from mancala import Mancala
from node import Node


class TestFsss(TestCase):
	def setUp(self) -> None:
		self.state = Node(Mancala())

	def gens(self, node, depth, iteration):
		n = Node(Mancala())
		n1 = Node(Mancala())
		n.parent = node
		n1.parent = node
		n.actions = [0, 1]
		n1.actions = [0, 1]
		node.childs = {0: n, 1: n1}
		if depth % 2 == 1:
			n.player = 2
			n1.player = 2
		else:
			n.player = 1
			n1.player = 1
		if depth == 0:
			if iteration == -1:
				iteration = 0
			n.leaf = True
			n1.leaf = True
			n.actions = []
			n1.actions = []
			if iteration == 0:
				n.value = 4
				n1.value = 3
			elif iteration == 1:
				n.value = 1
				n1.value = 8
			elif iteration == 2:
				n.value = 0
				n1.value = 5
			elif iteration == 3:
				n.value = 8
				n1.value = 0
			elif iteration == 4:
				n.value = 5
				n1.value = 6
			elif iteration == 5:
				n.value = 0
				n1.value = 3
			elif iteration == 6:
				n.value = 7
				n1.value = 4
			elif iteration == 7:
				n.value = 7
				n1.value = 1
			return iteration + 1
		else:
			it = self.gens(n, depth - 1, iteration)
			new_it = self.gens(n1, depth - 1, it)
			return new_it

	def test_fsss(self):
		self.skipTest("test_fsss not implemented")
	# self.gens(self.state, 3, -1)
	# self.state.actions = [0, 1]
	# print(fsss(self.state, 15))
