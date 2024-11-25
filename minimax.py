# minimax.py

from connectfour import PLAYER1, PLAYER2
from heuristic import score_position

MAX_DEPTH = 4  # Set a reasonable depth limit

def minimax(game, depth, maximizingPlayer, node_counter):
    node_counter['nodes'] += 1

    is_terminal = game.is_terminal_node()
    if depth == 0 or is_terminal:
        if is_terminal:
            if game.check_win(PLAYER1):
                return (None, float('inf'))
            elif game.check_win(PLAYER2):
                return (None, float('-inf'))
            else:  # Game is a draw
                return (None, 0)
        else:
            return (None, score_position(game, PLAYER1))

    valid_moves = game.get_valid_moves()

    if maximizingPlayer:
        value = float('-inf')
        best_move = valid_moves[0]
        for col in valid_moves:
            game.make_move(col, PLAYER1)
            new_score = minimax(game, depth - 1, False, node_counter)[1]
            game.undo_move(col)
            if new_score > value:
                value = new_score
                best_move = col
        return best_move, value
    else:
        value = float('inf')
        best_move = valid_moves[0]
        for col in valid_moves:
            game.make_move(col, PLAYER2)
            new_score = minimax(game, depth - 1, True, node_counter)[1]
            game.undo_move(col)
            if new_score < value:
                value = new_score
                best_move = col
        return best_move, value
