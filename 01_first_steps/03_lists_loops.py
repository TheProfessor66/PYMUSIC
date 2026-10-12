"""03 · Lists and loops

A list keeps several values in order: [60, 62, 64].
notes[0] is the first value, notes[-1] the last, len(notes) counts them.
A for loop repeats the indented lines once for each value in the list.

Run:  python 03_lists_loops.py

Exercises
  1. Add 72 at the end of NOTES. The loop plays one more line.
  2. Change TRANSPOSE to 7: every note moves up a fifth.
  3. Print the notes backwards with: for note in NOTES[::-1]:
"""

NOTES = [60, 62, 64, 65, 67]     # MIDI note numbers: C D E F G
TRANSPOSE = 0

print("first note:", NOTES[0])
print("last note:", NOTES[-1])
print("number of notes:", len(NOTES))
print()

# the indented lines run once per note
for note in NOTES:
    played = note + TRANSPOSE
    print(played, "#" * (played - 55))     # a bar as long as the pitch is high

print()

# range(n) gives 0, 1, 2 ... n-1: useful for counting steps
for step in range(8):
    print("step", step)
