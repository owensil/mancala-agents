#  Copyright (c) 2019 Owen Siljander

from unittest import TestCase
from mancala import Mancala
from node import Node
from algs import uct


class TestUct(TestCase):
	def setUp(self):
		self.n = Node(Mancala())

	def test_uct(self):
		constant = 1
		limit = 10
		uct(self.n, constant, limit)
		uct(self.n, constant, limit)
