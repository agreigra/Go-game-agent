alphabetaPlayer.py: (Reference implementation viewed in class)
	# Techniques used:
		TODO: évoquez comment vous avez décidé d'utiliser telle ou telle technique
		- Minimax algorithm
		- Alpha-Beta pruning
		- iterative deepening (max_time = 7.4 sec)
		- Transposition table (unlimited size)
	# Heuristique
		we didn't have a clear idea how to implement this, and online resource are complicated (research papers),
		so we tried a simple evaluation using score, piece positions and liberties.

mctsPlayer.py:
	Monte Carlo Tree Search: (inspired by Deep Learning and the Game of Go by Max Pumperla Kevin Ferguson)
	we started with this algorithm because we didn't have a clear idea how to implement the evaluation function,
	but the implementation of Goban.py wasn't fast enough to run multiple simulation (150-450 simulation in 7.4 seconds, but we needed 1000 at least to make a good move),
	so we dropped this idea, and we ended up with the above implementation of alpha-beta (alphabetaPlayer.py).

myPlayer.py:
	Just a copy of alphabetaPlayer.py for the AI Tournament
