# =======================
# CS 6110 - Final Project
# =======================

import random
import copy

from src.Entities import Entity
from src.Entities import Agent

class Environment:    
	def __init__(self, numRows, numCols, rawLayout):
		self.numRows = numRows
		self.numCols = numCols
		self.agents = []
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
					exits.append([i, j])
				# Agent B
				elif rawLayout[i][j] == 'b':
					newAgent = Agent('AgentBetray', agentId)
					newLocation = self.Location([newAgent])
					self.agents.append(newAgent)
					agentId += 1
				# Agent C
				elif rawLayout[i][j] == 'c':
					newAgent = Agent('AgentCooperate', agentId)
					newLocation = self.Location([newAgent])
					self.agents.append(newAgent)
					agentId += 1
				# TODO - add additional items here
				row.append(newLocation)
			while len(row) < numRows:
				row.append(self.Location([]))
			fullMap.append(row)
		while len(fullMap) < numCols:
			fullMap.append([self.Location([]) for _ in range(numRows)])

		self.map = fullMap
		self.exits = exits
	
	def findPotentialMoves(self, position):
		maxRows = len(self.map)
		maxCols = len(self.map[0])
		agentX = position[0]
		agentY = position[1]
		potentialMoves = []
		# Find all suitable spaces an Agent can move to
		for i in range(max(agentX-1, 0), min(agentX+2, maxRows)):
			for j in range(max(agentY-1, 0), min(agentY+2, maxCols)):
				if i == agentX and j == agentY:
					continue
				potentialLocation = self.Location(self.map[i][j])
				# If there is not another agent or a wall, that location is available to move to.
				if not potentialLocation.isEntityHere([[Entity('AgentBetray')], [Entity('AgentCooperate')], [Entity('WALL')]]):
					potentialMoves.append(self.map[i][j])
		
		return potentialMoves
	
	def runOneTimeStep(self):
		potentialMap = copy.deepcopy(self.map)
		for agent in self.agents:
			# Find current empty spaces
			agentPosition = agent.currentLocation
			potentialMoves = self.findPotentialMoves(agentPosition)
			agentPickedMove = agent.pickDesiredLocation(potentialMap, self.exits)
		# TODO give all agents a chance to move
		pass

	class Location:
		def __init__(self, entitiesHere):
			self.thingsHere = entitiesHere

		def isEntityHere(self, thingToFind):
			for thing in self.thingsHere:
				if thing.type == thingToFind:
					return True
			return False


