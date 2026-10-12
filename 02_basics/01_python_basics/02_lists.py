"""02 · Lists: a scale, a melody and its transformations

Python topics: lists [ ]; indexing (scale[2]); len(); for loops; building a new
list with .append(); slicing (melody[::-1] reverses); list comprehensions
([x + 12 for x in melody]).

Musical content: a melody is stored as positions in a scale (degrees), not as
notes. The same degrees in another scale give another melody. The four classical
transformations of a line are list operations:
    original    the list as written
    retrograde  the list reversed                       melody[::-1]
    inversion   every interval turned upside down       [-d for d in melody]
    transposed  every degree moved by the same amount   [d + 2 for d in melody]

Result: prints each form as degrees and as MIDI notes, draws them as a piano
roll (time across, pitch up), and plays the four forms one after another on
channel 1 while a cursor moves along the roll.

Run:  python 02_lists.py
      python 02_lists.py --print      (no MIDI: every message is printed)

Exercises
  1. Change SCALE to [0, 2, 3, 5, 7, 9, 10] (dorian) and run again. The degrees are
     unchanged; the notes and the plot change.
  2. Change SCALE to [0, 3, 5, 7, 10] (minor pentatonic). With five notes per
     octave, degrees 5 and above wrap into the next octave (degree 7 becomes 77,
     not 72): the function degree_to_note handles it with // and %.
  3. Add a fifth form to the dictionary forms:
     "retro-inversion": [-d for d in MELODY[::-1]],
     It appears in the plot and is played last.
"""
import matplotlib.pyplot as plt
import kit

SCALE = [0, 2, 4, 5, 7, 9, 11]       # major scale, in semitones above the root
ROOT = 60                            # C4
MELODY = [0, 2, 4, 3, 1, 4, 7, 6]    # degrees of the scale; 7 = the octave above 0
STEP = 0.22                          # seconds per note


def degree_to_note(degree):
    """Degree 0 = ROOT. Degrees beyond the scale wrap into the next octave;
    negative degrees go below."""
    octave = degree // len(SCALE)          # // : whole-number division (rounds down)
    index = degree % len(SCALE)            # %  : remainder, always 0..len-1
    return ROOT + 12 * octave + SCALE[index]


forms = {
    "original": MELODY,
    "retrograde": MELODY[::-1],
    "inversion": [-d for d in MELODY],
    "transposed +2": [d + 2 for d in MELODY],
}

events = []
plt.figure(figsize=(10, 4.5))
t = 0.0
for name, degrees in forms.items():
    notes = []
    for d in degrees:
        notes.append(degree_to_note(d))
    print(f"{name:16s} degrees {degrees}")
    print(f"{'':16s} notes   {notes}")
    times = [t + i * STEP for i in range(len(notes))]
    for when, n in zip(times, notes):
        events.append(kit.note(when, n, 90, STEP * 0.9))
    plt.hlines(notes, times, [x + STEP * 0.9 for x in times], linewidth=6)
    plt.text(t, max(notes) + 1.5, name, fontsize=9)
    t = times[-1] + STEP + 0.4

plt.xlabel("time (s)")
plt.ylabel("MIDI note")
plt.title("One melody, four forms")
plt.grid(axis="y", alpha=0.3)
plt.tight_layout()
kit.play(events, cursor=[plt.gca()])
