# =======================
# CS 6110 - Final Project
# =======================

import random

from src.Entitiy import Entity
from src.Agent import Agent

class Environment:    
    def __init__(self, rawLayout, numAgents):
        fullMap = []

        # Set up map layout
        for line in rawLayout:
            row = []
            for char in line:
                # Defaults to empty location
                newLocation = self.Location([])
                # Wall
                if char == 'X':
                    newLocation = self.Location(Entity('WALL'))
                # Exit
                elif char == 'O':
                    newLocation = self.Location(Entity('EXIT'))
                # TODO - add additional items here
                row.append(newLocation)
            fullMap.append(row)

        # Add agents to the world
        for i in range(numAgents):
            # TODO place agents throughout empty spaces
            pass

        self.map = fullMap
    
    def runOneTimeStep(self):
        # TODO give all agents a chance to move
        pass

    class Location:
        def __init__(self, entitiesHere):
            self.thingsHere = entitiesHere
