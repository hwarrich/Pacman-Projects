# multiAgents.py
# --------------
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


from util import manhattanDistance
from game import Directions
import random, util

from game import Agent
import math

class ReflexAgent(Agent):
    """
      A reflex agent chooses an action at each choice point by examining
      its alternatives via a state evaluation function.

      The code below is provided as a guide.  You are welcome to change
      it in any way you see fit, so long as you don't touch our method
      headers.
    """


    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {North, South, West, East, Stop}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        if successorGameState.isWin():
            return 10000000000
        if successorGameState.isLose():
            return -10000000000
        ghosts = successorGameState.getGhostPositions()
        toGhosts = 0
        for ghost in ghosts:
            if manhattanDistance(newPos,ghost)<=1:
                toGhosts -= 1000000
            else:
                toGhosts -= math.sqrt(manhattanDistance(newPos,ghost))
        foodList = newFood.asList()
        foodLeft = 10000 * 1 / len(foodList)
        closestFood = manhattanDistance(newPos, foodList[0])
        for food in foodList:
            x = manhattanDistance(newPos, food)
            if x < closestFood:
                closestFood = x
        return successorGameState.getScore() + 10*1/closestFood + foodLeft + toGhosts + newScaredTimes[0]


def scoreEvaluationFunction(currentGameState):
    """
      This default evaluation function just returns the score of the state.
      The score is the same one displayed in the Pacman GUI.

      This evaluation function is meant for use with adversarial search agents
      (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
      This class provides some common elements to all of your
      multi-agent searchers.  Any methods defined here will be available
      to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

      You *do not* need to make any changes here, but you can if you want to
      add functionality to all your adversarial search agents.  Please do not
      remove anything, however.

      Note: this is an abstract class: one that should not be instantiated.  It's
      only partially specified, and designed to be extended.  Agent (game.py)
      is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
      Your minimax agent (question 2)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action from the current gameState using self.depth
          and self.evaluationFunction.

          Here are some method calls that might be useful when implementing minimax.

          gameState.getLegalActions(agentIndex):
            Returns a list of legal actions for an agent
            agentIndex=0 means Pacman, ghosts are >= 1

          gameState.generateSuccessor(agentIndex, action):
            Returns the successor game state after an agent takes an action

          gameState.getNumAgents():
            Returns the total number of agents in the game
        """

        return self.miniMax(gameState, 0)[1]

    def miniMax(self, gameState, dep):
        if (dep == self.depth * gameState.getNumAgents()  or gameState.isWin() or gameState.isLose()):
            return self.evaluationFunction(gameState), 0
        whoseTurn = dep % gameState.getNumAgents()
        if(whoseTurn == 0):
            utilities = []
            for action in gameState.getLegalActions(0):
                utilities.append((self.miniMax(gameState.generateSuccessor(0, action), dep+1)[0], action))
            return max(utilities)

        else:
            utilities = []
            for action in gameState.getLegalActions(whoseTurn):
                utilities.append((self.miniMax(gameState.generateSuccessor(whoseTurn,action), dep+1)[0],action))
            return min(utilities)

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        myTuple = self.alphaBeta(gameState, -1000000000, 1000000000, 0)
        return myTuple[1]

    def alphaBeta(self, gameState, alpha, beta, dep):
        whoseTurn = dep % gameState.getNumAgents()
        if (whoseTurn == 0):
            return self.maxVal(gameState, alpha, beta, dep)
        else:
            return self.minVal(gameState, alpha, beta, dep)

    def maxVal(self, gameState, alpha, beta, dep):
        if (dep == self.depth * gameState.getNumAgents() or gameState.isWin() or gameState.isLose()):
            return self.evaluationFunction(gameState), 0
        v = -1000000000000000
        bestAction = 0
        for action in gameState.getLegalActions(0):
            utility = self.alphaBeta(gameState.generateSuccessor(0, action), alpha, beta, dep + 1)[0]
            if (utility > v):
                v = utility
                bestAction = action
            if (v > beta):
                return v, bestAction
            alpha = max(alpha, v)
        return v, bestAction

    def minVal(self, gameState, alpha, beta, dep):
        if (dep == self.depth * gameState.getNumAgents() or gameState.isWin() or gameState.isLose()):
            return self.evaluationFunction(gameState), 0
        whoseTurn = dep % gameState.getNumAgents()
        v = 1000000000000000
        bestAction = 0
        for action in gameState.getLegalActions(whoseTurn):
            utility = self.alphaBeta(gameState.generateSuccessor(whoseTurn, action), alpha, beta, dep + 1)[0]
            if (utility < v):
                v = utility
                bestAction = action
            if (v < alpha):
                return v, bestAction
            beta = min(beta, v)
        return v, bestAction

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
          Returns the expectimax action using self.depth and self.evaluationFunction

          All ghosts should be modeled as choosing uniformly at random from their
          legal moves.
        """
        myTuple = self.expectiMax(gameState, 0)
        return myTuple[1]

    def expectiMax(self, gameState, dep):
        if (dep == self.depth * gameState.getNumAgents() or gameState.isWin() or gameState.isLose()):
            return self.evaluationFunction(gameState), 0
        whoseTurn = dep % gameState.getNumAgents()
        if (whoseTurn == 0):
            utilities = []
            for action in gameState.getLegalActions(0):
                utilities.append((self.expectiMax(gameState.generateSuccessor(0, action), dep + 1)[0], action))
            return max(utilities)

        else:
            utilities = 0
            for action in gameState.getLegalActions(whoseTurn):
                utilities = utilities + ((1.0 / len(gameState.getLegalActions(whoseTurn))) *
                (self.expectiMax(gameState.generateSuccessor(whoseTurn, action), dep + 1)[0]))
            return utilities, 0

def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: With the exception of if the game state was a win or loss,
      features were multiplied by different values depending on their importance
      and combined linearly. If the game state was a win, the number returned was
      greater than any non-win state would have. If the game state was a win,
      the number returned was less than any non-win state would have. The linear
      combination included the state's score, the distance to the closest piece
      of food, the number of food items left, the distance to the ghosts, and the
      the number of moves that each ghost will remain scared. When the distance to any
      of the ghosts gets down to 1, the distance to the ghosts has the highest priority
      in the linear combination. The number of food items left has the next highest
      priority, then the distance to the closest food, and then the other features.

    """
    pos = currentGameState.getPacmanPosition()
    food = currentGameState.getFood()
    ghostStates = currentGameState.getGhostStates()
    scaredTimes = [ghostState.scaredTimer for ghostState in ghostStates]

    if currentGameState.isWin():
        return 10000000000
    if currentGameState.isWin():
        return -10000000000
    ghosts = currentGameState.getGhostPositions()
    toGhosts = 0
    for ghost in ghosts:
        if manhattanDistance(pos,ghost)<=1:
            toGhosts -= 100000
        else:
            toGhosts -= math.sqrt(manhattanDistance(pos,ghost))
    foodList = food.asList()
    foodLeft = 10000 * 1 / len(foodList)
    closestFood = manhattanDistance(pos, foodList[0])
    for food in foodList:
        x = manhattanDistance(pos, food)
        if x < closestFood:
            closestFood = x
    return currentGameState.getScore() + 10*1/closestFood + foodLeft + toGhosts + scaredTimes[0]



# Abbreviation
better = betterEvaluationFunction

