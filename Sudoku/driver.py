
from csp_lib.sudoku import (Sudoku, easy1, harder1)
from constraint_prop import AC3
from csp_lib.backtrack_util import mrv, mac
from backtrack import backtracking_search
# I promise that the attached assignment is my own work.
# I recognize that should this not be the case,
# I will be subject to penalties as outlined in the course syllabus. [Jesse Hernandez]

for puzzle in [easy1, harder1]:
    # each puzzle will first be printed to show what it looks like
    # before and after inference
    s = Sudoku(puzzle)  # construct a Sudoku problem
    if puzzle == easy1:
        print("This is the easy one before any inference")
    else:
        print("The hard puzzle before any inference")
    s.display(s.infer_assignment())
    print()
    AC3(s)  # inference is done with AC3 if the puzzle is not solved
    # backtracking inference will be done
    if puzzle == easy1:
        print("Now after inference the puzzle has been solved")
    else:
        print("After inference the hard puzzle has not been solved now I need backtracking")
    s.display(s.infer_assignment())
    print()
    if not s.goal_test(s.infer_assignment()):
        result = backtracking_search(s, select_unassigned_variable=mrv, inference=mac)
        s.display(s.infer_assignment())
        if result:
            print("The puzzle was able to be solved")
        else:
            print("The puzzle was not able to be solved")





    # solve as much as possible by AC3 then backtrack search if needed
    # using MRV and MAC.
    
