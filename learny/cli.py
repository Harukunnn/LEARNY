import argparse
from datetime import date
from typing import Dict
from .models import Deck
from .storage import load_data, save_data
from .srs import review_card


def get_deck(decks: Dict[str, Deck], name: str) -> Deck:
    if name not in decks:
        decks[name] = Deck(name=name)
    return decks[name]


def add_deck(args: argparse.Namespace, decks: Dict[str, Deck]):
    if args.name in decks:
        print("Deck already exists")
    else:
        decks[args.name] = Deck(name=args.name)
        save_data(decks)
        print(f"Added deck '{args.name}'")


def add_card(args: argparse.Namespace, decks: Dict[str, Deck]):
    deck = get_deck(decks, args.deck)
    deck.add_card(args.question, args.answer)
    save_data(decks)
    print("Card added")


def list_decks(args: argparse.Namespace, decks: Dict[str, Deck]):
    for name, deck in decks.items():
        stats = deck.stats()
        print(f"{name}: {stats['total']} cards, {stats['due']} due")


def review(args: argparse.Namespace, decks: Dict[str, Deck]):
    deck = get_deck(decks, args.deck)
    due = deck.due_cards()
    if not due:
        print("No cards due")
        return
    for card in due:
        review_card(card)
    save_data(decks)


def main():
    parser = argparse.ArgumentParser(description="Learny flashcards")
    sub = parser.add_subparsers(dest="cmd")

    deck_parser = sub.add_parser("add-deck", help="Create a new deck")
    deck_parser.add_argument("name")

    card_parser = sub.add_parser("add-card", help="Add card to deck")
    card_parser.add_argument("deck")
    card_parser.add_argument("question")
    card_parser.add_argument("answer")

    list_parser = sub.add_parser("list", help="List decks")

    review_parser = sub.add_parser("review", help="Review due cards")
    review_parser.add_argument("deck")

    args = parser.parse_args()
    decks = load_data()

    if args.cmd == "add-deck":
        add_deck(args, decks)
    elif args.cmd == "add-card":
        add_card(args, decks)
    elif args.cmd == "list":
        list_decks(args, decks)
    elif args.cmd == "review":
        review(args, decks)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
