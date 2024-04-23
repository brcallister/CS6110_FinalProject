# =======================
# CS 6110 - Final Project
# =======================

from src.OutputData import draw_image, print_env_to_console, print_stats_to_console

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

    '''
    Runs the full simulation

    env = the environment to run a Simulation on
    returns - the ending state of the environment
    '''
    def runSimulation(self, env):
        if self.outputInitial:
            print_env_to_console(env)
            print_stats_to_console(env)
            draw_image(env, "0_InitialMap.png")

        # Run the full simulation
        for step in range(self.numSteps):
            if not env.agents:
                print(f'Timestep {step + 1}: All {len(self.escapedAgents)} agents exited successfully!')
                return env
            env.runOneTimeStep()
            if self.printFrequency != 0 and step % self.printFrequency == self.printFrequency - 1:
                print_env_to_console(env)
                print_stats_to_console(env)
            if self.graphicFrequency != 0 and step % self.graphicFrequency == self.graphicFrequency - 1:
                draw_image(env, f"{step + 1}_Map.png")
        print(f'After {self.numSteps} timesteps, {len(env.agents)}/{len(env.agents) + len(self.escapedAgents)} agents remain in the building.')
        return env
