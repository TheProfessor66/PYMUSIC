"""01 · Running a program and printing

A Python file is a list of instructions, run from top to bottom.
print() shows text in the Terminal. A line starting with # is a comment:
Python ignores it.

Run:  python 01_print.py

Exercises
  1. Add a line that prints the name of an instrument. Run again.
  2. Remove one of the quotes in a print line and run: Python stops with a
     SyntaxError and names the line. Put the quote back.
  3. Print a line of 32 dashes with print("-" * 32).
"""

# text is written between quotes
print("Hello")
print("Python reads this file from top to bottom.")

# numbers are written without quotes; Python calculates them
print(120 / 60)

# several values in one print, separated by commas
print("Beats per second at 120 BPM:", 120 / 60)
