from heuristic import evaluate
from connectfour import ConnectFour, PLAYER1, PLAYER2
from dotsandboxes import DotsAndBoxes
from nim import Nim
from transpositiontable import TranspositionTable, EXACT

def minimax(game, depth, game_size, maximizingPlayer, node_counter, tt):
    """
    Standard Minimax search with optional transposition table support.
    
    Parameters:
        game: Current game state (ConnectFour, Nim, DotsAndBoxes).
        depth: Maximum search depth.
        game_size: String indicating the size of the game ('small', 'medium', 'large').
        maximizingPlayer: Boolean, True if we are maximizing the utility.
        node_counter: Dictionary used as a counter to count nodes explored. {'nodes': int}
        tt: TranspositionTable or None.

    Returns:
        (best_move, value):
            best_move: The best move found at this state for the given player.
            value: The evaluation score of this state.
    """
    node_counter['nodes'] += 1
    state_key = game.get_state_key(maximizingPlayer)

    # Check transposition table
    if tt is not None:
        use_entry, tt_move, tt_value = tt.mm_lookup(state_key, depth)
        if use_entry:
            return tt_move, tt_value

    # Check if terminal or depth limit
    is_terminal = game.is_terminal_node()
    winner = game.get_winner(maximizingPlayer)
    if depth == 0 or is_terminal:
        if winner is not None:
            # Terminal with known winner
            if winner:
                return (None, float('inf'))
            elif winner is False:
                return (None, float('-inf'))
            else:
                return (None, 0)  # Draw
        else:
            # Evaluate heuristic at leaf
            return (None, evaluate(game, maximizingPlayer))

    # Get valid moves
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

            # Recurse
            _, new_score = minimax(game, depth - 1, game_size, False, node_counter, tt)

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

        # Store results in transposition table
        if tt is not None:
            tt.mm_store(state_key, depth, value, best_move)

        return best_move, value

    else:
        value = float('inf')
        best_move = None
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

            # Recurse
            _, new_score = minimax(game, depth - 1, game_size, True, node_counter, tt)

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

        # Store results in transposition table
        if tt is not None:
            tt.mm_store(state_key, depth, value, best_move)

        return best_move, value
