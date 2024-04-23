# =======================
# CS 6110 - Final Project
# =======================

import os
import matplotlib.pyplot as plt

from src.Entities import Entity, Agent

OUTPUT_DIR = 'output'
if not os.path.exists('output'):
    os.makedirs('output')

def draw_image(environment, filename):
    ax = plt.gca()
    ax.set_facecolor('darkgray')
    plt.gcf().set_facecolor('darkgray')

    # Loop through array
    for row_index, row in enumerate(environment.map[::-1]):
        for col_index, location in enumerate(row):
            # Check lights first, so they can always be drawn first
            if location.isEntityHere([Entity('LIGHT')]):
                ax.plot(col_index, row_index, marker='s', color='yellow')
            for thing in location.thingsHere:
                color = 'white'
                marker = 'o'
                if thing.type == 'WALL':
                    color = 'black'
                    marker = 's'
                elif thing.type == 'EXIT':
                    color = 'blue'
                    marker = 'o'
                elif thing.type == 'EXIT_SIGN':
                    color = 'green'
                    marker = 'h'
                elif thing.type == 'AgentBetray':
                    color = 'red'
                    marker = 'x'
                elif thing.type == 'AgentCooperate':
                    color = 'green'
                    marker = 'x'
                # Plot a point at current location with determined color
                ax.plot(col_index, row_index, marker=marker, color=color)

    ax.set_title(filename, fontsize=10, fontweight='bold')
    plt.gca().set_yticks(ax.get_yticks())
    plt.gca().set_yticklabels(ax.get_yticklabels()[::-1])

    # Show plot
    # plt.show()

    plt.savefig(os.path.join(OUTPUT_DIR, filename))
    plt.close()

def print_env_to_console(environment, timestep):
    print(f'Current Environment (timestep: {timestep + 1}):')
    # Loop through array
    for row in environment.map:
        rowBuffer = ''
        for location in row:
            if location.isEntityHere([Entity('WALL')]):
                rowBuffer += 'X'
            elif location.isEntityHere([Entity('EXIT')]):
                rowBuffer += 'O'
            elif location.isEntityHere([Entity('EXIT_SIGN')]):
                rowBuffer += 'E'
            elif location.isEntityHere([Entity('AgentBetray')]):
                rowBuffer += 'b'
            elif location.isEntityHere([Entity('AgentCooperate')]):
                rowBuffer += 'c'
            elif location.isEntityHere([Entity('LIGHT')]):
                rowBuffer += 'L'
            else:
                rowBuffer += ' '
        print(rowBuffer)
    print()

def print_stats_to_console(env, timestep):
    if timestep == 0:
        print('Initial Setup:')
        numExits = 0
        numSigns = 0
        numLights = 0
        numCoopAgents = 0
        numBetrayAgents = 0
        for row in env.map:
            for location in row:
                for entity in location.thingsHere:
                    if entity.type == "EXIT":
                         numExits += 1
                    elif entity.type == "EXIT_SIGN":
                         numSigns += 1
                    elif entity.type == "LIGHT":
                         numLights += 1
                    elif entity.type == "AgentCooperate":
                         numCoopAgents += 1
                    elif entity.type == "AgentBetray":
                         numBetrayAgents += 1 
        print(f'\tNumber of Exits: {numExits}')
        print(f'\tNumber of Exit Signs: {numSigns}')
        if numLights != 0:
            print(f'\tNumber of Lights: {numLights}')
        print(f'\tNumber of Agents (Cooperative): {numCoopAgents}')
        print(f'\tNumber of Agents (Betrayers): {numBetrayAgents}')
    else:
        print(f'Current Stats (timestep {timestep + 1}):')
        print(f'\tTotal Number of Conflicts: {env.numTotalConflicts}')
        print(f'\tEscaped Agents: {len(env.escapedAgents)}')
        print(f'\tTotal Agents:   {len(env.agents) + len(env.escapedAgents)}')
        numCoopAgents = 0
        numBetrayAgents = 0
        for agent in env.escapedAgents:
            if agent.type == "AgentCooperate":
                numCoopAgents += 1
            elif agent.type == "AgentBetray":
                numBetrayAgents += 1
        print(f'\tNumber of Escaped Agents (Cooperative): {numCoopAgents}')
        print(f'\tNumber of Escaped Agents (Betrayers):   {numBetrayAgents}')
    print()
