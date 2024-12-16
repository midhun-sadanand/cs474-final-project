from heuristic import evaluate
from connectfour import ConnectFour, PLAYER1, PLAYER2
from dotsandboxes import DotsAndBoxes
from nim import Nim
from minimax import apply_move, undo_move
from transpositiontable import TranspositionTable, EXACT, LOWERBOUND, UPPERBOUND

def scout(game, depth, game_size, alpha, beta, maximizingPlayer, node_counter, tt):
    node_counter['nodes'] += 1
    state_key = game.get_state_key(maximizingPlayer)
    original_alpha = alpha
    original_beta = beta

    # transposition table (if specified) lookup
    if tt is not None:
        found, tt_move, tt_value = tt.ab_lookup(state_key, depth, alpha, beta)
        if found:
            return tt_move, tt_value

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

    if not valid_moves:
        return None, evaluate(game, maximizingPlayer)

    best_move = None
    first_move = True

    # abstracted function to store in transposition table (if specified) after full-window search
    def store_tt_result(value, move):
        if tt is not None:
            if value <= original_alpha:
                move_flag = UPPERBOUND
            elif value >= original_beta:
                move_flag = LOWERBOUND
            else:
                move_flag = EXACT
            tt.ab_store(state_key, depth, value, move, move_flag, original_alpha, original_beta)

    # slightly altered approach from alpha-beta pruning (based on first move or not)
    if maximizingPlayer:
        baseline_value = float('-inf')

        for move in valid_moves:

            # apply move
            if hasattr(game, 'set_current_player'):
                game.set_current_player(PLAYER1 if maximizingPlayer else PLAYER2)
            apply_move(game, move, maximizingPlayer)

            if first_move:
                # full (initial) search for the first move
                first_move = False

                full_best_move, score = scout(game, depth - 1, game_size, alpha, beta, False, node_counter, tt)

                # undo move
                undo_move(game, move, maximizingPlayer)

                baseline_value = score
                best_move = move
                alpha = max(alpha, baseline_value)
                
                # finished full-window search ==> must store in tranposition table (if specified)
                store_tt_result(baseline_value, best_move)

                if alpha >= beta:
                    break
            else:
                # re-search (using null window) --> no need to store in transposition table
                verify_alpha = baseline_value
                verify_beta = baseline_value + 1
                _, verify_score = scout(game, depth - 1, game_size, verify_alpha, verify_beta, False, node_counter, None)

                # undo move
                undo_move(game, move, maximizingPlayer)

                # if verify suggests equal or better move, re-search fully with original window
                if verify_score >= baseline_value:
                    # re-apply move
                    if hasattr(game, 'set_current_player'):
                        game.set_current_player(PLAYER1 if maximizingPlayer else PLAYER2)
                    apply_move(game, move, maximizingPlayer)

                    # recurse
                    _, full_score = scout(game, depth - 1, game_size, alpha, beta, False, node_counter, tt)

                    # undo again
                    undo_move(game, move, maximizingPlayer)

                    if full_score > baseline_value:
                        baseline_value = full_score
                        best_move = move
                        alpha = max(alpha, baseline_value)
                        # Store updated full search result in TT
                        store_tt_result(baseline_value, best_move)
                        if alpha >= beta:
                            break

        final_value = baseline_value
        if final_value == float('-inf'):
            best_move = None

    else:
        baseline_value = float('inf')

        for move in valid_moves:
            # apply move
            if hasattr(game, 'set_current_player'):
                game.set_current_player(PLAYER1 if maximizingPlayer else PLAYER2)
            apply_move(game, move, maximizingPlayer)

            if first_move:
                # full (initial) search for the first move
                first_move = False

                full_best_move, score = scout(game, depth - 1, game_size, alpha, beta, True, node_counter, tt)

                # undo move
                undo_move(game, move, maximizingPlayer)

                baseline_value = score
                best_move = move
                beta = min(beta, baseline_value)

                # store in transposition table (if specified) after full-serach
                store_tt_result(baseline_value, best_move)

                if beta <= alpha:
                    break
            else:
                # verification search (null-window) - no TT store
                verify_alpha = baseline_value - 1
                verify_beta = baseline_value
                _, verify_score = scout(game, depth - 1, game_size, verify_alpha, verify_beta, True, node_counter, None)

                # undo move
                undo_move(game, move, maximizingPlayer)

                # re-search fully if verify says there might be a better move in this branch than the one we found
                if verify_score <= baseline_value:

                    # apply move
                    if hasattr(game, 'set_current_player'):
                        game.set_current_player(PLAYER1 if maximizingPlayer else PLAYER2)
                    apply_move(game, move, maximizingPlayer)

                    # recurse
                    _, full_score = scout(game, depth - 1, game_size, alpha, beta, True, node_counter, tt)

                    # undo again
                    undo_move(game, move, maximizingPlayer)

                    # update if new value creates tighter constraint
                    if full_score < baseline_value:
                        baseline_value = full_score
                        best_move = move
                        beta = min(beta, baseline_value)
                        
                        # store updated full-search in transposition table (if specified)
                        store_tt_result(baseline_value, best_move)
                        if beta <= alpha:
                            break

        final_value = baseline_value
        if final_value == float('inf'):
            best_move = None

    return best_move, final_value
