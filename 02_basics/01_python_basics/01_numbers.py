"""01 · Numbers, names and print

Python topics: a name holds a value (NOTE = 57); arithmetic (+ - * / **);
print() with f-strings; calling a function (kit.mtof, kit.note).

Musical content: a MIDI note number becomes a frequency. Each semitone multiplies
the frequency by 2 ** (1/12); twelve semitones double it (one octave). An
interval is a ratio of frequencies: a fifth is close to 3/2, an octave is 2/1.

Result: prints a table of the twelve notes of one octave with their frequencies
and ratios; draws 20 ms of the three waves (root, second tone, octave); sends the
three notes to Live one after another, then together.

Run:  python 01_numbers.py
      python 01_numbers.py --print      (no MIDI: every message is printed)

Exercises
  1. Change NOTE to 60 (middle C). The table, the plot and the sound move; the
     ratios do not.
  2. Change SECOND to 6 (a tritone). The printed ratio becomes 1.414, the square
     root of 2: no small whole-number ratio, so the plotted waves do not realign
     within the window, and the chord sounds rough.
  3. Set SECOND = 4 (a major third) and PURE = 5 / 4. The equal-tempered third is
     printed as 13.7 cents wider than the pure third: about seven times the error
     of the fifth, and audible as a slow beating in the held chord.
"""
import math
import numpy as np
import matplotlib.pyplot as plt
import kit

NOTE = 57          # MIDI note number: 57 = A3
SECOND = 7         # semitones above NOTE for the second tone
A4 = 440.0         # tuning reference in Hz
PURE = 3 / 2       # the pure (whole-number) ratio the second tone is compared with


def mtof(note):                                   # the same formula as kit.mtof, with A4 as reference
    return A4 * 2 ** ((note - 69) / 12)


# --- a table: one line per semitone
names = ["A", "A#", "B", "C", "C#", "D", "D#", "E", "F", "F#", "G", "G#"]
print("note  name  freq (Hz)   ratio to root")
for i in range(13):
    n = NOTE + i
    f = mtof(n)
    print(f"{n:4d}  {names[(n - 69) % 12]:4s}  {f:9.2f}   {f / mtof(NOTE):.4f}  " + "#" * int(f / 20))

root = mtof(NOTE)
second = mtof(NOTE + SECOND)
octave = mtof(NOTE + 12)
ratio = second / root
cents = 1200 * math.log2(ratio / PURE)
print(f"\nroot {root:.2f} Hz   second tone {second:.2f} Hz   ratio {ratio:.4f}")
print(f"difference from the pure ratio {PURE:.4f}: {cents:+.2f} cents")

# --- the picture: 20 ms of each wave
t = np.arange(0, 0.02, 1 / 20000)
plt.figure(figsize=(9, 4))
for f, label in ((root, "root"), (second, f"+{SECOND} semitones"), (octave, "octave")):
    plt.plot(t * 1000, np.sin(2 * np.pi * f * t), label=f"{label}: {f:.1f} Hz")
plt.xlabel("time (ms)")
plt.ylabel("amplitude")
plt.title("The first 20 ms of each tone")
plt.legend(loc="upper right")
plt.tight_layout()

# --- the sound: three notes in turn, then together. MIDI sends key numbers.
events = []
for i, f in enumerate((root, second, octave)):
    events.append(kit.note(i * 0.7, round(kit.ftom(f)), 90, 0.6))
    events.append(kit.note(2.4, round(kit.ftom(f)), 80, 2.0))
kit.play(events)
