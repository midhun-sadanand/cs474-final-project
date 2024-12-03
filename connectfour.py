# connectfour.py

import random

# cell representation
EMPTY = 0
PLAYER1 = 1  
PLAYER2 = -1 

# visuals
SYMBOLS = {
    EMPTY: '·',
    PLAYER1: 'X',
    PLAYER2: 'O'
}

# 4x4 board
rows = 4
cols = 4

class ConnectFour:
    def __init__(self, initial_state):
        self.rows = rows
        self.cols = cols
        self.initial = initial_state
        self.board = self.initialize_board()

    def verify_board(self, board):
        player1_count = 0
        player2_count = 0

        # count each players' pieces
        for row in board:
            for cell in row:
                if cell == PLAYER1:
                    player1_count += 1
                elif cell == PLAYER2:
                    player2_count += 1

        # ensure valid number of pieces
        if player1_count - player2_count != 1:
            return False  # Invalid board state

        # check for floating pieces
        for col in range(4):
            empty_found = False
            for row in range(4):
                if board[3-row][3-col] == EMPTY:
                    empty_found = True
                elif empty_found:
                    return False 

        return True


    def initialize_board(self):
        if self.initial is True:
            return [[EMPTY for _ in range(self.cols)] for _ in range(self.rows)]
        else:
            board = [[random.choice([EMPTY, PLAYER1, PLAYER2]) for _ in range(self.cols)] for _ in range(self.rows)]
            while self.verify_board(board) is False:
                board = [[random.choice([EMPTY, PLAYER1, PLAYER2]) for _ in range(self.cols)] for _ in range(self.rows)]
            return board

    def display_board(self):
        print("\nCurrent Board:")
        for row in self.board:
            print(' '.join(SYMBOLS[cell] for cell in row))
        print(' ' + ' '.join(str(i) for i in range(self.cols)))

    def get_valid_moves(self):
        valid_moves = []
        for col in range(self.cols):
            if self.board[0][col] == EMPTY:
                valid_moves.append(col)
        return valid_moves

    def make_move(self, col, player):
        for row in reversed(range(self.rows)):
            if self.board[row][col] == EMPTY:
                self.board[row][col] = player
                return True
        return False

    def undo_move(self, col):
        for row in range(self.rows):
            if self.board[row][col] != EMPTY:
                self.board[row][col] = EMPTY
                return True
        return False

    def is_full(self):
        return all(self.board[0][col] != EMPTY for col in range(self.cols))

    def check_win(self, player):
        # horizontal
        for row in range(self.rows):
            for col in range(self.cols - 3):
                if all(self.board[row][col + i] == player for i in range(4)):
                    return True
        # vertical
        for col in range(self.cols):
            for row in range(self.rows - 3):
                if all(self.board[row + i][col] == player for i in range(4)):
                    return True
        # the 2 diagonals
        for row in range(3, self.rows):
            for col in range(self.cols - 3):
                if all(self.board[row - i][col + i] == player for i in range(4)):
                    return True
        for row in range(self.rows - 3):
            for col in range(self.cols - 3):
                if all(self.board[row + i][col + i] == player for i in range(4)):
                    return True
        return False

    def is_terminal_node(self):
        return self.check_win(PLAYER1) or self.check_win(PLAYER2) or self.is_full()

    def get_winner(self, maximizing_player):
        if self.check_win(PLAYER1):
            return True if maximizing_player else False
        elif self.check_win(PLAYER2):
            return False if maximizing_player else True
        else:
            return None
