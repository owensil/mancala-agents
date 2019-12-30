# CSCI 4511W Project - Fall 2019  
Mancala AI written in Python for my CSCI 4511W (Intro. to AI) project. The variant of mancala implemented is Awari, which is commonly used for research. Nonetheless, the algorithms themselves are disjoint from the rules of the game.

## Agents/Algorithms  
- Random Agent
- Monte-Carlo Tree Search (MCTS), the popular variant known as Upper Confidence Bound applied to Trees (UCT)  
- Alpha-Beta Pruning Minimax  
- Forward Search Sparse Sampling Minimax (FSSS-Minimax)  

For the sake of brevity, Alpha-Beta Minimax and FSSS-Minimax will be called Minimax and FSSS respectively.

## Overview
The program is separated into three sections: the mancala class, a node class, and the search algorithms. The mancala class is responsible for updating each players moves, capturing pieces, and performing moves. The node class is used for allowing searches through games states and is necessary for retaining information used to guide the algorithms searches.

## Known Issues
- Currently, the game is highly deterministic. Pitting FSSS against Minimax results in the two agents playing the same game repeatedly.  
- UCT is grossly underperformant. Commonly in literature, UCT will be used with upwards of several thousands of iterations (rollouts). Attempting such with this project would cause data collection to take on the order of days. It is unknown to me exactly how UCT is used in literature, this could also be an issue with end-game detection.  
- Detection of move loops is not implemented, this could vastly improve the performance of UCT. Currently, the game sets a hard limit on the number of moves before the game ends. Actually detecting this is quite tricky.
