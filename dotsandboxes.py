# dotsandboxes.py

import random

class DotsAndBoxes:
    def __init__(self, initial_state, size=3):
        self.initial = initial_state 
        # TODO: implement a way to randomize dots and boxes
        self.size = size  # Number of boxes per row/column
        self.h_lines = [[False] * (size) for _ in range(size + 1)]  # Horizontal lines
        self.v_lines = [[False] * (size + 1) for _ in range(size)]  # Vertical lines
        self.boxes = [[0] * size for _ in range(size)]  # 0: unclaimed, 1: Player1, -1: Player2
        self.current_player = 1  # Initialize current player

    def display_board(self):
        print("\nCurrent Board:")
        size = self.size
        for i in range(size * 2 + 1):
            line = ''
            if i % 2 == 0:
                # Dots and horizontal lines
                for j in range(size):
                    line += '•'
                    if self.h_lines[i // 2][j]:
                        line += '———'
                    else:
                        line += '   '
                line += '•'
            else:
                # Vertical lines and boxes
                for j in range(size + 1):
                    if self.v_lines[i // 2][j]:
                        line += '|'
                    else:
                        line += ' '
                    if j < size and i // 2 < size:
                        owner = self.boxes[i // 2][j]
                        if owner == 1:
                            line += ' X '
                        elif owner == -1:
                            line += ' O '
                        else:
                            line += '   '
                line += ''
            print(line)

    def get_valid_moves(self):
        moves = []
        # Horizontal lines
        for i in range(len(self.h_lines)):
            for j in range(len(self.h_lines[0])):
                if not self.h_lines[i][j]:
                    moves.append(('h', i, j))
        # Vertical lines
        for i in range(len(self.v_lines)):
            for j in range(len(self.v_lines[0])):
                if not self.v_lines[i][j]:
                    moves.append(('v', i, j))
        return moves

    def make_move(self, move):
        line_type, i, j = move
        if line_type == 'h':
            self.h_lines[i][j] = True
        else:
            self.v_lines[i][j] = True
        # Check for completed boxes
        self.update_boxes()

    def undo_move(self, move):
        line_type, i, j = move
        if line_type == 'h':
            self.h_lines[i][j] = False
        else:
            self.v_lines[i][j] = False
        # Revert boxes if they were claimed
        self.revert_boxes()

    def update_boxes(self):
        size = self.size
        for i in range(size):
            for j in range(size):
                if self.boxes[i][j] == 0:
                    if self.h_lines[i][j] and self.h_lines[i + 1][j] and self.v_lines[i][j] and self.v_lines[i][j + 1]:
                        # Assign box to the current player
                        self.boxes[i][j] = self.current_player

    def revert_boxes(self):
        size = self.size
        for i in range(size):
            for j in range(size):
                if self.boxes[i][j] == self.current_player:
                    if not (self.h_lines[i][j] and self.h_lines[i + 1][j] and self.v_lines[i][j] and self.v_lines[i][j + 1]):
                        self.boxes[i][j] = 0

    def is_terminal_node(self):
        return all(all(row) for row in self.h_lines) and all(all(row) for row in self.v_lines)

    def get_winner(self, maximizing_player):
        player1_score = sum(row.count(1) for row in self.boxes)
        player2_score = sum(row.count(-1) for row in self.boxes)
        if self.is_terminal_node():
            if player1_score > player2_score:
                return True if maximizing_player else False
            elif player2_score > player1_score:
                return False if maximizing_player else True
            else:
                return None  # Draw
        return None  # Game not over

    def set_current_player(self, player):
        self.current_player = player
