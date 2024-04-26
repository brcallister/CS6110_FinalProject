# =======================
# CS 6110 - Final Project
# =======================

import random
import math
from bresenham import bresenham
from src.Entities import Entity, Agent

class Environment:    
	def __init__(self, numRows, numCols, rawLayout):
		self.numRows = numRows
		self.numCols = numCols
		self.agents = []
		self.escapedAgents = []
		self.numTotalConflicts = 0
		self.numTotalSwitches = 0
		self.exits = []
		self.exitSigns = []
		self.map = []
		self.penalty = 1.75  # paper used 1 <= penalty <= 2.5

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
					self.exitSigns.append((i, j))
				row.append(newLocation)
			while len(row) < self.numCols:
				row.append(self.Location([]))
			self.map.append(row)
		while len(self.map) < self.numRows:
			self.map.append([self.Location([]) for _ in range(numRows)])
	
	def findPotentialMoves(self, position):
		# if we want to improve pathing, potentially keep track of agents last locations
		# and don't allow them to move back to previous locations (maybe let them forget previous locations over time if needed)
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
	
	def determineWinner(self, agentList):
		winner = None
		coopPayoff = 0
		betrayPayoff = 0
		losers = []
		# No conflict - there is only one agent
		if len(agentList) == 1:
			winner = agentList[0]
		# Resolve conflict - Multiple agents attempting to enter same location
		else:
			# Dictionary of Agent -> Decision
			agentDecisions = {}
			numCooperators = 0 # M from the paper
			numConflicts = len(agentList)   # N from the paper
			self.numTotalConflicts += numConflicts
			
			for contender in agentList:
				decision = contender.decideCoopOrBetray()
				agentDecisions[contender] = decision
				if decision == 'Cooperate':
					numCooperators += 1
			
			# all of the contenders are cooperators, so they each have equal likelihood of winning
			if numCooperators == numConflicts:
				winProbability = 1 / numCooperators

				# could potentially be no winner because they are too busy telling each other to go ahead first
				random.shuffle(agentList)
				for agent in agentList:
					if random.random() <= winProbability:
						coopPayoff = winProbability
						winner = agent
						break
			# there is one defector, so they win
			elif numConflicts - numCooperators == 1:
				# find the defector
				for contender in agentList:
					if contender.decideCoopOrBetray() == 'Betray':
						betrayPayoff = 1
						winner = contender
						break
			# there are multiple defectors
			elif numConflicts - numCooperators > 1:
				# win with probability 1 / (N - M)^P
				winProbability = 1 / ((numConflicts - numCooperators) ** self.penalty)
				# could potentially be no winner because the betrayers are too busy fighting
				random.shuffle(agentList)
				for contender in agentList:
					# cooperate has 0 probability to win
					if contender.decideCoopOrBetray() == 'Betray':
						if random.random() <= winProbability:
							betrayPayoff = winProbability
							winner = contender
			if winner is None:
				losers = agentList
			else:
				losers = agentList.remove(winner)

		return winner, losers, coopPayoff, betrayPayoff
	
	def lineOfSight(self, agentLocation, goalLocation):
		points = list(bresenham(agentLocation[1], agentLocation[0], goalLocation[1], goalLocation[0]))
		for (x, y) in points:
			if self.map[y][x].isEntityHere([Entity('WALL')]):
				return False
		return True
	
	def findClosestGoal(self, agentLocation, goals):
		minDistance = float('inf')
		closest = None
		for goal in goals:
			dist = math.sqrt((agentLocation[0] - goal[0])**2 + (agentLocation[1] - goal[1])**2)
			if dist < minDistance:
				closest = goal
				minDistance = dist
		return closest

	def runOneTimeStep(self):
		moves = {}
		winnerIdList = []
		losersList = []
		# Loop through agents, let each figure out where they want to move
		for agent in self.agents:
			agentPosition = agent.currentLocation
			# Check to see if we can see any exits
			exitsFound = []
			for exit in self.exits:
				if(self.lineOfSight(agentPosition, exit)):
					exitsFound.append(exit)
			if len(exitsFound) > 0:
				# Find the closets one we can see
				closestExit = self.findClosestGoal(agentPosition, exitsFound)
				if closestExit is not None:
					if (len(agent.goals) == 0):
						agent.goals.append(closestExit)
					elif(closestExit != agent.goals[-1]):
						agent.goals.append(closestExit)
			else:
				# If we can't find any exits, look for exit signs
				exitSignsFound = []
				for exitSign in self.exitSigns:
					if(self.lineOfSight(agentPosition, exitSign)):
						exitSignsFound.append(exitSign)
				if len(exitSignsFound) > 0:
					# Find the closets one we can see
					closestExitSign = self.findClosestGoal(agentPosition, exitSignsFound)
					if closestExitSign is not None:
						if (len(agent.goals) == 0):
							agent.goals.append(closestExitSign)
						elif(closestExitSign != agent.goals[-1]):
							agent.goals.append(closestExitSign)
				
			# If we can't see anything
			# TODO: Have agent move closer to another nearyby agent because of herd mentality
			
			potentialMoves = self.findPotentialMoves(agentPosition)
			
			agentPickedMove = agent.pickDesiredLocation(potentialMoves)
			agent.desiredLocation = agentPickedMove
			if agentPickedMove is not None:
				if agentPickedMove in moves:
					moves[agentPickedMove].append(agent)
				else:
					moves[agentPickedMove] = [agent]
		
		# Loop through our moves, resolve each conflict per move and pick agent to actually move
		for location, agentList in moves.items():
			winner, losers, coopPayoff, betrayPayoff = self.determineWinner(agentList)
			if losers is not None:
				losersList.extend(losers)
			if winner == None:
				break
			winnerIdList.append(winner.id)

			# Add the winner to new location (we MUST do this first, or the reference is killed)
			self.map[location[0]][location[1]].thingsHere.append(winner)
			# Remove the winner from their old location
			self.map[winner.currentLocation[0]][winner.currentLocation[1]].thingsHere.remove(winner)
			# Now update the winner's internal location
			winner.currentLocation = location

			# Remove agents that have successfully reached the exit
			if winner.currentLocation in self.exits:
				self.map[winner.currentLocation[0]][winner.currentLocation[1]].thingsHere.remove(winner)
				self.escapedAgents.append(winner)
				self.agents.remove(winner)

		# Give all non-winning agents a chance to swap their type
		for agent in losersList:
			self.numTotalSwitches += agent.changeRolesIfDesired(coopPayoff, betrayPayoff)

	class Location:
		def __init__(self, entitiesHere):
			self.thingsHere = entitiesHere

		def isEntityHere(self, thingsToFind):
			for thing in self.thingsHere:
				for entity in thingsToFind:
					if thing.type == entity.type:
						return True
			return False
