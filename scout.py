from heuristic import evaluate
from connectfour import ConnectFour, PLAYER1, PLAYER2
from dotsandboxes import DotsAndBoxes
from nim import Nim
from transpositiontable import TranspositionTable, EXACT, LOWERBOUND, UPPERBOUND

def scout(game, depth, game_size, alpha, beta, maximizingPlayer, node_counter, tt):
    """
    Scout search algorithm integrated with alpha-beta style verification and transposition table.
    
    Scout search:
    - Fully search the first move to establish a baseline value.
    - For subsequent moves, perform a verification (null-window) search to check if it can improve on the baseline.
    - If the verification search indicates that the move could be as good or better than the baseline for maximizing player 
      (or as good or worse for minimizing player), re-search fully with the original window to confirm.

    Adjusted Conditions for Full Re-Search:
    - Maximizing Player: If verify_score >= baseline_value, do a full re-search.
    - Minimizing Player: If verify_score <= baseline_value, do a full re-search.

    This ensures that Scout does not miss equally good moves and returns the same optimal move as Minimax.

    Parameters:
        game: Current game state.
        depth: Maximum search depth.
        game_size: String indicating game size ('small', 'medium', 'large').
        alpha, beta: Alpha-Beta bounds for the scout verification.
        maximizingPlayer: Boolean indicating if we're in a maximizing node.
        node_counter: Dictionary for counting explored nodes. {'nodes': int}
        tt: TranspositionTable or None.

    Returns:
        (best_move, value):
            best_move: The best move found for the current player. None if losing position.
            value: The evaluation score of the position from the perspective of the current player.
    """
    node_counter['nodes'] += 1
    state_key = game.get_state_key(maximizingPlayer)
    original_alpha = alpha
    original_beta = beta

    # Transposition Table lookup
    if tt is not None:
        found, tt_move, tt_value = tt.ab_lookup(state_key, depth, alpha, beta)
        if found:
            return tt_move, tt_value

    # Terminal or depth limit
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

    # No valid moves
    if not valid_moves:
        return None, evaluate(game, maximizingPlayer)

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
                # Full search for first child
                first_move = False
                _, score = scout(game, depth - 1, game_size, alpha, beta, False, node_counter, tt)

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
                # Verification (null-window) search
                verify_alpha = baseline_value
                verify_beta = baseline_value + 1
                _, verify_score = scout(game, depth - 1, game_size, verify_alpha, verify_beta, False, node_counter, tt)

                # Undo move
                if isinstance(game, ConnectFour):
                    game.undo_move(move)
                elif isinstance(game, Nim):
                    heap_index, remove_count = move
                    game.undo_move(heap_index, remove_count)
                elif isinstance(game, DotsAndBoxes):
                    game.set_current_player(PLAYER1)
                    game.undo_move(move)

                # If verify_score >= baseline_value, we re-search fully
                if verify_score >= baseline_value:
                    # Re-apply move for full search
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
                        if alpha >= beta:
                            break

        final_value = baseline_value
        # If baseline_value is still -inf, means losing position; best_move remains None
        if final_value == float('-inf'):
            best_move = None

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
                # Full search for first child
                first_move = False
                _, score = scout(game, depth - 1, game_size, alpha, beta, True, node_counter, tt)

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
                # Verification (null-window) search for minimizing player
                verify_alpha = baseline_value - 1
                verify_beta = baseline_value
                _, verify_score = scout(game, depth - 1, game_size, verify_alpha, verify_beta, True, node_counter, tt)

                # Undo move
                if isinstance(game, ConnectFour):
                    game.undo_move(move)
                elif isinstance(game, Nim):
                    heap_index, remove_count = move
                    game.undo_move(heap_index, remove_count)
                elif isinstance(game, DotsAndBoxes):
                    game.set_current_player(PLAYER2)
                    game.undo_move(move)

                # For minimizing player: if verify_score <= baseline_value, re-search fully
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
                        if beta <= alpha:
                            break

        final_value = baseline_value
        # If final_value == inf, means no move improved the situation; best_move might remain None if no better option was found
        if final_value == float('inf'):
            best_move = None

    # Store results in TT
    if tt is not None:
        if final_value <= original_alpha:
            move_flag = UPPERBOUND
        elif final_value >= original_beta:
            move_flag = LOWERBOUND
        else:
            move_flag = EXACT
        tt.ab_store(state_key, depth, final_value, best_move, move_flag, original_alpha, original_beta)

    return best_move, final_value
