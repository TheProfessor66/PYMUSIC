"""07 · Time: why a sequencer drifts and how to stop it

Python topics: the time module (time.perf_counter() reads a precise clock in
seconds, time.sleep() pauses); measuring by subtracting two readings; writing a
loop in two ways and comparing them by measurement; threading, to run the two
loops at the same time.

Musical content: a sequencer has to fire step n at exactly start + n * step.
Two ways of writing the loop:

  SLEEP-AFTER    do the step's work, then sleep one step length.
                 The work time and every late wake-up add up: the loop drifts.

  DEADLINE       compute when step n is due, wait until that moment, then work.
                 A late step does not push the next one: no drift.

Both loops run at the same time and send a note at every step: sleep-after on
channel 1 (high note), deadline on channel 2 (low note), with an accent every
four steps. Each step also does 1-6 ms of "work" (standing in for reading a
camera frame or sending messages). They start together and audibly separate:
first a flam, then two different rhythms. Each loop records when its steps
actually happened.

Result: the two loops play in Live; afterwards the error of every 8th step
is printed and the error of every step is plotted.

Run:  python 07_clock.py
      python 07_clock.py --print      (no MIDI: every message is printed)

Exercises
  1. Set WORK = (0, 0). The drift becomes smaller but does not disappear: sleep()
     always wakes a little late.
  2. Set WORK = (5, 15). The sleep-after loop now drifts by about 10 ms per step;
     the deadline loop is unchanged as long as the work is shorter than a step.
  3. Set WORK = (140, 160), longer than a step (125 ms). Now the deadline loop
     falls behind too, by the excess of every step: no clock can keep time if the
     work does not fit in the step.
"""
import random
import threading
import time
import numpy as np
import matplotlib.pyplot as plt
import kit

STEP = 0.125          # sixteenth notes at 120 BPM
STEPS = 64            # four bars
WORK = (1, 6)         # each step does this many milliseconds of work (random in the range)

out = kit.output()
lock = threading.Lock()   # one output, two loops: they take turns to send


held = {}                 # the note each loop is holding, switched off at its next step


def step(n, channel, pitch):
    """What happens at each step: end the previous note, start a new one, do some work."""
    e = kit.note(0, pitch, 110 if n % 4 == 0 else 70, 0.1, channel)
    with lock:
        if channel in held:
            out.note_off(held[channel])
        out.note_on(e)
        held[channel] = e
    time.sleep(random.uniform(*WORK) / 1000)


def sleep_after(start, times):
    while time.perf_counter() < start:
        time.sleep(0.0005)
    for n in range(STEPS):
        times.append(time.perf_counter() - start)
        step(n, 1, 84)
        time.sleep(STEP)


def deadline(start, times):
    for n in range(STEPS):
        due = start + n * STEP
        while time.perf_counter() < due:          # wait for the deadline in small naps
            time.sleep(0.0005)
        times.append(time.perf_counter() - start)
        step(n, 2, 48)


a, b = [], []
start = time.perf_counter() + 0.5
threads = [threading.Thread(target=sleep_after, args=(start, a)),
           threading.Thread(target=deadline, args=(start, b))]
print(f"[{kit.MODE}] playing both loops for {STEPS * STEP:.0f} s: sleep-after on channel 1, deadline on channel 2")
for th in threads:
    th.start()
for th in threads:
    th.join()
for e in held.values():
    out.note_off(e)
out.close()

err_a = [(t - n * STEP) * 1000 for n, t in enumerate(a)]      # ms late
err_b = [(t - n * STEP) * 1000 for n, t in enumerate(b)]
print("\nstep   sleep-after late   deadline late")
for n in range(0, STEPS, 8):
    print(f"{n:4d}   {err_a[n]:10.1f} ms     {err_b[n]:8.2f} ms")
print(f"\nsleep-after drifts {err_a[-1] / (STEPS / 16):.1f} ms per bar; "
      f"deadline worst error {max(err_b):.2f} ms")

plt.figure(figsize=(9, 3.8))
plt.plot(err_a, ".-", label="sleep-after")
plt.plot(err_b, ".-", label="deadline")
plt.axhline(STEP * 1000, color="0.6", linestyle=":", label="one full step")
plt.xlabel("step")
plt.ylabel("lateness (ms)")
plt.title("How late each step was")
plt.legend()
plt.tight_layout()
kit.play([])                  # nothing more to send: shows the figure
