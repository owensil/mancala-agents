#  Copyright (c) 2019 Owen Siljander
from unittest import TestCase

from mancala import Mancala


class TestMancala(TestCase):
	def setUp(self):
		self.m = Mancala()
		self.g = Mancala()

	def test_init(self):
		self.assertEqual(self.m.p1_store, 0)
		self.assertEqual(self.m.p2_store, 0)
		self.assertEqual(self.m.is_terminal, False)
		self.assertEqual([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11], self.m.actions)
		self.assertEqual([4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4], self.m.board)

	def invalid_play(self, board, move, player):
		"""Simply used to verify that moves will fail when they're invalid choices"""
		# This can probably be replaced by self.assertRaises() but I can't be bothered
		try:
			board.play(move, player)
		except ValueError:
			pass
		else:
			self.fail()

	def test_play(self):
		# This does the major brunt of the testing, I can't really be bothered to write tests for
		# remove_slam and update_actions since they're all heavily tied to each other
		# Test 1 - Valid Move
		self.m.play(0, 1)
		self.assertEqual([0, 5, 5, 5, 5, 4, 4, 4, 4, 4, 4, 4], self.m.board, "Test 1 - Valid Move")
		self.m.play(7, 2)
		self.assertEqual([0, 5, 5, 5, 5, 4, 4, 0, 5, 5, 5, 5], self.m.board, "Test 1 - Valid Move")
		self.m = Mancala()
		self.m.play(0, 1)
		# Test 2 - Invalid move
		self.invalid_play(self.m, 0, 1)
		self.assertEqual([0, 5, 5, 5, 5, 4, 4, 4, 4, 4, 4, 4], self.m.board, "Test 2 - Invalid move")
		# Test 3 - Wrap around move
		self.m.play(11, 2)
		self.assertEqual([1, 6, 6, 6, 5, 4, 4, 4, 4, 4, 4, 0], self.m.board, "Test 3 - Wrap around move")
		# Test 4 - Player 1 must feed
		# -- new board --
		self.m.board = [1, 6, 6, 6, 5, 4, 0, 0, 0, 0, 0, 0]
		self.m.update_actions(1)
		self.assertEqual([1, 2, 3, 4, 5], self.m.actions, "Test 4 - Player 1 must feed")
		# Test 5 - Invalid move
		self.invalid_play(self.m, 9, 1)
		self.assertEqual([1, 6, 6, 6, 5, 4, 0, 0, 0, 0, 0, 0], self.m.board, "Test 5 - Invalid move")
		# -- new board --
		# Test 6 - Grand slam detection for p1
		self.m.board = [1, 0, 2, 0, 0, 6, 2, 1, 2, 2, 1, 2]
		self.m.update_actions(1)
		self.assertEqual([0, 2], self.m.get_actions(1), "Test 6 - Grand slam detection for p1")
		self.invalid_play(self.m, 5, 1)
		self.assertEqual([1, 0, 2, 0, 0, 6, 2, 1, 2, 2, 1, 2], self.m.board)
		# -- new board --
		# Test 7 - Grand slam detection for p2
		self.m.board = [2, 1, 2, 2, 1, 2, 1, 0, 2, 0, 0, 6]
		self.m.update_actions(2)
		self.assertEqual(self.m.get_actions(2), [6, 8], "Test 7 - Grand slam detection for p2")
		self.invalid_play(self.m, 11, 2)
		self.assertEqual(self.m.board, [2, 1, 2, 2, 1, 2, 1, 0, 2, 0, 0, 6])
		# Test 8 - Captures
		self.m.board = [4, 4, 4, 3, 2, 3, 2, 1, 2, 2, 1, 2]
		self.m.update_actions(1)
		self.m.play(5, 1)
		self.assertEqual(8, self.m.p1_store)
		# TEST
		self.m.board = [4, 5, 2, 0, 3, 3, 3, 3, 2, 2, 0, 4]
		self.m.update_actions(1)
		self.m.play(5, 1)
		self.assertEqual(False, self.m.is_terminal)
		print(self.m.board)

	def test_reward(self):
		# TODO
		self.assertEqual(1, 1)

	def test_get_actions(self):
		self.assertEqual([0, 1, 2, 3, 4, 5], self.g.get_actions(1))
		self.assertEqual([6, 7, 8, 9, 10, 11], self.g.get_actions(2))
		self.g.play(0, 1)
		self.assertEqual([1, 2, 3, 4, 5], self.g.get_actions(1))
		self.g.play(8, 2)
		self.assertEqual([6, 7, 9, 10, 11], self.g.get_actions(2))

	def test__remove_slam(self):
		self.assertEqual(1, 1)

	def test_update_actions(self):
		# valid move
		self.m.play(0, 1)
		self.assertEqual([1, 2, 3, 4, 5], self.m.get_actions(1))
		self.assertEqual([6, 7, 8, 9, 10, 11], self.m.get_actions(2))
		self.assertEqual([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11], self.m.actions)
		self.m.board = [6, 1, 0, 0, 10, 3, 2, 2, 1, 0, 0, 0]
		self.m.update_actions(1)
		self.assertEqual([0, 1, 4, 6, 7, 8], self.m.actions)
		self.m.board = [0, 0, 0, 0, 4, 3, 2, 2, 1, 0, 0, 0]
		self.m.update_actions(1)
		for i in [4, 5, 6, 7, 8]:
			self.assertIn(i, self.m.actions)
		self.assertEqual(5, len(self.m.actions))
