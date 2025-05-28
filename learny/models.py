from dataclasses import dataclass, field
from datetime import date, timedelta
from typing import List, Dict

@dataclass
class Flashcard:
    question: str
    answer: str
    interval: int = 1
    review_date: date = field(default_factory=date.today)
    ease_factor: float = 2.5
    repetition: int = 0

    def update(self, quality: int) -> None:
        """Update scheduling data based on review quality (0-5)."""
        if quality < 3:
            self.repetition = 0
            self.interval = 1
        else:
            if self.repetition == 0:
                self.interval = 1
            elif self.repetition == 1:
                self.interval = 6
            else:
                self.interval = int(self.interval * self.ease_factor)
            self.ease_factor += (0.1 - (5 - quality) * (0.08 + (5 - quality) * 0.02))
            if self.ease_factor < 1.3:
                self.ease_factor = 1.3
            self.repetition += 1
        self.review_date = date.today() + timedelta(days=self.interval)

@dataclass
class Deck:
    name: str
    cards: List[Flashcard] = field(default_factory=list)

    def add_card(self, question: str, answer: str) -> Flashcard:
        card = Flashcard(question=question, answer=answer)
        self.cards.append(card)
        return card

    def due_cards(self) -> List[Flashcard]:
        today = date.today()
        return [c for c in self.cards if c.review_date <= today]

    def stats(self) -> Dict[str, int]:
        today = date.today()
        due = sum(1 for c in self.cards if c.review_date <= today)
        total = len(self.cards)
        return {"due": due, "total": total}
