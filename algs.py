#  Copyright (c) 2019 Owen Siljander
import logging
from datetime import datetime
from math import log, sqrt
from random import randint, seed

from node import Node, NEG_INF, POS_INF
from mancala import Mancala

AB_NODES_EXPANDED = 0
UCT_NODES_EXPANDED = 0
FS_NODES_EXPANDED = 0
EPSILON = 0.00001
EPSIL = 0.001

seed(datetime.now)

# Logging
config = "%(asctime)s [%(levelname)s]:%(name)s - %(message)s"
logging.basicConfig(format=config, filename='log.log', level=logging.DEBUG, filemode="w")
rand_log = logging.getLogger("rand_agent")
rand_log.disabled = False
rand_log.setLevel(logging.DEBUG)

alpha_log = logging.getLogger("alphabeta")
alpha_log.disabled = False
alpha_log.setLevel(logging.DEBUG)

uct_log = logging.getLogger("uct")
uct_log.disabled = False
uct_log.setLevel(logging.DEBUG)

fs_log = logging.getLogger("fsss")
fs_log.disabled = False
fs_log.setLevel(logging.DEBUG)


# ******************************************************************************
# * Random Agent
# ******************************************************************************

def random_agent(m_node: Node) -> None:
	"""
	Random agent, picks pseudo-random moves
	:param m_node: Node to play move for
	:return: void
	"""
	# rand_log.info("----- Random Agent Playing -----")
	actions = m_node.get_actions()
	try:
		choice = actions[randint(0, len(actions) - 1)]
	except ValueError as e:
		# rand_log.error("Encountered empty range, aborting. {0}".format(e))
		raise ValueError("No possible move")
	else:
		# rand_log.info("Random Playing move {0}. P1 {1} P2 {2}, Board {3}".format(choice, m_node.manc.p1_store, m_node.manc.p2_store, m_node.manc.board))
		m_node.play(choice)
	# rand_log.info("Random made their move")


# ******************************************************************************
# * Depth-limited Alpha-Beta Minimax
# ******************************************************************************

def alphabeta(m_node, alpha, beta, depth, is_root):
	"""
	Depth-limited Alpha-Beta Minimax search. Return value should not be captured by user.
	:param m_node: Node representing state within transition graph.
	:param alpha: Alpha
	:param beta: Beta
	:param depth: Depth limit of search.
	:param is_root: Used internally, not set by user
	:return: None
	"""
	global AB_NODES_EXPANDED
	# Terminal, return reward
	AB_NODES_EXPANDED += 1
	if m_node.leaf or depth == 0:
		return m_node.reward()
	best_value = None
	best_action = -1
	for action in m_node.get_actions():
		res_value = alphabeta(m_node.rollout(action), alpha, beta, depth - 1, False)
		if best_value is None:
			best_value = res_value
			if is_root:
				best_action = action
		if m_node.player == 1:
			if res_value > best_value:
				best_value = res_value
				if is_root:
					best_action = action
			alpha = max(alpha, best_value)
		elif m_node.player == 2:
			if res_value < best_value:
				if is_root:
					best_action = action
				best_value = min(best_value, res_value)
			beta = min(beta, best_value)
		# Children can't influence choice at root, don't explore further
		if alpha >= beta:
			break
	if is_root:
		# Back at root node, play out action
		# alpha_log.info("Playing move {0}. P1 {1} P2 {2}, Board {3}".format(best_action, m_node.manc.p1_store, m_node.manc.p2_store, m_node.manc.board))
		m_node.play(best_action)
		alpha_log.info("Alpha-Beta finished with {0} nodes expanded".format(AB_NODES_EXPANDED))
		AB_NODES_EXPANDED = 0
		return
	else:
		# Propagate value back up tree
		return best_value


# ******************************************************************************
# * UCT
# ******************************************************************************

def default_policy(n: Node) -> float:
	"""
	Simulates node to end of game
	:param n: Node to be simulated from
	:return: Resulting reward
	"""
	m = Node.copy_node(n)
	global UCT_NODES_EXPANDED
	UCT_NODES_EXPANDED += 1
	while not m.leaf:
		random_agent(m)
	if m.manc.p1_store > m.manc.p2_store:
		return 1
	elif m.manc.p1_store == m.manc.p2_store:
		return 0.5
	else:
		return 0


def heuristic_policy(n: Node) -> float:
	m = Node.copy_node(n)
	global UCT_NODES_EXPANDED
	UCT_NODES_EXPANDED += 1
	while not m.leaf:
		random_agent(m)
	return m.reward()


def back_propagate(n: Node, delta: float) -> None:
	"""
	Backpropagates rollout policy results back up the tree
	:param n: Node to backpropagate from
	:param delta: Delta reward, i.e. "how much success"
	:return: None
	"""
	while n is not None:
		n.visits += 1
		n.tot_reward += delta
		n = n.parent


def best_uct_child(n: Node, c: float) -> Node:
	"""
	Calculates best UCT bound for children
	:param n: Node to calculate best child for
	:param c: Constant for UCB1
	:return: Node, for use as part of selecting node to simulate (default_policy)
	"""
	best = NEG_INF
	max_child = n.children[0]
	for i in n.children:
		res = i.tot_reward / i.visits + c * sqrt(2)/2 * sqrt(log(n.visits / i.visits))
		if res > best:
			best = res
			max_child = i
	return max_child


def expand(n: Node) -> Node:
	"""
	Plays an untried action for node n
	:param n: Node to expand
	:return: Child node of n
	"""
	# uct_log.debug("expand: Expanding node, board {0}".format(n.manc.board))
	a = n.untried_actions[0]
	n.untried_actions.remove(a)
	# uct_log.debug("expand: Expanding node with action {0}".format(a))
	n0 = n.rollout(a)
	n.children.append(n0)
	# uct_log.debug("expand: Added child {0} to node {1}".format(n0, n))
	n0.parent = n
	n0.action = a
	return n0


