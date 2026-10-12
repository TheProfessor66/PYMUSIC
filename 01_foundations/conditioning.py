"""Turning raw input values into usable control: scale, curve, smooth, threshold.

Each piece is small and testable alone. An instrument chains them.
"""
from one_euro import OneEuro

def scale(x, in_lo, in_hi, out_lo=0.0, out_hi=1.0, clip=True):
    """Map x from one range to another (Max: [scale])."""
    t = (x - in_lo) / (in_hi - in_lo) if in_hi != in_lo else 0.0
    if clip:
        t = min(1.0, max(0.0, t))
    return out_lo + t * (out_hi - out_lo)

def curve(t, shape=1.0):
    """Shape a 0..1 value: shape > 1 gives finer control near 0, < 1 near 1."""
    return t ** shape

class Calibrator:
    """Learns a player's resting value and maximum, then rescales to 0..1."""
    def __init__(self):
        self.lo, self.hi, self.collecting = 0.0, 1.0, None

    def start(self):
        self.collecting = []

    def feed(self, x):
        if self.collecting is not None:
            self.collecting.append(x)

    def finish(self):
        if self.collecting:
            self.lo, self.hi = min(self.collecting), max(self.collecting)
        self.collecting = None

    def __call__(self, x):
        return scale(x, self.lo, self.hi)

class Hysteresis:
    """A continuous value becomes on/off events. Two thresholds stop chattering:
    on above `high`, off again only below `low`."""
    def __init__(self, low=0.4, high=0.6):
        self.low, self.high, self.state = low, high, False

    def __call__(self, x):
        if not self.state and x > self.high:
            self.state = True
            return "on"
        if self.state and x < self.low:
            self.state = False
            return "off"
        return None

class Chain:
    """filter -> calibrate -> curve, for one feature."""
    def __init__(self, min_cutoff=1.5, beta=5.0, shape=1.0):
        self.filter = OneEuro(min_cutoff, beta)
        self.cal = Calibrator()
        self.shape = shape

    def __call__(self, x, t):
        x = self.filter(x, t)
        self.cal.feed(x)
        return curve(self.cal(x), self.shape)
