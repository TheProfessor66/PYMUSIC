"""Shared tools for the steps in this folder. Python computes and draws; the sound
comes from Ableton Live, through MIDI. Max is used as a control surface (step 11).

    python 01_numbers.py            MIDI to Live through the IAC Driver
    python 01_numbers.py --print    no MIDI: prints every message instead

Channels used throughout:
    1   melody instrument          (Live: a synth; CC 74 mapped to its filter cutoff)
    2   bass instrument
    10  drums                      (Live: a Drum Rack; 36 kick, 38 snare, 42 hat, 37 rim, 39 clap)

What the steps call:
    note(time, pitch, velocity, duration, channel)   one note event
    cc(time, number, value, channel)                 one controller event
    play(events, cursor=[axes, ...])                 shows the figure, plays the events
                                                     in real time, moves a cursor along
                                                     the time axis of the given plots
"""
import sys
import time
import math
import matplotlib.pyplot as plt

MODE = "print" if "--print" in sys.argv else "midi"


# ------------------------------------------------------------------ pitch
def mtof(note):
    """MIDI note number -> frequency in Hz (69 = A 440 Hz, +12 = one octave up)."""
    return 440.0 * 2 ** ((note - 69) / 12)


def ftom(freq):
    """Frequency in Hz -> MIDI note number, with a fractional part for pitches between notes."""
    return 69 + 12 * math.log2(freq / 440.0)


# ------------------------------------------------------------------ events
def note(time, pitch, velocity=100, duration=0.2, channel=1):
    return {"t": time, "kind": "note", "pitch": pitch, "vel": int(velocity), "dur": duration, "ch": channel}


def cc(time, number, value, channel=1):
    return {"t": time, "kind": "cc", "cc": number, "value": int(max(0, min(127, round(value)))), "ch": channel}


def grid_text(pattern, on="x", off="."):
    """[1, 0, 0, 1] -> 'x..x'"""
    return "".join(on if v else off for v in pattern)


# ------------------------------------------------------------------ outputs
class MidiOut:
    def __init__(self):
        import mido
        self.mido = mido
        names = [n for n in mido.get_output_names() if "IAC" in n]
        if not names:
            sys.exit("No IAC Driver port found. Audio MIDI Setup > Window > Show MIDI Studio > "
                     "IAC Driver > tick 'Device is online'. Or run with --print.")
        self.port = mido.open_output(names[0])

    def note_on(self, e):
        p = int(round(e["pitch"]))
        self.port.send(self.mido.Message("note_on", channel=e["ch"] - 1, note=p, velocity=e["vel"]))

    def note_off(self, e):
        p = int(round(e["pitch"]))
        self.port.send(self.mido.Message("note_off", channel=e["ch"] - 1, note=p))

    def cc(self, e):
        self.port.send(self.mido.Message("control_change", channel=e["ch"] - 1, control=e["cc"], value=e["value"]))

    def close(self):
        for ch in range(16):
            self.port.send(self.mido.Message("control_change", channel=ch, control=123, value=0))


class PrintOut:
    def __init__(self):
        self.t0 = None

    def now(self):
        if self.t0 is None:
            self.t0 = time.perf_counter()
        return time.perf_counter() - self.t0

    def note_on(self, e):
        print(f"  {self.now():6.3f}s  note  ch{e['ch']:<2d} {e['pitch']:6.2f}  vel {e['vel']:3d}  {e['dur'] * 1000:4.0f} ms")

    def note_off(self, e):
        pass

    def cc(self, e):
        print(f"  {self.now():6.3f}s  cc    ch{e['ch']:<2d} #{e['cc']:<3d}  {e['value']:3d}")

    def close(self):
        pass


_out = None


def output():
    """The output chosen on the command line, opened once."""
    global _out
    if _out is None:
        _out = MidiOut() if MODE == "midi" else PrintOut()
    return _out


# ------------------------------------------------------------------ playing
def play(events, cursor=(), lead_in=0.5):
    """Send the events at their times, measured from now. While playing, a vertical
    line moves along the time axis of every plot in `cursor`. Afterwards the figure
    stays open until its window is closed."""
    out = output()
    queue = []                                         # (time, order, action, event)
    for e in events:
        if e["kind"] == "note":
            queue.append((e["t"], 2, "on", e))
            queue.append((e["t"] + e["dur"], 0, "off", e))   # at equal times, offs go first
        else:
            queue.append((e["t"], 1, "cc", e))          # a controller before a note at the same time
    queue.sort(key=lambda q: (q[0], q[1]))

    screen = plt.get_fignums() and plt.get_backend().lower() != "agg"
    lines = []
    if screen:
        plt.show(block=False)
        for ax in cursor:
            limits = ax.get_xlim()
            lines.append(ax.axvline(limits[0], color="#B03A2E", linewidth=1.2))
            ax.set_xlim(limits)
        plt.pause(0.3)

    print(f"[{MODE}] {sum(1 for e in events if e['kind'] == 'note')} notes, "
          f"{sum(1 for e in events if e['kind'] == 'cc')} controller values, "
          f"{queue[-1][0] if queue else 0:.1f} s")
    start = time.perf_counter() + lead_in
    try:
        for t, _, action, e in queue:
            due = start + t
            while True:                                # wait for the deadline (step 07)
                left = due - time.perf_counter()
                if left <= 0:
                    break
                if lines and left > 0.06:              # time to spare: move the cursor
                    now = time.perf_counter() - start
                    for ln in lines:
                        ln.set_xdata([now, now])
                    plt.gcf().canvas.draw_idle()
                    plt.gcf().canvas.flush_events()
                else:
                    time.sleep(min(left, 0.001))
            if action == "on":
                out.note_on(e)
            elif action == "off":
                out.note_off(e)
            else:
                out.cc(e)
    except KeyboardInterrupt:
        print("stopped")
    finally:
        out.close()

    if plt.get_fignums():
        if screen:
            print("close the figure window to finish")
            plt.show()
        else:
            name = sys.argv[0].rsplit("/", 1)[-1].replace(".py", ".png")
            plt.savefig(name, dpi=110, bbox_inches="tight")
            print(f"[no screen: figure written to {name}]")
        plt.close("all")
