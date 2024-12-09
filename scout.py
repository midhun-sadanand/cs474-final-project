from heuristic import evaluate
from connectfour import ConnectFour, PLAYER1, PLAYER2
from dotsandboxes import DotsAndBoxes
from nim import Nim
from transpositiontable import TranspositionTable, EXACT, LOWERBOUND, UPPERBOUND

def scout(game, depth, game_size, alpha, beta, maximizingPlayer, node_counter, tt):
    """
    Scout search algorithm integrated with alpha-beta style verification and transposition table support.

    Improvements over previous versions:
    - Verification (null-window) searches do NOT store results into TT. They are quick checks only.
    - Only full-window searches (initial baseline and re-search after verification) store results into TT.
    - Whenever a full search or re-search determines a new best move and final_value, we store that result 
      as EXACT or bounded appropriately.

    This ensures that the TT is always updated with correct and complete information from full searches, 
    preventing suboptimal moves being returned due to partial (verification) results.

    Parameters:
        game: Current game state (ConnectFour, Nim, DotsAndBoxes).
        depth: Maximum search depth.
        game_size: 'small', 'medium', or 'large' indicating the game size.
        alpha, beta: Alpha-Beta window parameters.
        maximizingPlayer: Boolean, True if we are maximizing the utility.
        node_counter: Dictionary for counting nodes: {'nodes': int}.
        tt: TranspositionTable or None.

    Returns:
        (best_move, value):
            best_move: The best move found at this state.
            value: The evaluation score at this state.
    """
    node_counter['nodes'] += 1
    state_key = game.get_state_key(maximizingPlayer)
    original_alpha = alpha
    original_beta = beta

    # Transposition Table lookup
    # We only trust full-window searches stored previously.
    if tt is not None:
        found, tt_move, tt_value = tt.ab_lookup(state_key, depth, alpha, beta)
        if found:
            return tt_move, tt_value

    # Terminal or depth check
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

    # Get valid moves
    if isinstance(game, Nim):
        valid_moves = game.get_valid_moves(game_size)
    else:
        valid_moves = game.get_valid_moves()

    if not valid_moves:
        return None, evaluate(game, maximizingPlayer)

    best_move = None
    first_move = True

    # Function to store the result in TT after a full-window search
    def store_tt_result(value, move):
        if tt is not None:
            if value <= original_alpha:
                move_flag = UPPERBOUND
            elif value >= original_beta:
                move_flag = LOWERBOUND
            else:
                move_flag = EXACT
            tt.ab_store(state_key, depth, value, move, move_flag, original_alpha, original_beta)

    if maximizingPlayer:
        baseline_value = float('-inf')

        for move in valid_moves:
            # Apply move
            if isinstance(game, ConnectFour):
                game.make_move(move, PLAYER1)
            elif isinstance(game, Nim):
                heap_index, remove_count = move
                game.make_move(heap_index, remove_count)
            elif isinstance(game, DotsAndBoxes):
                game.set_current_player(PLAYER1)
                game.make_move(move)

            if first_move:
                # Full (initial) search for the first move
                first_move = False
                # Perform a full scout search to establish baseline
                full_best_move, score = scout(game, depth - 1, game_size, alpha, beta, False, node_counter, tt)

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
                # Store result of this full-window search
                store_tt_result(baseline_value, best_move)

                if alpha >= beta:
                    break
            else:
                # Verification search (null-window) - do NOT store TT here
                verify_alpha = baseline_value
                verify_beta = baseline_value + 1
                _, verify_score = scout(game, depth - 1, game_size, verify_alpha, verify_beta, False, node_counter, None)

                # Undo move
                if isinstance(game, ConnectFour):
                    game.undo_move(move)
                elif isinstance(game, Nim):
                    heap_index, remove_count = move
                    game.undo_move(heap_index, remove_count)
                elif isinstance(game, DotsAndBoxes):
                    game.set_current_player(PLAYER1)
                    game.undo_move(move)

                # If verify suggests equal or better move, re-search fully with original window
                if verify_score >= baseline_value:
                    # Re-apply move
                    if isinstance(game, ConnectFour):
                        game.make_move(move, PLAYER1)
                    elif isinstance(game, Nim):
                        heap_index, remove_count = move
                        game.make_move(heap_index, remove_count)
                    elif isinstance(game, DotsAndBoxes):
                        game.set_current_player(PLAYER1)
                        game.make_move(move)

                    _, full_score = scout(game, depth - 1, game_size, alpha, beta, False, node_counter, tt)

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
            # Apply move
            if isinstance(game, ConnectFour):
                game.make_move(move, PLAYER2)
            elif isinstance(game, Nim):
                heap_index, remove_count = move
                game.make_move(heap_index, remove_count)
            elif isinstance(game, DotsAndBoxes):
                game.set_current_player(PLAYER2)
                game.make_move(move)

            if first_move:
                # Full (initial) search for the first move
                first_move = False
                full_best_move, score = scout(game, depth - 1, game_size, alpha, beta, True, node_counter, tt)

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
                # Store result of this full-window search
                store_tt_result(baseline_value, best_move)

                if beta <= alpha:
                    break
            else:
                # Verification search (null-window) - no TT store
                verify_alpha = baseline_value - 1
                verify_beta = baseline_value
                _, verify_score = scout(game, depth - 1, game_size, verify_alpha, verify_beta, True, node_counter, None)

                # Undo move
                if isinstance(game, ConnectFour):
                    game.undo_move(move)
                elif isinstance(game, Nim):
                    heap_index, remove_count = move
                    game.undo_move(heap_index, remove_count)
                elif isinstance(game, DotsAndBoxes):
                    game.set_current_player(PLAYER2)
                    game.undo_move(move)

                # If verify suggests equal or worse (for minimizing) move, re-search fully
                if verify_score <= baseline_value:
                    if isinstance(game, ConnectFour):
                        game.make_move(move, PLAYER2)
                    elif isinstance(game, Nim):
                        heap_index, remove_count = move
                        game.make_move(heap_index, remove_count)
                    elif isinstance(game, DotsAndBoxes):
                        game.set_current_player(PLAYER2)
                        game.make_move(move)

                    _, full_score = scout(game, depth - 1, game_size, alpha, beta, True, node_counter, tt)

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
                        # Store updated full search result in TT
                        store_tt_result(baseline_value, best_move)
                        if beta <= alpha:
                            break

        final_value = baseline_value
        if final_value == float('inf'):
            best_move = None

    return best_move, final_value
