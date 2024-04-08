# CS 6110 - Final Project

TODO

### Table of Contents
- [Setup](README.md#setup)
- [Usage](README.md#usage)
- [Input](README.md#input)
- [Output](README.md#output)
- [Research](README.md#research)

## Setup
#### Dependencies
1. Ensure that Python is installed on your machine. You can download the latest version of Python from the official website: [Python Downloads](https://www.python.org/downloads/).

2. Ensure all third-party dependencies are installed:
    - `pip install matplotlib`

#### Simulation Setup
1. Add desired layout files to the `input` directory
2. Update simulation settings in `Main.py`

## Usage

For best results, run this program from its top-level directory:
`python ./Main.py`

## Input

Input files are expected in the `input` directory, and in the following format:
  - The first line of the file should contain two numbers, separated by a single space. These numbers correspond to the number of rows and columns in the map, respectively. (i.e. `5 8` for a file that has 5 rows and 8 columns)
  - After that, each line will hold the map data:
      - `X` represents a Wall
      - `O` represents an Exit
      - Empty spaces represent locations where agents can freely traverse
  - Extra whitespace or newlines are ignored
  - See [this input file](input/Debug1.txt) for an example

## Output

All persistent output data is placed in the `output` directory.
- This information will be overwritten on each subsequent run, so copy any desired files out of this directory before re-running the simulation.

## Research

### Pedestrian Behavior
#### Pedestrian Mindsets
* Herd mentality [Spence 2011]: Especially when pedestrians
feel unfamiliar with the surrounding environment, they will
evacuate with the people around them. In psychology, this
phenomenon is also called the herd effect. During the evacuation, this mentality often manifests as following the route
of most pedestrians. However, this blind obedience often
causes congestion at the exit.

* Panic psychology [Aguirre 2005]: When an emergency occurs without warning, the evacuees will panic because they
are unprepared, which is caused by people’s lack of knowledge and experience of safe evacuation and unfamiliarity
with the environment. This psychological mechanism will reduce the decision-making ability of pedestrians to evacuate
and promote the phenomenon of congestion and congestion.

* Impulsive psychology [Frijda 2010]: When the density of
pedestrians is high and the space is narrow, it is easy to
cause congestion, and pedestrians will unconsciously and
eagerly leave the crowd. The greater the congestion, the
higher the chance of casualties.

* Sympathy and helping psychology [Tugarinov et al. 2020]:
Social psychology studies have found that in many evacuation scenarios, some people will help the weak around them,
such as the elderly and children, and not everyone is selfish

#### Models

* It is important to note that the mathematical models used to predict how individuals react in an evacuation settings is discussed in other papers. Sections 2.2 and 2.3 of `Crowd Evacuation Conflicts` summarize these findings.

* Grid of environment is a 2D array. Each spot is 0.4m * 0.4 m^2 and only one person can occupy a space.

* Motion of pedestrian `i` is described by `SF`. This is in `Crowd Evacuation Conflicts` section 3, figure (1)

* At each time step of the model, there may be a certain number of empty grids that the pedestrian can choose to move into. We calculate the probablity that pedestrian `i` moving to gird space `j` is calculated in `Crowd Evacuation Conflicts` section 3, figure (2). `kf` represents how familiar pedestrian `i` is with the location of the exit. In the paper a constant value of 10 is used, so we can probably play around with this value.

### The Game
#### Math behind the Game Theory

* Conflict arrises when to people try to occupy the same space at the same time step. Who occupies the space is decided by a prisoners dillema like game. Values of the game are described in `Crowd Evacuation Conflicts` section 3.1, Tables (1-3).

* Tables (2-3) gives us formulats to calculate the probablity of pedestrian movement in the event of a conflict, where `p` represents the penalty for defectors. Table (3) is for 3 or more players trying to go for the same space. 

* Each pedestrian may compete with their neighbors within a Moore neighborhood (All squares that are in contact with the space they are occupying).

* `N` refers to the number of conflicts, and `M` refers to the number of agents with the roll of Collaborator. Therefore the number of traitors is `(N-M)`. 

* If there are only collaborators, each individual has an equal chance of getting into the square which is calculated by `1/M`

* If there is only one traitor, then that traitor enters the space.

* If there are more than one traitors, the traitor will enter the space with a probablity of `1/(N - M)^p`

* Other litterature suggests `p` should be 1 ≥ `p` ≥ 2.5

#### Agent Strategies

* Pedestrians who fail to enter the target will change their strategy according to specific rules. These rules can be found in `Crowd Evacuation Conflicts` section 3.2, Figures (3-5).

* `Ui` and `Uj` are set as the income obtained by
pedestrians in the actual game, and `d` represents inertia. Usually, due to inertia, pedestrians tend to maintain the current strategy, but when the income gap is relatively large, pedestrians will change the current strategy. 

* Updates are calculated after each cycle `c`. 

* `Mx` is the estimated payoff of the current policy. `My` is the estimated payoff of the opposite policy. 

* If a person fails in a game (They don't get to move) then the pedestrian will update their strategy by changing to the opposite strategy with probability `W(Sx-Sy)`, this is described in `Crowd Evacuation Conflicts` section 3.2, Figures (5). `k` represents noise, which represents the strength of irrationality. This is set to 0.1 but we could probably play around with this

