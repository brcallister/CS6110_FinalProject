# =======================
# CS 6110 - Final Project
# =======================

import math
import random

class Entity:
	def __init__(self, entityType):
		self.type = entityType

class Agent(Entity):
	def __init__(self, entityType, id, startLocation):
		super().__init__(entityType)
		self.id = id
		self.currentLocation = startLocation      # [x,y]
		self.desiredLocation = []      # [x,y] of the location they want to move to
		self.familiarityWithExit = 10  # TODO: figure out how this actually works
		self.numberTimesNotMoved = 0

	def calculateSF(self, location, exit):
		sf = 1/(math.sqrt((exit[0] - location[0])**2 + (exit[1] - location[1])**2))
		return sf

	def pickDesiredLocation(self, potentialMoves, exits):
		if len(potentialMoves) == 0:
			return None
		
		movementProbs = {}
		# For every exit that exists, we need to find what exit the agent will move toward
		for exit in exits:
			# Find the sum of all SF values for this potential move (3 figure 2 in paper)
			sumSf = 0
			for move in potentialMoves:
				if move == exit:
					return (move[0], move[1])
				sumSf += math.exp(self.familiarityWithExit * self.calculateSF(move, exit))
			# Now calculate the probability of making that move (3 figure 2 in paper)
			for move in potentialMoves:
				moveSf = self.calculateSF(move, exit)
				prob = math.exp(self.familiarityWithExit*moveSf) / sumSf
				# using a tuple as a key will allow us to konw what move towards what exit is best for our agent
				movementProbs[(move[0], move[1])] = prob

		# TODO: We may still want to just swap to this
		# bestMove = max(movementProbs, key=movementProbs.get)
		
		# Pick a move based on the calculated probabilities
		moves, probs = zip(*movementProbs.items())
		# Apply an exponent function on the probabilities so better decisions are more heavily weighted
		probs = [x ** 32 for x in probs]
		# Rescale to add to 100 so the probabilities are easier to debug
		probs = [x / sum(probs) * 100 for x in probs]
		# Choose a move randomly based on the probabilities
		chosenMove = random.choices(moves, weights=probs, k=1)[0]
		return chosenMove
	
	def changeRolesIfDesired(self):
		# TODO: use the formulas in the paper
		if self.numberTimesNotMoved >= 10:
			if self.type == 'AgentBetray':
				self.type = 'AgentCooperate'
			elif self.type == 'AgentCooperate':
				self.type = 'AgentBetray'
	
	def decideCoopOrBetray(self):
		# Right now, they will just decide based off of their agent type
		if self.type == "AgentCooperate":
			return "Cooperate"
		return "Betray"
