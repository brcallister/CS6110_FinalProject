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

	def calculateSF(self, location, exit):
		sf = 1.0/(math.sqrt((exit[0] - location[0])**2 + (exit[1] - location[1])**2))
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
				if (move[0], move[1]) in movementProbs:
					if prob > movementProbs[(move[0], move[1])]:
						movementProbs[(move[0], move[1])] = prob
				else:
					movementProbs[(move[0], move[1])] = prob

		# TODO: We may still want to just swap to this
		chosenMove = max(movementProbs, key=movementProbs.get)
		
		# Pick a move based on the calculated probabilities
		# moves, probs = zip(*movementProbs.items())
		# Apply an exponent function on the probabilities so better decisions are more heavily weighted
		# probs = [x ** 32 for x in probs]
		# Rescale to add to 100 so the probabilities are easier to debug
		# probs = [x / sum(probs) * 100 for x in probs]
		# Choose a move randomly based on the probabilities
		# chosenMove = random.choices(moves, weights=probs, k=1)[0]
		return chosenMove
	
	# returns 1 if switched, 0 if not
	def changeRolesIfDesired(self, coopPayoff, betrayPayoff):
		d = 3  # inertia (this wasn't specified in the paper)
		m_x = 0
		m_y = 0
		if self.type == 'AgentCooperate':
			m_x = d * coopPayoff  # formula 3 from paper
			m_y = betrayPayoff    # formula 4 from paper
		else:
			m_x = d * betrayPayoff  # formula 3 from paper
			m_y = coopPayoff        # formula 4 from paper
		probabilitySwitchType = (1 / (1 + (math.exp(((m_x - m_y) / 0.1)))))  # formula 5 from paper

		if random.random() <= probabilitySwitchType:
			if self.type == 'AgentBetray':
				self.type = 'AgentCooperate'
			elif self.type == 'AgentCooperate':
				self.type = 'AgentBetray'
			return 1
		return 0
	
	def decideCoopOrBetray(self):
		# Right now, they will just decide based off of their agent type
		if self.type == "AgentCooperate":
			return "Cooperate"
		return "Betray"
