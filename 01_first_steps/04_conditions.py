"""04 · Decisions: if, elif, else

if runs its indented lines only when a condition is true.
Comparisons:  ==  equal   !=  not equal   <  >  <=  >=
%  gives the remainder of a division: step % 4 == 0 is true on every beat.

Run:  python 04_conditions.py

Exercises
  1. Change the velocity limits so that 64 counts as "loud".
  2. Make the hi-hat play on odd steps only: step % 2 == 1.
  3. Add a snare on steps 4 and 12: if step == 4 or step == 12:
"""

# a velocity (0-127) described in words
for velocity in [20, 64, 100, 127]:
    if velocity < 40:
        word = "soft"
    elif velocity < 90:
        word = "medium"
    else:
        word = "loud"
    print(velocity, word)

print()

# one bar of sixteen steps: kick on every beat, hi-hat on even steps
for step in range(16):
    line = f"{step:2d} "
    if step % 4 == 0:
        line += "KICK "
    if step % 2 == 0:
        line += "hat"
    print(line)
