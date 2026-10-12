"""09 · Mapping: one gesture, several parameters

Python topics: a mapping kept as data (a list of dictionaries, the same shape as
a JSON file); functions stored in a dictionary and chosen by name; a loop that
advances time event by event.

Musical content: the mapping decides what a gesture does. Here one control
value (0..1, a slow rise and fall standing in for a hand or a face) drives four
parameters at once (a one-to-many mapping, Hunt et al. 2003):

    pitch       quantised to a scale, so the line is in tune
    brightness  filter cutoff, sent as CC 74 with each note
    rate        notes per second
    velocity    how hard each note is played

Each entry names a parameter, its output range and a curve:
    linear    equal steps of control give equal steps of output
    exp       slow at first, fast at the end (useful for rate and frequency)
    log       fast at first, slow at the end
    inverted  output range written high-to-low, e.g. [0.9, 0.1]

Result: plots the four curves and the four parameter traces over time, prints a
few events, and plays the result on channel 1 (CC 74 mapped to the filter
cutoff, as in step 03).

Run:  python 09_mapping.py
      python 09_mapping.py --print      (no MIDI: every message is printed)

Exercises
  1. Change the "rate" curve from "exp" to "linear". The density rises early;
     compare the event count printed at the end.
  2. Invert brightness: "range": [0.9, 0.05]. High pitches are now dark and low
     pitches bright: the same gesture reads as another instrument.
  3. Change SCALE to [0, 1, 5, 7, 8] and the "pitch" range to [36, 84]. The mapping
     is unchanged in form; the musical result is entirely different.
"""
import numpy as np
import matplotlib.pyplot as plt
import kit

SECONDS = 10
SCALE = [0, 2, 3, 7, 9]          # semitones within an octave
MAPPING = [
    {"param": "pitch",      "range": [48, 79],   "curve": "linear"},
    {"param": "brightness", "range": [0.05, 0.9], "curve": "log"},
    {"param": "rate",       "range": [2, 14],    "curve": "exp"},
    {"param": "velocity",   "range": [50, 120],  "curve": "linear"},
]

CURVES = {
    "linear": lambda x: x,
    "exp": lambda x: x ** 3,
    "log": lambda x: x ** (1 / 3),
}


def gesture(t):
    """The control input: rises and falls once over SECONDS, with a small wobble."""
    return float(np.clip(np.sin(np.pi * t / SECONDS) ** 1.5 + 0.05 * np.sin(2 * np.pi * 0.7 * t), 0, 1))


def apply(control):
    params = {}
    for m in MAPPING:
        lo, hi = m["range"]
        params[m["param"]] = lo + CURVES[m["curve"]](control) * (hi - lo)
    return params


def quantise(note):
    """Snap a continuous note number to the nearest note of SCALE."""
    candidates = [12 * o + s for o in range(11) for s in SCALE]
    return min(candidates, key=lambda c: abs(c - note))


# --- run the instrument: one event at a time, the gap set by the current rate
t = 0.0
events = []          # (time, note, parameters): for printing and plotting
midi = []            # the messages sent
while t < SECONDS:
    p = apply(gesture(t))
    note = quantise(p["pitch"])
    midi.append(kit.cc(t, 74, p["brightness"] * 127))
    midi.append(kit.note(t, note, p["velocity"], 0.8 / p["rate"]))
    events.append((t, note, p))
    t += 1 / p["rate"]

for e in events[:: max(1, len(events) // 8)]:
    t_, note, p = e
    print(f"t {t_:5.2f}s  note {note}  bright {p['brightness']:.2f}  rate {p['rate']:5.1f}/s  velocity {p['velocity']:.0f}")
print(f"{len(events)} events in {SECONDS} s")

# --- figure: the curves, and the parameters over time
fig, axes = plt.subplots(2, len(MAPPING), figsize=(12, 5))
x = np.linspace(0, 1, 100)
times = np.array([e[0] for e in events])
for i, m in enumerate(MAPPING):
    lo, hi = m["range"]
    axes[0, i].plot(x, lo + CURVES[m["curve"]](x) * (hi - lo))
    axes[0, i].set_title(f"{m['param']} ({m['curve']})", fontsize=9)
    axes[0, i].set_xlabel("control", fontsize=8)
    values = [e[1] if m["param"] == "pitch" else e[2][m["param"]] for e in events]
    axes[1, i].plot(times, values, "." if m["param"] == "pitch" else "-")
    axes[1, i].set_xlabel("time (s)", fontsize=8)
axes[1, 0].set_ylabel("over time")
axes[0, 0].set_ylabel("curve")
plt.tight_layout()
kit.play(midi, cursor=list(axes[1]))
