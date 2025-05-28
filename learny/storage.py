import json
from pathlib import Path
from typing import Dict
from .models import Deck, Flashcard

DATA_FILE = Path.home() / ".learny_data.json"

def load_data() -> Dict[str, Deck]:
    decks: Dict[str, Deck] = {}
    if DATA_FILE.exists():
        data = json.loads(DATA_FILE.read_text())
        for name, cards in data.items():
            deck = Deck(name=name)
            for c in cards:
                card = Flashcard(**c)
                deck.cards.append(card)
            decks[name] = deck
    return decks

def save_data(decks: Dict[str, Deck]) -> None:
    data = {name: [c.__dict__ for c in deck.cards] for name, deck in decks.items()}
    DATA_FILE.write_text(json.dumps(data, default=str, indent=2))
