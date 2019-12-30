#  Copyright (c) 2019 Owen Siljander
from algs import alphabeta
from mancala import Mancala
from node import Node


def main():
	n = Node(Mancala())
	while not n.leaf:
		alphabeta(n, -1000, 1000, 1, 5, True)
		print(n.manc)
		a = int(input("Enter action: "))
		n.play(a)


if __name__ == "__main__":
	main()
