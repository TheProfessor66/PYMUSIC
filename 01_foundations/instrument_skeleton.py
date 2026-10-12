"""The layers of an instrument, each as a small replaceable part.

    INPUT -> FEATURES -> CONDITIONING -> MAPPING -> BEHAVIOUR -> OUTPUT
    camera,   numbers     smoothing,     which      time, state,  MIDI, OSC
    sensors,  per frame   calibration    feature    rules         to Live, Max,
    replay                               drives what              MMMAudio

The mapping is data (mapping.json), not code: it can be edited, versioned
and compared without touching the program.

Run without hardware (replays a recorded face stream, prints the MIDI it would send):
    python instrument_skeleton.py
Send real MIDI to the IAC bus instead:
    python instrument_skeleton.py --midi
Use another mapping file (one per group, for example):
    python instrument_skeleton.py --midi --mapping drone.json
"""
import argparse
import json

import replay
from conditioning import Chain, Hysteresis

# ---------------------------------------------------------------- output layer
class PrintOut:
    def cc(self, ch, cc, value):   print(f"CC   ch{ch} #{cc:<3d} {value:3d}")
    def note(self, ch, note, vel): print(f"NOTE ch{ch} {note:3d} vel {vel}")

class MidiOut:
    def __init__(self):
        import mido
        self.mido = mido
        self.port = mido.open_output(next(n for n in mido.get_output_names() if "IAC" in n))
    def cc(self, ch, cc, value):
        self.port.send(self.mido.Message("control_change", channel=ch - 1, control=cc, value=value))
    def note(self, ch, note, vel):
        kind = "note_on" if vel else "note_off"
        self.port.send(self.mido.Message(kind, channel=ch - 1, note=note, velocity=vel))

# ---------------------------------------------------------------- the instrument
class Instrument:
    def __init__(self, config, out):
        self.out = out
        self.cont = config["continuous"]               # a list: one feature may appear several times
        self.trig = {m["feature"]: m for m in config["triggers"]}
        self.chains = {m["feature"]: Chain(**m.get("conditioning", {})) for m in self.cont}
        self.gates = {f: Hysteresis(m["low"], m["high"]) for f, m in self.trig.items()}
        self.last_cc = {}
        self.step = 0                      # behaviour: state that persists between frames
        self.scale = config["behaviour"]["scale"]

    def frame(self, t, features):
        # conditioning + mapping: continuous features -> controllers
        values = {f: chain(features[f], t) for f, chain in self.chains.items()}
        targets = {}                                   # (channel, cc) -> contributions
        for m in self.cont:
            lo, hi = m.get("range", [0, 127])          # e.g. [127, 0] inverts
            targets.setdefault((m["channel"], m["cc"]), []).append(lo + values[m["feature"]] * (hi - lo))
        for key, vals in targets.items():              # several features on one CC: many-to-one, averaged
            value = int(round(sum(vals) / len(vals)))
            if self.last_cc.get(key) != value:        # send only changes
                self.out.cc(key[0], key[1], value)
                self.last_cc[key] = value
        # behaviour: a trigger feature steps through a scale, one note per event
        for f, m in self.trig.items():
            event = self.gates[f](features[f])
            if event == "on":
                note = m["root"] + self.scale[self.step % len(self.scale)]
                self.out.note(m["channel"], note, 100)
                self.step += 1
            elif event == "off":
                prev = m["root"] + self.scale[(self.step - 1) % len(self.scale)]
                self.out.note(m["channel"], prev, 0)

    def calibrate(self, frames):
        for chain in self.chains.values():
            chain.cal.start()
        for t, feats in frames:
            for f in self.chains:
                self.chains[f](feats[f], t)
        for chain in self.chains.values():
            chain.cal.finish()

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--midi", action="store_true")
    ap.add_argument("--stream", default="gesture_example.csv")
    ap.add_argument("--mapping", default="mapping.json")
    a = ap.parse_args()
    config = json.load(open(a.mapping))
    inst = Instrument(config, MidiOut() if a.midi else PrintOut())
    inst.calibrate(replay.read(a.stream)[:150])        # first 5 s as calibration
    for t, feats in replay.play(a.stream, realtime=a.midi):
        inst.frame(t, feats)
