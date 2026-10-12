# Python basics, step by step

Eleven short programs, from basic to intermediate. Python computes, prints and draws; the sound comes from Ableton Live, through MIDI. Max is a control surface: four faders that steer the real-time instrument of step 11. Each file begins with what it teaches, what it does, and a list of exercises; every exercise is a change to a value or a few lines, with a result that can be heard or seen.

```bash
cd 02_basics/01_python_basics
python 01_numbers.py            # MIDI to Live through the IAC Driver
python 01_numbers.py --print    # no MIDI: prints every message
```

A figure opens and a red cursor moves along it while the events are sent; close the figure window to finish.

## Live

1. **IAC Driver, once.** Audio MIDI Setup → Window → Show MIDI Studio → IAC Driver → tick "Device is online".
2. **Live → Settings → Link, Tempo & MIDI.** Under Input Ports, "IAC Driver (Bus 1)": Track and Remote on.
3. **Three MIDI tracks**, Monitor set to In:

| Track | MIDI From | Instrument | Used by |
|---|---|---|---|
| Melody | IAC Driver, Ch. 1 | any synth with a filter (Wavetable, Drift, Analog) | all steps |
| Bass | IAC Driver, Ch. 2 | any bass sound | 05, 07, 10, 11 |
| Drums | IAC Driver, Ch. 10 | Drum Rack: C1 (36) kick, C#1 (37) rim, D1 (38) snare, D#1 (39) clap, F#1 (42) hat | 04, 05, 10, 11 |

4. **CC 74 to the filter, once.** Cmd+M (MIDI Map mode), click the Melody synth's filter frequency, run `python 03_functions.py`, Cmd+M again. Steps 03, 08, 09 and 11 move it.

Save this set; every step uses it.

## Max

`control.maxpat` holds four faders and sends each movement as `/fader <number> <0-127>` to Python on port 9001. Only step 11 listens to it. A MIDI controller can be used instead: CC 1 to 4 move faders 1 to 4 (`FADER_CCS` in `11_live.py`).

## Steps

| Step | Python | Music and instruments | Seen | Heard |
|---|---|---|---|---|
| `01_numbers.py` | names, arithmetic, print, f-strings | note numbers and frequencies; intervals as ratios | frequency table; waveforms | root, fifth, octave |
| `02_lists.py` | lists, indexing, slicing, loops, comprehensions | scale degrees; retrograde, inversion, transposition | piano roll | the four forms |
| `03_functions.py` | def, parameters, return | control shapes: ramp, LFO, sample-and-hold, envelope | the shapes | a chord, filter moved by each shape |
| `04_step_sequencer.py` | dictionaries of lists, nested loops, if, % | step grid, swing, polymeter | onsets against the grid | drum pattern |
| `05_euclidean.py` | a function returning a list; rotation; math.lcm | Euclidean rhythms; two cycles against each other | necklaces | each rhythm; the layered pair |
| `06_markov.py` | nested dictionaries, weighted random, seed, counting | Markov melody | designed vs measured probabilities | the melody |
| `07_clock.py` | time, measurement, threads | why loops drift; the deadline clock | lateness per step | two loops separating |
| `08_smoothing.py` | state in a loop; filtering a list; statistics | jitter and lag of control data | raw and filtered signals | the filter driven by each |
| `09_mapping.py` | mapping as data; functions in a dictionary | one gesture to four parameters; curves | curves and traces | the resulting phrase |
| `10_classes.py` | class, __init__, self, methods, `__main__` guard | tracks with their own state; polymeter | track plot | eight bars, three channels |
| `11_live.py` | importing a module; receiving while playing; a lock; try/finally | a complete real-time instrument: input, mapping, behaviour, output | live step display | the tracks, changed by the Max faders or a MIDI controller |

`kit.py` holds the shared parts: `note()`, `cc()`, `play()`, the MIDI output and the printed output.
