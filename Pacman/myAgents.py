import game
from pacman import Directions
from game import Agent, Actions
from pacmanAgents import LeftTurnAgent

"""
September 2nd, 2021
Prof Roch
I promise that the attached assignment is my own work. I recognize that should this not be the case,
I will be subject to penalties as outlined in the course syllabus. Jesse Hernandez

I am programming by myself so all code modified in this file 
will belong to me. Any references will be cited : I pulled some code from the LeftTurnAgent
file so credit to the original Author of pacmanAgents.py
In getAction I tried to make a call to LeftTurnAgent.getAction but could not make it work so
I used the code for that method. Meaning that bit of code is not my own but belongs to the original person from uc berkly
"""


class TimidAgent(Agent):
    """
    A simple agent for PacMan
    """

    def __init__(self):
        super().__init__()  # Call parent constructor
        # Add anything else you think you need here

    def inDanger(self, pacman, ghost, dist=3):
        """inDanger(pacman, ghost) - Is the pacman in danger
        For better or worse, our definition of danger is when the pacman and
        the specified ghost are:
           in the same row or column,
           the ghost is not scared,
           and the agents are <= dist units away from one another

        If the pacman is not in danger, we return Directions.STOP
        If the pacman is in danger we return the direction to the ghost.
        """
        ghostScared = ghost.isScared()  # Given the ghost state I can check if it is scared
        if ghostScared:
            return Directions.STOP  # If the ghost is scared it presents no danger
        else:
            ghostLocation = ghost.getPosition()  # Need the position of ghost and pacman
            pacLocation = pacman.getPosition()
            if ghostLocation[0] == pacLocation[0]:  # This checks if their x coordinate is the same
                # meaning that they are in the same column
                if (abs(ghostLocation[1] - pacLocation[1])) <= dist:  # Since they are in the same column
                    # pacman might be in danger so the distance needs to be measured
                    # pacman is in danger if that distance is less than or equal to 3 units
                    if ghostLocation[1] - pacLocation[1] > 0:
                        return Directions.NORTH  # Since they are in the same column the danger is either north or south
                    else:
                        return Directions.SOUTH  # If the outcome is positive then danger is north otherwise it is south
                else:
                    return Directions.STOP  # lastly no if statement caught danger when in the same column so safe
            elif ghostLocation[1] == pacLocation[1]:  # this is to test for being in the same row
                if (abs(ghostLocation[0] - pacLocation[0])) <= dist:
                    if ghostLocation[0] - pacLocation[0] > 0:  # then the same checks from the last block
                        return Directions.EAST  # except this time danger can only be either west or east
                    else:
                        return Directions.WEST
                else:
                    return Directions.STOP
            else:
                return Directions.STOP  # after both blocks there is absolutely no danger

    def getAction(self, state):
        """
        state - GameState
        
        This function is meant to try avoiding the ghosts whenever pacman is in danger.
        by this I mean whenever a ghost is within 3 distance units from pacman it will take evasive maneuvers
        to escape the ghost.
        If pacman is not in danger then it will move according to LeftTurnAgent that is take a left turn whenever
        possible
        """
        pacState = state.getPacmanState()
        allGhosts = state.getGhostStates()  # here is all the ghost states
        # I am checking each ghost for danger individually

        legal = state.getLegalPacmanActions()  # This holds a list of all legal moves
        heading = pacState.getDirection()
        right = Directions.RIGHT[heading]  # what is right based on current heading
        left = Directions.LEFT[heading]  # What is left based on current heading

        if heading == Directions.STOP:
            heading = Directions.NORTH  # if pacman is stopped we assume it is facing true north
        allDangers = [self.inDanger(pacState, ghost) for ghost in allGhosts]
        # creates a list that holds all returns from inDanger
        """ IN the next chunk I am testing to see if the ghosts are scarred to just assume pacman is safe
        and then just behave exacly like LeftTurnAgent.getAction()
        """
        allSafe = True
        for danger in allDangers:
            if danger != Directions.STOP:
                allSafe = False
        if allSafe:
            if left in legal:
                action = left
            else:
                # No left turn
                if heading in legal:
                    action = heading  # continue in current direction
                elif Directions.RIGHT[heading] in legal:
                    action = Directions.RIGHT[heading]  # Turn right
                elif Directions.REVERSE[heading] in legal:
                    action = Directions.REVERSE[heading]  # Turn around
                else:
                    action = Directions.STOP  # Can't move!

            return action

        else:  # The following block is going check all 4 directions for a possible move
            if left in legal and left not in allDangers:
                action = left  # If left is legal and safe we turn left
            else:
                if heading in legal and heading not in allDangers:
                    action = heading  # current direction is safe and valid so keep moving
                elif right in legal and right not in allDangers:
                    action = Directions.RIGHT[heading]  # If right is legal and safe we turn right
                elif Directions.REVERSE[heading] in legal and Directions.REVERSE[heading] not in allDangers:
                    action = Directions.REVERSE[heading]  # last resort to go back if possible
                else:
                    action = Directions.STOP  # since there are no more legal moves pacman stops
            return action
