"""Record a control stream to a file, and play it back with its original timing.

Recording what a camera or a sensor produced lets every later stage
(conditioning, mapping, behaviour) be developed and tested without the
hardware, and lets two mappings be compared on exactly the same input.

File format (CSV): time in seconds, then one column per feature.
"""
import csv
import time

class Recorder:
    def __init__(self, path, names):
        self.f = open(path, "w", newline="")
        self.w = csv.writer(self.f)
        self.w.writerow(["t"] + list(names))
        self.names = list(names)

    def write(self, t, values):
        self.w.writerow([f"{t:.4f}"] + [f"{values[n]:.5f}" for n in self.names])

    def close(self):
        self.f.close()

def read(path):
    with open(path) as f:
        rows = list(csv.DictReader(f))
    return [(float(r.pop("t")), {k: float(v) for k, v in r.items()}) for r in rows]

def play(path, realtime=True):
    """Yield (t, {feature: value}) frames, sleeping between them if realtime."""
    t0 = time.perf_counter()
    for t, frame in read(path):
        if realtime:
            wait = t - (time.perf_counter() - t0)
            if wait > 0:
                time.sleep(wait)
        yield t, frame

def make_example(path="gesture_example.csv", fps=30, seconds=12, seed=2):
    """A synthetic face stream: slow mouth openings, two fast ones, blinks, tracker noise."""
    import math, random
    rng = random.Random(seed)
    rec = Recorder(path, ["jawOpen", "browInnerUp", "eyeBlinkLeft"])
    for i in range(fps * seconds):
        t = i / fps
        jaw = 0.08 + 0.35 * max(0.0, math.sin(2 * math.pi * 0.15 * t)) ** 2
        if 6.0 < t < 6.6 or 9.0 < t < 9.4:
            jaw = 0.75
        brow = 0.1 + 0.25 * (0.5 + 0.5 * math.sin(2 * math.pi * 0.07 * t + 1))
        blink = 0.9 if any(abs(t - b) < 0.08 for b in (1.5, 3.2, 4.0, 7.7, 10.1)) else 0.05
        rec.write(t, {"jawOpen": jaw + rng.gauss(0, 0.02),
                      "browInnerUp": brow + rng.gauss(0, 0.015),
                      "eyeBlinkLeft": blink + rng.gauss(0, 0.02)})
    rec.close()

if __name__ == "__main__":
    make_example()
    frames = read("gesture_example.csv")
    print(f"{len(frames)} frames, {frames[-1][0]:.1f} s, features: {list(frames[0][1])}")