def tree_policy(n: Node, constant) -> Node:
	"""
	Selects which node to simulate next and generate reward for
	:param n: Node to expand from
	:param constant: Constant for UCB1
	:return: Selected node with best UCB1
	"""
	# uct_log.debug("tree_policy: Selecting node for simulation")
	while not n.leaf:
		# First do any untried actions
		if n.untried_actions:
			return expand(n)
		else:
			n = best_uct_child(n, constant)
	return n


def uct(m_node: Node, constant, limit, policy) -> None:
	"""
	Generates an action to choose based on the UCT algorithm.
	:param m_node: Node to choose action for
	:param constant: Constant for UCB1
	:param limit: Max number of expansions
	:param policy: Policy for reward
	:return: Action
	"""
	global UCT_NODES_EXPANDED
	i = 0
	# uct_log.info("----- UCT Agent Playing -----")
	while i < limit:
		# uct_log.debug("uct: m_node has untried actions {0}".format(m_node.untried_actions))
		# uct_log.debug("uct: m_node has children {0}".format([x for x in m_node.children]))
		n1 = tree_policy(m_node, constant)  # UCT Algorithm
		if policy == 0:
			delta = default_policy(n1)  # Simulate random game
		else:
			delta = heuristic_policy(n1)
		back_propagate(n1, delta)  # Push results back up tree
		i += 1
	# should return an action, maybe have it play instead? or helper
	m_node.play(best_uct_child(m_node, constant).action)
	# uct_log.info("Expanded {0} nodes".format(UCT_NODES_EXPANDED))
	UCT_NODES_EXPANDED = 0


# uct_log.info("----- UCT Agent Finished -----")


# ******************************************************************************
# * FSSS-Minimax
# ******************************************************************************

# Upper and Lower bounds U and L
# <G, A, S, T>: Graph, Actions, States, Transition


def traverse(state: Node, alpha: float, beta: float) -> tuple:
	"""
	Selects which node to expand for search
	:param state: Current node to select action of
	:param alpha: Alpha
	:param beta: Beta
	:return: tuple
	"""
	global FS_NODES_EXPANDED
	assert (state.player == 1 or state.player == 2)
	# fs_log.debug("Traversing node {0} as player {1}".format(state, state.player))
	for i in state.get_actions():
		if i not in state.childs.keys():
			FS_NODES_EXPANDED += 1
			state.childs[i] = state.rollout(i)
		state.Uprime[i] = min(beta, state.childs[i].U)
		state.Lprime[i] = max(alpha, state.childs[i].L)
	aprime = alpha
	bprime = beta
	# Max player
	if state.player == 1:
		# Get key that produces largest value
		i_star = max(state.Uprime.keys(), key=(lambda k: state.Uprime[k]))
		try:
			# Get max value for when key is not the maximum
			v = max(state.Uprime[x] for x in state.Uprime.keys() if x != i_star)
			aprime = max(alpha, v)
		except ValueError as e:
			# fs_log.error("Node has only one child, returning...")
			pass
		if aprime == state.Uprime[i_star]:
			aprime = aprime - EPSILON
	else:
		# Get key that produces smallest value
		i_star = min(state.Lprime.keys(), key=(lambda k: state.Lprime[k]))
		# Get max value for when key is not the maximum
		try:
			v = min(state.Lprime[x] for x in state.Lprime.keys() if x != i_star)
			bprime = min(beta, v)
		except ValueError as e:
			# fs_log.error("Node has only one child, returning...")
			pass
		if bprime == state.Lprime[i_star]:
			bprime = bprime + EPSILON
	# fs_log.debug("Best action for board {0} is {1}".format(state.manc.board, i_star))
	return i_star, aprime, bprime


def search(state: Node, alpha: float, beta: float, limit: int) -> None:
	"""
	Generates the upper and lower bounds U and L for the node
	:param state: Node to search
	:param alpha: Alpha
	:param beta: Beta
	:param limit: Depth limit
	:return: None
	"""
	# fs_log.debug("Searching node {0} as player {1}".format(state, state.player))
	if state.leaf or limit == 0:
		state.L = state.U = state.reward()
		# fs_log.debug("Node is terminal or reaches depth limit, returning reward {0}".format(state.L))
		return
	i_star, aprime, bprime = traverse(state, alpha, beta)
	search(state.childs[i_star], aprime, bprime, limit - 1)
	# fs_log.debug("Finished recursive search, back at node {0}".format(state))
	# Update state upper and lower bounds
	actions = state.get_actions()
	# fs_log.debug("Setting L and U to be first child")
	state.L = state.childs[actions[0]].L
	state.U = state.childs[actions[0]].U
	# fs_log.debug("Covering other actions")
	for i in actions:
		if state.player == 1:
			# Maximize
			state.L = max(state.L, state.childs[i].L)
			state.U = max(state.U, state.childs[i].U)
		elif state.player == 2:
			state.L = min(state.L, state.childs[i].L)
			state.U = min(state.U, state.childs[i].U)
	# fs_log.debug("Update L and U are {0} and {1}".format(state.L, state.U))
	return


def fsss(state: Node, limit: int):
	global FS_NODES_EXPANDED
	while abs(state.L - state.U) > EPSILON:
		# fs_log.debug("Searching root node")
		search(state, NEG_INF, POS_INF, limit)
	fs_log.info("FSSS finished with {0} nodes expanded".format(FS_NODES_EXPANDED))
	FS_NODES_EXPANDED = 0
	action = max(state.childs.keys(), key=(lambda k: state.childs[k].L))
	state.play(action)
