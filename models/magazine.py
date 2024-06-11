from connection import get_connection

class Magazine:
    def __init__(self, id, name, category):
        self._id = id
        self._name = name
        self._category = category
        self._save_to_db()

    def _save_to_db(self):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('INSERT INTO magazines (id, name, category) VALUES (?, ?, ?)', (self._id, self._name, self._category))
        conn.commit()
        conn.close()

    @property
    def id(self):
        return self._id

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('UPDATE magazines SET name = ? WHERE id = ?', (value, self._id))
        conn.commit()
        conn.close()
        self._name = value

    @property
    def category(self):
        return self._category

    @category.setter
    def category(self, value):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('UPDATE magazines SET category = ? WHERE id = ?', (value, self._id))
        conn.commit()
        conn.close()
        self._category = value

    def articles(self):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM articles WHERE magazine_id = ?', (self._id,))
        articles = cursor.fetchall()
        conn.close()
        return articles

    def contributors(self):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT DISTINCT authors.* FROM authors
            JOIN articles ON articles.author_id = authors.id
            WHERE articles.magazine_id = ?
        ''', (self._id,))
        contributors = cursor.fetchall()
        conn.close()
        return contributors

    def article_titles(self):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT title FROM articles WHERE magazine_id = ?', (self._id,))
        titles = cursor.fetchall()
        conn.close()
        return [title[0] for title in titles]

    def contributing_authors(self):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT authors.*, COUNT(articles.id) as article_count FROM authors
            JOIN articles ON articles.author_id = authors.id
            WHERE articles.magazine_id = ?
            GROUP BY authors.id
            HAVING article_count > 2
        ''', (self._id,))
        authors = cursor.fetchall()
        conn.close()
        return authors if authors else None

