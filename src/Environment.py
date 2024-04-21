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
				# If there is not another agent or a wall, that location is available to move to.
				if not self.map[i][j].isEntityHere([[Entity('AgentBetray')], [Entity('AgentCooperate')], [Entity('WALL')]]):
					potentialMoves.append((i, j))
		
		return potentialMoves
	
	def runOneTimeStep(self):
		potentialMap = copy.deepcopy(self.map)
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
				agent.currentLocation = location
				agent.numberTimesNotMoved = 0
			else:
				# TODO: Figure out conflict
				pass
			if agent.currentLocation in self.exits:
				self.escapedAgents.append(agent)
				self.agents.remove(agent) # TODO make sure this works as expected
		
		# Loop through the actual map and update agent locations
		


	class Location:
		def __init__(self, entitiesHere):
			self.thingsHere = entitiesHere

		def isEntityHere(self, thingsToFind):
			for ent in thingsToFind:
				for thing in self.thingsHere:
					if thing.type == ent:
						return True
			return False


