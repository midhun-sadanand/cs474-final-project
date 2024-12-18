# cs474-final-project

**Group Members:**

    Midhun Sadanand
    Raymond Hou
    Daniel Liu

How to Run the Test Script

    1. run "make" in terminal
    2. Usage: ./FinalProj [connectfour|nim|dotsandboxes] [small/medium/large] [initial/random] [cmp1/cmp2/cmp3/cmp4/cmp5]

Brief Description of Final Project

    Our final project compares the performance of a minimax algorithm using 5 different comparison agents, which are combinations of minimax, alpha-beta pruning, transposition table storage, and SCOUT, to solve small, medium, and large state space configurations of Connect Four, 3-row Nim, and simplified Dots and Boxes. 
    We measure node evaluations and compute time.

What Our Code Does

    1. user input argument parsing: specifies game, state space size, initial or random board configuration, which comparison agent
    2. minimax: evaluates all possible game state up to the specified depth to determine the best move for the maximizing player
    3. alpha-beta pruning: optimizes minimax by pruning branches that do not influence the found best move
    4. transposition table: caches results of previously seen states, similar to memoization and DP
    5. scout: alpha-beta pruning variant that uses full-window and null-window searches to re-evaluate moves
    6. game representations: connectfour, nim, and dotsandboxes rules, board/state configurations, and terminal conditions, and player-turn based actions
    7. heuristic: incentivize and label intermediate states with arbitrary increments (similar to pegging policies)
    8. node counter and time measurement implementation to interpret final results

    PS. We randomly sample states for the large dotsandboxes case, since otherwise 
    the current minimax algorithm runs for an unreasonable amount of time to compute the best move.

Research Question

    How much more efficient does alpha-beta pruning, SCOUT (with re-search), and/or transposition tables 
    make the minimax algorithm when calculating the best move for the following 3 games?
        Connect Four
        Nim
        Dots and Boxes
    And how do these improvements scale with increasingly large state spaces?

Results

    1. ALPHA-BETA PRUNING

    Cmp4 (Alpha-Beta Pruning + Transposition Tables) performs the best overall by cutting off
    unnecessary searches and reusing cached results, making it the most efficient option.
    As the games get larger, combining Alpha-Beta Pruning with Transposition Tables becomes essential for 
    keeping the computation time manageable and showing clear improvements over basic Minimax.

    On its own, Cmp1 (Alpha-Beta Pruning) does better than basic Minimax by skipping irrelevant branches but still falls 
    behind methods that use caching, especially in bigger games. 


    2. MINIMAX + TRANSPOSITION

    Cmp3 (Minimax + Transposition Tables) greatly improves both the number of nodes explored and the time taken by saving and 
    reusing previously evaluated game states. These benefits become even more noticeable as the games get more complex. 
     
    
    3. SCOUT
     
    Cmp2 (SCOUT) struggles because it needs to redundantly check moves to ensure the optimal output, 
    adding extra work and decreasing efficiency in smaller or medium sized games.
     
    Cmp5 tries to fix SCOUT's problems by adding Transposition Tables, but it still isn't as fast or efficient as
    Cmp3 and Cmp4 due to SCOUT's re-checking process. 