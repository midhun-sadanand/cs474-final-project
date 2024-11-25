# alphabeta.py

from connectfour import PLAYER1, PLAYER2
from heuristic import score_position

MAX_DEPTH = 4  # Set a reasonable depth limit

def alphabeta(game, depth, alpha, beta, maximizingPlayer, node_counter):
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
            new_score = alphabeta(game, depth - 1, alpha, beta, False, node_counter)[1]
            game.undo_move(col)
            if new_score > value:
                value = new_score
                best_move = col
            alpha = max(alpha, value)
            if alpha >= beta:
                break  # Beta cut-off
        return best_move, value
    else:
        value = float('inf')
        best_move = valid_moves[0]
        for col in valid_moves:
            game.make_move(col, PLAYER2)
            new_score = alphabeta(game, depth - 1, alpha, beta, True, node_counter)[1]
            game.undo_move(col)
            if new_score < value:
                value = new_score
                best_move = col
            beta = min(beta, value)
            if alpha >= beta:
                break  # Alpha cut-off
        return best_move, value
