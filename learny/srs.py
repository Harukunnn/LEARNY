from datetime import date
from .models import Flashcard

def review_card(card: Flashcard) -> None:
    """Interactively review a card and update its schedule."""
    print(f"Question: {card.question}")
    input("Press Enter to show answer...")
    print(f"Answer: {card.answer}\n")
    print("How did you do? (5=Easy, 4=Good, 3=Hard, <3=Again)")
    try:
        quality = int(input("Quality [0-5]: ") or 0)
    except ValueError:
        quality = 0
    if quality < 0 or quality > 5:
        quality = 0
    card.update(quality)
    print(f"Next review on {card.review_date}\n")
