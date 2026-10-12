"""02 · Names and numbers

A name stores a value so it can be used later: BPM = 120.
Names in capitals are settings: values meant to be changed.
Arithmetic:  +  -  *  /   and  **  for powers.
An f-string puts values inside text: f"{BPM} BPM".

Run:  python 02_names.py

Exercises
  1. BPM = 90: every printed value changes, the code does not.
  2. STEPS_PER_BEAT = 3: triplets instead of sixteenths.
  3. Add a name BARS = 8 and print how long eight bars last in seconds.
"""

BPM = 120               # beats per minute
STEPS_PER_BEAT = 4      # four steps per beat: sixteenth notes
BEATS_PER_BAR = 4

beat = 60 / BPM                         # seconds per beat
step = beat / STEPS_PER_BEAT            # seconds per step
bar = beat * BEATS_PER_BAR              # seconds per bar

print(f"{BPM} BPM")
print(f"one beat lasts {beat} s")
print(f"one step lasts {step * 1000} ms")
print(f"one bar lasts {bar} s")

# rounding for display: :.1f means one decimal
print(f"one step lasts {step * 1000:.1f} ms")
