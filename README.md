# cs474-final-project

**Group Members:**
    Midhun Sadanand
    Raymond Hou
    Daniel Liu

**Research Question**

    How much more efficient does alpha-beta pruning make the minimax algorithm when calculating 
    the best move for the following 3 games?
        Connect Four
        3-pile Nim
        Dots and Boxes

**How to Run the Test Script**

    1. run "make" in terminal
    2. Usage: ./FinalProj [connectfour|nim|dotsandboxes]

**Brief Description of Final Project**

    Our final project compares the performance of a minimax algorithm with and without alpha-beta 
    pruning in solving simplified Connect Four, 3-row Nim, and simplified Dots and Boxes. 
    We measure node evaluations and compute time.

**What Our Code Does**

**Results**

    Connect Four:   AB pruning improves upon Minimax algorithm with over 60% reduction in nodes explored and time spent searching.
    3-row Nim:      AB pruning improves upon Minimax algorithm with over 95% reduction in nodes explored and time spent searching
    Dots and Boxes: AB pruning improves upon Minimax algorithm with over 95% reduction in nodes explored and time spent searching.
