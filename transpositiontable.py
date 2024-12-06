# transposition_table.py

EXACT = 0
LOWERBOUND = 1
UPPERBOUND = 2

class TranspositionTable:
    def __init__(self):
        self.table = {}

    def mm_lookup(self, state_key, depth):
        # returns (1) if entry is in table (2) the best_move (3) the value associated with that move
        if state_key in self.table:
            stored_depth, value, best_move = self.table[state_key]

            if stored_depth >= depth:
                return True, best_move, value
        return False, None, None

    def mm_store(self, state_key, depth, value, best_move):
        self.table[state_key] = (depth, value, best_move)

    def ab_lookup(self, state_key, depth, alpha, beta):
        # returns (1) if entry is in table (2) the best_move (3) the value associated with that move
        if state_key in self.table:
            stored_depth, value, best_move, flag, stored_alpha, stored_beta = self.table[state_key]

            if stored_depth >= depth:
                # Depending on the flag, use it to cut off or update alpha/beta
                if flag == EXACT:
                    return True, best_move, value
                elif flag == LOWERBOUND and value > alpha:
                    return True, best_move, value
                elif flag == UPPERBOUND and value < beta:
                    return True, best_move, value
        return False, None, None

    def ab_store(self, state_key, depth, value, best_move, flag, alpha, beta):
        self.table[state_key] = (depth, value, best_move, flag, alpha, beta)
