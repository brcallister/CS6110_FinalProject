# =======================
# CS 6110 - Final Project
# =======================

import os
from src.ReadInData import read_in_data
from src.Simulation import Simulation
from src.OutputData import draw_image

if __name__ == "__main__":
    # Read environment information in from file
    env = read_in_data(os.path.join("input", "TODO.txt"))

    # Specify the type of simulation to run
    simulation = Simulation()

    # Run the actual simulation
    finalEnv = simulation.runSimulation(env)

    # Output the final world state
    draw_image(finalEnv, 'TODO.png')
