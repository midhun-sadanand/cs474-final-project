from heuristic import evaluate
from connectfour import ConnectFour, PLAYER1, PLAYER2
from nim import Nim
from dotsandboxes import DotsAndBoxes
from transpositiontable import TranspositionTable, EXACT, LOWERBOUND, UPPERBOUND

def alphabeta(game, depth, game_size, alpha, beta, maximizingPlayer, node_counter, tt):
    node_counter['nodes'] += 1

    original_alpha = alpha
    original_beta = beta

    state_key = game.get_state_key(maximizingPlayer)

    # If using TT, try lookup
    if tt is not None:
        found, tt_move, tt_value = tt.ab_lookup(state_key, depth, alpha, beta)
        if found:
            # EXACT hit or cutoff recognized by LOWERBOUND/UPPERBOUND
            return tt_move, tt_value

    # Check if node is terminal or depth reached
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

    if isinstance(game, Nim):
        valid_moves = game.get_valid_moves(game_size)
    else:
        valid_moves = game.get_valid_moves()

    if maximizingPlayer:
        value = float('-inf')
        best_move = None

        for move in valid_moves:
            # Make move
            if isinstance(game, ConnectFour):
                game.make_move(move, PLAYER1)
            elif isinstance(game, Nim):
                heap_index, remove_count = move
                game.make_move(heap_index, remove_count)
            elif isinstance(game, DotsAndBoxes):
                game.set_current_player(PLAYER1)
                game.make_move(move)

            # Search deeper
            new_score = alphabeta(game, depth - 1, game_size, alpha, beta, False, node_counter, tt)[1]

            # Undo move
            if isinstance(game, ConnectFour):
                game.undo_move(move)
            elif isinstance(game, Nim):
                heap_index, remove_count = move
                game.undo_move(heap_index, remove_count)
            elif isinstance(game, DotsAndBoxes):
                game.set_current_player(PLAYER1)
                game.undo_move(move)

            if new_score > value:
                value = new_score
                best_move = move

            alpha = max(alpha, value)
            if alpha >= beta:
                break

        # Store results in TT if in use
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
            if isinstance(game, ConnectFour):
                game.make_move(move, PLAYER2)
            elif isinstance(game, Nim):
                heap_index, remove_count = move
                game.make_move(heap_index, remove_count)
            elif isinstance(game, DotsAndBoxes):
                game.set_current_player(PLAYER2)
                game.make_move(move)

            new_score = alphabeta(game, depth - 1, game_size, alpha, beta, True, node_counter, tt)[1]

            if isinstance(game, ConnectFour):
                game.undo_move(move)
            elif isinstance(game, Nim):
                heap_index, remove_count = move
                game.undo_move(heap_index, remove_count)
            elif isinstance(game, DotsAndBoxes):
                game.set_current_player(PLAYER2)
                game.undo_move(move)

            if new_score < value:
                value = new_score
                best_move = move

            beta = min(beta, value)
            if alpha >= beta:
                break

        if tt is not None:
            if value <= original_alpha:
                move_flag = UPPERBOUND
            elif value >= original_beta:
                move_flag = LOWERBOUND
            else:
                move_flag = EXACT
            tt.ab_store(state_key, depth, value, best_move, move_flag, original_alpha, original_beta)

        return best_move, value
