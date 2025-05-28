# LEARNY

Learny is a simple command-line flashcard application inspired by Anki. It stores your decks in `~/.learny_data.json` and provides a spaced-repetition learning experience.

## Features

- Multiple decks
- Spaced repetition based on the SM-2 algorithm
- Add and review cards from the command line
- Tags for cards
- Import/Export decks as JSON
- Manage decks and cards (list, tag, delete)
- Statistics on how many cards are due

## Usage

```bash
# create a deck
python -m learny add-deck French

# add a card to the deck
python -m learny add-card French "bonjour" "hello" --tags=greeting,basic

# list all decks
python -m learny list

# list cards in a deck
python -m learny list-cards French

# add a tag to an existing card (use the card id from list-cards)
python -m learny tag-card French <card_id> vocab

# review due cards
python -m learny review French

# export a deck
python -m learny export-deck French french.json

# import a deck into a new deck
python -m learny import-deck NewDeck french.json
```
