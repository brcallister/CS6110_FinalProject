# =======================
# CS 6110 - Final Project
# =======================

class Entity:
    def __init__(self, entityType):
        self.type = entityType

class Agent(Entity):
    def __init__(self, entityType, id):
        super().__init__(entityType)
        self.id = id
        self.currentLocation = []      # [x,y]
        self.desiredLocation = []      # [x,y] of the location they want to move to
        self.familiarityWithExit = 10  # TODO: figure out how this actually works
        self.numberTimesNotMoved = 0

    def pickDesiredLocation(self, environment):
        # based off of the environment
        # can only move to a currently empty location
        # want to move towards the exit
        pass

    def changeRoles(self):
        # if they haven't moved after a certain number of times, switch from
        # cooperate to betray
        # use the formulas in the paper
        pass
