#  Copyright (c) 2019 Owen Siljander
import time

from algs import *
from mancala import Mancala
from node import Node

# logging imported from algs.py
config = "%(asctime)s [%(levelname)s]:%(name)s - %(message)s"
logging.basicConfig(format=config, filename='log.log', level=logging.DEBUG, filemode="w")
main_log = logging.getLogger("main")
main_log.setLevel(logging.INFO)
# main_log.disabled = True

NUM_GAMES = 1


def cur_time():
	return int(round(time.time() * 1000))


class Measure:
	def __init__(self, name: str = "Generic Test"):
		self.num_games = 0
		self.name = name
		self.start = 0
		self.end = 0
		self.avg = 0
		self.tim = 0
		self.avg_dif = 0
		self.min_moves = 10000
		self.max_moves = -1
		self.min_time = 10000
		self.max_time = -1
		self.p1_wins = 0
		self.p2_wins = 0
		self.draws = 0

	def __repr__(self):
		if self.num_games == 0:
			return "No games played"
		r = "Test {0} completed with {1} games played.\n".format(self.name, self.num_games)
		r += "Average number of moves: ---- {0}\n".format(self.avg / self.num_games)
		r += "Average time: =============== {0}ms\n".format(self.tim / self.num_games)
		r += "Avg Reward: ---------------- {0}\n".format(self.avg_dif / self.num_games)
		r += "Max number of moves: ======== {0}\n".format(self.max_moves)
		r += "Min number of moves: -------- {0}\n".format(self.min_moves)
		r += "Max time: =================== {0}\n".format(self.max_time)
		r += "Min time: ------------------- {0}\n".format(self.min_time)
		r += "Player 1 won {0} time(s), Player 2 won {1} time(s), there were {2} draw(s)".format(self.p1_wins,
		                                                                                         self.p2_wins,
		                                                                                         self.draws)
		return r

	def avg(self, x):
		return sum(x)/len(x)

	def start_stats(self):
		self.start = cur_time()

	def update_stats(self, n: Node):
		self.num_games += 1
		self.end = cur_time()
		up_time = self.end - self.start
		self.tim += up_time
		self.avg += n.manc.num_moves
		self.min_moves = min(self.min_moves, n.manc.num_moves)
		self.max_moves = max(self.max_moves, n.manc.num_moves)
		self.min_time = min(self.min_time, up_time)
		self.max_time = max(self.max_time, up_time)
		self.avg_dif += n.reward()
		if n.manc.p1_store > n.manc.p2_store:
			self.p1_wins += 1
		elif n.manc.p2_store > n.manc.p1_store:
			self.p2_wins += 1
		else:
			self.draws += 1

	def end_stats(self):
		print(self)


def alphabeta_uct():
	# alphabeta v uct
	stats = Measure("Alpha-Beta v. UCT")
	for i in range(0, NUM_GAMES):
		# main_log.info("--------------------- GAME STARTED ---------------------")
		player = 1
		n = Node(Mancala())
		n.is_root = True
		stats.start_stats()
		try:
			while not n.leaf:
				if player % 2 == 1:
					uct(n, 1)
				else:
					# alphabeta(m_node, alpha, beta, player, depth)
					alphabeta(n, -1000, 1000, 2, True)
				player += 1
			stats.update_stats(n)
		except Exception:
			stats.end_stats()
		print("Game {0} finished. Moves: {1}. Winner: Player {2}".format(i, n.manc.num_moves,
		                                                                 1 if n.manc.p1_store > n.manc.p2_store else 2))
	stats.end_stats()


def alphabeta_alphabeta():
	# Test 1000 games with random agent
	stats = Measure("Alpha-Beta v. Alpha-Beta")
	player = 1
	for i in range(0, NUM_GAMES):
		# main_log.info("--------------------- GAME STARTED ---------------------")
		n = Node(Mancala())
		stats.start_stats()
		while not n.leaf:
			if player % 2 == 1:
				alphabeta(n, -1000, 1000, 2, True)
			else:
				alphabeta(n, -1000, 1000, 3, True)

			player += 1
		stats.update_stats(n)
		print("Game {0} finished. Moves: {1}. Winner: Player {2}".format(i, n.manc.num_moves,
		                                                                 1 if n.manc.p1_store > n.manc.p2_store else 2))
	stats.end_stats()


def random_alphabeta():
	# Test 1000 games with random agent
	stats = Measure("Random v. Alpha-Beta")
	player = 1
	for i in range(0, NUM_GAMES):
		# main_log.info("--------------------- GAME STARTED ---------------------")
		n = Node(Mancala())
		stats.start_stats()
		while not n.leaf:
			if player % 2 == 1:
				random_agent(n, 1)
			else:
				alphabeta(n, -1000, 1000, 2, 3, True)
			player += 1
		stats.update_stats(n)
		print("Game {0} finished. Moves: {1}. Winner: Player {2}".format(i, n.manc.num_moves,
		                                                                 1 if n.manc.p1_store > n.manc.p2_store else 2))
	stats.end_stats()


def alphabeta_fsss():
	depth1 = 7
	depth2 = 7
	stats = Measure("Alpha-Beta v. FSSS")
	player = 1
	for i in range(0, NUM_GAMES):
		# main_log.info("--------------------- GAME STARTED ---------------------")
		n = Node(Mancala())
		stats.start_stats()
		while not n.leaf:
			if player % 2 == 1:
				main_log.info("Alpha-Beta started")
				alphabeta(n, -1000, 1000, depth1, True)
			else:
				main_log.info("FSSS started")
				fsss(n, depth2)

			player += 1
		stats.update_stats(n)
		print("Game {0} finished. Moves: {1}. Winner: Player {2}".format(i, n.manc.num_moves,
		                                                                 1 if n.manc.p1_store > n.manc.p2_store else 2))
	stats.end_stats()


def generic():
	depth = 3
	depth2 = 5000
	# for depth in [1,3,5]:
	# 	for depth2 in [25,50,100]:
	print("Format: Depth {0} Iterations {1}".format(depth, depth2))
	stats = Measure("REE")
	player = 1
	for i in range(0, NUM_GAMES):
		print(".", end="")
		n = Node(Mancala())
		stats.start_stats()
		while not n.leaf:
			if player % 2 == 1:
				# random_agent(n)
				alphabeta(n, NEG_INF, POS_INF, depth, True)
				# fsss(n, depth)
				# uct(n, 1, 25, 1)
			else:
				# alphabeta(n, NEG_INF, POS_INF, depth2, True)
				# uct(n, 1, depth2, 1)
				uct(n, 1, depth2, 0)
			player += 1
		player = 1
		# main_log.info("GAME ENDED NOOB")
		stats.update_stats(n)
		# print("Game {0} finished. Moves: {1}. Winner: Player {2}".format(i, n.manc.num_moves,
		#                                                                  1 if n.manc.p1_store > n.manc.p2_store else 2))
	stats.end_stats()


def main():
	# alphabeta_uct()
	# random_alphabeta()
	# alphabeta_alphabeta()
	# alphabeta_fsss()
	generic()
	pass


if __name__ == "__main__":
	main()
