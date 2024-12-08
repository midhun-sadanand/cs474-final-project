from heuristic import evaluate
from connectfour import ConnectFour, PLAYER1, PLAYER2
from nim import Nim
from dotsandboxes import DotsAndBoxes
from transpositiontable import TranspositionTable, EXACT, LOWERBOUND, UPPERBOUND

def scout(game, depth, alpha, beta, maximizingPlayer, node_counter, tt):
    node_counter['nodes'] += 1
    
    original_alpha = alpha
    original_beta = beta

    state_key = game.get_state_key(maximizingPlayer)

    # If using a TT, try lookup
    if tt is not None:
        found, tt_move, tt_value = tt.ab_lookup(state_key, depth, alpha, beta)
        if found:
            return tt_move, tt_value

    # Terminal or depth check
    is_terminal = game.is_terminal_node()
    winner = game.get_winner(maximizingPlayer)
    if depth == 0 or is_terminal:
        if winner is not None:
            if winner:  # maximizing player wins
                return (None, float('inf'))
            elif winner is False:  # maximizing player loses
                return (None, float('-inf'))
            else:  # draw
                return (None, 0)
        else:
            return (None, evaluate(game, maximizingPlayer))

    valid_moves = game.get_valid_moves()

    # If no moves, evaluate the position
    if not valid_moves:
        return (None, evaluate(game, maximizingPlayer))

    best_move = None
    first_move = True
    value = float('-inf') if maximizingPlayer else float('inf')

    # Scout logic:
    # 1. For the first move, search full window as normal.
    # 2. For subsequent moves, do a null-window search (alpha, alpha+1) to verify.
    #    - If null-window search > alpha, re-search with full window.
    #    - If null-window search >= beta, cutoff.
    # This logic works best when moves are ordered (best moves first).
    
    for move in valid_moves:
        # Make the move
        if isinstance(game, ConnectFour):
            game.make_move(move, PLAYER1 if maximizingPlayer else PLAYER2)
        elif isinstance(game, Nim):
            heap_index, remove_count = move
            game.make_move(heap_index, remove_count)
        elif isinstance(game, DotsAndBoxes):
            game.set_current_player(PLAYER1 if maximizingPlayer else PLAYER2)
            game.make_move(move)

        if first_move:
            # Full window search for the first move
            new_move, new_score = scout(game, depth - 1, alpha, beta, not maximizingPlayer, node_counter, tt)
            first_move = False
        else:
            # Null-window search to confirm superiority
            new_move, new_score = scout(game, depth - 1, alpha, alpha + 1, not maximizingPlayer, node_counter, tt)
            if maximizingPlayer:
                # If the null-window search shows improvement
                if new_score > alpha and new_score < beta:
                    # Re-search with full window
                    _, new_score = scout(game, depth - 1, new_score, beta, not maximizingPlayer, node_counter, tt)
            else:
                # For minimizingPlayer, the logic is symmetrical with inverted signs
                # However, since scout is typically explained from maximizing perspective,
                # we rely on the symmetrical logic by flipping maximizingPlayer each call.
                # This means the alpha/beta logic should still hold.
                # If new_score < beta and new_score > alpha, re-search
                if new_score < beta and new_score > alpha:
                    _, new_score = scout(game, depth - 1, alpha, new_score, not maximizingPlayer, node_counter, tt)

        # Undo the move
        if isinstance(game, ConnectFour):
            game.undo_move(move)
        elif isinstance(game, Nim):
            heap_index, remove_count = move
            game.undo_move(heap_index, remove_count)
        elif isinstance(game, DotsAndBoxes):
            game.set_current_player(PLAYER1 if maximizingPlayer else PLAYER2)
            game.undo_move(move)

        # Update alpha/beta based on maximizing/minimizing logic
        if maximizingPlayer:
            if new_score > value:
                value = new_score
                best_move = move
            alpha = max(alpha, value)
        else:
            if new_score < value:
                value = new_score
                best_move = move
            beta = min(beta, value)

        # Cutoff check
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
