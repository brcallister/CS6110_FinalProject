# =======================
# CS 6110 - Final Project
# =======================

import os
from src.ReadInData import read_in_data
from src.Environment import Environment
from src.Simulation import Simulation
from src.OutputData import draw_image

if __name__ == "__main__":
    # Read layout information in from file
    rawLayout = read_in_data(os.path.join("input", "Debug1.txt"))

    # Create full environment according to specs
    env = Environment(rawLayout, numAgents=10)

    # Specify the type of simulation to run
    simulation = Simulation(numSteps=15, printFreq=5, graphicFreq=5, outputInitial=True)

    # Run the actual simulation
    finalEnv = simulation.runSimulation(env)

    # Output the final world state
    draw_image(finalEnv, 'TODO_FinalDebug.png')
