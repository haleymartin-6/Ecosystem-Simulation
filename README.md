# Ecosystem-Simulation
This project simulates an ecosystem consisting of foxes, rabbits, and grass. The simulation runs on a grid-based field where rabbits feed on grass and reproduce, while foxes hunt rabbits to survive. The simulation is visualized using Matplotlib animations.

# Features
Rabbits: Move around the field, eat grass, and reproduce. They can die from starvation or being eaten by foxes.
Foxes: Move around the field, hunt rabbits, and reproduce. They have a limited starvation time, after which they die if they haven't eaten.
Grass: Grows at a configurable rate and serves as the primary food source for rabbits.
Installation
This simulation requires Python 3.x and the following Python packages:

numpy
matplotlib
You can install the required packages using pip:

pip install numpy matplotlib

# Usage
You can run the simulation with default settings or customize various parameters using command-line arguments.

# Default Run
To run the simulation with default settings, use:
python alife.py

# Command-line Arguments
You can customize the simulation by passing the following arguments:

--grass-rate: Probability of grass growing at any given location (default: 0.05).
--fox-k-value: The number of cycles a fox can survive without food (default: 10).
--field-size: Size of the field (x/y dimensions) (default: 400).
--init-rabbits: Initial number of rabbits (default: 10).
--init-foxes: Initial number of foxes (default: 10).
--speed: Number of generations per frame in the simulation (default: 1).
For example, to run a simulation with a high grass growth rate and more initial rabbits, use:

python alife.py --grass-rate 0.1 --init-rabbits 20

# Simulation Details
Movement and Interaction
Rabbits move randomly on the field, eat grass to survive, and reproduce based on the amount of grass eaten.
Foxes move randomly but at a faster rate, hunt rabbits, and reproduce if they have eaten. They have a starvation timer that resets upon eating a rabbit.

# Visualization
The simulation displays the field in real-time, where:

Green squares represent grass.
Tan squares represent unoccupied space.
Blue squares represent rabbits.
Red squares represent foxes.
Population dynamics of both species are also plotted over time at the end of the simulation.

