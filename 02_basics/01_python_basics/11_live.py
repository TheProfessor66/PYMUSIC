"""11 · A complete loop: input, mapping, behaviour, output, in real time

Python topics: importing your own module (the tracks from step 10); a deadline
clock running for real (step 07); receiving messages while the clock runs (a
server in a background thread that calls a function for every message);
shared state between the two, protected by a lock; try/finally, so all notes
stop when the program is stopped.

Musical content: this is the shape of every instrument in the projects:

    INPUT          ->  MAPPING          ->  BEHAVIOUR     ->  OUTPUT
    four faders        on_fader():          the tracks        MIDI to Live
    (Max or a MIDI     fader 1: density     of step 10
    controller)        fader 2: filter

The input is four faders, 0..1 each, from either
    - control.maxpat: four sliders that Max sends as /fader <number> <0-127>
      to port 9001, or
    - a MIDI controller connected to the computer: the CC numbers listed in
      FADER_CCS (1 to 4 by default) move faders 1 to 4.
Fader 1 changes the density of the "perc" track (1 to 12 onsets in 12 steps)
and how often the melody plays (every 4th, 2nd or every step). Fader 2 is the
filter cutoff of channel 1 (CC 74). Faders 3 and 4 are free for the exercises.

Result: one line per step in the terminal: which tracks fired, faders 1 and 2
as bars, and how late the step was. Stop with Ctrl+C or PyCharm's red square.

Run:  python 11_live.py                       Max: open control.maxpat first
      python 11_live.py --bpm 90 --bars 64
      python 11_live.py --print               no MIDI: every message is printed

Exercises
  1. Move fader 1 slowly from bottom to top and watch the perc track's onsets
     appear in the terminal one by one: always evenly spread (step 05).
  2. Map fader 3 to the bass: in on_fader(), when index == 3, set
     bass.k = 1 + round(value * 7). The bass goes from 1 to 8 onsets per bar.
  3. Map fader 4 to the rotation of the "high" track:
     by_name["high"].rotation = int(value * 8).
  4. Smooth the filter in the clock loop with the one-pole of step 08: keep
     state["smooth"], move it once per step with
     state["smooth"] += 0.2 * (faders[2] - state["smooth"]), and send that as
     CC 74. A sudden jump of fader 2 becomes a glide over about one bar.
"""
import argparse
import importlib
import threading
import time
import kit

tracks_module = importlib.import_module("10_classes")      # a file name starting with a digit needs this form

ap = argparse.ArgumentParser()
ap.add_argument("--print", action="store_true")
ap.add_argument("--bpm", type=float, default=112)
ap.add_argument("--bars", type=int, default=32)
args = ap.parse_args()

FADER_CCS = {1: 1, 2: 2, 3: 3, 4: 4}        # MIDI controller: CC number -> fader number

tracks = tracks_module.make_tracks()
by_name = {tr.name: tr for tr in tracks}
state = {"faders": {1: 0.5, 2: 0.5, 3: 0.5, 4: 0.5}}       # shared between the input thread and the clock
lock = threading.Lock()


# ------------------------------------------------------------------ mapping
def on_fader(index, value):
    """index 1..4, value 0..1. Runs in the input thread, every time a fader moves."""
    with lock:
        state["faders"][index] = value
        if index == 1:
            perc = by_name["perc"]
            perc.k = 1 + round(value * (perc.n - 1))
            by_name["melody"].every = 4 if value < 0.33 else (2 if value < 0.66 else 1)


# ------------------------------------------------------------------ inputs
def listen_osc(port=9001):
    from pythonosc.dispatcher import Dispatcher
    from pythonosc.osc_server import ThreadingOSCUDPServer
    d = Dispatcher()
    d.map("/fader", lambda address, index, value: on_fader(int(index), float(value) / 127))
    server = ThreadingOSCUDPServer(("127.0.0.1", port), d)
    threading.Thread(target=server.serve_forever, daemon=True).start()
    print(f"listening for /fader from Max on port {port}")


def listen_midi():
    import mido
    names = [n for n in mido.get_input_names() if "IAC" not in n]
    if not names:
        return
    def callback(msg):
        if msg.type == "control_change" and msg.control in FADER_CCS:
            on_fader(FADER_CCS[msg.control], msg.value / 127)
    mido.open_input(names[0], callback=callback)
    print(f"listening for CC {list(FADER_CCS)} from {names[0]}")


listen_osc()
try:
    listen_midi()
except Exception as e:
    print("no MIDI input:", e)
for i in range(1, 5):
    on_fader(i, state["faders"][i])

# ------------------------------------------------------------------ clock and output
out = kit.output()
step_len = 60 / args.bpm / 4
print(f"[{kit.MODE}] {args.bpm} BPM, step {step_len * 1000:.1f} ms; tracks: {', '.join(t.name for t in tracks)}\n")
held = []
start = time.perf_counter() + 0.3
try:
    for step in range(args.bars * 16):
        due = start + step * step_len
        while time.perf_counter() < due:
            time.sleep(0.0005)
        late = (time.perf_counter() - due) * 1000
        for e in held:
            out.note_off(e)
        held = []
        marks = ""
        with lock:
            faders = dict(state["faders"])
            out.cc(kit.cc(0, 74, faders[2] * 127, channel=1))
            for tr in tracks:
                note = tr.tick(step)
                if note is not None:
                    e = kit.note(0, note, 100, step_len * 0.9, tr.channel)
                    out.note_on(e)
                    held.append(e)
                marks += f" {tr.name[:4]:>4s}" if note is not None else "    ."
        bar = "|" if step % 16 == 0 else " "
        f1 = "#" * int(faders[1] * 10)
        f2 = "#" * int(faders[2] * 10)
        print(f"{bar}{step:4d} {marks}   f1 {f1:10s} f2 {f2:10s}  late {late:4.2f} ms")
except KeyboardInterrupt:
    print("stopped")
finally:
    for e in held:
        out.note_off(e)
    out.close()
