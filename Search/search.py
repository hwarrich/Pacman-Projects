# search.py
# ---------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print "Start:", problem.getStartState()
    print "Is the start a goal?", problem.isGoalState(problem.getStartState())
    print "Start's successors:", problem.getSuccessors(problem.getStartState())
    """
     # get start state
    startState = problem.getStartState()
    # if node state is goal return nothing
    if problem.isGoalState(startState):
        return []

    # make frontier, explored set, initial actions, and push
    # startState with initial actions to frontier as tuple
    frontier = util.PriorityQueue()
    explored = []
    initActions = []
    frontier.push((startState, initActions, 0), 0)

    # while the frontier is not empty
    # pop off state and associated actions
    while (True):
        # if empty frontier return failure
        if (frontier.isEmpty()):
            raise Exception('Failure')
        myState, actions, cost = frontier.pop()
        # if goal state return actions to get to goal state
        if (problem.isGoalState(myState)):
            return actions
        # if not explored add to explored set
        if (myState not in explored):
            explored.append(myState)
            # for all sucessor states, add state, action, and final cost to frontier
            # use final cost as priority
            for child in problem.getSuccessors(myState):
                newNode, newAction, newStepCost = child
                finalAction = actions + [newAction]
                finalCost = cost -1
                if (newNode not in explored):
                    frontier.push((newNode, finalAction, finalCost), finalCost)
    # util.raiseNotDefined()

def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
     # get start state
    startState = problem.getStartState()
    # if node state is goal return nothing
    if problem.isGoalState(startState):
        return []

    # make frontier, explored set, initial actions, and push
    # startState with initial actions to frontier as tuple
    frontier = util.PriorityQueue()
    explored = []
    initActions = []
    frontier.push((startState, initActions, 0), 0)

    # while the frontier is not empty
    # pop off state and associated actions
    while (True):
        # if empty frontier return failure
        if (frontier.isEmpty()):
            raise Exception('Failure')
        myState, actions, cost = frontier.pop()
        # if goal state return actions to get to goal state
        if (problem.isGoalState(myState)):
            return actions
        # if not explored add to explored set
        if (myState not in explored):
            explored.append(myState)
            # for all sucessor states, add state, action, and final cost to frontier
            # use final cost as priority
            for child in problem.getSuccessors(myState):
                newNode, newAction, newStepCost = child
                finalAction = actions + [newAction]
                finalCost = cost + 1
                if (newNode not in explored):
                    frontier.push((newNode, finalAction, finalCost), finalCost)

def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    # get start state
    startState = problem.getStartState()
    # if node state is goal return nothing
    if problem.isGoalState(startState):
        return []

    # make frontier, explored set, initial actions, and push
    # startState with initial actions to frontier as tuple
    frontier = util.PriorityQueue()
    explored = []
    initActions = []
    frontier.push((startState, initActions, 0), 0)

    # while the frontier is not empty
    # pop off state and associated actions
    while (True):
        # if empty frontier return failure
        if (frontier.isEmpty()):
            raise Exception('Failure')
        myState, actions, cost = frontier.pop()
        # if goal state return actions to get to goal state
        if (problem.isGoalState(myState)):
            return actions
        # if not explored add to explored set
        if (myState not in explored):
            explored.append(myState)
            # for all sucessor states, add state, action, and final cost to frontier
            # use final cost as priority
            for child in problem.getSuccessors(myState):
                newNode, newAction, newStepCost = child
                finalAction = actions + [newAction]
                finalCost = cost + newStepCost
                if (newNode not in explored):
                    frontier.push((newNode, finalAction, finalCost), finalCost)

    # util.raiseNotDefined()

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    # get start state
    startState = problem.getStartState()
    # if node state is goal return nothing
    if problem.isGoalState(startState):
        return []

    # make frontier, explored set, initial actions, and push
    # startState with initial actions to frontier as tuple
    frontier = util.PriorityQueue()
    explored = []
    initActions = []
    frontier.push((startState, initActions, 0), 0)

    # while the frontier is not empty
    # pop off state and associated actions
    while (True):
        # if empty frontier return failure
        if (frontier.isEmpty()):
            raise Exception('Failure')
        myState, actions, cost = frontier.pop()
        # if goal state return actions to get to goal state
        if (problem.isGoalState(myState)):
            return actions
        # if not explored add to explored set
        if (myState not in explored):
            explored.append(myState)
            # for all sucessor states, add state, action, and final cost to frontier
            # use final cost as priority
            for child in problem.getSuccessors(myState):
                newNode, newAction, newStepCost = child
                finalAction = actions + [newAction]
                hcost = heuristic(newNode, problem)
                finalCost = cost + newStepCost + hcost
                if (newNode not in explored):
                    frontier.push((newNode, finalAction, cost + newStepCost), finalCost)
    # util.raiseNotDefined()


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
