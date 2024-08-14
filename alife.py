"""
File name: alife.py
Description: Fox and rabbit ecosystem animation
"""

import random as rnd
import copy
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.colors import ListedColormap
import argparse

DEFAULT_SIZE = 400    # x/y dimensions of the field
WRAP = True  # When moving beyond the border, do we wrap around to the other side
OFFSPRING = 2  # The number of offspring when a rabbit reproduces
DEFAULT_GRASS_RATE = 0.05  # Probability of grass growing at any given location, e.g., 2%
DEFAULT_INIT_RABBITS = 10 # Number of starting rabbits
DEFAULT_INIT_FOXES =10
DEFAULT_FOX_K_VALUE = 10  # Fox can go without food for 10 cycles
DEFAULT_SPEED = 1  # Number of generations per frame

# Parse command-line arguments
parser = argparse.ArgumentParser(description='Run artificial life simulation with rabbits and foxes.')
parser.add_argument('--grass-rate', type=float, default=DEFAULT_GRASS_RATE,
                    help='Probability of grass growing at any given location (e.g., 0.1 for 10%).')
parser.add_argument('--fox-k-value', type=int, default=DEFAULT_FOX_K_VALUE,
                    help='The k value determining how long a fox can go without food.')
parser.add_argument('--field-size', type=int, default=DEFAULT_SIZE,
                    help='Size of the field (x/y dimensions).')
parser.add_argument('--init-rabbits', type=int, default=DEFAULT_INIT_RABBITS,
                    help='Number of initial rabbits in the field.')
parser.add_argument('--init-foxes', type=int, default=DEFAULT_INIT_FOXES,
                    help='Number of initial foxes in the field.')
parser.add_argument('--speed', type=int, default=DEFAULT_SPEED,
                    help='Number of generations per frame in the simulation.')
args = parser.parse_args()

# Assign command-line arguments to variables
GRASS_RATE = args.grass_rate
FOX_K_VALUE = args.fox_k_value
SIZE = args.field_size
INIT_RABBITS = args.init_rabbits
INIT_FOXES = args.init_foxes
SPEED = args.speed

GRASS_COLOR = 'green'   # 1
UNOCCUPIED_COLOR = 'tan'  # 0
RABBIT_COLOR = 'blue'   # 2
FOX_COLOR = 'red'       # 3

custom_cmap = ListedColormap([UNOCCUPIED_COLOR, GRASS_COLOR, RABBIT_COLOR, FOX_COLOR])


class Rabbit:
    def __init__(self):
        self.x = rnd.randrange(0, SIZE)
        self.y = rnd.randrange(0, SIZE)
        self.eaten = 0
        self.dead = False

    def reproduce(self):
        self.eaten = 0
        return copy.deepcopy(self)

    def eat(self, amount):
        self.eaten += amount

    def move(self):
        if WRAP:
            self.x = (self.x + rnd.choice([-1, 0, 1])) % SIZE
            self.y = (self.y + rnd.choice([-1, 0, 1])) % SIZE
        else:
            self.x = min(SIZE - 1, max(0, (self.x + rnd.choice([-1, 0, 1]))))
            self.y = min(SIZE - 1, max(0, (self.y + rnd.choice([-1, 0, 1]))))

    def kill(self):
        self.dead = True

class Fox:
    def __init__(self):
        self.starvation_counter = 0
        self.x = rnd.randrange(0, SIZE)
        self.y = rnd.randrange(0, SIZE)
        self.eaten = 0
        self.starvation_time = FOX_K_VALUE  # Fox can go without food for FOX_K_VALUE cycles

    def reproduce(self):
        self.eaten = 0
        self.starvation_counter = 0
        return copy.deepcopy(self)

    def eat(self, rabbits):
        for rabbit in rabbits:
            if self.x == rabbit.x and self.y == rabbit.y:
                self.eaten += 1
                rabbit.kill()

    def move(self):
        if WRAP:
            self.x = (self.x + rnd.choice([-2, 0, 2])) % SIZE
            self.y = (self.y + rnd.choice([-2, 0, 2])) % SIZE
        else:
            self.x = min(SIZE - 1, max(0, (self.x + rnd.choice([-2, 0, 2]))))
            self.y = min(SIZE - 1, max(0, (self.y + rnd.choice([-2, 0, 2]))))

    def starve(self):
        self.starvation_counter += 1
        if self.eaten > 0:
            self.starvation_counter = 0  # Reset starvation counter if fox eats
        return self.starvation_counter >= self.starvation_time and self.eaten == 0


