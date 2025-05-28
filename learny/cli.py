import argparse
import json
from datetime import date
from pathlib import Path
from typing import Dict, List
from .models import Deck, Flashcard
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
    tags = [t.strip() for t in (args.tags or [])]
    deck.add_card(args.question, args.answer, tags=tags)
    save_data(decks)
    print("Card added")


def list_decks(args: argparse.Namespace, decks: Dict[str, Deck]):
    for name, deck in decks.items():
        stats = deck.stats()
        print(f"{name}: {stats['total']} cards, {stats['due']} due")


def list_cards(args: argparse.Namespace, decks: Dict[str, Deck]):
    deck = get_deck(decks, args.deck)
    for card in deck.cards:
        tags = ",".join(card.tags)
        print(f"{card.id} | {card.question} | due {card.review_date} | {tags}")


def tag_card(args: argparse.Namespace, decks: Dict[str, Deck]):
    deck = get_deck(decks, args.deck)
    card = next((c for c in deck.cards if c.id == args.card_id), None)
    if not card:
        print("Card not found")
        return
    if args.tag not in card.tags:
        card.tags.append(args.tag)
        save_data(decks)
    print("Tag added")


def export_deck(args: argparse.Namespace, decks: Dict[str, Deck]):
    deck = decks.get(args.deck)
    if not deck:
        print("Deck not found")
        return
    Path(args.file).write_text(json.dumps([c.to_dict() for c in deck.cards], indent=2))
    print("Deck exported")


def import_deck(args: argparse.Namespace, decks: Dict[str, Deck]):
    deck = get_deck(decks, args.deck)
    data = json.loads(Path(args.file).read_text())
    for c in data:
        deck.cards.append(Flashcard.from_dict(c))
    save_data(decks)
    print("Deck imported")


def delete_deck(args: argparse.Namespace, decks: Dict[str, Deck]):
    if args.name in decks:
        del decks[args.name]
        save_data(decks)
        print("Deck deleted")
    else:
        print("Deck not found")


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
    card_parser.add_argument("--tags", type=lambda s: s.split(","), default=[], help="comma separated tags")

    list_parser = sub.add_parser("list", help="List decks")

    list_cards_parser = sub.add_parser("list-cards", help="List cards in deck")
    list_cards_parser.add_argument("deck")

    tag_parser = sub.add_parser("tag-card", help="Add tag to a card")
    tag_parser.add_argument("deck")
    tag_parser.add_argument("card_id")
    tag_parser.add_argument("tag")

    export_parser = sub.add_parser("export-deck", help="Export deck to file")
    export_parser.add_argument("deck")
    export_parser.add_argument("file")

    import_parser = sub.add_parser("import-deck", help="Import deck from file")
    import_parser.add_argument("deck")
    import_parser.add_argument("file")

    delete_parser = sub.add_parser("delete-deck", help="Delete a deck")
    delete_parser.add_argument("name")

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
    elif args.cmd == "list-cards":
        list_cards(args, decks)
    elif args.cmd == "tag-card":
        tag_card(args, decks)
    elif args.cmd == "export-deck":
        export_deck(args, decks)
    elif args.cmd == "import-deck":
        import_deck(args, decks)
    elif args.cmd == "delete-deck":
        delete_deck(args, decks)
    elif args.cmd == "review":
        review(args, decks)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
