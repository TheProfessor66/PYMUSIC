"""06 · Dictionaries and chance: a Markov melody

Python topics: a dictionary of dictionaries; random.choices with weights;
random.seed (the same seed gives the same sequence: chance that can be repeated);
counting with a dictionary; a while loop.

Musical content: a first-order Markov chain chooses the next note from weights
that depend only on the current note. The table TRANSITIONS is the whole
composition: which notes follow which, and how often. Generated lines differ
every time but share the table's character.

Result: generates LENGTH notes, prints how often each transition actually
happened, plots the designed probabilities against the measured ones (with a
short run they disagree; with a long run they converge), and plays the first
32 notes on channel 1.

Run:  python 06_markov.py
      python 06_markov.py --print      (no MIDI: every message is printed)

Exercises
  1. Change SEED to another number. A different line, the same style. Set it
     back to 1: exactly the first line again.
  2. Set LENGTH = 30, then 3000, and compare the plot. The bars approach the
     designed weights as the run grows (the law of large numbers).
  3. Make "G" lead almost always to "C": {"C": 0.9, "A": 0.1}. The line becomes
     more predictable; the printed count of G->C rises to about 90 %.
"""
import random
import matplotlib.pyplot as plt
import numpy as np
import kit

SEED = 1
LENGTH = 400
STEP = 0.16
NOTES = {"C": 60, "D": 62, "E": 64, "G": 67, "A": 69}

TRANSITIONS = {                       # from -> {to: weight}
    "C": {"D": 0.4, "E": 0.4, "G": 0.2},
    "D": {"C": 0.5, "E": 0.5},
    "E": {"D": 0.3, "G": 0.5, "A": 0.2},
    "G": {"E": 0.4, "A": 0.3, "C": 0.3},
    "A": {"G": 0.7, "C": 0.3},
}

random.seed(SEED)
state = "C"
line = [state]
while len(line) < LENGTH:
    options = TRANSITIONS[state]
    state = random.choices(list(options), weights=list(options.values()))[0]
    line.append(state)

print(" ".join(line[:32]), "...")

# --- count what happened
counts = {a: {b: 0 for b in NOTES} for a in NOTES}
for a, b in zip(line, line[1:]):
    counts[a][b] += 1
print(f"\nmeasured over {LENGTH} notes (designed weight in brackets)")
for a in NOTES:
    total = sum(counts[a].values()) or 1
    row = "  ".join(f"{b}:{counts[a][b] / total:4.0%} ({TRANSITIONS[a].get(b, 0):.1f})" for b in NOTES)
    print(f"{a} -> {row}")

# --- plot designed vs measured
fig, axes = plt.subplots(1, len(NOTES), figsize=(12, 2.8), sharey=True)
x = np.arange(len(NOTES))
for ax, a in zip(axes, NOTES):
    total = sum(counts[a].values()) or 1
    ax.bar(x - 0.2, [TRANSITIONS[a].get(b, 0) for b in NOTES], 0.4, color="0.75", label="designed")
    ax.bar(x + 0.2, [counts[a][b] / total for b in NOTES], 0.4, color="0.2", label="measured")
    ax.set_xticks(x, list(NOTES))
    ax.set_title(f"after {a}", fontsize=9)
axes[0].set_ylabel("probability")
axes[0].legend(fontsize=7)
plt.suptitle(f"Transitions: designed and measured over {LENGTH} notes", fontsize=10)
plt.tight_layout()

# --- play the first 32 notes
events = [kit.note(i * STEP, NOTES[name], 90, STEP * 0.9) for i, name in enumerate(line[:32])]
kit.play(events)
