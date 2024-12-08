import random

EMPTY = 0
PLAYER1 = 1  
PLAYER2 = -1 

SYMBOLS = {
    EMPTY: '·',
    PLAYER1: 'X',
    PLAYER2: 'O'
}

class ConnectFour:
    def __init__(self, initial_state, game_size):
        if(game_size == 'medium'):
            self.rows = 5
            self.cols = 5
        elif(game_size == 'large'):
            self.rows = 6
            self.cols = 7
        else:
            self.rows = 4
            self.cols = 4
        self.initial = initial_state
        self.board = self.initialize_board()

    def get_state_key(self, maximizingPlayer):
        return (maximizingPlayer, tuple(tuple(row) for row in self.board))

    def verify_board(self, board):
        player1_count = sum(cell == PLAYER1 for row in board for cell in row)
        player2_count = sum(cell == PLAYER2 for row in board for cell in row)

        # Must differ by exactly 1 for a valid game state
        if player1_count - player2_count != 1:
            return False

        # Check gravity (no floating pieces)
        for col in range(self.cols):
            empty_found = False
            for row in range(self.rows):
                if board[(self.rows-1) - row][(self.cols-1) - col] == EMPTY:
                    empty_found = True
                elif empty_found:
                    # Found a piece above an empty slot
                    return False
        return True

    def initialize_board(self):
        if self.initial:
            return [[EMPTY for _ in range(self.cols)] for _ in range(self.rows)]
        else:
            # Instead of randomizing every cell, we will place a small number of moves
            # This ensures faster initialization and a valid state.
            board = [[EMPTY for _ in range(self.cols)] for _ in range(self.rows)]
            
            # Let's place a small random number of moves:
            # For large boards, place at most 3 moves of Player1 and 2 moves of Player2 to keep it valid.
            # Player1_count = Player2_count + 1
            moves_to_place = random.randint(0, 3)  # up to 3 moves of Player1
            player1_count = moves_to_place
            player2_count = moves_to_place - 1 if moves_to_place > 0 else 0

            # Place Player1_count pieces of PLAYER1 and Player2_count pieces of PLAYER2 in valid positions
            for p in range(player1_count):
                self.place_random_piece(board, PLAYER1)
            for p in range(player2_count):
                self.place_random_piece(board, PLAYER2)

            return board

    def place_random_piece(self, board, player):
        # Place a piece in a random valid column
        valid_cols = [c for c in range(self.cols) if board[0][c] == EMPTY]
        if not valid_cols:
            return
        col = random.choice(valid_cols)
        for r in reversed(range(self.rows)):
            if board[r][col] == EMPTY:
                board[r][col] = player
                break

    def display_board(self):
        print("\nCurrent Board:")
        for row in self.board:
            print(' '.join(SYMBOLS[cell] for cell in row))
        print(' ' + ' '.join(str(i) for i in range(self.cols)))

    def get_valid_moves(self):
        return [col for col in range(self.cols) if self.board[0][col] == EMPTY]

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
        # diagonals
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
