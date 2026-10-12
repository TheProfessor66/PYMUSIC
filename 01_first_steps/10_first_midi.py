"""10 · A first note in Ableton Live

mido sends MIDI. The IAC Driver carries it to Live (Audio MIDI Setup,
IAC Driver: Device is online; in Live, a MIDI track receiving from the
IAC Driver, Monitor In, with an instrument).

A note is two messages: note_on starts it, note_off ends it.

Run:  python 10_first_midi.py

Exercises
  1. Change NOTES to a chord: play all note_on messages first, then wait,
     then all note_off messages.
  2. Lower LENGTH to 0.05: short notes, the same rhythm.
  3. Send a controller before each note: mido.Message("control_change",
     control=74, value=...) and hear the filter move (if CC 74 is mapped).
"""
import time
import mido

BPM = 120
NOTES = [60, 64, 67, 72]
LENGTH = 0.4                     # seconds each note is held

ports = [name for name in mido.get_output_names() if "IAC" in name]
if not ports:
    print("No IAC Driver found: switch it on in Audio MIDI Setup.")
    raise SystemExit

out = mido.open_output(ports[0])
print("sending to", ports[0])

beat = 60 / BPM
for note in NOTES:
    print("note", note)
    out.send(mido.Message("note_on", note=note, velocity=100))
    time.sleep(LENGTH)
    out.send(mido.Message("note_off", note=note))
    time.sleep(beat - LENGTH)

out.close()
