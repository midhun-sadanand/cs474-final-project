# cs474-final-project

**Group Members:**
    Midhun Sadanand
    Raymond Hou
    Daniel Liu

How to Run the Test Script

    1. run "make" in terminal
    2. Usage: ./FinalProj [connectfour|nim|dotsandboxes] [initial/random]

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

Results (for initial state)

    Connect Four:   AB pruning improves Minimax algorithm by above 60% in node and time reduction
    3-row Nim:      AB pruning improves Minimax algorithm by above 95% in node and time reduction
    Dots and Boxes: AB pruning improves Minimax algorithm by above 95% in node and time reduction
