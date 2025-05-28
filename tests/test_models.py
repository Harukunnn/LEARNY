import unittest
from datetime import date
from learny.models import Flashcard, Deck

class TestFlashcard(unittest.TestCase):
    def test_update_quality(self):
        card = Flashcard(question="q", answer="a")
        card.update(5)
        self.assertGreaterEqual(card.interval, 1)
        self.assertGreaterEqual(card.review_date, date.today())

    def test_to_dict_round_trip(self):
        card = Flashcard(question="q", answer="a", tags=["t"])
        data = card.to_dict()
        new_card = Flashcard.from_dict(data)
        self.assertEqual(new_card.question, "q")
        self.assertEqual(new_card.tags, ["t"])
        self.assertEqual(new_card.review_date, card.review_date)

class TestDeck(unittest.TestCase):
    def test_add_card(self):
        deck = Deck(name="demo")
        deck.add_card("q", "a")
        self.assertEqual(len(deck.cards), 1)

    def test_add_card_with_tags(self):
        deck = Deck(name="demo")
        card = deck.add_card("q", "a", tags=["tag1", "tag2"])
        self.assertIn("tag1", card.tags)
        self.assertEqual(len(deck.cards), 1)

if __name__ == '__main__':
    unittest.main()
