# =======================
# CS 6110 - Final Project
# =======================

import os

def read_in_data(filename):
    lines = []
    if not os.path.isfile(filename):
        print(f"Error: Input file '{filename}' does not exist.")
        print("Please make sure the file exists and try again.")
        exit(1)

    with open(filename, 'r') as file:
        lines = [line.strip() for line in file.readlines() if line.strip()]
    return lines
