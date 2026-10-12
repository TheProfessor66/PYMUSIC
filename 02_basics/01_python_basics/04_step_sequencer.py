"""04 · Loops and conditions: a step sequencer

Python topics: a dictionary of lists (one list per instrument); nested for loops;
if; enumerate() (gives the position and the value together); the modulo
operator % to repeat a pattern; computing a time for every event.

Musical content: a step sequencer is a grid. Each row is an instrument, each
column a step; 1 means play. The time of step n is n * step_length. Swing delays
every second step by a fraction of a step; that fraction is the whole difference
between a straight and a shuffled groove.

Result: prints the grid, plots the onset times of every event against the
straight grid (the swung steps are visibly displaced), and plays four bars on
the drums (channel 10: the Drum Rack in Live).

Run:  python 04_step_sequencer.py
      python 04_step_sequencer.py --print      (no MIDI: every message is printed)

Exercises
  1. Set SWING = 0.0, then 0.33 (triplet feel), then 0.5. Listen to each and read
     the printed delay of the off-beat steps in milliseconds.
  2. Add a row "clap": [0, 0, 1, 0] * 4 and its note 39 in DRUMS. A four-step
     list repeated four times is a full bar.
  3. Make the snare row 12 steps long while the others stay 16. With step % len(row)
     the rows drift against each other (polymeter) and coincide again after
     48 steps (three bars), the least common multiple of 12 and 16.
"""
import matplotlib.pyplot as plt
import kit

BPM = 112
SWING = 0.2            # 0 = straight; fraction of a step that every odd step is delayed
BARS = 4

GRID = {
    "kick":  [1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0],
    "snare": [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1],
    "hat":   [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
}
DRUMS = {"kick": 36, "snare": 38, "hat": 42}       # General MIDI drum notes

step_len = 60 / BPM / 4                     # a sixteenth note in seconds
steps = 16 * BARS
print(f"{BPM} BPM: one step = {step_len * 1000:.1f} ms; swing delays odd steps by {SWING * step_len * 1000:.1f} ms\n")
for name, row in GRID.items():
    print(f"{name:6s} {kit.grid_text(row)}")

events = []
plt.figure(figsize=(11, 3))
for y, (name, row) in enumerate(GRID.items()):
    times = []
    for step in range(steps):
        if row[step % len(row)] == 1:
            t = step * step_len
            if step % 2 == 1:
                t = t + SWING * step_len
            times.append(t)
            velocity = 110 if step % 4 == 0 else 80        # accent the beats
            events.append(kit.note(t, DRUMS[name], velocity, 0.05, channel=10))
    plt.plot(times, [y] * len(times), "|", markersize=18, markeredgewidth=2)

for step in range(steps + 1):                                   # the straight grid
    plt.axvline(step * step_len, color="0.85" if step % 4 else "0.5", linewidth=0.8, zorder=0)
plt.yticks(range(len(GRID)), list(GRID))
plt.xlabel("time (s)")
plt.title(f"Onsets against the straight grid (swing {SWING})")
plt.tight_layout()
kit.play(events, cursor=[plt.gca()])
