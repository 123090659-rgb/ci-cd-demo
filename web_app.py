"""web_app.py - Flask frontend with an SQLite backend.

The main page shows:
- the merged orders table (orders_merged)
- the summary table (avg amount_cny per region)

Every request re-queries the database, so the page updates automatically
whenever the database file changes (e.g. after the pipeline re-runs).
"""

import sqlite3

from flask import Flask, render_template

DB_PATH = "orders.db"

app = Flask(__name__)


def query_db(sql):
    """Run a SELECT and return all rows as plain dicts (Jinja friendly)."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    rows = conn.execute(sql).fetchall()
    conn.close()
    return [dict(row) for row in rows]


@app.route("/")
def index():
    orders = query_db("SELECT * FROM orders_merged")
    summary = query_db("SELECT * FROM summary_by_region ORDER BY region")
    return render_template("pipeline.html", orders=orders, summary=summary)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
