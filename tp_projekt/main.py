from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# Funkce pro inicializaci databáze
def init_db():
    conn = sqlite3.connect('library.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS Book (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            author TEXT NOT NULL,
            is_available INTEGER DEFAULT 1
        )
    ''')
    conn.commit()
    conn.close()

@app.route('/')
def index():
    """Úvodní stránka"""
    return render_template('index.html')

@app.route('/books')
def books():
    """Výpis všech knih"""
    conn = sqlite3.connect('library.db')
    c = conn.cursor()
    c.execute('SELECT id, title, author, is_available FROM Book')
    all_books = c.fetchall()
    conn.close()
    return render_template('books.html', books=all_books)

@app.route('/add_book', methods=['GET', 'POST'])
def add_book():
    """Přidání nové knihy do databáze"""
    if request.method == 'POST':
        title = request.form['title']
        author = request.form['author']

        conn = sqlite3.connect('library.db')
        c = conn.cursor()
        c.execute('INSERT INTO Book (title, author, is_available) VALUES (?, ?, 1)', (title, author))
        conn.commit()
        conn.close()

        return redirect(url_for('books'))
    return render_template('add_book.html')

@app.route('/borrow/<int:book_id>')
def borrow_book(book_id):
    """Změna stavu knihy na 'vypůjčeno'"""
    conn = sqlite3.connect('library.db')
    c = conn.cursor()
    c.execute('UPDATE Book SET is_available = 0 WHERE id = ?', (book_id,))
    conn.commit()
    conn.close()
    return redirect(url_for('books'))

@app.route('/return/<int:book_id>')
def return_book(book_id):
    """Změna stavu knihy na 'dostupné'"""
    conn = sqlite3.connect('library.db')
    c = conn.cursor()
    c.execute('UPDATE Book SET is_available = 1 WHERE id = ?', (book_id,))
    conn.commit()
    conn.close()
    return redirect(url_for('books'))

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
