# main.py

"""
Group Members: 
    Midhun Sadanand
    Raymond Hou
    Daniel Liu

How to Run the Test Script
    1. run "make" in terminal
    2. Usage: ./FinalProj [connectfour|nim|dotsandboxes] [small/medium/large] [initial/random] [cmp1/cmp2/cmp3/cmp4/cmp5]

Brief Description of Final Project
    Our final project compares the performance of a minimax algorithm using 5 different comparison agents, which are combinations of
    minimax, alpha-beta pruning, transposition table storage, and SCOUT, to solve small, medium, and large state space configurations of 
    Connect Four, 3-row Nim, and simplified Dots and Boxes. 
    We measure node evaluations and compute time.

What Our Code Does
    1. argument parsing based on user input that specifies game, state space size, initial or random board configuration, which comparison agent to use against baseline minimax
    2. minimax:
    3. alpha-beta pruning:
    4. transposition table:
    5. scout

Research Question
    How much more efficient does alpha-beta pruning, SCOUT (with re-search), and/or transposition tables 
    make the minimax algorithm when calculating the best move for the following 3 games?
        Connect Four
        Nim
        Dots and Boxes
    And how do these improvements scale with increasingly large state spaces?

Results (for initial state)
    todo:
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
from sampling import minimax_sample 

def main():
    if len(sys.argv) < 5:
        print("Usage: ./FinalProj [connectfour|nim|dotsandboxes] [small/medium/large] [initial/random] [cmp1/cmp2/cmp3/cmp4/cmp5]")
        sys.exit(1)

    game_choice = sys.argv[1].lower().replace('_', '')
    if(game_choice not in ['connectfour', 'nim', 'dotsandboxes']):
        print("Usage: ./FinalProj [connectfour|nim|dotsandboxes] [small/medium/large] [initial/random] [cmp1/cmp2/cmp3/cmp4/cmp5]")
        sys.exit(1)

    game_size = sys.argv[2]
    if(game_size not in ['small', 'medium', 'large']):
        print("Usage: ./FinalProj [connectfour|nim|dotsandboxes] [small/medium/large] [initial/random] [cmp1/cmp2/cmp3/cmp4/cmp5]")
        sys.exit(1)

    state = sys.argv[3]
    if(state not in ['initial', 'random']):
        print("Usage: ./FinalProj [connectfour|nim|dotsandboxes] [small/medium/large] [initial/random] [cmp1/cmp2/cmp3/cmp4/cmp5]")
        sys.exit(1)

    agent = sys.argv[4]
    if(agent not in ['cmp1', 'cmp2', 'cmp3', 'cmp4', 'cmp5']):
        print("Usage: ./FinalProj [connectfour|nim|dotsandboxes] [initial/random] [cmp1/cmp2/cmp3/cmp4/cmp5]")
        sys.exit(1)

    if(agent in ['cmp3', 'cmp4', 'cmp5']):
        has_tt = True
    else:
        has_tt = False
    
    if game_choice == 'connectfour':
        if(state == 'initial'):
            game = ConnectFour(True, game_size)
        elif (state == 'random'):
            game = ConnectFour(False, game_size)
        MAX_DEPTH = 4
    elif game_choice == 'nim':
        if(state == 'initial'):
            game = Nim(True, game_size)
        elif (state == 'random'):
            game = Nim(False, game_size)
        MAX_DEPTH = 10
    elif game_choice == 'dotsandboxes':
        if(state == 'initial'):
            game = DotsAndBoxes(True, game_size)
            MAX_DEPTH = 3
        elif (state == 'random'):
            game = DotsAndBoxes(False, game_size)
            MAX_DEPTH = 6

    game.display_board()

    node_counter_minimax = {'nodes': 0}
    node_counter_agent = {'nodes': 0}

    # minimax algo
    start_time_minimax = time.time()
    if(game_choice == 'dotsandboxes' and game_size == 'large'):
        best_move_minimax, _ = minimax_sample(game, MAX_DEPTH, game_size, True, node_counter_minimax, 1000)
    else:
        best_move_minimax, _ = minimax(game, MAX_DEPTH, game_size, True, node_counter_minimax, None)
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
        best_move_agent, _ = alphabeta(game, MAX_DEPTH, game_size, float('-inf'), float('inf'), True, node_counter_agent, tt)
        end_time_agent = time.time()
        time_agent = end_time_agent - start_time_agent
    
    # COMPARISON 3: minimax + transposition tables
    elif(agent == 'cmp3'):
        agent = "Minimax + Transposition"
        start_time_agent = time.time()
        best_move_agent, _ = minimax(game, MAX_DEPTH, game_size, True, node_counter_agent, tt)
        end_time_agent = time.time()
        time_agent = end_time_agent - start_time_agent

    # COMPARISONS 2 AND 5: scout (+ transposition tables)
    elif(agent in ['cmp2', 'cmp5']):
        if(agent == 'cmp2'):
            agent = "Scout"
        else:
            agent = "Scout + Transposition"
        start_time_agent = time.time()
        best_move_agent, _ = scout(game, MAX_DEPTH, game_size, float('-inf'), float('inf'), True, node_counter_agent, tt)
        end_time_agent = time.time()
        time_agent = end_time_agent - start_time_agent

    # metrics
    if(game_choice == 'dotsandboxes' and game_size == 'large'):
        print(f"\nMinimax Sampling Results for {game_choice.replace('_', ' ').title()}:")
    else:
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
