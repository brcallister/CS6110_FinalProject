# =======================
# CS 6110 - Final Project
# =======================

import os

INPUT_DIR = 'input'

'''
Reads in a file from the 'input' folder, and cleans it up.
Expects the first line to be the dimensions of the map [row, col]
Then expects the map data after that.

Empty lines are ignored.
Extra whitespace before/after the actual map is ignored.
Returns numRows, numCols, the array of all other data
'''
def read_in_data(filename):
    filepath = os.path.join(INPUT_DIR, filename)
    lines = []
    if not os.path.isfile(filepath):
        print(f"Error: Input file '{filepath}' does not exist.")
        print("Please make sure the file exists and try again.")
        exit(1)

    with open(filepath, 'r') as file:
        lines = [line.strip() for line in file.readlines() if line.strip()]
    dim = lines[0].split(' ')
    return int(dim[0]), int(dim[1]), lines[1:]
