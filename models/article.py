from connection import get_connection

class Article:
    def __init__(self, author, magazine, title):
        self._author_id = author.id
        self._magazine_id = magazine.id
        self._title = title
        self._save_to_db()

    def _save_to_db(self):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('INSERT INTO articles (author_id, magazine_id, title) VALUES (?, ?, ?)', (self._author_id, self._magazine_id, self._title))
        conn.commit()
        conn.close()

    @property
    def title(self):
        return self._title

    @property
    def author(self):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT id, name FROM authors WHERE id = ?', (self._author_id,))
        author = cursor.fetchone()
        conn.close()
        if author:
            return {'id': author[0], 'name': author[1]}
        return None

    @property
    def magazine(self):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT id, name, category FROM magazines WHERE id = ?', (self._magazine_id,))
        magazine = cursor.fetchone()
        conn.close()
        if magazine:
            return {'id': magazine[0], 'name': magazine[1], 'category': magazine[2]}
        return None


