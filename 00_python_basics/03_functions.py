"""03 · Functions: shapes of control

Python topics: def; parameters and default values; return; one function called
many times with different arguments; functions that return lists.

Musical content: a controller (a MIDI CC message) changes a parameter of
the sound while it plays. Here the parameter is the filter cutoff of the
instrument on channel 1 (CC 74). A held chord is played while a function
generates the cutoff, 50 values per second. Four functions, four shapes:

    ramp(start, end)          a straight line: a filter sweep
    lfo(rate, depth)          a sine: periodic movement (wah, tremolo)
    steps(n, seed)            random levels held for a while (sample and hold)
    envelope(attack, decay)   a fast rise and a slow fall

Result: plots the four shapes; plays the chord four times, each with one shape
on CC 74, while the cursor moves along the plot.

Setup in Live: on the channel 1 instrument, enter MIDI Map mode (Cmd+M), click the
filter frequency, run the script once (or move any CC 74 source), leave Map mode.

Run:  python 03_functions.py
      python 03_functions.py --print      (no MIDI: every message is printed)

Exercises
  1. Change "lfo(rate=2)": lfo(rate=2) to lfo(rate=7). The plot shows more cycles;
     the filter moves faster. Then add depth=0.1: the same rate, barely moving.
  2. Write a function saw(rate): a ramp that repeats, using (t * rate) % 1.
     Add it to SHAPES and listen.
  3. Change RATE (values per second) from 50 to 5. The plot becomes a staircase and
     the sweep is heard in steps ("zipper" noise): the control rate is too low.
"""
import math
import random
import matplotlib.pyplot as plt
import kit

DURATION = 3.0          # seconds per shape
RATE = 50               # controller values per second
CHORD = [48, 55, 60, 63, 67]


def times():
    """The moments at which a controller value is sent."""
    return [i / RATE for i in range(int(DURATION * RATE))]


def ramp(start=0.0, end=1.0):
    return [start + (end - start) * t / DURATION for t in times()]


def lfo(rate=2.0, depth=0.5, centre=0.5):
    return [centre + depth * math.sin(2 * math.pi * rate * t) for t in times()]


def steps(n=8, seed=2):
    rng = random.Random(seed)
    levels = [rng.random() for _ in range(n)]
    return [levels[int(t / DURATION * n)] for t in times()]


def envelope(attack=0.1, decay=1.5):
    out = []
    for t in times():
        if t < attack:
            out.append(t / attack)
        else:
            out.append(math.exp(-(t - attack) / decay * 3))
    return out


SHAPES = {
    "ramp(0, 1)": ramp(0, 1),
    "lfo(rate=2)": lfo(rate=2),
    "steps(8)": steps(8),
    "envelope(0.1, 1.5)": envelope(0.1, 1.5),
}

events = []
fig, axes = plt.subplots(1, len(SHAPES), figsize=(12, 3), sharey=True)
gap = 0.4
for i, (name, values) in enumerate(SHAPES.items()):
    start = i * (DURATION + gap)
    for p in CHORD:
        events.append(kit.note(start, p, 80, DURATION))
    for t, v in zip(times(), values):
        events.append(kit.cc(start + t, 74, v * 127))
    x = [start + t for t in times()]
    axes[i].plot(x, values)
    axes[i].set_xlim(start, start + DURATION)
    axes[i].set_title(name, fontsize=9)
    axes[i].set_xlabel("time (s)")
axes[0].set_ylabel("CC 74 (0..1)")
plt.tight_layout()
kit.play(events, cursor=list(axes))
