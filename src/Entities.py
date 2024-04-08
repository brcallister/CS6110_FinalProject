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
        # TODO we should have all data that the agent needs to track in here, such as type or instance info
