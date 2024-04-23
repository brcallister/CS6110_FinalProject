# =======================
# CS 6110 - Final Project
# =======================

import random

from src.Entities import Entity, Agent

class Environment:    
	def __init__(self, numRows, numCols, rawLayout):
		self.numRows = numRows
		self.numCols = numCols
		self.agents = []
		self.escapedAgents = []
		self.numTotalConflicts = 0
		self.exits = []
		self.map = []

		# Set up map layout
		agentId = 0
		for i in range(len(rawLayout)):
			row = []
			for j in range(len(rawLayout[i])):
				# Defaults to empty location
				newLocation = self.Location([])
				# Wall
				if rawLayout[i][j] == 'X':
					newLocation = self.Location([Entity('WALL')])
				# Exit
				elif rawLayout[i][j] == 'O':
					newLocation = self.Location([Entity('EXIT')])
					self.exits.append((i, j))
				# Agent B
				elif rawLayout[i][j] == 'b':
					newAgent = Agent('AgentBetray', agentId, (i,j))
					newLocation = self.Location([newAgent])
					self.agents.append(newAgent)
					agentId += 1
				# Agent C
				elif rawLayout[i][j] == 'c':
					newAgent = Agent('AgentCooperate', agentId, (i,j))
					newLocation = self.Location([newAgent])
					self.agents.append(newAgent)
					agentId += 1
				# Light
				elif rawLayout[i][j] == 'L':
					newLocation = self.Location([Entity('LIGHT')])
				# Exit Sign
				elif rawLayout[i][j] == 'E':
					newLocation = self.Location([Entity('EXIT_SIGN')])
				row.append(newLocation)
			while len(row) < self.numCols:
				row.append(self.Location([]))
			self.map.append(row)
		while len(self.map) < self.numRows:
			self.map.append([self.Location([]) for _ in range(numRows)])
	
	def findPotentialMoves(self, position):
		agentX, agentY = position[1], position[0]
		potentialMoves = []
		# Find all suitable spaces an Agent can move to
		for i in range(max(agentX-1, 0), min(agentX+2, self.numCols)):
			for j in range(max(agentY-1, 0), min(agentY+2, self.numRows)):
				if i == agentX and j == agentY:
					continue
				# If there is not another agent or a wall, that location is available to move to.
				if not self.map[j][i].isEntityHere([Entity('AgentBetray'), Entity('AgentCooperate'), Entity('WALL'), Entity('EXIT_SIGN')]):
					potentialMoves.append((j, i))
		return potentialMoves
	
	def runOneTimeStep(self):
		moves = {}
		# Loop through agents, let each figure out where they want to move
		for agent in self.agents:
			agentPosition = agent.currentLocation
			potentialMoves = self.findPotentialMoves(agentPosition)
			agentPickedMove = agent.pickDesiredLocation(potentialMoves, self.exits)
			agent.desiredLocation = agentPickedMove
			if agentPickedMove in moves:
				moves[agentPickedMove].append(agent)
			else:
				moves[agentPickedMove] = [agent]
		
		# Loop through our moves, resolve each conflict per move and pick agent to actually move
		for location, agentList in moves.items():
			winner = None
			# No conflict - there is only one agent
			if len(agentList) == 1:
				winner = agentList[0]
			# Resolve conflict - Multiple agents attempting to enter same location
			else:
				# Dictionary of Agent -> Decision
				agentDecisions = {}
				for contender in agentList:
					decision = contender.decideCoopOrBetray()
					agentDecisions[contender] = decision
				# TODO: Non-randomly figure out winner
				winner = random.choice(list(agentDecisions.keys()))
				
			# Add the winner to new location (we MUST do this first, or the reference is killed)
			self.map[location[0]][location[1]].thingsHere.append(winner)
			# Remove the winner from their old location
			self.map[winner.currentLocation[0]][winner.currentLocation[1]].thingsHere.remove(winner)
			# Now update the winner's internal location
			winner.currentLocation = location
			# Reset number of times since winner last moved
			winner.numberTimesNotMoved = 1

			# Remove agents that have successfully reached the exit
			if winner.currentLocation in self.exits:
				self.map[winner.currentLocation[0]][winner.currentLocation[1]].thingsHere.remove(winner)
				self.escapedAgents.append(winner)
				self.agents.remove(winner)

		# Give all agents a chance to swap their type
		for agent in self.agents:
			agent.changeRolesIfDesired()

	class Location:
		def __init__(self, entitiesHere):
			self.thingsHere = entitiesHere

		def isEntityHere(self, thingsToFind):
			for thing in self.thingsHere:
				for entity in thingsToFind:
					if thing.type == entity.type:
						return True
			return False
