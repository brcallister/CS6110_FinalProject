# =======================
# CS 6110 - Final Project
# =======================

from src.Environment import Environment
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
            draw_image(env, "TODO_Initial.png")

        # Run the full simulation
        for step in range(self.numSteps):
            env.runOneTimeStep()
            if self.printFrequency != 0 and step % self.printFrequency == self.printFrequency - 1:
                print_env_to_console(env)
                print_stats_to_console(env)
            if self.graphicFrequency != 0 and step % self.graphicFrequency == self.graphicFrequency - 1:
                draw_image(env, "TODO_stepNum.png")

        return env