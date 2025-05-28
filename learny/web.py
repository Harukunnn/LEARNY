from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import parse_qs, urlparse
from html import escape
from typing import Dict

from .models import Deck
from .storage import load_data, save_data


class LearnyHandler(BaseHTTPRequestHandler):
    decks: Dict[str, Deck] = load_data()

    def _send_html(self, html: str, status: int = 200) -> None:
        self.send_response(status)
        self.send_header('Content-Type', 'text/html; charset=utf-8')
        self.end_headers()
        self.wfile.write(html.encode('utf-8'))

    def do_GET(self) -> None:
        parsed = urlparse(self.path)
        path = parsed.path
        query = parse_qs(parsed.query)

        if path == '/':
            self._send_html(self.page_index())
        elif path.startswith('/deck/'):
            parts = path.strip('/').split('/')
            if len(parts) == 2 and parts[1] == 'add':
                deck = escape(parts[0])
                self._send_html(self.page_add_card(deck))
            elif len(parts) == 1:
                deck = escape(parts[0])
                self._send_html(self.page_deck(deck))
            else:
                self.send_error(404)
        elif path == '/review':
            deck = query.get('deck', [''])[0]
            self._send_html(self.page_review(deck))
        else:
            self.send_error(404)

    def do_POST(self) -> None:
        parsed = urlparse(self.path)
        path = parsed.path
        length = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(length).decode()
        data = parse_qs(body)

        if path == '/add-deck':
            name = data.get('name', [''])[0]
            if name and name not in self.decks:
                self.decks[name] = Deck(name=name)
                save_data(self.decks)
            self.redirect('/')
        elif path.startswith('/deck/') and path.endswith('/add'):
            parts = path.strip('/').split('/')
            deck_name = parts[0]
            deck = self.decks.setdefault(deck_name, Deck(name=deck_name))
            question = data.get('question', [''])[0]
            answer = data.get('answer', [''])[0]
            if question and answer:
                deck.add_card(question, answer)
                save_data(self.decks)
            self.redirect(f'/deck/{deck_name}')
        elif path == '/review':
            deck_name = data.get('deck', [''])[0]
            quality = int(data.get('quality', ['0'])[0])
            deck = self.decks.get(deck_name)
            if deck and deck.due_cards():
                card = deck.due_cards()[0]
                card.update(quality)
                save_data(self.decks)
            self.redirect(f'/review?deck={deck_name}')
        else:
            self.send_error(404)

    def redirect(self, location: str) -> None:
        self.send_response(303)
        self.send_header('Location', location)
        self.end_headers()

    def page_index(self) -> str:
        items = []
        for name, deck in self.decks.items():
            stats = deck.stats()
            items.append(
                f"<li><a href='/deck/{escape(name)}'>{escape(name)}</a> - "
                f"{stats['due']} due / {stats['total']} cards</li>"
            )
        decks_html = '\n'.join(items)
        return f"""
        <html><body>
        <h1>Learny Decks</h1>
        <ul>{decks_html}</ul>
        <h2>Add Deck</h2>
        <form method='post' action='/add-deck'>
            <input name='name' placeholder='Deck name'>
            <input type='submit' value='Create'>
        </form>
        </body></html>
        """

    def page_deck(self, name: str) -> str:
        deck = self.decks.get(name)
        if not deck:
            return "<html><body>Deck not found</body></html>"
        stats = deck.stats()
        return f"""
        <html><body>
        <h1>Deck: {escape(name)}</h1>
        <p>{stats['due']} cards due / {stats['total']} total</p>
        <a href='/review?deck={escape(name)}'>Review</a>
        <h2>Add Card</h2>
        <form method='post' action='/deck/{escape(name)}/add'>
            <input name='question' placeholder='Question'><br>
            <input name='answer' placeholder='Answer'><br>
            <input type='submit' value='Add'>
        </form>
        </body></html>
        """

    def page_add_card(self, name: str) -> str:
        return f"""
        <html><body>
        <h1>Add Card to {escape(name)}</h1>
        <form method='post' action='/deck/{escape(name)}/add'>
            <input name='question' placeholder='Question'><br>
            <input name='answer' placeholder='Answer'><br>
            <input type='submit' value='Add'>
        </form>
        </body></html>
        """

    def page_review(self, name: str) -> str:
        deck = self.decks.get(name)
        if not deck:
            return "<html><body>Deck not found</body></html>"
        due = deck.due_cards()
        if not due:
            return (
                f"<html><body><h1>No cards due for {escape(name)}</h1>"
                f"<a href='/deck/{escape(name)}'>Back</a></body></html>"
            )
        card = due[0]
        return f"""
        <html><body>
        <h1>{escape(name)} Review</h1>
        <div>Question: {escape(card.question)}</div>
        <form method='post' action='/review'>
            <input type='hidden' name='deck' value='{escape(name)}'>
            <div><strong>Answer:</strong> {escape(card.answer)}</div>
            <label>Quality (0-5): <input name='quality' type='number' min='0' max='5'></label>
            <input type='submit' value='Submit'>
        </form>
        </body></html>
        """


def run(server_class=HTTPServer, handler_class=LearnyHandler, port: int = 8000) -> None:
    server = server_class(('', port), handler_class)
    print(f"Serving on http://localhost:{port}")
    server.serve_forever()


if __name__ == '__main__':
    run()
