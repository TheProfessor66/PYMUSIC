"""09 · Mapping

An instrument turns an input (a fader, a sensor, a face) into control values.
Inputs are kept between 0 and 1; one function scales them to any range.
This is the same idea as the scale object in Max.

Run:  python 09_mapping.py

Exercises
  1. Map the input to MIDI notes 48 to 72 and round the result with round().
  2. Replace the input list with a slow rise: [i / 20 for i in range(21)].
  3. Square the input before scaling (x ** 2): small movements change less,
     large movements change more. Compare the bars.
"""


def scale(x, out_low, out_high):
    """Map x from 0..1 to out_low..out_high."""
    return out_low + x * (out_high - out_low)


INPUT = [0.0, 0.1, 0.25, 0.5, 0.75, 0.9, 1.0]       # for example, a fader

for x in INPUT:
    cutoff = scale(x, 0, 127)                  # a MIDI controller value
    hz = scale(x, 200, 8000)                   # a filter frequency
    print(f"{x:4.2f}  CC {cutoff:5.1f}  {hz:6.0f} Hz  " + "|" * int(cutoff / 4))
