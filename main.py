# main.py

import time
from connectfour import ConnectFour
from minimax import minimax, MAX_DEPTH as MINIMAX_DEPTH
from alphabeta import alphabeta, MAX_DEPTH as ALPHABETA_DEPTH

def main():
    game = ConnectFour()
    game.display_board()

    node_counter_minimax = {'nodes': 0}
    node_counter_alphabeta = {'nodes': 0}

    # Run Minimax with depth limit
    start_time_minimax = time.time()
    best_move_minimax, _ = minimax(game, MINIMAX_DEPTH, True, node_counter_minimax)
    end_time_minimax = time.time()
    time_minimax = end_time_minimax - start_time_minimax

    # Run Minimax with Alpha-Beta Pruning and depth limit
    start_time_alphabeta = time.time()
    best_move_alphabeta, _ = alphabeta(game, ALPHABETA_DEPTH, float('-inf'), float('inf'), True, node_counter_alphabeta)
    end_time_alphabeta = time.time()
    time_alphabeta = end_time_alphabeta - start_time_alphabeta

    # Display results
    print("\nMinimax with Depth Limit:")
    print(f"Best Move: Column {best_move_minimax}")
    print(f"Nodes Explored: {node_counter_minimax['nodes']}")
    print(f"Time Taken: {time_minimax:.6f} seconds")

    print("\nAlpha-Beta Pruning with Depth Limit:")
    print(f"Best Move: Column {best_move_alphabeta}")
    print(f"Nodes Explored: {node_counter_alphabeta['nodes']}")
    print(f"Time Taken: {time_alphabeta:.6f} seconds")

    # Comparison
    node_reduction = ((node_counter_minimax['nodes'] - node_counter_alphabeta['nodes']) / node_counter_minimax['nodes']) * 100
    time_reduction = ((time_minimax - time_alphabeta) / time_minimax) * 100

    print("\nPerformance Improvement:")
    print(f"Node Reduction: {node_reduction:.2f}%")
    print(f"Time Reduction: {time_reduction:.2f}%")

if __name__ == "__main__":
    main()
