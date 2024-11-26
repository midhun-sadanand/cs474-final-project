# main.py

import time
import sys
from connectfour import ConnectFour
from nim import Nim
from dotsandboxes import DotsAndBoxes
from minimax import minimax
from alphabeta import alphabeta

def main():
    if len(sys.argv) < 2:
        print("Usage: python main.py [connectfour|nim|dotsandboxes]")
        sys.exit(1)

    game_choice = sys.argv[1].lower().replace('_', '')

    if game_choice == 'connectfour':
        game = ConnectFour()
        MAX_DEPTH = 4
    elif game_choice == 'nim':
        game = Nim()
        MAX_DEPTH = 10
    elif game_choice == 'dotsandboxes':
        game = DotsAndBoxes()
        MAX_DEPTH = 3
    else:
        print("Invalid game choice.")
        sys.exit(1)

    game.display_board()

    node_counter_minimax = {'nodes': 0}
    node_counter_alphabeta = {'nodes': 0}

    # Run Minimax
    start_time_minimax = time.time()
    best_move_minimax, _ = minimax(game, MAX_DEPTH, True, node_counter_minimax)
    end_time_minimax = time.time()
    time_minimax = end_time_minimax - start_time_minimax

    # Run Alpha-Beta Pruning
    start_time_alphabeta = time.time()
    best_move_alphabeta, _ = alphabeta(game, MAX_DEPTH, float('-inf'), float('inf'), True, node_counter_alphabeta)
    end_time_alphabeta = time.time()
    time_alphabeta = end_time_alphabeta - start_time_alphabeta

    # Display results
    print(f"\nMinimax Results for {game_choice.replace('_', ' ').title()}:")
    print(f"Best Move: {best_move_minimax}")
    print(f"Nodes Explored: {node_counter_minimax['nodes']}")
    print(f"Time Taken: {time_minimax:.6f} seconds")

    print(f"\nAlpha-Beta Pruning Results for {game_choice.replace('_', ' ').title()}:")
    print(f"Best Move: {best_move_alphabeta}")
    print(f"Nodes Explored: {node_counter_alphabeta['nodes']}")
    print(f"Time Taken: {time_alphabeta:.6f} seconds")

    # Comparison
    if node_counter_minimax['nodes'] > 0:
        node_reduction = ((node_counter_minimax['nodes'] - node_counter_alphabeta['nodes']) / node_counter_minimax['nodes']) * 100
    else:
        node_reduction = 0
    if time_minimax > 0:
        time_reduction = ((time_minimax - time_alphabeta) / time_minimax) * 100
    else:
        time_reduction = 0

    print("\nPerformance Improvement:")
    print(f"Node Reduction: {node_reduction:.2f}%")
    print(f"Time Reduction: {time_reduction:.2f}%")

if __name__ == "__main__":
    main()
