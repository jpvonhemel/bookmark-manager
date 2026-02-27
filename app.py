import os
import psycopg2
from psycopg2.extras import RealDictCursor
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

DB_HOST = os.environ.get("DB_HOST", "db")
DB_PORT = os.environ.get("DB_PORT", "5432")
DB_NAME = os.environ.get("DB_NAME", "bookmarks")
DB_USER = os.environ.get("DB_USER", "bookmarks")
DB_PASS = os.environ.get("DB_PASS", "bookmarks")


def get_db():
    """Connect to the PostgreSQL database."""
    conn = psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASS,
    )
    return conn


DEFAULT_BOOKMARKS = [
    ("Anthropic", "https://anthropic.com", "AI"),
    ("Google", "https://google.com", "Search"),
    ("Vanguard", "https://vanguard.com", "Finance"),
    ("GitHub", "https://github.com", "Development"),
    ("Pulse", "https://pulse.vonhemel.com", "Personal"),
]


def init_db():
    """Create the bookmarks table and add defaults if empty."""
    conn = get_db()
    cur = conn.cursor()
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS bookmarks (
            id SERIAL PRIMARY KEY,
            title TEXT NOT NULL,
            url TEXT NOT NULL,
            category TEXT DEFAULT '',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """
    )
    # Only seed defaults if the table is empty (fresh install)
    cur.execute("SELECT COUNT(*) FROM bookmarks")
    count = cur.fetchone()[0]
    if count == 0:
        cur.executemany(
            "INSERT INTO bookmarks (title, url, category) VALUES (%s, %s, %s)",
            DEFAULT_BOOKMARKS,
        )
    conn.commit()
    cur.close()
    conn.close()


@app.route("/")
def index():
    """Show all bookmarks."""
    conn = get_db()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute("SELECT * FROM bookmarks ORDER BY created_at DESC")
    bookmarks = cur.fetchall()
    cur.close()
    conn.close()
    return render_template("index.html", bookmarks=bookmarks)


@app.route("/add", methods=["POST"])
def add_bookmark():
    """Add a new bookmark."""
    title = request.form["title"]
    url = request.form["url"]
    category = request.form.get("category", "")

    conn = get_db()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO bookmarks (title, url, category) VALUES (%s, %s, %s)",
        (title, url, category),
    )
    conn.commit()
    cur.close()
    conn.close()
    return redirect(url_for("index"))


@app.route("/delete/<int:bookmark_id>", methods=["POST"])
def delete_bookmark(bookmark_id):
    """Delete a bookmark."""
    conn = get_db()
    cur = conn.cursor()
    cur.execute("DELETE FROM bookmarks WHERE id = %s", (bookmark_id,))
    conn.commit()
    cur.close()
    conn.close()
    return redirect(url_for("index"))


# Create the database table when the app starts
init_db()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
