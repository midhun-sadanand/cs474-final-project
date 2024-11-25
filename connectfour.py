import time

# Constants representing players and empty cells
EMPTY = 0
PLAYER1 = 1  # AI
PLAYER2 = -1  # Opponent

# Symbols for visual representation
SYMBOLS = {
    EMPTY: '·',
    PLAYER1: 'X',
    PLAYER2: 'O'
}

class ConnectFour:
    def __init__(self, rows=4, cols=4):
        self.rows = rows
        self.cols = cols
        self.board = [[EMPTY for _ in range(cols)] for _ in range(rows)]

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
        return False  # Column is full

    def undo_move(self, col):
        for row in range(self.rows):
            if self.board[row][col] != EMPTY:
                self.board[row][col] = EMPTY
                return True
        return False

    def is_full(self):
        return all(self.board[0][col] != EMPTY for col in range(self.cols))

    def check_win(self, player):
        # Check horizontal, vertical, and diagonal lines for a win
        # Horizontal
        for row in range(self.rows):
            for col in range(self.cols - 3):
                if all(self.board[row][col + i] == player for i in range(4)):
                    return True
        # Vertical
        for col in range(self.cols):
            for row in range(self.rows - 3):
                if all(self.board[row + i][col] == player for i in range(4)):
                    return True
        # Diagonal (positive slope)
        for row in range(3, self.rows):
            for col in range(self.cols - 3):
                if all(self.board[row - i][col + i] == player for i in range(4)):
                    return True
        # Diagonal (negative slope)
        for row in range(self.rows - 3):
            for col in range(self.cols - 3):
                if all(self.board[row + i][col + i] == player for i in range(4)):
                    return True
        return False

    def is_terminal_node(self):
        return self.check_win(PLAYER1) or self.check_win(PLAYER2) or self.is_full()
