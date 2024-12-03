# heuristic.py

from connectfour import ConnectFour, PLAYER1, PLAYER2, EMPTY
from nim import Nim
from dotsandboxes import DotsAndBoxes

def evaluate(game, maximizing_player):
    if isinstance(game, Nim):
        return evaluate_nim(game, maximizing_player)
    elif isinstance(game, DotsAndBoxes):
        return evaluate_dots_and_boxes(game, maximizing_player)
    elif isinstance(game, ConnectFour):
        player = PLAYER1 if maximizing_player else PLAYER2
        return evaluate_connect_four(game, player)
    else:
        return 0

def evaluate_nim(game, maximizing_player):
    # calcualte nimbers (is there a game winning move)
    nimber = 0
    for heap in game.heaps:
        nimber ^= heap
    if nimber == 0:
        return float('-inf') if maximizing_player else float('inf')
    else:
        return float('inf') if maximizing_player else float('-inf')

def evaluate_dots_and_boxes(game, maximizing_player):
    # difference in box counts
    player1_score = sum(row.count(1) for row in game.boxes)
    player2_score = sum(row.count(-1) for row in game.boxes)
    return (player1_score - player2_score) if maximizing_player else (player2_score - player1_score)

def evaluate_connect_four(game, player):
    score = 0

    # incentivize central column for more scoring patterns
    center_array = [game.board[i][game.cols // 2] for i in range(game.rows)]
    center_count = center_array.count(player)
    score += center_count * 3

    # count up horizontal scoring
    for row in range(game.rows):
        row_array = game.board[row]
        for col in range(game.cols - 3):
            window = row_array[col:col + 4]
            score += evaluate_window(window, player)

    # count up vertical scoring
    for col in range(game.cols):
        col_array = [game.board[row][col] for row in range(game.rows)]
        for row in range(game.rows - 3):
            window = col_array[row:row + 4]
            score += evaluate_window(window, player)

    # count up diagonal scoring
    for row in range(game.rows - 3):
        for col in range(game.cols - 3):
            window = [game.board[row + i][col + i] for i in range(4)]
            score += evaluate_window(window, player)
    for row in range(3, game.rows):
        for col in range(game.cols - 3):
            window = [game.board[row - i][col + i] for i in range(4)]
            score += evaluate_window(window, player)

    return score

def evaluate_window(window, player):
    score = 0
    opp_player = PLAYER2 if player == PLAYER1 else PLAYER1

    # incentivize close to 4-in-a-row
    if window.count(player) == 4:
        score += 100
    elif window.count(player) == 3 and window.count(EMPTY) == 1:
        score += 5
    elif window.count(player) == 2 and window.count(EMPTY) == 2:
        score += 2

    # deincentivize opp being close to 4-in-a-row
    if window.count(opp_player) == 3 and window.count(EMPTY) == 1:
        score -= 4

    return score
