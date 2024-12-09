EXACT = 0
LOWERBOUND = 1
UPPERBOUND = 2

class TranspositionTable:
    """
    A Transposition Table for storing game states encountered during 
    Minimax, Alpha-Beta, and Scout searches.

    Stores data for two different search types:
    - ab_table: For Alpha-Beta/Scout searches (with bounds).
    - mm_table: For plain Minimax (no bounds).
    """
    def __init__(self):
        self.ab_table = {}
        self.mm_table = {}

    def ab_lookup(self, state_key, depth, alpha, beta):
        """
        Lookup for alpha-beta or scout result in the transposition table.
        """
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
        """
        Store alpha-beta or scout node result.
        """
        self.ab_table[state_key] = (depth, value, best_move, flag, alpha, beta)

    def mm_lookup(self, state_key, depth):
        """
        Lookup for minimax result in the transposition table.
        """
        if state_key in self.mm_table:
            stored_depth, value, best_move = self.mm_table[state_key]
            if stored_depth >= depth:
                return True, best_move, value
        return False, None, None

    def mm_store(self, state_key, depth, value, best_move):
        """
        Store minimax node result.
        """
        self.mm_table[state_key] = (depth, value, best_move)
