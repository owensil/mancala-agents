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


## Resources

**[1]** Baier, Hendrik, and Mark HM Winands. "Monte-Carlo tree search and minimax hybrids." In 2013 IEEE Conference on Computational Inteligence in Games (CIG), pp. 1-8. IEEE, 2013.  

**[2]** Baier, Hendrik, and Mark HM Winands. "MCTS-minimax hybrids." IEEE Transactions on Computational Intelligence and AI in Games 7, no. 2 (2014): 167-179.  

**[3]** Browne, Cameron B., Edward Powley, Daniel Whitehouse, Simon M. Lucas, Peter I. Cowling, Philipp Rohlfshagen, Stephen Tavener, Diego Perez, Spyridon Samothrakis, and Simon Colton. "A survey of monte carlo tree search methods." IEEE Transactions on Computational Intelligence and AI in games 4, no. 1 (2012): 1-43.  

**[4]** James, Steven, George Konidaris, and Benjamin Rosman. "An analysis of monte carlo tree search." In Thirty-First AAAI Conference on Artificial Intelligence. 2017.  

**[5]** Kocsis, Levente, and Csaba Szepesvári. "Bandit based monte-carlo planning." In European conference on machine learning, pp. 282-293. Springer, Berlin, Heidelberg, 2006.  

**[6]** Rada, Roy. "Characterizing Search Spaces." In IJCAI, pp. 780-782. 1983.  

**[7]** Ramanujan, Raghuram, Ashish Sabharwal, and Bart Selman. "On the behavior of UCT in synthetic search spaces." In Proc. 21st Int. Conf. Automat. Plan. Sched., Freiburg, Germany. 2011.  

**[8]** Ramanujan, Raghuram, and Bart Selman. "Trade-offs in sampling-based adversarial planning." In Twenty-First International Conference on Automated Planning and Scheduling. 2011.  

**[9]** Ramanujan, Raghuram, Ashish Sabharwal, and Bart Selman. "On adversarial search spaces and sampling-based planning." In Twentieth International Conference on Automated Planning and Scheduling. 2010.  

**[10]** ROVARIS, GABRIELE. "Design of artificial intelligence for mancala games." (2017).  

**[11]** Weinstein, Ari, Michael L. Littman, and Sergiu Goschin. "Rollout-based game-tree search outprunes traditional alpha-beta." In European Workshop on Reinforcement Learning, pp. 155-167. 2013.  
