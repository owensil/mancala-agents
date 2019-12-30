#  Copyright (c) 2019 Owen Siljander

from unittest import TestCase

from algs import alphabeta
from mancala import Mancala
from node import Node

NEG_INF = -1000
POS_INF = 1000


class TestAlphabeta(TestCase):
	def setUp(self):
		self.n = Node(Mancala())

	def test_alphabeta(self):
		alphabeta(self.n, NEG_INF, POS_INF, 5, True)
		self.assertIn(self.n.manc.board, [[0, 5, 5, 5, 5, 4, 4, 4, 4, 4, 4, 4], [4, 0, 5, 5, 5, 5, 4, 4, 4, 4, 4, 4],
		                                  [4, 4, 0, 5, 5, 5, 5, 4, 4, 4, 4, 4], [4, 4, 4, 0, 5, 5, 5, 5, 4, 4, 4, 4],
		                                  [4, 4, 4, 4, 0, 5, 5, 5, 5, 4, 4, 4], [4, 4, 4, 4, 4, 0, 5, 5, 5, 5, 4, 4]])
