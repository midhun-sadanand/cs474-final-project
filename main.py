# main.py

"""
Group Members: 
    Midhun Sadanand
    Raymond Hou
    Daniel Liu

How to Run the Test Script
    1. run "make" in terminal
    2. Usage: ./FinalProj [connectfour|nim|dotsandboxes] [small/medium/large] [initial/random] [cmp1/cmp2/cmp3/cmp4/cmp5]"
    
    Comparison 1: minimax vs. alpha-beta pruning algorithm
    Comparison 2: minimax vs. scout algorithm
    Comparison 3: minimax vs. transposition tables + mimimax
    Comparison 4: minimax vs. transposition tables + alpha-beta
    Comparison 5: minimax vs. transposition tables + scout


Brief Description of Final Project
    Our final project compares the performance of a minimax algorithm with and without alpha-beta 
    pruning in solving simplified Connect Four, 3-row Nim, and simplified Dots and Boxes. 
    We measure node evaluations and compute time.

What Our Code Does


Research Question
    How much more efficient does alpha-beta pruning make the minimax algorithm when calculating 
    the best move for the following 3 games?
        Connect Four
        3-pile Nim
        Dots and Boxes

Results (for initial states)
    Connect Four:   AB pruning improves Minimax algorithm by above 60% in node and time reduction
    3-row Nim:      AB pruning improves Minimax algorithm by above 95% in node and time reduction
    Dots and Boxes: AB pruning improves Minimax algorithm by above 95% in node and time reduction
"""

import time
import sys
from connectfour import ConnectFour
from nim import Nim
from dotsandboxes import DotsAndBoxes
from minimax import minimax
from alphabeta import alphabeta
from scout import scout
from transpositiontable import TranspositionTable  

def main():
    if len(sys.argv) < 4:
        print("Usage: ./FinalProj [connectfour|nim|dotsandboxes] [small/medium/large] [initial/random] [cmp1/cmp2/cmp3/cmp4/cmp5]")
        sys.exit(1)

    game_choice = sys.argv[1].lower().replace('_', '')
    game_size = sys.argv[2]
    state = sys.argv[3]
    agent = sys.argv[4]

    if(agent in ['cmp3', 'cmp4', 'cmp5']):
        has_tt = True
    else:
        has_tt = False
    
    if game_choice == 'connectfour':
        if(state == 'initial'):
            game = ConnectFour(True)
        elif (state == 'random'):
            game = ConnectFour(False)
        else:
            print("Usage: ./FinalProj [connectfour|nim|dotsandboxes] [small/medium/large] [initial/random] [cmp1/cmp2/cmp3/cmp4/cmp5]")
            sys.exit(1)
        MAX_DEPTH = 4
    elif game_choice == 'nim':
        if(state == 'initial'):
            game = Nim(True)
        elif (state == 'random'):
            game = Nim(False)
        else:
            print("Usage: ./FinalProj [connectfour|nim|dotsandboxes] [small/medium/large] [initial/random] [cmp1/cmp2/cmp3/cmp4/cmp5]")
            sys.exit(1)
        MAX_DEPTH = 10
    elif game_choice == 'dotsandboxes':
        if(state == 'initial'):
            game = DotsAndBoxes(True)
            MAX_DEPTH = 3
        elif (state == 'random'):
            game = DotsAndBoxes(False)
            MAX_DEPTH = 10
        else:
            print("Usage: ./FinalProj [connectfour|nim|dotsandboxes] [small/medium/large] [initial/random] [cmp1/cmp2/cmp3/cmp4/cmp5]")
            sys.exit(1)
    else:
        print("Usage: ./FinalProj [connectfour|nim|dotsandboxes] [small/medium/large] [initial/random] [cmp1/cmp2/cmp3/cmp4/cmp5]")
        sys.exit(1)

    game.display_board()

    node_counter_minimax = {'nodes': 0}
    node_counter_agent = {'nodes': 0}

    # minimax algo
    start_time_minimax = time.time()
    best_move_minimax, _ = minimax(game, MAX_DEPTH, True, node_counter_minimax, None)
    end_time_minimax = time.time()
    time_minimax = end_time_minimax - start_time_minimax

    tt = TranspositionTable() if has_tt else None

    # COMPARISONS 1 AND 4: minimax w/ alpha-beta algo (+ transposition tables)
    if(agent in ['cmp1', 'cmp4']):
        if(agent == 'cmp1'):
            agent = "Alpha-Beta Pruning"
        else:
            agent = "Alpha-Beta Pruning + Transposition"
        start_time_agent = time.time()
        best_move_agent, _ = alphabeta(game, MAX_DEPTH, float('-inf'), float('inf'), True, node_counter_agent, tt)
        end_time_agent = time.time()
        time_agent = end_time_agent - start_time_agent
    
    # COMPARISON 3: minimax + transposition tables
    elif(agent == 'cmp3'):
        agent = "Minimax + Transposition"
        start_time_agent = time.time()
        best_move_agent, _ = minimax(game, MAX_DEPTH, True, node_counter_agent, tt)
        end_time_agent = time.time()
        time_agent = end_time_agent - start_time_agent

    # COMPARISONS 2 AND 5: scout (+ transposition tables)
    elif(agent in ['cmp2', 'cmp5']):
        if(agent == 'cmp2'):
            agent = "Scout"
        else:
            agent = "Scout + Transposition"
        start_time_agent = time.time()
        best_move_agent, _ = scout(game, MAX_DEPTH, float('-inf'), float('inf'), True, node_counter_agent, tt)
        end_time_agent = time.time()
        time_agent = end_time_agent - start_time_agent

    # not valid comparison
    else:
        print("Usage: ./FinalProj [connectfour|nim|dotsandboxes] [initial/random] [cmp1/cmp2/cmp3/cmp4/cmp5]")
        sys.exit(1)

    # metrics
    print(f"\nMinimax Results for {game_choice.replace('_', ' ').title()}:")
    print(f"Best Move: {best_move_minimax}")
    print(f"Nodes Explored: {node_counter_minimax['nodes']}")
    print(f"Time Taken: {time_minimax:.6f} seconds")

    print("\n{} Results for {}:".format(agent, game_choice.replace('_', ' ').title()))
    print(f"Best Move: {best_move_agent}")
    print(f"Nodes Explored: {node_counter_agent['nodes']}")
    print(f"Time Taken: {time_agent:.6f} seconds")

    # analysis of improvement
    if node_counter_minimax['nodes'] > 0:
        node_reduction = ((node_counter_minimax['nodes'] - node_counter_agent['nodes']) / node_counter_minimax['nodes']) * 100
    else:
        node_reduction = 0
    if time_minimax > 0:
        time_reduction = ((time_minimax - time_agent) / time_minimax) * 100
    else:
        time_reduction = 0

    print("\nPerformance Improvement:")
    print(f"Node Reduction: {node_reduction:.2f}%")
    print(f"Time Reduction: {time_reduction:.2f}%")

if __name__ == "__main__":
    main()
