# heuristic.py

from connectfour import EMPTY, PLAYER1, PLAYER2

def evaluate_window(window, player):
    score = 0
    opp_player = PLAYER2 if player == PLAYER1 else PLAYER1

    if window.count(player) == 4:
        score += 100
    elif window.count(player) == 3 and window.count(EMPTY) == 1:
        score += 5
    elif window.count(player) == 2 and window.count(EMPTY) == 2:
        score += 2

    if window.count(opp_player) == 3 and window.count(EMPTY) == 1:
        score -= 4

    return score

def score_position(game, player):
    score = 0

    # Center column preference
    center_array = [game.board[i][game.cols // 2] for i in range(game.rows)]
    center_count = center_array.count(player)
    score += center_count * 3

    # Horizontal scoring
    for row in range(game.rows):
        row_array = game.board[row]
        for col in range(game.cols - 3):
            window = row_array[col:col + 4]
            score += evaluate_window(window, player)

    # Vertical scoring
    for col in range(game.cols):
        col_array = [game.board[row][col] for row in range(game.rows)]
        for row in range(game.rows - 3):
            window = col_array[row:row + 4]
            score += evaluate_window(window, player)

    # Positive diagonal scoring
    for row in range(game.rows - 3):
        for col in range(game.cols - 3):
            window = [game.board[row + i][col + i] for i in range(4)]
            score += evaluate_window(window, player)

    # Negative diagonal scoring
    for row in range(3, game.rows):
        for col in range(game.cols - 3):
            window = [game.board[row - i][col + i] for i in range(4)]
            score += evaluate_window(window, player)

    return score
