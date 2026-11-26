# ci-cd-demo

A tiny Flask application created for the CI/CD workflow exercise (Exercise 1).

## Application

- `app.py` – Flask app with three routes:
  - `GET /` – returns a JSON greeting
  - `GET /add/<a>/<b>` – adds two numbers
  - `GET /health` – health check (returns `{"status": "ok"}`)
- `tests/test_app.py` – pytest tests for the app
- `Dockerfile` – builds a container image for the app

## GitHub Actions workflows

### `.github/workflows/ci.yml` — Continuous Integration

| | |
|---|---|
| **Triggers** | `push` to `main`, and `pull_request` targeting `main` |
| **Job** | `test` on `ubuntu-latest`, with a matrix over Python 3.11 and 3.12 |
| **Steps** | checkout → setup-python → `pip install -r requirements.txt` → `pytest -v` |

Every push to main and every pull request runs the full test suite on two Python
versions. If any test fails, the run is marked red and the PR should not be merged.

### `.github/workflows/cd.yml` — Continuous Delivery

| | |
|---|---|
| **Triggers** | `push` to `main`, and `workflow_dispatch` (manual run) |
| **Job** | `build-and-push` on `ubuntu-latest` |
| **Steps** | checkout → setup Docker Buildx → login to `ghcr.io` (using the built-in `GITHUB_TOKEN`) → build & push image |

The Docker image is published to the GitHub Container Registry with two tags:
`latest` and the commit SHA (`ghcr.io/<owner>/<repo>:<sha>`), so every build is
traceable to the exact commit.

## Running locally

```bash
pip install -r requirements.txt
pytest -v          # run tests
python app.py      # start the app on http://localhost:8000
```
