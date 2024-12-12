from heuristic import evaluate
from connectfour import ConnectFour, PLAYER1, PLAYER2
from dotsandboxes import DotsAndBoxes
from nim import Nim
from transpositiontable import TranspositionTable, EXACT
import random

def minimax(game, depth, game_size, maximizingPlayer, node_counter, tt, sample_size=None):
    node_counter['nodes'] += 1
    state_key = game.get_state_key(maximizingPlayer)

    # transposition table (if specified) lookup
    if tt is not None:
        use_entry, tt_move, tt_value = tt.mm_lookup(state_key, depth)
        if use_entry:
            return tt_move, tt_value

    # are we at terminal state / did we reach depth limit?
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
            # use heuristic to evaluate / predict
            return (None, evaluate(game, maximizingPlayer))

    # get valid moves
    if isinstance(game, Nim):
        valid_moves = game.get_valid_moves(game_size)
    else:
        valid_moves = game.get_valid_moves()

    if sample_size is not None and len(valid_moves) > sample_size:
        valid_moves = random.sample(valid_moves, sample_size)

    # greedy strategy based on which player
    if maximizingPlayer:
        value = float('-inf')
        best_move = None
        for move in valid_moves:
            # apply move
            if isinstance(game, ConnectFour):
                game.make_move(move, PLAYER1)
            elif isinstance(game, Nim):
                heap_index, remove_count = move
                game.make_move(heap_index, remove_count)
            elif isinstance(game, DotsAndBoxes):
                game.set_current_player(PLAYER1)
                game.make_move(move)

            # recurse
            _, new_score = minimax(game, depth - 1, game_size, False, node_counter, tt, sample_size)

            # undo move
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

        # store in transposition table (if specified)
        if tt is not None:
            tt.mm_store(state_key, depth, value, best_move)

        return best_move, value

    else:
        value = float('inf')
        best_move = None
        for move in valid_moves:
            # apply move
            if isinstance(game, ConnectFour):
                game.make_move(move, PLAYER2)
            elif isinstance(game, Nim):
                heap_index, remove_count = move
                game.make_move(heap_index, remove_count)
            elif isinstance(game, DotsAndBoxes):
                game.set_current_player(PLAYER2)
                game.make_move(move)

            # recurse
            _, new_score = minimax(game, depth - 1, game_size, True, node_counter, tt, sample_size)

            # undo move
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

        # store in transposition table (if specified)
        if tt is not None:
            tt.mm_store(state_key, depth, value, best_move)

        return best_move, value
