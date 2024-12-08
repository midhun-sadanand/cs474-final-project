from heuristic import evaluate
from connectfour import ConnectFour, PLAYER1, PLAYER2
from dotsandboxes import DotsAndBoxes
from nim import Nim
from transpositiontable import TranspositionTable, EXACT

def minimax(game, depth, maximizingPlayer, node_counter, tt):
    node_counter['nodes'] += 1

    state_key = game.get_state_key(maximizingPlayer)

    # If using transposition table, attempt lookup
    if tt is not None:
        use_entry, tt_move, tt_value = tt.mm_lookup(state_key, depth)
        if use_entry:
            return tt_move, tt_value

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

    if maximizingPlayer:
        value = float('-inf')
        best_move = None
        for move in valid_moves:
            if isinstance(game, ConnectFour):
                game.make_move(move, PLAYER1)
            elif isinstance(game, Nim):
                heap_index, remove_count = move
                game.make_move(heap_index, remove_count)
            elif isinstance(game, DotsAndBoxes):
                game.set_current_player(PLAYER1)
                game.make_move(move)

            new_score = minimax(game, depth - 1, False, node_counter, tt)[1]

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

        # Store results in TT if in use (only EXACT for minimax)
        if tt is not None:
            tt.mm_store(state_key, depth, value, best_move)

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

            new_score = minimax(game, depth - 1, True, node_counter, tt)[1]

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

        # Store results in TT if in use (only EXACT for minimax)
        if tt is not None:
            tt.mm_store(state_key, depth, value, best_move)

        return best_move, value
