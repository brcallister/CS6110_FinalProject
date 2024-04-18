# =======================
# CS 6110 - Final Project
# =======================

import random

from src.Entities import Entity

class Environment:    
    def __init__(self, numRows, numCols, rawLayout):
        self.numRows = numRows
        self.numCols = numCols
        fullMap = []

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
                # Agent B
                elif char == 'b':
                    newLocation = self.Location([Entity('AgentBetray')])
                # Agent C
                elif char == 'c':
                    newLocation = self.Location([Entity('AgentCooperate')])
                # TODO - add additional items here
                row.append(newLocation)
            while len(row) < numRows:
                row.append(self.Location([]))
            fullMap.append(row)
        while len(fullMap) < numCols:
            fullMap.append([self.Location([]) for _ in range(numRows)])

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


