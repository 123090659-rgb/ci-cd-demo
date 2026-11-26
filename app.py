"""A tiny Flask application used for the CI/CD exercise."""

from flask import Flask, jsonify

app = Flask(__name__)


def add(a: float, b: float) -> float:
    """Add two numbers (used by the calculator endpoint)."""
    return a + b


@app.route("/")
def index():
    return jsonify(message="Hello from the CI/CD demo app!")


@app.route("/add/<a>/<b>")
def add_numbers(a: str, b: str):
    return jsonify(a=float(a), b=float(b), result=add(float(a), float(b)))


@app.route("/health")
def health():
    return jsonify(status="ok"), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