class Field:
    def __init__(self):
        self.field = np.ones(shape=(SIZE, SIZE), dtype=int)
        self.rabbits_field = np.zeros(shape=(SIZE, SIZE), dtype=int)
        self.foxes_field = np.zeros(shape=(SIZE, SIZE), dtype=int)
        self.rabbits = []
        self.foxes = []

    def add_rabbit(self, rabbit):
        self.rabbits.append(rabbit)

    def add_foxes(self, fox):
        self.foxes.append(fox)

    def move(self):
        for r in self.rabbits:
            self.rabbits_field[r.x, r.y] = 0        # make place rabbit is leaving 0 (unoccupied in rabbit field)
            r.move()
            self.rabbits_field[r.x, r.y] = 2        # make current location of rabbit 2

        for f in self.foxes:
            self.foxes_field[f.x, f.y] = 0          # make place rabbit is leaving 0 (unoccupied in fox field)
            f.move()
            self.foxes_field[f.x, f.y] = 3          # make current location of fox 3

    def eat(self):
        """ All rabbits try to eat grass at their current location """
        for r in self.rabbits:
            r.eat(self.field[r.x, r.y])
            self.field[r.x, r.y] = 0

        for f in self.foxes:
            f.eat(self.rabbits)  # Call the eat function in the Fox class

    def survive(self):
        for rabbit in self.rabbits:
            if rabbit.dead:                                 # check if fox already ate rabbit
                self.rabbits_field[rabbit.x, rabbit.y] = 0
                self.rabbits.remove(rabbit)

        for rabbit in self.rabbits:
            if rabbit.eaten < 1:                            # check if rabbit has starved
                self.rabbits_field[rabbit.x, rabbit.y] = 0
                self.rabbits.remove(rabbit)

        for f in self.foxes:
            if f.starve():
                self.foxes_field[f.x, f.y] = 0
                self.foxes.remove(f)

    def reproduce(self):
        # Reproduce rabbits
            born_rabbits = []
            for r in self.rabbits:
                for _ in range(rnd.randint(1, OFFSPRING)):
                    if r.eaten > 0:
                        born_rabbits.append(r.reproduce())
            self.rabbits += born_rabbits

            # Reproduce foxes
            born_foxes = []
            for f in self.foxes:
                if f.eaten > 0:
                    born_foxes.append(f.reproduce())
            self.foxes += born_foxes

    def grow(self):
        growloc = (np.random.rand(SIZE, SIZE) < GRASS_RATE) * 1
        self.field = np.maximum(self.field, growloc)

    def generation(self):
        self.move()
        self.eat()
        self.survive()
        self.reproduce()
        self.grow()

def main():
    field = Field()
    rabbit_population = []
    fox_population = []

    # populate rabbits
    for _ in range(INIT_RABBITS):
        field.add_rabbit(Rabbit())

    # populate foxes
    for _ in range(INIT_FOXES):
        field.add_foxes(Fox())

    fig = plt.figure(figsize=(10, 10))
    im = plt.imshow(field.field, cmap=custom_cmap, interpolation='none', vmin=0, vmax=3)
    plt.title("Ecosystem Simulation")

    def animate_with_plot(i):           # animation function with plot at end of animation

        for _ in range(SPEED):
            field.generation()
            if i % 1000 == 0:
                rabbit_population.append(len(field.rabbits))
                fox_population.append(len(field.foxes))

        max_array = np.maximum.reduce([field.rabbits_field, field.foxes_field, field.field])

        im.set_array(max_array)

        plt.title("Generation: " + str(i * SPEED) + " Rabbits: " + str(len(field.rabbits)) + " Foxes: " + str(
            len(field.foxes)))
        return im,

    anim = animation.FuncAnimation(fig, animate_with_plot, frames=100**10, interval=1)
    plt.show()

    # Plot the populations after the animation finishes
    plt.figure(figsize=(10, 6))
    plt.plot(range(1, len(rabbit_population) + 1), rabbit_population, label='Rabbits', color='blue')
    plt.plot(range(1, len(fox_population) + 1), fox_population, label='Foxes', color='red')
    plt.xlabel('Generations (x1000)')
    plt.ylabel('Population')
    plt.title('Population Dynamics (Every 1000 Cycles)')
    plt.legend()
    plt.grid(True)
    plt.show()

if __name__ == '__main__':
    main()
