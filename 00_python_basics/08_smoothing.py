"""08 · Control data: noise, smoothing and lag

Python topics: a variable that keeps its value between loop iterations (state);
a function that filters a whole list; numpy statistics (np.std, np.diff);
comparing several solutions by measurement.

Musical content: every sensor (camera tracker, accelerometer, contact mic level)
delivers a noisy number many times per second. Before it controls sound it is
smoothed. Every smoothing method trades jitter (trembling when the hand is
still) for lag (late response when the hand moves):

    moving average   mean of the last N values
    one-pole         y = y + a * (x - y)        (the same line is a lowpass
                                                 filter in gen~, Mojo or C++)
    median           middle of the last N values: removes single spikes

The input is a simulated 30 frames-per-second control: still, then a slow rise,
then a sudden jump at 5 s, with tracker noise and two dropouts (spikes to 0).

Result: prints jitter (while still) and lag (after the jump) for each filter;
plots the raw signal (top) and the filters (bottom); then holds a chord on
channel 1 and sends the raw signal as CC 74 (filter cutoff), followed by the
filter named in PLAY. The cursor follows in the plot. The jitter is heard as a
trembling filter, the dropouts as sudden dark gaps, the lag as a slow opening.

Setup: CC 74 mapped to the filter cutoff of the channel 1 instrument (see step 03).

Run:  python 08_smoothing.py
      python 08_smoothing.py --print      (no MIDI: every message is printed)

Exercises
  1. Change ALPHA from 0.15 to 0.05, then 0.5. Watch the two printed numbers move
     in opposite directions. Pick the value that sounds best and note its numbers.
  2. Add a chained filter to the dictionary filters:
     "median+one-pole": one_pole(median(raw, N), ALPHA),
     and set PLAY = "median+one-pole". The dropouts vanish and the jitter stays low.
  3. Set NOISE = 0 (the two dropouts remain). Jitter is zero for every signal;
     the moving average and the one-pole now only add lag, while the median still
     removes the dropouts at almost no cost.
"""
import numpy as np
import matplotlib.pyplot as plt
import kit

FPS = 30
SECONDS = 8
NOISE = 0.03
ALPHA = 0.15          # one-pole: fraction of the way to move each frame
N = 5                 # window length for moving average and median
PLAY = "one-pole"     # which filter is heard after the raw signal (a key of filters)

rng = np.random.default_rng(3)
t = np.arange(SECONDS * FPS) / FPS
true = np.where(t < 2, 0.2, 0.2 + 0.15 * (t - 2))       # still, then rising
true = np.where(t >= 5, 0.85, np.minimum(true, 0.6))     # jump at 5 s
raw = true + rng.normal(0, NOISE, len(t))
raw[[70, 190]] = 0.0                                      # two dropouts


def moving_average(x, n):
    out = []
    for i in range(len(x)):
        window = x[max(0, i - n + 1): i + 1]
        out.append(sum(window) / len(window))
    return np.array(out)


def one_pole(x, a):
    out = []
    y = x[0]                          # the state: kept from one frame to the next
    for value in x:
        y = y + a * (value - y)
        out.append(y)
    return np.array(out)


def median(x, n):
    return np.array([np.median(x[max(0, i - n + 1): i + 1]) for i in range(len(x))])


filters = {
    "raw": raw,
    "moving average": moving_average(raw, N),
    "one-pole": one_pole(raw, ALPHA),
    "median": median(raw, N),
}

still = (t > 0.5) & (t < 1.9)
jump = int(5 * FPS)
print(f"{'':24s} jitter while still   lag after jump (to 90 %)")
for name, y in filters.items():
    jitter = np.std(np.diff(y[still])) * 1000
    above = y[jump:] > 0.6 + 0.9 * 0.25                     # frames past 90 % of the jump
    lag = f"{np.argmax(above) / FPS * 1000:6.0f} ms" if above.any() else "not reached"
    print(f"{name:24s} {jitter:8.1f} (x1000)      {lag}")

# --- figure: raw on top (heard first), filters below (PLAY heard second)
second = SECONDS + 1.0                                   # the second pass starts here
fig, (top, bottom) = plt.subplots(2, 1, figsize=(10, 6))
top.plot(t, raw, color="0.6", linewidth=0.8, label="raw")
top.plot(t, true, "k:", linewidth=1, label="true gesture")
top.set_title("Pass 1: raw signal", loc="left", fontsize=10)
top.legend(fontsize=8, loc="upper left")
for name, y in filters.items():
    if name != "raw":
        bottom.plot(t + second, y, label=name, linewidth=2.2 if name == PLAY else 1.0)
bottom.plot(t + second, true, "k:", linewidth=1)
bottom.set_title(f"Pass 2: filters (heard: {PLAY})", loc="left", fontsize=10)
bottom.legend(fontsize=8, loc="upper left")
bottom.set_xlabel("time (s)")
for ax in (top, bottom):
    ax.set_ylabel("control 0..1")
plt.tight_layout()

# --- sound: a held chord, the control as CC 74, raw first and then PLAY
events = []
for start, signal in ((0.0, raw), (second, filters[PLAY])):
    for p in [48, 55, 60, 64]:
        events.append(kit.note(start, p, 80, SECONDS))
    for time, value in zip(t, signal):
        events.append(kit.cc(start + time, 74, value * 127))
kit.play(events, cursor=[top, bottom])
