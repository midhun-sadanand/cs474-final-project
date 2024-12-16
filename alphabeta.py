from heuristic import evaluate
from connectfour import ConnectFour, PLAYER1, PLAYER2
from dotsandboxes import DotsAndBoxes
from nim import Nim
from minimax import apply_move, undo_move
from transpositiontable import TranspositionTable, EXACT, LOWERBOUND, UPPERBOUND

def alphabeta(game, depth, game_size, alpha, beta, maximizingPlayer, node_counter, tt):
    node_counter['nodes'] += 1
    original_alpha = alpha
    original_beta = beta
    state_key = game.get_state_key(maximizingPlayer)

    # transposition table (if specified) lookup
    if tt is not None:
        found, tt_move, tt_value = tt.ab_lookup(state_key, depth, alpha, beta)
        if found:
            return tt_move, tt_value

    # check if terminal node / if depth is reached
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

    if isinstance(game, Nim):
        valid_moves = game.get_valid_moves(game_size)
    else:
        valid_moves = game.get_valid_moves()

    # similar to minimax algorithm here (+ alpha-beta cutoff)
    if maximizingPlayer:
        value = float('-inf')
        best_move = None

        for move in valid_moves:
            
            # apply move
            if hasattr(game, 'set_current_player'):
                game.set_current_player(PLAYER1 if maximizingPlayer else PLAYER2)
            apply_move(game, move, maximizingPlayer)

            # recurse
            _, new_score = alphabeta(game, depth - 1, game_size, alpha, beta, False, node_counter, tt)

            # undo move
            undo_move(game, move, maximizingPlayer)

            if new_score > value:
                value = new_score
                best_move = move

            alpha = max(alpha, value)
            if alpha >= beta:
                break

        # store in transposition table (if specified)
        if tt is not None:
            if value <= original_alpha:
                move_flag = UPPERBOUND
            elif value >= original_beta:
                move_flag = LOWERBOUND
            else:
                move_flag = EXACT
            tt.ab_store(state_key, depth, value, best_move, move_flag, original_alpha, original_beta)

        return best_move, value

    else:
        value = float('inf')
        best_move = None

        for move in valid_moves:
            # apply move
            if hasattr(game, 'set_current_player'):
                game.set_current_player(PLAYER1 if maximizingPlayer else PLAYER2)
            apply_move(game, move, maximizingPlayer)

            # recurse
            _, new_score = alphabeta(game, depth - 1, game_size, alpha, beta, True, node_counter, tt)

            # undo move
            undo_move(game, move, maximizingPlayer)

            if new_score < value:
                value = new_score
                best_move = move

            beta = min(beta, value)
            if alpha >= beta:
                break

        # store in transposition table (if specified)
        if tt is not None:
            if value <= original_alpha:
                move_flag = UPPERBOUND
            elif value >= original_beta:
                move_flag = LOWERBOUND
            else:
                move_flag = EXACT
            tt.ab_store(state_key, depth, value, best_move, move_flag, original_alpha, original_beta)

        return best_move, value
