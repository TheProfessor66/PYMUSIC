# PYMUSIC

Python as the control, logic and architecture layer of musical instruments. Sound is made by Ableton Live; Max is used as a control surface.

## Install (macOS, Apple Silicon)

```bash
mkdir -p ~/PycharmProjects && cd ~/PycharmProjects
git clone https://github.com/TheProfessor66/PYMUSIC.git
cd PYMUSIC
curl -LsSf https://astral.sh/uv/install.sh | sh          # once, if uv is not installed
uv venv --python 3.13 --prompt pymusic
uv pip install -r requirements.txt
```

## Open in PyCharm

1. File → Open → `~/PycharmProjects/PYMUSIC` → New Window.
2. Settings → Project → Python Interpreter → Add Interpreter → Add Local Interpreter → Select existing → `.venv/bin/python`.
3. Run scripts from PyCharm's Terminal, inside each folder (the scripts read files next to them):

```bash
cd 01_first_steps && python 01_print.py
```

Every script states at its top what it does and how to run it.

| Folder | Contents | Runs without hardware |
|---|---|---|
| `01_first_steps` | ten very short programs: print, names, lists, conditions, functions, dictionaries, time, chance, mapping, a first MIDI note | yes, except the last one |
| `02_basics/01_python_basics` | eleven steps from basic to intermediate Python, each with a figure, played by Live (MIDI); `kit.py`; `control.maxpat` (four faders for step 11) | `--print` shows the messages; sound needs Live |
| `02_basics/02_foundations` | `conditioning.py`, `one_euro.py`, `replay.py`, `instrument_skeleton.py`, `mapping.json`, `gesture_example.csv` | yes (`--midi` sends to Live) |
| `02_basics/03_bridges` | `midi_to_ableton.py`, `osc_to_max.py`: the two connections, each in a few lines | needs Live or Max |

## First runs, without hardware

```bash
cd 01_first_steps
python 01_print.py           # then 02 to 10 in order
cd ../02_basics/01_python_basics
python 01_numbers.py --print        # then 02 to 11 in order
cd ../02_foundations
python instrument_skeleton.py
```

## With hardware

- **MIDI to Live:** Audio MIDI Setup → MIDI Studio → IAC Driver → "Device is online"; in Live, the IAC Driver input on for Track and Remote. The steps send MIDI by default; the scripts in `02_basics/02_foundations` with `--midi`.
- **Max:** open `02_basics/01_python_basics/control.maxpat` and run `python 11_live.py`; the faders arrive as `/fader <number> <0-127>` on port 9001.
