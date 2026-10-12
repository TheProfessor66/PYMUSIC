"""07 · Time

time.sleep(s) waits s seconds. time.perf_counter() reads a precise clock.
import makes the tools of a module available: import time.
A while loop repeats as long as its condition is true.
Ctrl+C stops a program at any time.

Run:  python 07_time.py

Exercises
  1. BPM = 60: the ticks slow down to one per second.
  2. TICKS = 16 and a different mark every fourth tick (use %).
  3. Print how late each tick is: compare time.perf_counter() with start + i * beat.
"""
import time

BPM = 120
TICKS = 8

beat = 60 / BPM
start = time.perf_counter()

i = 0
while i < TICKS:
    now = time.perf_counter() - start
    print(f"tick {i}   {now:.3f} s")
    time.sleep(beat)
    i += 1          # same as i = i + 1

print("done")
