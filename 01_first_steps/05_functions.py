"""05 · Functions

def gives a name to a few lines of code, so they can be used many times.
Values go in through the parameters, a result comes out with return.
A parameter can have a default value: def beat_seconds(bpm=120).

Run:  python 05_functions.py

Exercises
  1. Call mtof(69) and check it prints 440.0.
  2. Write a function octave_up(note) that returns note + 12, and print
     octave_up(60).
  3. Call clamp(150, 0, 127) and clamp(-5, 0, 127): the results stay
     inside the MIDI range.
"""


def beat_seconds(bpm=120):
    """Seconds per beat at a tempo."""
    return 60 / bpm


def mtof(note):
    """MIDI note number to frequency in Hz. Note 69 is A, 440 Hz."""
    return 440 * 2 ** ((note - 69) / 12)


def clamp(value, low, high):
    """Keep a value between low and high."""
    if value < low:
        return low
    if value > high:
        return high
    return value


print(beat_seconds())          # uses the default, 120
print(beat_seconds(90))
print()

for note in [57, 60, 64, 67, 69]:
    print(note, f"{mtof(note):.2f} Hz")
print()

print(clamp(200, 0, 127))
