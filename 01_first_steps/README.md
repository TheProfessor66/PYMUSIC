# 01_first_steps

Ten short programs, for a first contact with Python, before `02_basics/01_python_basics`. They print in the Terminal; only the last one sends MIDI to Live.

| File | Python | Content |
|---|---|---|
| `01_print.py` | running a file, `print`, comments | text and numbers in the Terminal |
| `02_names.py` | names, arithmetic, f-strings | tempo, beat and step durations |
| `03_lists_loops.py` | lists, indexing, `for`, `range` | a melody as a list of notes |
| `04_conditions.py` | `if`, `elif`, `else`, `%` | velocities in words; kick and hi-hat on a grid |
| `05_functions.py` | `def`, parameters, `return`, defaults | beat length, note to frequency, clamping |
| `06_dictionaries.py` | dictionaries, `.items()` | a drum map and a step pattern |
| `07_time.py` | `import`, `time`, `while` | a ticking metronome |
| `08_random.py` | `random`, seeds | a random melody on a scale |
| `09_mapping.py` | a mapping function | one input from 0 to 1 scaled to several ranges |
| `10_first_midi.py` | a package: `mido` | notes sent to Ableton Live |

Each file starts with what it does, how to run it and three exercises.

```bash
cd 01_first_steps
python 01_print.py
```
