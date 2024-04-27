# =======================
# CS 6110 - Final Project
# =======================

from src.OutputData import draw_image, draw_graph, print_env_to_console, print_stats_to_console

class Simulation:
    '''
    Constructor for the Simulation class

    numSteps = the number of time steps the simulation should run for
    printFreq = after how many time steps to print information to the console - 0 means never
    graphicFreq = after how many time steps to output information via graphics - 0 means never
    outputInitial = whether to output information about the starting state
    '''
    def __init__(self, numSteps, printFreq, graphicFreq, outputInitial=True):
        self.numSteps = numSteps
        self.printFrequency = printFreq
        self.graphicFrequency = graphicFreq
        self.outputInitial = outputInitial
        self.numAgentsEscaped = []
        self.numAgentsEscapedType = []

    '''
    Writes all stored data out to graphs
    '''
    def outputAllGraphs(self):
        draw_graph(self.numAgentsEscaped, 
                           ['Agents Escaped over Time', "Agents still in Building", "Escaped Agents"],
                           "EscapedAgentNumbers.png")
        draw_graph(self.numAgentsEscapedType, 
                           ['Agents Escaped by Type over Time', "Escaped Agents (Cooperative)", "Escaped Agents (Betrayers)"],
                           "EscapedAgentTypes.png")

    '''
    Runs the full simulation

    env = the environment to run a Simulation on
    returns - the ending state of the environment
    '''
    def runSimulation(self, env):
        if self.outputInitial:
            print_env_to_console(env, 0)
            print_stats_to_console(env, 0)
            draw_image(env, "0_InitialMap.png")

        # Run the full simulation
        for step in range(self.numSteps):
            if not env.agents:
                print_stats_to_console(env, step)
                print(f'Timestep {step + 1}: All {len(env.escapedAgents)} agents exited successfully!')
                self.outputAllGraphs()
                return env
            
            # Run a single time step in the simulation
            env.runOneTimeStep()

            # Record data for graphs later
            numAgentsStillInBuilding = len(env.agents)
            numAgentsEscaped = len(env.escapedAgents)
            self.numAgentsEscaped.append((numAgentsStillInBuilding, numAgentsEscaped))
            numCoopEscaped = sum(1 for agent in env.escapedAgents if agent.type == "AgentCooperate")
            numBetrayEscaped = sum(1 for agent in env.escapedAgents if agent.type == "AgentBetray")
            self.numAgentsEscapedType.append((numCoopEscaped, numBetrayEscaped))

            # Print according to how often the user specified
            if self.printFrequency != 0 and step % self.printFrequency == self.printFrequency - 1:
                print_stats_to_console(env, step)
                print_env_to_console(env, step)
            if self.graphicFrequency != 0 and step % self.graphicFrequency == self.graphicFrequency - 1:
                draw_image(env, f"{step + 1}_Map.png")
        print_stats_to_console(env, step)
        print(f'After {self.numSteps} timesteps, {len(env.agents)}/{len(env.agents) + len(env.escapedAgents)} agents remain in the building.')
        self.outputAllGraphs()
        return env
