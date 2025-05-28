"""Simple Tkinter GUI for Learny flashcards."""

import tkinter as tk
from tkinter import simpledialog, messagebox
from .storage import load_data, save_data
from .models import Deck, Flashcard

class LearnyApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Learny Flashcards")
        self.geometry("400x300")
        self.decks = load_data()
        self.create_widgets()
        self.refresh_deck_list()

    def create_widgets(self):
        self.deck_list = tk.Listbox(self)
        self.deck_list.pack(fill=tk.BOTH, expand=True)

        btn_frame = tk.Frame(self)
        btn_frame.pack(fill=tk.X)
        tk.Button(btn_frame, text="Add Deck", command=self.add_deck).pack(side=tk.LEFT, expand=True, fill=tk.X)
        tk.Button(btn_frame, text="Add Card", command=self.add_card).pack(side=tk.LEFT, expand=True, fill=tk.X)
        tk.Button(btn_frame, text="Review", command=self.review_deck).pack(side=tk.LEFT, expand=True, fill=tk.X)

    def refresh_deck_list(self):
        self.deck_list.delete(0, tk.END)
        for name, deck in self.decks.items():
            stats = deck.stats()
            self.deck_list.insert(tk.END, f"{name} ({stats['due']} / {stats['total']} due)")

    def get_selected_deck(self) -> Deck | None:
        selection = self.deck_list.curselection()
        if not selection:
            return None
        name = list(self.decks.keys())[selection[0]]
        return self.decks[name]

    def add_deck(self):
        name = simpledialog.askstring("Deck Name", "Enter new deck name:")
        if name:
            if name in self.decks:
                messagebox.showinfo("Info", "Deck already exists")
            else:
                self.decks[name] = Deck(name=name)
                save_data(self.decks)
                self.refresh_deck_list()

    def add_card(self):
        deck = self.get_selected_deck()
        if not deck:
            messagebox.showwarning("No Deck", "Select a deck first")
            return
        question = simpledialog.askstring("Question", "Enter question:")
        if not question:
            return
        answer = simpledialog.askstring("Answer", "Enter answer:")
        if not answer:
            return
        deck.add_card(question, answer)
        save_data(self.decks)
        self.refresh_deck_list()

    def review_deck(self):
        deck = self.get_selected_deck()
        if not deck:
            messagebox.showwarning("No Deck", "Select a deck first")
            return
        due = deck.due_cards()
        if not due:
            messagebox.showinfo("Review", "No cards due")
            return
        for card in due:
            self.review_card_gui(card)
        save_data(self.decks)
        self.refresh_deck_list()

    def review_card_gui(self, card: Flashcard):
        qwin = tk.Toplevel(self)
        qwin.title("Review")
        tk.Label(qwin, text=card.question, wraplength=300).pack(padx=20, pady=20)
        tk.Button(qwin, text="Show Answer", command=lambda: self.show_answer(qwin, card)).pack()
        qwin.grab_set()
        self.wait_window(qwin)

    def show_answer(self, window: tk.Toplevel, card: Flashcard):
        for widget in window.winfo_children():
            widget.destroy()
        tk.Label(window, text=card.answer, wraplength=300).pack(padx=20, pady=10)
        frame = tk.Frame(window)
        frame.pack(pady=10)
        for q, label in [(5, "Easy"), (4, "Good"), (3, "Hard"), (1, "Again")]:
            tk.Button(frame, text=label, command=lambda q=q: self.finish_review(window, card, q)).pack(side=tk.LEFT, padx=5)

    def finish_review(self, window: tk.Toplevel, card: Flashcard, quality: int):
        card.update(quality)
        window.destroy()


def main():
    app = LearnyApp()
    app.mainloop()

if __name__ == "__main__":
    main()
