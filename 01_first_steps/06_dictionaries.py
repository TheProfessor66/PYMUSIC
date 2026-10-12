"""06 · Dictionaries

A dictionary stores values under names (keys): {"kick": 36, "snare": 38}.
drums["kick"] gives 36. Adding a key: drums["clap"] = 39.
A dictionary is useful for settings and for mappings: which input controls what.

Run:  python 06_dictionaries.py

Exercises
  1. Add "clap": 39 to DRUMS and a clap line to PATTERN.
  2. Change the snare pattern so it plays on steps 4 and 12 only.
  3. Print only the names of the drums: for name in DRUMS:
"""

DRUMS = {"kick": 36, "snare": 38, "hat": 42}        # Drum Rack note numbers

# one string per drum: x = play, . = rest
PATTERN = {
    "kick":  "x...x...x...x...",
    "snare": "....x.......x...",
    "hat":   "x.x.x.x.x.x.x.x.",
}

print("the kick is note", DRUMS["kick"])
print()

# .items() gives each key together with its value
for name, row in PATTERN.items():
    print(f"{name:6s} {DRUMS[name]}  {row}")
print()

# which drums play on each step
for step in range(16):
    playing = []
    for name, row in PATTERN.items():
        if row[step] == "x":
            playing.append(name)
    print(step, playing)
