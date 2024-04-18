# =======================
# CS 6110 - Final Project
# =======================

import os
import matplotlib.pyplot as plt

OUTPUT_DIR = 'output'
if not os.path.exists('output'):
    os.makedirs('output')

def draw_image(environment, filename):
    ax = plt.gca()

    # Loop through array
    for row_index, row in enumerate(environment.map[::-1]):
        for col_index, location in enumerate(row):
            for thing in location.thingsHere:
                color = 'white'
                marker = 'o'
                if thing.type == 'WALL':
                    color = 'black'
                    marker = 's'
                elif thing.type == 'EXIT':
                    color = 'blue'
                    marker = 'o'
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

def print_env_to_console(environment):
    print('Current Enviroment:')
    # Loop through array
    for row in environment.map:
        rowBuffer = ''
        for location in row:
            if location.isEntityHere('WALL'):
                rowBuffer += 'X'
            elif location.isEntityHere('EXIT'):
                rowBuffer += 'O'
            elif location.isEntityHere('AgentBetray'):
                rowBuffer += 'b'
            elif location.isEntityHere('AgentCooperate'):
                rowBuffer += 'c'
            else:
                rowBuffer += ' '
        print(rowBuffer)
    print()

def print_stats_to_console(environment):
    # TODO: maybe print additional stats to console?
    # print('Current Stats: ')
    # print('Agents safe: ')
    # print('Agents still in building: ')
    # print('Time taken: ')
    pass
