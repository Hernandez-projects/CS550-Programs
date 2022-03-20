"""
I promise that the attached assignment is my own work.
I recognize that should this not be the case,
 I will be subject to penalties as outlined in the course syllabus.Jesse Hernandez

driver for graph search problem
"""

from statistics import (mean, stdev)  # Only available in Python 3.4 and newer

from npuzzle import NPuzzle
from basicsearch_lib02.tileboard import TileBoard
from basicsearch_lib02.timer import Timer
from searchstrategies import (BreadthFirst, DepthFirst, Manhattan)
from problemsearch import graph_search
import collections


def driver():
    exampleOne = NPuzzle(8)
    print(exampleOne.actions(exampleOne.state))
    print(exampleOne.boardsize)
    print(exampleOne.state.__repr__())


# To do:  Run driver() if this is the entry module
driver()
