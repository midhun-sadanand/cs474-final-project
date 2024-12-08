import random

EMPTY = 0
PLAYER1 = 1
PLAYER2 = -1 

class DotsAndBoxes:
    def __init__(self, initial_state, size=3):
        self.initial = initial_state 
        self.size = size  
        self.h_lines = [[0] * (size) for _ in range(size + 1)]  
        self.v_lines = [[0] * (size + 1) for _ in range(size)]
        self.boxes = [[0] * size for _ in range(size)]
        self.current_player = PLAYER1
        if not self.initial:
            self.randomize_lines()

    def get_state_key(self, maximizingPlayer):
        h_lines_key = tuple(tuple(row) for row in self.h_lines)
        v_lines_key = tuple(tuple(row) for row in self.v_lines)
        boxes_key = tuple(tuple(row) for row in self.boxes)
        # Include maximizingPlayer and current_player to differentiate states
        return (maximizingPlayer, self.current_player, h_lines_key, v_lines_key, boxes_key)

    def display_board(self):
        print("\nCurrent Board:")
        size = self.size
        for i in range(size * 2 + 1):
            line = ''
            if i % 2 == 0:
                for j in range(size):
                    line += '•'
                    if self.h_lines[i // 2][j] == PLAYER1:
                        line += '\033[31m———\033[0m'
                    elif self.h_lines[i // 2][j] == PLAYER2:
                        line += '\033[34m———\033[0m'
                    else:
                        line += '   '
                line += '•'
            else:
                for j in range(size + 1):
                    if self.v_lines[i // 2][j] == PLAYER1:
                        line += '\033[31m|\033[0m'
                    elif self.v_lines[i // 2][j] == PLAYER2:
                        line += '\033[34m|\033[0m'
                    else:
                        line += ' '
                    if j < size and i // 2 < size:
                        owner = self.boxes[i // 2][j]
                        if owner == PLAYER1:
                            line += ' X '
                        elif owner == PLAYER2:
                            line += ' O '
                        else:
                            line += '   '
                line += ''
            print(line)

    def get_valid_moves(self):
        moves = []
        for i in range(len(self.h_lines)):
            for j in range(len(self.h_lines[0])):
                if self.h_lines[i][j] == 0:
                    moves.append(('h', i, j))
        for i in range(len(self.v_lines)):
            for j in range(len(self.v_lines[0])):
                if self.v_lines[i][j] == 0:
                    moves.append(('v', i, j))
        return moves

    def make_move(self, move):
        line_type, i, j = move
        if line_type == 'h':
            self.h_lines[i][j] = self.current_player
        else:
            self.v_lines[i][j] = self.current_player
        self.update_boxes()

    def undo_move(self, move):
        line_type, i, j = move
        if line_type == 'h':
            self.h_lines[i][j] = 0
        else:
            self.v_lines[i][j] = 0
        self.revert_boxes()

    def update_boxes(self):
        size = self.size
        for i in range(size):
            for j in range(size):
                if self.boxes[i][j] == 0:
                    if (self.h_lines[i][j] != 0 and 
                        self.h_lines[i + 1][j] != 0 and 
                        self.v_lines[i][j] != 0 and 
                        self.v_lines[i][j + 1] != 0):
                        self.boxes[i][j] = self.current_player

    def randomize_lines(self):
        total_lines = (len(self.h_lines) * len(self.h_lines[0])) + (len(self.v_lines) * len(self.v_lines[0]))
        one_third = total_lines // 3
        moves = [PLAYER1] * one_third + [PLAYER2] * one_third + [EMPTY] * one_third
        if len(moves) < total_lines:
            moves += [EMPTY] * (total_lines - len(moves))
        random.shuffle(moves)

        for i in range(len(self.h_lines)):
            for j in range(len(self.h_lines[i])):
                self.h_lines[i][j] = moves.pop()
        for i in range(len(self.v_lines)):
            for j in range(len(self.v_lines[i])):
                self.v_lines[i][j] = moves.pop()

        self.update_boxes()

    def revert_boxes(self):
        # Recompute box ownership after undo
        size = self.size
        for i in range(size):
            for j in range(size):
                if self.boxes[i][j] != 0:
                    if not (self.h_lines[i][j] != 0 and 
                            self.h_lines[i + 1][j] != 0 and 
                            self.v_lines[i][j] != 0 and 
                            self.v_lines[i][j + 1] != 0):
                        self.boxes[i][j] = 0

    def is_terminal_node(self):
        # If all lines are filled, it's terminal
        return (all(all(cell != 0 for cell in row) for row in self.h_lines) and
                all(all(cell != 0 for cell in row) for row in self.v_lines))

    def get_winner(self, maximizing_player):
        player1_score = sum(row.count(PLAYER1) for row in self.boxes)
        player2_score = sum(row.count(PLAYER2) for row in self.boxes)
        if self.is_terminal_node():
            if player1_score > player2_score:
                return True if maximizing_player else False
            elif player2_score > player1_score:
                return False if maximizing_player else True
            else:
                return None
        return None

    def set_current_player(self, player):
        self.current_player = player
