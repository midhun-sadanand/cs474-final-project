# alphabeta.py

from heuristic import evaluate
from connectfour import ConnectFour, PLAYER1, PLAYER2
from nim import Nim
from dotsandboxes import DotsAndBoxes

def alphabeta(game, depth, alpha, beta, maximizingPlayer, node_counter):
    node_counter['nodes'] += 1

    is_terminal = game.is_terminal_node()
    winner = game.get_winner(maximizingPlayer)
    if depth == 0 or is_terminal:
        if winner is not None:
            if winner:
                return (None, float('inf'))
            elif winner is False:
                return (None, float('-inf'))
            else:
                return (None, 0) 
        else:
            return (None, evaluate(game, maximizingPlayer))

    valid_moves = game.get_valid_moves()

    # greedy maximize
    if maximizingPlayer:
        value = float('-inf')
        best_move = None
        for move in valid_moves:
            if hasattr(game, 'set_current_player'):
                # maximizing player
                game.set_current_player(1)  
            if isinstance(game, ConnectFour):
                game.make_move(move, PLAYER1)
            elif isinstance(game, Nim):
                heap_index, remove_count = move
                game.make_move(heap_index, remove_count)
            elif isinstance(game, DotsAndBoxes):
                game.make_move(move)
            else:
                game.make_move(move)
            new_score = alphabeta(game, depth - 1, alpha, beta, False, node_counter)[1]
            if isinstance(game, ConnectFour):
                game.undo_move(move)
            elif isinstance(game, Nim):
                heap_index, remove_count = move
                game.undo_move(heap_index, remove_count)
            elif isinstance(game, DotsAndBoxes):
                game.undo_move(move)
            else:
                game.undo_move(move)
            if new_score > value:
                value = new_score
                best_move = move
            alpha = max(alpha, value)
            # beta cutoff
            if alpha >= beta:
                break
        return best_move, value
    # greedy minimize
    else:
        value = float('inf')
        best_move = None
        for move in valid_moves:
            if hasattr(game, 'set_current_player'):
                game.set_current_player(-1)  
            if isinstance(game, ConnectFour):
                game.make_move(move, PLAYER2)
            elif isinstance(game, Nim):
                heap_index, remove_count = move
                game.make_move(heap_index, remove_count)
            elif isinstance(game, DotsAndBoxes):
                game.make_move(move)
            else:
                game.make_move(move)
            new_score = alphabeta(game, depth - 1, alpha, beta, True, node_counter)[1]
            if isinstance(game, ConnectFour):
                game.undo_move(move)
            elif isinstance(game, Nim):
                heap_index, remove_count = move
                game.undo_move(heap_index, remove_count)
            elif isinstance(game, DotsAndBoxes):
                game.undo_move(move)
            else:
                game.undo_move(move)
            if new_score < value:
                value = new_score
                best_move = move
            beta = min(beta, value)
            # beta cutoff
            if alpha >= beta:
                break
        return best_move, value
