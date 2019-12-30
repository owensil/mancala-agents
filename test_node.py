#  Copyright (c) 2019 Owen Siljander

from unittest import TestCase

from mancala import Mancala
from node import Node


class TestNode(TestCase):
	def setUp(self) -> None:
		self.n = Node(Mancala())
		self.n.player = 1
		self.m = Node.copy_node(self.n)

	def test_rollout(self):
		self.n.rollout(0)
		self.n.rollout(1)
		self.n.rollout(2)
		self.n.rollout(3)
		self.n.rollout(4)
		self.n.rollout(5)
		self.assertEqual(1, self.n.player, "Self.n.player changed, it shouldn't after roll outs!")
		self.n.player = 2
		self.n.rollout(6)
		self.n.rollout(7)
		self.n.rollout(8)
		self.n.rollout(9)
		self.n.rollout(10)
		self.n.rollout(11)
		self.assertEqual([0, 1, 2, 3, 4, 5], self.n.untried_actions)
		self.assertEqual([4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4], self.n.manc.board)
		self.n.player = 1

		action = self.m.untried_actions[0]
		new = self.m.rollout(action)
		new.parent = self.m
		self.m.untried_actions.remove(action)
		self.m.children.append(new)
		new.action = action

		self.assertEqual([], self.n.children)
		self.assertEqual([new], self.m.children)
		self.assertEqual([0, 1, 2, 3, 4, 5], self.n.untried_actions)
		self.assertNotEqual(new, self.m)
		self.assertNotEqual(self.m, self.n)
		self.assertEqual(1, self.m.player, "Self.m.player changed, it shouldn't!")
		self.assertEqual(1, self.n.player, "Self.n.player changed, it shouldn't after being copied!")
		self.assertEqual(2, new.player)
		self.assertEqual(self.m, new.parent)
		self.m.player = 2
		self.m.play(6)
		self.assertEqual([], self.m.children)
		self.assertEqual(None, self.m.parent)
		self.assertEqual({}, self.m.Uprime)
		self.assertEqual({}, self.m.Lprime)

	def test_play(self):
		self.n.play(0)
		self.assertEqual([0, 5, 5, 5, 5, 4, 4, 4, 4, 4, 4, 4], self.n.manc.board)
		self.assertEqual(2, self.n.player)
