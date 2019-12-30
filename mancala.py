#  Copyright (c) 2019 Owen Siljander
import logging
from copy import copy

# config = "[%(levelname)s]:%(name)s - %(message)s"
# logging.basicConfig(format=config, filename='log.log', level=logging.DEBUG, filemode="w")
# LOG = logging.getLogger("mancala")
# LOG.setLevel(logging.DEBUG)
# LOG.disabled = True
# LOG.setLevel(logging.INFO)
# Board attributes
PITS_PER_ROW = 6
COUNT_PER_PIT = 4
BD_SIZE = 12  # BD_SIZE//2 is the first pit for player 2
MOVE_LIMIT = 300


class Mancala:
	"""
	Representation of a Mancala game board.
	"""

	def __init__(self):
		# Create board based on defines
		self.board = [COUNT_PER_PIT] * (2 * PITS_PER_ROW)
		self.actions = []
		self.is_terminal = False
		self.p1_store = 0
		self.p2_store = 0
		self.num_moves = 0
		self.actions = [i for i in range(0, BD_SIZE)]

	def __repr__(self):
		r = "P1 {0}, P2 {1}, ".format(self.p1_store, self.p2_store)
		for i in range(0, BD_SIZE):
			if i == BD_SIZE // 2:
				r += "|  "
			r += "{0}  ".format(self.board[i])
		return r

	def _remove_slam(self, player=1) -> None:
		"""
		Detects a "grand slam" move and removes the respective actions.
		:param player: Player number who is suspected of being able to perform a grand slam.
		:return: void
		:raises ValueError: Invalid player number.
		"""
		# LOG.debug("_remove_slam: Checking grand slam. Player {0}".format(player))
		check_zero = False
		slam = True
		end_of_segment = 0
		opponent = 2 // player
		# Dynamic range, 0 to half size of board for p2, half size of board to end for p1
		for i in range((opponent - 1) * BD_SIZE // 2, BD_SIZE // player):
			# find contiguous segment of 1 or 2 with all other entries being zero
			if (self.board[i] == 1 or self.board[i] == 2) and not check_zero:
				end_of_segment = i
			elif self.board[i] == 0 and check_zero:
				continue
			elif self.board[i] == 0 and not check_zero:
				check_zero = True
			else:
				slam = False
				break
		if slam:
			cpy = copy(self.get_actions(player))
			# LOG.debug("_remove_slam: Slam found, checking moves")
			for i in self.get_actions(player):
				if i + self.board[i] == (player - 1) * BD_SIZE + end_of_segment:
					self.actions.remove(i)
			# Check if only moves are grand slams
			if not self.get_actions(player):
				# LOG.debug("_remove_slam: Grand slam is only possible move for player")
				self.actions += cpy

	def _end_game(self) -> None:
		"""Ends the game, adds all pieces in players row to their store"""
		# LOG.info("----- Game ended -----")
		# for i in range(0, BD_SIZE):
		# 	if i < BD_SIZE // 2:
		# 		self.p1_store += self.board[i]
		# 	else:
		# 		self.p2_store += self.board[i]
		# 	self.board[i] = 0
		# LOG.info("Game ended. P1 {0} P2 {1}".format(self.p1_store, self.p2_store))
		self.is_terminal = True

	def update_actions(self, player: int) -> None:
		"""
		Updates actions for all players based on current board and list of actions
		:param player: Current player's turn
		"""
		# LOG.info("update_actions: Current actions are {0}, board {1}".format(self.actions, self.board))
		p1_movable = False
		p2_movable = False
		# Check if players have a move
		self.actions = []
		for i in range(0, BD_SIZE):
			if self.board[i] != 0:
				self.actions.append(i)
				if i < BD_SIZE // 2:
					p1_movable = True
				else:
					p2_movable = True
		if (not p1_movable and not p2_movable) or (player == 1 and not p1_movable or player == 2 and not p2_movable):
			# end condition
			# LOG.debug("update_actions: No legal move found.")
			self._end_game()
			return
		elif not p1_movable and p2_movable:
			# p2 must give p1 a legal action
			# LOG.debug("update_actions: Player 1 cannot move, player 2 feeds.")
			for i in self.get_actions(2):
				# P2 Must be able to reach opponents board
				if self.board[i] + i < 12:
					try:
						self.actions.remove(i)
					except ValueError as e:
						raise ValueError("Couldn't remove action, {0}".format(e))
		# LOG.error("update_actions: Failed to remove action".format(i, e))
		elif not p2_movable and p1_movable:
			# p1 must give p2 a legal action
			# LOG.debug("update_actions: Player 2 cannot move, player 1 feeds.")
			for i in self.get_actions(1):
				if self.board[i] + i < 6:
					try:
						self.actions.remove(i)
					except ValueError as e:
						raise ValueError("Couldn't remove action, {0}".format(e))
		# LOG.error("update_actions: Failed to remove action".format(i, e))
		elif p1_movable and p2_movable:
			# LOG.debug("update_actions: Both players can move, detecting grand slams.")
			self._remove_slam(player)
		# LOG.info("update_actions: Resulting actions are {0}".format(self.actions))
		# forgot why i put this here
		if not self.actions:
			# LOG.debug("Player has no moves")
			self._end_game()
			return

	def play(self, pit: int, player: int = 1) -> None:
		"""
		Plays a move based on selected pit and player.
		:param pit: Chosen pit number to play.
		:param player: Player number.
		:return: None
		"""
		if player != 1 and player != 2 or pit < 0 or pit >= BD_SIZE or (player == 1 and pit >= BD_SIZE // 2) or (
				player == 2 and pit < BD_SIZE // 2):
			raise ValueError("Invalid input to function. Player {0}, Action {1}, Board {2}".format(player, pit, self.board))
		elif self.is_terminal:
			raise ValueError("play: State is terminal, no more moves are allowed")
		# LOG.info("play: Playing move {0} for player {1}, board {2}".format(pit, player, self.board))
		# Remove action
		try:
			self.actions.remove(pit)
		except ValueError as e:
			# LOG.error("play: Invalid move chosen {0}. {1}".format(pit, e))
			raise ValueError("Couldn't remove action")
		affected = []
		# Get pieces, clear pit
		pieces = self.board[pit]
		self.board[pit] = 0
		# Distribute
		opponent = 2 // player
		i = pit
		while pieces > 0:
			if i == BD_SIZE - 1:
				i = 0
			else:
				i += 1
			pieces -= 1
			self.board[i] += 1
			# If pit contains 2 or 3 pieces and is on opponents side
			if (self.board[i] == 2 or self.board[i] == 3) and (
					opponent - 1) * BD_SIZE // 2 <= i < opponent * BD_SIZE // 2:
				affected.append(i)
			else:
				affected = []
		# Check for captures
		count = 0
		for i in affected:
			count += self.board[i]
			self.board[i] = 0
		if player == 1:
			self.p1_store += count
		else:
			self.p2_store += count
		self.num_moves += 1
		if self.p1_store > BD_SIZE * COUNT_PER_PIT // 2 or self.p2_store > BD_SIZE * COUNT_PER_PIT // 2 or \
				self.num_moves > MOVE_LIMIT:
			# LOG.debug("Player has captured more than half the pieces")
			self._end_game()
		else:
			self.update_actions(2 // player)

	def plain_reward(self) -> int:
		"""Reward function that indicates quality of terminal state."""
		return self.p1_store - self.p2_store

	def reward(self, player: int) -> float:
		h1 = self.board[(player - 1) * BD_SIZE // 2]
		h2 = sum(self.board[i] for i in range((player - 1) * BD_SIZE // 2, player * BD_SIZE // 2))
		h3 = sum(self.board[i] != 0 for i in range((player - 1) * BD_SIZE // 2, player * BD_SIZE // 2))
		h4 = 0
		h6 = 0
		if player == 1:
			h4 = self.p1_store
			h6 = self.p2_store
		elif player == 2:
			h4 = self.p2_store
			h6 = self.p1_store
		# Heuristic 5: "1 If previous move was the rightmost, 0 otherwise" is being ignored
		# It has weight 0.418841 if need in the future. These heuristics are taken from
		# Design of artificial intelligence for mancala games
		# https://www.politesi.polimi.it/handle/10589/134455
		heuristics = [h1, h2, h3, h4, h6]
		weights = [0.198649, 0.190084, 0.370793, 1, 0.565937]
		return sum(x * y for x, y in zip(heuristics, weights))

	def get_actions(self, player):
		"""
		Returns the list of available actions for the player.
		:param player: Integer that indicates player.
		:return: List of valid actions.
		"""
		return [x for x in self.actions if (player - 1) * BD_SIZE // 2 <= x < player * BD_SIZE // 2]
