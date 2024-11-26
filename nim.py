# nim.py

import random

class Nim:
    def __init__(self, initial_state, heaps=[3, 5, 7]):
        self.initial = initial_state
        self.heaps = self.init_heaps(heaps)
        
    def init_heaps(self, heaps):
        if self.initial is True:
            return heaps.copy()
        else:
            return [random.randint(1, 7), random.randint(1, 7), random.randint(1, 7)]

    def display_board(self):
        print("\nCurrent Heaps:")
        for i, heap in enumerate(self.heaps):
            print(f"Heap {i}: {'|' * heap} ({heap})")

    def get_valid_moves(self):
        valid_moves = []
        for i, heap in enumerate(self.heaps):
            if heap > 0:
                for remove in range(1, heap + 1):
                    valid_moves.append((i, remove))
        return valid_moves

    def make_move(self, heap_index, remove_count):
        self.heaps[heap_index] -= remove_count

    def undo_move(self, heap_index, remove_count):
        self.heaps[heap_index] += remove_count

    def is_terminal_node(self):
        return all(heap == 0 for heap in self.heaps)

    def get_winner(self, maximizing_player):
        if self.is_terminal_node():
            # The player who made the last move wins
            return not maximizing_player
        return None  # Game not over
