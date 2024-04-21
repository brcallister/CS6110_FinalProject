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
		fullMap = []
		exits = []

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
					exits.append((i, j))
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
				# TODO - add additional items here
				row.append(newLocation)
			while len(row) < self.numCols:
				row.append(self.Location([]))
			fullMap.append(row)
		while len(fullMap) < self.numRows:
			fullMap.append([self.Location([]) for _ in range(numRows)])

		self.map = fullMap
		self.exits = exits
	
	def findPotentialMoves(self, position):
		agentX, agentY = position[1], position[0]
		potentialMoves = []
		# Find all suitable spaces an Agent can move to
		for i in range(max(agentX-1, 0), min(agentX+2, self.numCols)):
			for j in range(max(agentY-1, 0), min(agentY+2, self.numRows)):
				if i == agentX and j == agentY:
					continue
				# If there is not another agent or a wall, that location is available to move to.
				if not self.map[j][i].isEntityHere([Entity('AgentBetray'), Entity('AgentCooperate'), Entity('WALL')]):
					potentialMoves.append((j, i))
		return potentialMoves
	
	def runOneTimeStep(self):
		moves = {}
		for agent in self.agents:
			# Find current empty spaces
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
			# There is only one agent, so no conflict
			if len(agentList) == 1:
				agent = agentList[0]
				self.map[agent.currentLocation[0]][agent.currentLocation[1]].thingsHere.remove(agent)
				agent.currentLocation = location
				self.map[agent.currentLocation[0]][agent.currentLocation[1]].thingsHere.append(agent)
				agent.numberTimesNotMoved = 0
			else:
				# TODO: Figure out conflict
				pass
			if agent.currentLocation in self.exits:
				self.map[agent.currentLocation[0]][agent.currentLocation[1]].thingsHere.remove(agent)
				self.escapedAgents.append(agent)
				self.agents.remove(agent)

	class Location:
		def __init__(self, entitiesHere):
			self.thingsHere = entitiesHere

		def isEntityHere(self, thingsToFind):
			for thing in self.thingsHere:
				for entity in thingsToFind:
					if thing.type == entity.type:
						return True
			return False


