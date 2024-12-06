EXACT = 0
LOWERBOUND = 1
UPPERBOUND = 2

class TranspositionTable:
    def __init__(self):
        self.ab_table = {}
        self.mm_table = {}

    def ab_lookup(self, state_key, depth, alpha, beta):
        # Attempt to refine alpha and beta based on stored info
        if state_key in self.ab_table:
            stored_depth, value, best_move, flag, stored_alpha, stored_beta = self.ab_table[state_key]
            if stored_depth >= depth:
                if flag == EXACT:
                    # We have an exact value that fits the current search
                    return True, best_move, value
                elif flag == LOWERBOUND:
                    # value is a lower bound on the node's value
                    if value > alpha:
                        alpha = value
                    if alpha >= beta:
                        # cutoff
                        return True, best_move, value
                elif flag == UPPERBOUND:
                    # value is an upper bound on the node's value
                    if value < beta:
                        beta = value
                    if alpha >= beta:
                        # cutoff
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
