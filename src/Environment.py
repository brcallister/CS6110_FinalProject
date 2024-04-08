# =======================
# CS 6110 - Final Project
# =======================

import random

from src.Entities import Entity

class Environment:    
    def __init__(self, numRows, numCols, rawLayout, numAgents):
        self.numRows = numRows
        self.numCols = numCols
        fullMap = []

        # TODO - beware, currently this creates a jagged array.
        # TODO - we should either anticipate that or update that in this implementation
        
        # Set up map layout
        for line in rawLayout:
            row = []
            for char in line:
                # Defaults to empty location
                newLocation = self.Location([])
                # Wall
                if char == 'X':
                    newLocation = self.Location([Entity('WALL')])
                # Exit
                elif char == 'O':
                    newLocation = self.Location([Entity('EXIT')])
                # TODO - add additional items here
                row.append(newLocation)
            fullMap.append(row)

        # Add agents to the world
        for i in range(numAgents):
            # TODO place agents throughout valid empty spaces
            pass

        self.map = fullMap
    
    def runOneTimeStep(self):
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


