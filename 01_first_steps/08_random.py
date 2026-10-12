"""08 · Chance

The random module chooses values: random.choice(list) picks one element,
random.random() gives a number between 0 and 1.
random.seed(n) makes the choices repeat exactly on every run.

Run:  python 08_random.py

Exercises
  1. Remove the random.seed line: every run gives a new melody.
  2. Change SCALE to a minor pentatonic: [0, 3, 5, 7, 10].
  3. Use DENSITY: a note plays only if random.random() < DENSITY,
     otherwise print a rest.
"""
import random

random.seed(1)

ROOT = 60
SCALE = [0, 2, 4, 7, 9]         # major pentatonic, in semitones above ROOT
LENGTH = 16
DENSITY = 0.7

melody = []
for i in range(LENGTH):
    degree = random.choice(SCALE)
    melody.append(ROOT + degree)

print(melody)
for note in melody:
    print(note, " " * (note - ROOT) + "o")      # higher note, further right
