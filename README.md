# LEARNY

Learny is a lightweight flashcard application implemented in pure Python. It
stores all decks in `~/.learny_data.json` and schedules reviews using a simple
SM‑2 spaced‑repetition algorithm.  A Tkinter GUI lets you manage your cards and
review them when they become due.

## Features

- Multiple decks
- Spaced repetition (SM‑2)
- Desktop GUI to add and review cards
- Optional command‑line and web interfaces

## Usage

Start the GUI with:

```bash
python -m learny
```

Within the window you can create decks, add cards and review any cards that are
due for the day.

### Command‑line interface

The CLI is still available for quick actions:

```bash
python -m learny add-deck <name>
python -m learny add-card <deck> <question> <answer>
python -m learny list
python -m learny review <deck>
```

### Web interface

A very small web server can also be started with:

```bash
python -m learny.web
```

Open <http://localhost:8000/> to manage your decks from the browser.

