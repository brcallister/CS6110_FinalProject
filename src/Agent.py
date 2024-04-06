# =======================
# CS 6110 - Final Project
# =======================

from src.Entitiy import Entity

class Agent(Entity):
    def __init__(self, entityType, id):
        super().__init__(entityType)
        self.id = id
        print('TODO we should have all data that the agent needs to track in here, such as type or instance info')
