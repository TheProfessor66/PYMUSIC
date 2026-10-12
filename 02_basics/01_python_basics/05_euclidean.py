"""05 · An algorithm: Euclidean rhythms

Python topics: a function that returns a list; a list comprehension with a
condition; rotation by slicing (p[r:] + p[:r]); tuples; math.lcm.

Musical content: E(k, n) spreads k onsets over n steps as evenly as possible.
Toussaint (2005) showed that many traditional rhythms are Euclidean:
    E(3, 8)   tresillo                 x..x..x.
    E(5, 8)   cinquillo                x.x.xx.x  (a rotation of x.xx.xx.)
    E(7, 12)  West African bell        x.x.x.xx.x.x  (a rotation of x.xx.x.xx.x.)
    E(5, 16)  bossa nova               x...x..x..x..x..  (a rotation of it)
One line of arithmetic generates them: step i is an onset when (i * k) % n < k.

Result: prints each rhythm and the gaps between its onsets (a Euclidean rhythm
only ever has two gap sizes, differing by one), draws each as a necklace (steps on
a circle, onsets in black), and plays them in turn, two cycles each: onsets on
channel 1, a quiet hi-hat on every step on channel 10.

Run:  python 05_euclidean.py
      python 05_euclidean.py --print      (no MIDI: every message is printed)

Exercises
  1. Change the rotation of (5, 16, ...) from 0 to 3. The gaps are the same
     numbers in another order; the necklace is the same shape turned; the accent
     moves and the rhythm is heard differently.
  2. Put a rhythm that is not Euclidean into RHYTHMS as a list instead of a tuple,
     e.g. son clave [1,0,0,1,0,0,1,0,0,0,1,0,1,0,0,0]. Its gaps are 3, 3, 4, 2, 4:
     three sizes, so it is not Euclidean.
  3. Set LAYER = (3, 8, 4, 7): E(3,8) on channel 1 against E(4,7) on channel 2.
     They meet again after math.lcm(8, 7) = 56 steps; the printout marks the
     coincidences.
"""
import math
import numpy as np
import matplotlib.pyplot as plt
import kit

STEP = 0.13                   # seconds per step
RHYTHMS = [(3, 8, 0), (5, 8, 0), (7, 12, 0), (5, 16, 0)]   # (k, n, rotation)
LAYER = (3, 8, 5, 12)         # two rhythms played together at the end: k1, n1, k2, n2


def euclid(k, n, rotation=0):
    pattern = [1 if (i * k) % n < k else 0 for i in range(n)]
    return pattern[rotation:] + pattern[:rotation]


def gaps(pattern):
    """Distances between successive onsets, wrapping round the end of the cycle."""
    onsets = [i for i, v in enumerate(pattern) if v]
    return [(onsets[(j + 1) % len(onsets)] - onsets[j]) % len(pattern) or len(pattern)
            for j in range(len(onsets))]


patterns = []
for r in RHYTHMS:
    p = euclid(*r) if isinstance(r, tuple) else r
    label = f"E{r}" if isinstance(r, tuple) else "list"
    g = gaps(p)
    print(f"{label:14s} {kit.grid_text(p):18s} gaps {g}   sizes {sorted(set(g))}")
    patterns.append((label, p))

# --- necklaces
fig, axes = plt.subplots(1, len(patterns), figsize=(2.6 * len(patterns), 2.9))
for ax, (label, p) in zip(np.atleast_1d(axes), patterns):
    a = np.pi / 2 - 2 * np.pi * np.arange(len(p)) / len(p)        # step 0 at the top, clockwise
    x, y = np.cos(a), np.sin(a)
    on = [i for i, v in enumerate(p) if v]
    ax.plot(np.append(x[on], x[on[0]]), np.append(y[on], y[on[0]]), color="0.6")
    ax.scatter(x, y, s=60, facecolors=["k" if v else "w" for v in p], edgecolors="k", zorder=3)
    ax.set_title(label, fontsize=9)
    ax.set_aspect("equal")
    ax.axis("off")
plt.tight_layout()

# --- sound: each rhythm for two cycles, with a quiet hat on every step
t = 0.0
events = []
for label, p in patterns:
    for i in range(2 * len(p)):
        events.append(kit.note(t, 42, 50, 0.05, channel=10))
        if p[i % len(p)]:
            events.append(kit.note(t, 64, 100, STEP * 0.8))
        t += STEP

# --- two rhythms together, until they coincide again
k1, n1, k2, n2 = LAYER
a, b = euclid(k1, n1), euclid(k2, n2)
cycle = math.lcm(n1, n2)
print(f"\nE({k1},{n1}) on channel 1 against E({k2},{n2}) on channel 2: the pair repeats every {cycle} steps")
line = ""
t += 0.4
fast = STEP / 2
for i in range(cycle):
    hit_a, hit_b = a[i % n1], b[i % n2]
    if hit_a:
        events.append(kit.note(t, 69, 100, fast * 0.8, channel=1))
    if hit_b:
        events.append(kit.note(t, 45, 100, fast * 0.8, channel=2))
    line += "X" if hit_a and hit_b else ("a" if hit_a else ("b" if hit_b else "."))
    t += fast
print(line, "  (X = both)")
kit.play(events)
