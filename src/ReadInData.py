# =======================
# CS 6110 - Final Project
# =======================

import os

from src.Environment import Environment

def read_in_data(filename):
    if not os.path.isfile(filename):
        print(f"Error: Input file '{filename}' does not exist.")
        print("Please make sure the file exists and try again.")
        exit(1)

    print('TODO build the environment from file, then return the env object')
    return None
