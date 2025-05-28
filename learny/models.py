from dataclasses import dataclass, field, asdict
from datetime import date, timedelta
from typing import List, Dict, Any
from uuid import uuid4

@dataclass
class Flashcard:
    question: str
    answer: str
    tags: List[str] = field(default_factory=list)
    id: str = field(default_factory=lambda: uuid4().hex)
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

    def to_dict(self) -> Dict[str, Any]:
        data = asdict(self)
        data["review_date"] = self.review_date.isoformat()
        return data

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> "Flashcard":
        if isinstance(data.get("review_date"), str):
            data["review_date"] = date.fromisoformat(data["review_date"])
        return Flashcard(**data)

@dataclass
class Deck:
    name: str
    cards: List[Flashcard] = field(default_factory=list)

    def add_card(self, question: str, answer: str, tags: List[str] | None = None) -> Flashcard:
        card = Flashcard(question=question, answer=answer, tags=tags or [])
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
