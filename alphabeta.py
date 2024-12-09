from heuristic import evaluate
from connectfour import ConnectFour, PLAYER1, PLAYER2
from dotsandboxes import DotsAndBoxes
from nim import Nim
from transpositiontable import TranspositionTable, EXACT, LOWERBOUND, UPPERBOUND

def alphabeta(game, depth, game_size, alpha, beta, maximizingPlayer, node_counter, tt):
    """
    Alpha-Beta search with transposition table support.
    
    Parameters:
        game: Current game state (ConnectFour, Nim, DotsAndBoxes).
        depth: Maximum search depth.
        game_size: String indicating the size of the game.
        alpha, beta: Alpha-Beta window parameters.
        maximizingPlayer: Boolean, True if we are maximizing the utility.
        node_counter: Dictionary for counting nodes. {'nodes': int}
        tt: TranspositionTable or None.

    Returns:
        (best_move, value):
            best_move: The best move found.
            value: The evaluation score.
    """
    node_counter['nodes'] += 1
    original_alpha = alpha
    original_beta = beta
    state_key = game.get_state_key(maximizingPlayer)

    # Transposition table lookup
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

    if isinstance(game, Nim):
        valid_moves = game.get_valid_moves(game_size)
    else:
        valid_moves = game.get_valid_moves()

    if maximizingPlayer:
        value = float('-inf')
        best_move = None

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

            # Recurse
            _, new_score = alphabeta(game, depth - 1, game_size, alpha, beta, False, node_counter, tt)

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

        # Store in TT
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
            # Apply move
            if isinstance(game, ConnectFour):
                game.make_move(move, PLAYER2)
            elif isinstance(game, Nim):
                heap_index, remove_count = move
                game.make_move(heap_index, remove_count)
            elif isinstance(game, DotsAndBoxes):
                game.set_current_player(PLAYER2)
                game.make_move(move)

            # Recurse
            _, new_score = alphabeta(game, depth - 1, game_size, alpha, beta, True, node_counter, tt)

            # Undo move
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

        # Store in TT
        if tt is not None:
            if value <= original_alpha:
                move_flag = UPPERBOUND
            elif value >= original_beta:
                move_flag = LOWERBOUND
            else:
                move_flag = EXACT
            tt.ab_store(state_key, depth, value, best_move, move_flag, original_alpha, original_beta)

        return best_move, value
