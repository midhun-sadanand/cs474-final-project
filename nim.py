import random

class Nim:
    def __init__(self, initial_state, game_size, heaps=[3, 5, 7]):
        self.initial = initial_state
        self.heaps = self.init_heaps(heaps, game_size)
        
    def get_state_key(self, maximizingPlayer):
        return (maximizingPlayer, tuple(self.heaps))

    def init_heaps(self, heaps, game_size):
        if(game_size == 'large'):
            if self.initial is True:
                return heaps
            else:
                return [random.randint(1, 7) for _ in range(len(heaps))]
        elif(game_size == 'medium'):
            if self.initial is True:
                return heaps[1:]
            else:
                return [random.randint(1, 7) for _ in range(len(heaps[1:]))]
        else:
            if self.initial is True:
                return heaps[2:]
            else:
                return [random.randint(1, 7) for _ in range(len(heaps[2:]))]

    def display_board(self):
        print("\nCurrent Heaps:")
        for i, heap in enumerate(self.heaps):
            print(f"Heap {i}: {'|' * heap} ({heap})")

    def get_valid_moves(self, game_size):
        if(game_size == 'small'):
            valid_moves = []
            for i, heap in enumerate(self.heaps):
                if heap > 0:
                    for remove in range(1, 4):
                        valid_moves.append((i, remove))
            return valid_moves
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
            # last move wins (player who didn't maximize)
            return not maximizing_player
        return None
