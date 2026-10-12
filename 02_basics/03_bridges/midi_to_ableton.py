"""Send MIDI notes and controllers from Python to Ableton Live (or Max).

macOS setup, once:
    Audio MIDI Setup > Window > Show MIDI Studio > IAC Driver > "Device is online".
    In Live: Settings > Link, Tempo & MIDI > IAC Driver (Bus 1): Track = On, Remote = On.
    In Max the same port appears in [notein] / [ctlin] port menus.

Install:  pip install mido python-rtmidi
Run:      python midi_to_ableton.py
"""
import time
import mido

print("outputs:", mido.get_output_names())
port_name = next(n for n in mido.get_output_names() if "IAC" in n)
out = mido.open_output(port_name)

pattern = [48, 55, 58, 60, 63, 60, 58, 55]          # MIDI note numbers
step = 60 / 120 / 2                                  # eighth notes at 120 BPM

try:
    for i in range(32):
        note = pattern[i % len(pattern)]
        out.send(mido.Message("control_change", control=74, value=(i * 4) % 128))
        out.send(mido.Message("note_on", note=note, velocity=90))
        time.sleep(step * 0.8)
        out.send(mido.Message("note_off", note=note))
        time.sleep(step * 0.2)
finally:
    out.reset()                                      # all notes off
