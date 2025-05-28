# LEARNY

Learny is a simple flashcard application inspired by Anki. It stores your decks
in `~/.learny_data.json` and provides a spaced-repetition learning experience.
=======
Learny is a simple command-line flashcard application inspired by Anki. It stores your decks in `~/.learny_data.json` and provides a spaced-repetition learning experience.


## Features

- Multiple decks
- Spaced repetition based on the SM-2 algorithm
- Add and review cards from the command line
- Statistics on how many cards are due


## Command-line Usage
=======
## Usage


```bash
# create a deck
python -m learny add-deck French

# add a card to the deck
python -m learny add-card French "bonjour" "hello"

# list all decks
python -m learny list

# review due cards
python -m learny review French


## Web Interface

Learny also ships with a minimal web UI. Run the web server and open your
browser to manage your decks interactively:

```bash
python -m learny.web
```

The server listens on http://localhost:8000/ where you can add decks, add cards
and review due cards using a simple HTML interface.

