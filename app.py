import sqlite3
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)
DATABASE = "bookmarks.db"


def get_db():
    """Connect to the SQLite database."""
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row  # So we can access columns by name
    return conn


def init_db():
    """Create the bookmarks table if it doesn't exist."""
    conn = get_db()
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS bookmarks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            url TEXT NOT NULL,
            category TEXT DEFAULT '',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """
    )
    conn.commit()
    conn.close()


@app.route("/")
def index():
    """Show all bookmarks."""
    conn = get_db()
    bookmarks = conn.execute(
        "SELECT * FROM bookmarks ORDER BY created_at DESC"
    ).fetchall()
    conn.close()
    return render_template("index.html", bookmarks=bookmarks)


@app.route("/add", methods=["POST"])
def add_bookmark():
    """Add a new bookmark."""
    title = request.form["title"]
    url = request.form["url"]
    category = request.form.get("category", "")

    conn = get_db()
    conn.execute(
        "INSERT INTO bookmarks (title, url, category) VALUES (?, ?, ?)",
        (title, url, category),
    )
    conn.commit()
    conn.close()
    return redirect(url_for("index"))


@app.route("/delete/<int:bookmark_id>", methods=["POST"])
def delete_bookmark(bookmark_id):
    """Delete a bookmark."""
    conn = get_db()
    conn.execute("DELETE FROM bookmarks WHERE id = ?", (bookmark_id,))
    conn.commit()
    conn.close()
    return redirect(url_for("index"))


# Create the database table when the app starts
init_db()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
