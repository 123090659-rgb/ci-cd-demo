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

### `.github/workflows/data-pipeline.yml` — Data Pipeline (Exercise 2)

| | |
|---|---|
| **Triggers** | `push` with `paths: ["data/**"]` — only when a file in `data/` changes |
| **Job** | `update-database` on `ubuntu-latest`, Python 3.11 |
| **Steps** | checkout → setup-python 3.11 → `pip install pandas flask` → `python clean_and_merge.py` → commit updated `orders.db` back to the repo |

Pipeline (`clean_and_merge.py`) responsibilities:
1. Read `data/order.txt` and `data/customer.txt`
2. Remove duplicate rows
3. Convert all amounts to CNY (USD=6.9, EUR=7.5, CNY=1.0, JPY=0.05) into `amount_cny`
4. Merge orders with customers on `customer_id`
5. Write merged data to SQLite (`orders.db`, table `orders_merged`)
6. Write average `amount_cny` by region (`summary_by_region` table)

The updated database is committed back to the repository by the workflow.
GitHub Actions does **not** update your local machine automatically — run
`git pull` to bring the fresh `orders.db` down to your desktop/laptop.

## Data pipeline web app

`web_app.py` — Flask frontend with an SQLite backend:
- Reads `orders.db` on every request, so it updates automatically when the
  database changes (plus a 30-second auto refresh)
- Main page shows the merged orders table and the avg `amount_cny` per region

## Running locally

```bash
pip install -r requirements.txt
pytest -v          # run tests
python app.py      # start the app on http://localhost:8000
```

Data pipeline (Exercise 2):

```bash
pip install pandas flask
python clean_and_merge.py   # rebuild orders.db from data/*.txt
python web_app.py           # view merged data + summary at http://localhost:8000
```
