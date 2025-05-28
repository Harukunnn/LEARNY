# LEARNY

Learny is a simple command-line flashcard application inspired by Anki. It stores your decks in `~/.learny_data.json` and provides a spaced-repetition learning experience.

## Features

- Multiple decks
- Spaced repetition based on the SM-2 algorithm
- Add and review cards from the command line
- Statistics on how many cards are due

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
```
