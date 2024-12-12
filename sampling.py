from heuristic import evaluate
from connectfour import ConnectFour, PLAYER1, PLAYER2
from dotsandboxes import DotsAndBoxes
from nim import Nim
from transpositiontable import TranspositionTable, EXACT
import random

def minimax_sample(game, depth, game_size, maximizingPlayer, node_counter, tt, sample_size=None):
    node_counter['nodes'] += 1
    state_key = game.get_state_key(maximizingPlayer)

    # Check transposition table
    if tt is not None:
        use_entry, tt_move, tt_value = tt.mm_lookup(state_key, depth)
        if use_entry:
            return tt_move, tt_value

    # Check for terminal node or depth limit
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

    # Random sampling if needed
    if sample_size is not None and len(valid_moves) > sample_size:
        valid_moves = random.sample(valid_moves, sample_size)

    if maximizingPlayer:
        value = float('-inf')
        best_move = None
        for move in valid_moves:
            # Make move
            if hasattr(game, 'set_current_player'):
                game.set_current_player(PLAYER1 if maximizingPlayer else PLAYER2)
            apply_move(game, move, maximizingPlayer)

            # Recurse
            _, new_score = minimax_sample(game, depth - 1, game_size, False, node_counter, tt, sample_size)

            # Undo
            undo_move(game, move, maximizingPlayer)

            if new_score > value:
                value = new_score
                best_move = move

        if tt is not None:
            tt.mm_store(state_key, depth, value, best_move)
        return best_move, value

    else:
        value = float('inf')
        best_move = None
        for move in valid_moves:
            # Make move
            if hasattr(game, 'set_current_player'):
                game.set_current_player(PLAYER1 if maximizingPlayer else PLAYER2)
            apply_move(game, move, maximizingPlayer)

            # Recurse
            _, new_score = minimax_sample(game, depth - 1, game_size, True, node_counter, tt, sample_size)

            # Undo
            undo_move(game, move, maximizingPlayer)

            if new_score < value:
                value = new_score
                best_move = move

        if tt is not None:
            tt.mm_store(state_key, depth, value, best_move)
        return best_move, value

def apply_move(game, move, maximizingPlayer):
    if isinstance(game, ConnectFour):
        game.make_move(move, PLAYER1 if maximizingPlayer else PLAYER2)
    elif isinstance(game, Nim):
        heap_index, remove_count = move
        game.make_move(heap_index, remove_count)
    elif isinstance(game, DotsAndBoxes):
        game.make_move(move)

def undo_move(game, move, maximizingPlayer):
    if isinstance(game, ConnectFour):
        game.undo_move(move)
    elif isinstance(game, Nim):
        heap_index, remove_count = move
        game.undo_move(heap_index, remove_count)
    elif isinstance(game, DotsAndBoxes):
        game.undo_move(move)
