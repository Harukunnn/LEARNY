import unittest
from datetime import date
from learny.models import Flashcard, Deck

class TestFlashcard(unittest.TestCase):
    def test_update_quality(self):
        card = Flashcard(question="q", answer="a")
        card.update(5)
        self.assertGreaterEqual(card.interval, 1)
        self.assertGreaterEqual(card.review_date, date.today())

class TestDeck(unittest.TestCase):
    def test_add_card(self):
        deck = Deck(name="demo")
        deck.add_card("q", "a")
        self.assertEqual(len(deck.cards), 1)

if __name__ == '__main__':
    unittest.main()
