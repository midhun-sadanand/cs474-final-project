EXACT = 0
LOWERBOUND = 1
UPPERBOUND = 2

class TranspositionTable:
    def __init__(self):
        self.ab_table = {}
        self.mm_table = {}

    def ab_lookup(self, state_key, depth, alpha, beta):
        if state_key in self.ab_table:
            stored_depth, value, best_move, flag, stored_alpha, stored_beta = self.ab_table[state_key]
            if stored_depth >= depth:
                if flag == EXACT:
                    return True, best_move, value
                elif flag == LOWERBOUND:
                    if value > alpha:
                        alpha = value
                    if alpha >= beta:
                        return True, best_move, value
                elif flag == UPPERBOUND:
                    if value < beta:
                        beta = value
                    if alpha >= beta:
                        return True, best_move, value
        return False, None, None

    def ab_store(self, state_key, depth, value, best_move, flag, alpha, beta):
        self.ab_table[state_key] = (depth, value, best_move, flag, alpha, beta)

    def mm_lookup(self, state_key, depth):
        if state_key in self.mm_table:
            stored_depth, value, best_move = self.mm_table[state_key]
            if stored_depth >= depth:
                return True, best_move, value
        return False, None, None

    def mm_store(self, state_key, depth, value, best_move):
        self.mm_table[state_key] = (depth, value, best_move)
