from heuristic import evaluate
from connectfour import ConnectFour, PLAYER1, PLAYER2
from nim import Nim
from dotsandboxes import DotsAndBoxes
from transpositiontable import TranspositionTable, EXACT, LOWERBOUND, UPPERBOUND

def scout(game, depth, alpha, beta, maximizingPlayer, node_counter, tt):
    """
    Scout integrated with alpha-beta pruning:
    
    - First move: full alpha-beta search to establish baseline_value.
    - Subsequent moves: null-window verification search. If verification suggests 
      improvement, re-search fully with alpha-beta.
    - Use TT for EXACT hits and adjust alpha/beta for LOWERBOUND/UPPERBOUND as in alpha-beta.
    - Always return the best move found.
    """

    node_counter['nodes'] += 1
    state_key = game.get_state_key(maximizingPlayer)
    original_alpha = alpha
    original_beta = beta

    # TT Lookup
    if tt is not None:
        found, tt_move, tt_value = tt.ab_lookup(state_key, depth, alpha, beta)
        if found:
            # If TT provided a conclusive result (EXACT or cutoff), return it
            return tt_move, tt_value

    # Terminal or depth reached
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

    valid_moves = game.get_valid_moves()
    if not valid_moves:
        return None, evaluate(game, maximizingPlayer)

    # SCOUT + Alpha-Beta logic
    best_move = None
    first_move = True

    if maximizingPlayer:
        baseline_value = float('-inf')

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

            if first_move:
                # First move: full alpha-beta search
                first_move = False
                _, score = scout(game, depth - 1, alpha, beta, False, node_counter, tt)

                # Undo move
                if isinstance(game, ConnectFour):
                    game.undo_move(move)
                elif isinstance(game, Nim):
                    heap_index, remove_count = move
                    game.undo_move(heap_index, remove_count)
                elif isinstance(game, DotsAndBoxes):
                    game.set_current_player(PLAYER1)
                    game.undo_move(move)

                baseline_value = score
                best_move = move
                alpha = max(alpha, baseline_value)
                if alpha >= beta:
                    break
            else:
                # Verification step: null-window search
                # We test if this move could possibly beat baseline_value
                verify_alpha = baseline_value
                verify_beta = baseline_value + 1

                _, verify_score = scout(game, depth - 1, verify_alpha, verify_beta, False, node_counter, tt)

                # Undo move
                if isinstance(game, ConnectFour):
                    game.undo_move(move)
                elif isinstance(game, Nim):
                    heap_index, remove_count = move
                    game.undo_move(heap_index, remove_count)
                elif isinstance(game, DotsAndBoxes):
                    game.set_current_player(PLAYER1)
                    game.undo_move(move)

                if verify_score > baseline_value:
                    # Re-search with full window since we might have a better move
                    if isinstance(game, ConnectFour):
                        game.make_move(move, PLAYER1)
                    elif isinstance(game, Nim):
                        heap_index, remove_count = move
                        game.make_move(heap_index, remove_count)
                    elif isinstance(game, DotsAndBoxes):
                        game.set_current_player(PLAYER1)
                        game.make_move(move)

                    _, full_score = scout(game, depth - 1, alpha, beta, False, node_counter, tt)

                    # Undo again
                    if isinstance(game, ConnectFour):
                        game.undo_move(move)
                    elif isinstance(game, Nim):
                        heap_index, remove_count = move
                        game.undo_move(heap_index, remove_count)
                    elif isinstance(game, DotsAndBoxes):
                        game.set_current_player(PLAYER1)
                        game.undo_move(move)

                    if full_score > baseline_value:
                        baseline_value = full_score
                        best_move = move
                        alpha = max(alpha, baseline_value)
                        if alpha >= beta:
                            break

    else:
        baseline_value = float('inf')

        for move in valid_moves:
            # Make move
            if isinstance(game, ConnectFour):
                game.make_move(move, PLAYER2)
            elif isinstance(game, Nim):
                heap_index, remove_count = move
                game.make_move(heap_index, remove_count)
            elif isinstance(game, DotsAndBoxes):
                game.set_current_player(PLAYER2)
                game.make_move(move)

            if first_move:
                # First move: full alpha-beta search
                first_move = False
                _, score = scout(game, depth - 1, alpha, beta, True, node_counter, tt)

                # Undo move
                if isinstance(game, ConnectFour):
                    game.undo_move(move)
                elif isinstance(game, Nim):
                    heap_index, remove_count = move
                    game.undo_move(heap_index, remove_count)
                elif isinstance(game, DotsAndBoxes):
                    game.set_current_player(PLAYER2)
                    game.undo_move(move)

                baseline_value = score
                best_move = move
                beta = min(beta, baseline_value)
                if beta <= alpha:
                    break
            else:
                # Verification step for minimizing player
                # null-window: [baseline_value-1, baseline_value]
                verify_alpha = baseline_value - 1
                verify_beta = baseline_value

                _, verify_score = scout(game, depth - 1, verify_alpha, verify_beta, True, node_counter, tt)

                # Undo move
                if isinstance(game, ConnectFour):
                    game.undo_move(move)
                elif isinstance(game, Nim):
                    heap_index, remove_count = move
                    game.undo_move(heap_index, remove_count)
                elif isinstance(game, DotsAndBoxes):
                    game.set_current_player(PLAYER2)
                    game.undo_move(move)

                if verify_score < baseline_value:
                    # Re-search fully
                    if isinstance(game, ConnectFour):
                        game.make_move(move, PLAYER2)
                    elif isinstance(game, Nim):
                        heap_index, remove_count = move
                        game.make_move(heap_index, remove_count)
                    elif isinstance(game, DotsAndBoxes):
                        game.set_current_player(PLAYER2)
                        game.make_move(move)

                    _, full_score = scout(game, depth - 1, alpha, beta, True, node_counter, tt)

                    # Undo again
                    if isinstance(game, ConnectFour):
                        game.undo_move(move)
                    elif isinstance(game, Nim):
                        heap_index, remove_count = move
                        game.undo_move(heap_index, remove_count)
                    elif isinstance(game, DotsAndBoxes):
                        game.set_current_player(PLAYER2)
                        game.undo_move(move)

                    if full_score < baseline_value:
                        baseline_value = full_score
                        best_move = move
                        beta = min(beta, baseline_value)
                        if beta <= alpha:
                            break

    # Store results in TT
    if tt is not None:
        if baseline_value <= original_alpha:
            move_flag = UPPERBOUND
        elif baseline_value >= original_beta:
            move_flag = LOWERBOUND
        else:
            move_flag = EXACT
        tt.ab_store(state_key, depth, baseline_value, best_move, move_flag, original_alpha, original_beta)

    return best_move, baseline_value
