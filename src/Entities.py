# =======================
# CS 6110 - Final Project
# =======================

import math

class Entity:
	def __init__(self, entityType):
		self.type = entityType

class Agent(Entity):
	def __init__(self, entityType, id):
		super().__init__(entityType)
		self.id = id
		self.currentLocation = []      # [x,y]
		self.desiredLocation = []      # [x,y] of the location they want to move to
		self.familiarityWithExit = 10  # TODO: figure out how this actually works
		self.numberTimesNotMoved = 0

	def calculateSF(self, location, exit):
		sf = 1/(math.sqrt((exit[0] - location[0])**2 + (exit[1] - location[1])**2))
		return sf

	def pickDesiredLocation(self, potentialMoves, exits):
		if len(potentialMoves) == 0:
			return
		movementProbs = {}
		# For every exit that exists, we need to find what exit the agent will move toward
		for exit in exits:
			# Find the sum of all SF values for this potential move (3 figure 2 in paper)
			sumSf = 0
			for move in potentialMoves:
				sumSf += math.exp(self.familiarityWithExit * self.calculateSF(move, exit))
			# Now calculate the probability of making that move (3 figure 2 in paper)
			for move in potentialMoves:
				moveSf = self.calculateSF(move, exit)
				prob = math.exp(self.familiarityWithExit*moveSf) / sumSf
				# using a tuple as a key will allow us to konw what move towards what exit is best for our agent
				movementProbs[(move[0], move[1], exit[0], exit[1])] = prob
		
		# Now that we have all probabilites, we need to find the best one.
		bestMove = max(movementProbs, key=movementProbs.keys)
		return bestMove

	def changeRoles(self):
		# if they haven't moved after a certain number of times, switch from
		# cooperate to betray
		# use the formulas in the paper
		pass
