"""10 · Classes: tracks with their own state

Python topics: class, __init__, self, attributes and methods; several objects
made from one class, each with its own state; two classes with the same method
name used interchangeably; the guard  if __name__ == "__main__":  which lets
another file import these classes without running the demonstration.

Musical content: a track is a small machine with a memory: its pattern, its
position, its sound. Each time the sequencer ticks, every track answers with a
note or with None. Because each track keeps its own position, tracks of
different lengths can run side by side (polymeter) and a track can change itself
while it plays (here, the Markov track walks its table; the Euclidean track can
rotate every bar).

    class EuclidTrack     E(k, n) rhythm on one pitch, optionally rotating
    class MarkovTrack     a melody from a transition table (step 06)

Result: runs eight bars of four tracks, prints the grid of the first two bars,
draws every note as a mark on its track's line, and plays the result:
bass on channel 2, two percussion tracks on channel 10, the melody on channel 1.

Run:  python 10_classes.py
      python 10_classes.py --print      (no MIDI: every message is printed)

Exercises
  1. Add a fifth track to the list in make_tracks():
     EuclidTrack("clap", 5, 7, 39, channel=10),
     Its 7-step cycle shifts against the 16-step bar.
  2. Set rotate_every=1 for the "bass" track. It rotates by one step each bar:
     the same five onsets, a new accent every bar.
  3. Give EuclidTrack a method mute() that sets self.k = 0, and call it on the
     "perc" track halfway through: if step == 64: tracks[1].mute()
"""
import random
import matplotlib.pyplot as plt
import kit


class EuclidTrack:
    def __init__(self, name, k, n, note, channel=1, rotate_every=0):
        self.name = name
        self.k, self.n = k, n
        self.note = note
        self.channel = channel
        self.rotate_every = rotate_every       # bars between rotations (0 = never)
        self.position = 0
        self.rotation = 0

    def tick(self, step):
        """Called once per sequencer step. Returns a MIDI note or None."""
        if self.rotate_every and step > 0 and step % (16 * self.rotate_every) == 0:
            self.rotation += 1
        i = (self.position + self.rotation) % self.n
        self.position += 1
        hit = (i * self.k) % self.n < self.k
        return self.note if hit else None


class MarkovTrack:
    def __init__(self, name, table, notes, start, every=2, channel=1, seed=0):
        self.name = name
        self.table, self.notes = table, notes
        self.state = start
        self.every = every                     # plays on every `every`-th step
        self.channel = channel
        self.rng = random.Random(seed)         # its own random generator: its own memory

    def tick(self, step):
        if step % self.every:
            return None
        note = self.notes[self.state]
        options = self.table[self.state]
        self.state = self.rng.choices(list(options), weights=list(options.values()))[0]
        return note


def make_tracks():
    table = {"C": {"D": 0.4, "E": 0.4, "G": 0.2}, "D": {"C": 0.5, "E": 0.5},
             "E": {"D": 0.3, "G": 0.5, "A": 0.2}, "G": {"E": 0.4, "A": 0.3, "C": 0.3},
             "A": {"G": 0.7, "C": 0.3}}
    notes = {"C": 72, "D": 74, "E": 76, "G": 79, "A": 81}
    return [
        EuclidTrack("bass", 5, 16, 36, channel=2),
        EuclidTrack("perc", 7, 12, 37, channel=10),               # rim
        EuclidTrack("high", 3, 8, 42, channel=10, rotate_every=2),  # hi-hat
        MarkovTrack("melody", table, notes, "C", every=2, channel=1, seed=4),
    ]


if __name__ == "__main__":
    BPM, BARS = 118, 8
    step_len = 60 / BPM / 4
    tracks = make_tracks()
    events = []
    hits = {tr.name: [] for tr in tracks}
    rows = {tr.name: "" for tr in tracks}
    for step in range(BARS * 16):
        for tr in tracks:
            note = tr.tick(step)
            if step < 32:
                rows[tr.name] += "." if note is None else "x"
            if note is not None:
                events.append(kit.note(step * step_len, note, 100, step_len * 0.9, tr.channel))
                hits[tr.name].append((step, note))
    for name, row in rows.items():
        print(f"{name:7s} {row[:16]} {row[16:]}")

    plt.figure(figsize=(11, 3.2))
    for y, (name, h) in enumerate(hits.items()):
        plt.plot([s * step_len for s, _ in h], [y] * len(h), "|", markersize=14, markeredgewidth=2)
    for bar in range(BARS + 1):
        plt.axvline(bar * 16 * step_len, color="0.6", linewidth=0.8, zorder=0)
    plt.yticks(range(len(hits)), list(hits))
    plt.xlabel("time (s) (vertical lines = bars)")
    plt.title("Four tracks, each with its own length and state")
    plt.tight_layout()
    kit.play(events, cursor=[plt.gca()])
