from playerInterface import *
from Goban import Board
from numpy.random import normal
from random import shuffle, choice
from time import time


class myPlayer(PlayerInterface):

    def __init__(self):
        self.board = Board()
        self.mycolor = None
        self.transposition_table = {}
        self.max_time = 7.4
        self.start_time = 0

    def getPlayerName(self):
        return "Team 38"

    def getPlayerMove(self):
        if self.board.is_game_over():
            return "PASS" 
        move = self.choose_action()
        self.board.push(move)
        return Board.flat_to_name(move) 

    def playOpponentMove(self, move):
        self.board.push(Board.name_to_flat(move)) 

    def newGame(self, color):
        self.mycolor = color
        self.opponent = Board.flip(color)

    def endGame(self, winner):
        if self.mycolor == winner:
            print("I won :D")
        else:
            print("I lost :(")

    def choose_action(self):
        depth = 1
        self.start_time = time()
        (eval_score, selected_action) = (-1, -1)
        while(True):
            tmp_time = time()
            self.transposition_table = {}
            new_score, new_action = self.minimax(depth, True, float('-inf'), float('+inf'))
            if (time()-self.start_time < self.max_time):
                (eval_score, selected_action) = (new_score, new_action)
            print("MINIMAX AB ID(%d) : eval=%f, action=%d, time=%s" % (depth, eval_score, selected_action, time()-tmp_time))
            if (time()-self.start_time >= self.max_time):
                break
            depth+=1
        return selected_action

    def minimax(self, depth, is_max_turn, alpha, beta):
        transposition = self.transposition_table.get(str(self.board._currentHash))
        if transposition != None:
            return transposition
        if depth == 0 or (time()-self.start_time >= self.max_time) or self.board.is_game_over():
            result = (self.evaluate(), None) # self.player_color
            self.transposition_table.update({str(self.board._currentHash): result})
            return result
        key_of_actions = list(self.board.generate_legal_moves())
        shuffle(key_of_actions) #randomness
        best_value = float('-inf') if is_max_turn else float('+inf')
        best_action = -1
        action_targets = []
        for action_key in key_of_actions:
            self.board.push(action_key)
            eval_child, action_child = self.minimax(depth-1, not is_max_turn, alpha, beta)
            self.board.pop()
            if is_max_turn and best_value < eval_child:
                best_value = eval_child
                action_targets.clear()
                action_targets.append(action_key)
                alpha = max(alpha, best_value)
                if beta <= alpha:
                    break
            elif (not is_max_turn) and best_value > eval_child:
                best_value = eval_child
                action_targets.clear()
                action_targets.append(action_key)
                beta = min(beta, best_value)
                if beta <= alpha:
                    break
            elif best_value == eval_child:
                action_targets.append(action_key)
        if not not action_targets:
            best_action = choice(action_targets) #randomness
        self.transposition_table.update({str(self.board._currentHash): (best_value, best_action)})
        return (best_value, best_action)

    def evaluate(self):
        position_score = [ 0, 0, 0, 0, 0, 0, 0, 0, 0,
                           0, 2, 2, 2, 1, 2, 2, 2, 0,
                           0, 2, 2, 2, 1, 2, 2, 2, 0,
                           0, 2, 2, 1, 1, 1, 2, 2, 0,
                           0, 1, 1, 1, 1, 1, 1, 1, 0,
                           0, 2, 2, 1, 1, 1, 2, 2, 0,
                           0, 2, 2, 2, 1, 2, 2, 2, 0,
                           0, 2, 2, 2, 1, 2, 2, 2, 0,
                           0, 0, 0, 0, 0, 0, 0, 0, 0]

        score_pieces = 0
        if self.board.next_player() == Board._BLACK:
            score_pieces += (self.board._nbWHITE-self.board._nbBLACK)*3 # score for white
        else:
            score_pieces += (self.board._nbBLACK-self.board._nbWHITE)*3 # score for black

        score_liberties = 0
        score_positions = 0
        for fcoord in range(len(self.board)):
            if self.board[fcoord] == Board._EMPTY:
                pass
            elif self.board[fcoord] == self.board.next_player():
                # Liberties
                string = self.board._getStringOfStone(fcoord)
                score_liberties -= self.board._stringLiberties[string]*1
                # Corner + position
                score_positions -= position_score[fcoord]*10
            else:
                # Liberties
                string = self.board._getStringOfStone(fcoord)
                score_liberties += self.board._stringLiberties[string]*1
                # Corner + position
                score_positions += position_score[fcoord]*10

        if self.board.next_player() == self.mycolor:
            score_pieces *= -1
            score_liberties *= -1
            score_positions *= -1

        
        return score_pieces*normal(1, 0.1) + score_positions*normal(1, 0.1) + score_liberties*normal(1, 0.1)