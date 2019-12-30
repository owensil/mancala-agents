#  Copyright (c) 2019 Owen Siljander
from copy import copy

from mancala import Mancala

# import logging

# These aren't really replaceable with Python's handy dandy `i = float('inf')`
NEG_INF = -1000
POS_INF = 1000


# Used for logging, this has a severe impact on runtime performance due to number of calls to the functions
# below, use this only for diagnosing issues. Typical log file sizes are anywhere from 25-100+MB
# config = "%(asctime)s [%(levelname)s]:%(name)s - %(message)s"
# logging.basicConfig(format=config, filename='log.log', level=logging.DEBUG, filemode="w")
# node_log = logging.getLogger("node")
# node_log.disabled = True
# LOG.setLevel(logging.INFO)
# node_log.setLevel(logging.DEBUG)


class Node:
	def __init__(self, manc: Mancala, player: int = 1, depth: int = 0, parent=None, terminal: bool = False):
		"""
		Node class representing a specific game state within a search tree. Contains useful tree m_node attributes.
		:param manc: Mancala class.
		:param player: Player number, 1 or 2.
		:param depth: Depth of node. Root node is depth 0. This isn't really used but may be useful.
		:param parent: Parent node.
		:param terminal: Indicates if node is a leaf node or not.
		"""
		# node_log.debug("Node created, is_terminal: {0}".format(terminal))
		self.leaf = terminal  # Is a leaf node (i.e. terminal game state)
		self.depth = depth  # Depth of node
		self.visits = 0  # Number of visits to node, UCT
		self.tot_reward = 0  # Reward of node, UCT
		self.parent = parent  # Parent node
		self.action = -1  # Action taken to get here from parent
		self.player = player  # Current player's turn
		if manc.is_terminal:
			self.leaf = True
		self.manc = manc  # Mancala board
		self.untried_actions = self.manc.get_actions(player)  # Used in UCT to avoid UCB1 computations
		self.children = []  # Children of the node
		self.U = POS_INF  # Upper bound, FSSS-Minimax
		self.L = NEG_INF  # Lower bound, FSSS-Minimax
		self.Uprime = {}  # Used in FSSS-Minimax
		self.Lprime = {}  # Used in FSSS-Minimax
		# This is a bandage for needing a map in FSSS-Minimax, child node mapped by action
		self.childs = {}

		# Testing purposes
		self.value = 0
		self.actions = []

	@staticmethod
	def copy_node(n):
		"""
		Copies most required data into a new node, this is much faster than performing a deepcopy every time
		:param n: Node to be copied
		:return: Copied node
		"""
		m = Node(Mancala(), n.player, n.depth, None, n.manc.is_terminal)
		m.manc.board = copy(n.manc.board)
		m.manc.actions = copy(n.manc.actions)
		m.manc.is_terminal = n.manc.is_terminal
		m.manc.p1_store = n.manc.p1_store
		m.manc.p2_store = n.manc.p2_store
		m.manc.num_moves = n.manc.num_moves
		return m

	def rollout(self, action: int):
		"""
		Plays an action but returns a new node with this action played within the game
		:param action: Action to play
		:return: Node with its game having played the action
		"""
		n = Node.copy_node(self)
		n.play(action)
		return n

	def play(self, action: int) -> None:
		"""
		Plays an action, modifying the current game and hence the node
		:param action: Action to play
		:return: None
		"""
		self.manc.play(action, self.player)
		self.player = 2 // self.player
		self.untried_actions = self.get_actions()
		# All information about the node as a part of a tree is clobbered
		self.children = []
		self.parent = None
		self.Uprime = {}
		self.Lprime = {}
		self.childs = {}
		self.L = NEG_INF
		self.U = POS_INF
		if self.manc.is_terminal:
			self.leaf = True

	def plain_reward(self) -> int:
		"""A plain and simple heuristic for determining value of the state of the game"""
		return self.manc.plain_reward()

	def reward(self) -> float:
		"""More advanced heuristic calculation version of self.plain_reward()"""
		return self.manc.reward(self.player)

	def get_actions(self):
		"""Get's the available actions for the current node"""
		return self.manc.get_actions(self.player)

	# Below functions are used for testing FSSS-Minimax
	def test_get_actions(self):
		return self.actions

	def test_reward(self):
		return self.value
