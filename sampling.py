from heuristic import evaluate
from connectfour import ConnectFour, PLAYER1, PLAYER2
from dotsandboxes import DotsAndBoxes
from nim import Nim
from transpositiontable import TranspositionTable, EXACT
from minimax import apply_move, undo_move
import random

def minimax_sample(game, depth, game_size, maximizingPlayer, node_counter, sample_size=None):
    node_counter['nodes'] += 1

    # are we at terminal node / did we reach depth limit?
    is_terminal = game.is_terminal_node()
    winner = game.get_winner(maximizingPlayer)
    if depth == 0 or is_terminal:
        if winner is not None:
            if winner:
                return (None, float('inf'))
            elif winner is False:
                return (None, float('-inf'))
            else:
                return (None, 0)  # Draw
        else:
            return (None, evaluate(game, maximizingPlayer))

    # get valid moves
    if isinstance(game, Nim):
        valid_moves = game.get_valid_moves(game_size)
    else:
        valid_moves = game.get_valid_moves()

    # random sampling to ensure computation time doesn't take too long
    if sample_size is not None and len(valid_moves) > sample_size:
        valid_moves = random.sample(valid_moves, sample_size)

    # exact same as minimax algorithm here
    if maximizingPlayer:
        value = float('-inf')
        best_move = None
        for move in valid_moves:

            if hasattr(game, 'set_current_player'):
                game.set_current_player(PLAYER1 if maximizingPlayer else PLAYER2)
            apply_move(game, move, maximizingPlayer)

            _, new_score = minimax_sample(game, depth - 1, game_size, False, node_counter, sample_size)

            undo_move(game, move, maximizingPlayer)

            if new_score > value:
                value = new_score
                best_move = move

        return best_move, value

    else:
        value = float('inf')
        best_move = None
        for move in valid_moves:

            if hasattr(game, 'set_current_player'):
                game.set_current_player(PLAYER1 if maximizingPlayer else PLAYER2)
            apply_move(game, move, maximizingPlayer)

            _, new_score = minimax_sample(game, depth - 1, game_size, True, node_counter, sample_size)

            undo_move(game, move, maximizingPlayer)

            if new_score < value:
                value = new_score
                best_move = move

        return best_move, value
