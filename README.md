# 🤖 Financial Complaint Classifier — MLOps Deployment Exercise

> **Course exercise** from the [MLOps Engineer](https://platzi.com/cursos/mlops/) track on **[Platzi](https://platzi.com)**. This repository demonstrates how to deploy a production-ready Machine Learning inference service using modern MLOps practices.

---

## 📌 Overview

This project exposes a **REST API** that classifies financial consumer complaints into one of three categories using a pre-trained Scikit-Learn model. It is built with **FastAPI**, persists predictions to **PostgreSQL**, and is fully containerized with **Docker Compose**.

The three prediction labels are:

| Label | Category |
|---|---|
| 0 | Bank Account Services |
| 1 | Credit Report or Prepaid Card |
| 2 | Mortgage / Loan |

---

## 🏗️ Architecture

```
┌──────────────┐     HTTP POST /predicts      ┌────────────────────────┐
│   API Client │ ──────────────────────────▶  │   FastAPI (uvicorn)    │
└──────────────┘                              │                        │
                                              │  NLP Pipeline (NLTK)   │
                                              │  ├─ Tokenization        │
                                              │  ├─ Stopword removal    │
                                              │  ├─ POS tagging         │
                                              │  └─ TF-IDF vectorizer   │
                                              │                        │
                                              │  Scikit-Learn model     │
                                              │  (joblib .pkl)          │
                                              └────────────┬───────────┘
                                                           │
                                              ┌────────────▼───────────┐
                                              │   PostgreSQL (asyncpg) │
                                              │  Stores every prediction│
                                              └────────────────────────┘
```

### Services (Docker Compose)

| Service | Image | Port | Purpose |
|---|---|---|---|
| `web` | Custom (Python 3.11-slim) | `8000` | FastAPI inference API |
| `db` | `postgres:15-alpine` | `5432` | Prediction storage |
| `adminer` | `adminer` | `8080` | Database UI explorer |
| `grafana` | `grafana/grafana` | `3000` | Observability dashboards |

---

## 📂 Project Structure

```
.
├── config/
│   ├── grafana_datasources.yaml   # Grafana provisioning — data sources
│   ├── grafana_dashboards.yaml    # Grafana provisioning — dashboard loader
│   └── prometheus.yaml            # Prometheus scrape configuration
├── models/
│   ├── model.pkl                  # Pre-trained Scikit-Learn classifier
│   └── count_vectorizer.pkl       # Fitted CountVectorizer
├── src/
│   └── app/
│       ├── main.py                # FastAPI app entrypoint
│       ├── lifespan.py            # Startup/shutdown lifecycle (model loading)
│       ├── settings.py            # Pydantic settings (env vars)
│       ├── db/
│       │   ├── engine.py          # Async SQLAlchemy engine + session
│       │   └── models.py          # SQLModel table definitions
│       ├── predicts/
│       │   ├── router.py          # POST /predicts endpoint
│       │   ├── services.py        # Inference logic + DB persistence
│       │   └── utils.py           # NLP preprocessing pipeline
│       └── healthcheck/
│           └── router.py          # GET /health endpoint
├── Dockerfile
├── docker-compose.yaml
├── requirements.txt
├── .env.example                   # Environment variable template
└── .gitignore
```

---

## 🚀 Getting Started

### Prerequisites

- [Docker](https://docs.docker.com/get-docker/) ≥ 24
- [Docker Compose](https://docs.docker.com/compose/) ≥ 2

### 1. Clone the repository

```bash
git clone <your-repo-url>
cd app_deployment_class
```

### 2. Set up environment variables

```bash
cp .env.example .env
# Edit .env and set a secure DB_PASSWORD
```

`.env` reference:

```env
DB_USER=postgres
DB_PASSWORD=changeme
DB_NAME=postgres
```

### 3. Build and run

```bash
docker compose up --build
```

### 4. Verify the service is healthy

```bash
curl http://localhost:8000/health
```

---

## 📡 API Reference

### `POST /predicts`

Classifies one or more financial complaint texts.

**Request body:**

```json
{
  "sentences": [
    {
      "client_name": "John Doe",
      "text": "I have a problem with my mortgage payment and the bank is not responding."
    }
  ]
}
```

**Response:**

```json
{
  "predictions": [
    {
      "client_name": "John Doe",
      "prediction": "Mortgage/Loan"
    }
  ]
}
```

### `GET /health`

Returns the health status of the service.

---

## ⚙️ MLOps Design Decisions

This project applies several production-grade practices covered in the Platzi MLOps course:

| Practice | Implementation |
|---|---|
| **Singleton model loading** | Model and vectorizer loaded once at startup via `lifespan`, stored in `app.state` |
| **Async inference** | CPU-bound inference offloaded to a threadpool via `run_in_threadpool` |
| **Dependency injection** | Database session managed via FastAPI `Depends(get_session)` |
| **NLP baked into the image** | NLTK corpora downloaded at Docker build time (`RUN python -m nltk.downloader -d /usr/share/nltk_data ...`), not at runtime |
| **Non-root container** | Uvicorn runs as `appuser` (CIS hardening) |
| **Secret management** | No hardcoded credentials — all secrets injected via `.env` file |
| **Grafana provisioning** | Datasources and dashboards declared as code in `config/` |

---

## 🛠️ Tech Stack

- **[FastAPI](https://fastapi.tiangolo.com/)** — Async REST framework
- **[SQLModel](https://sqlmodel.tiangolo.com/)** + **[asyncpg](https://magicstack.github.io/asyncpg/)** — Async ORM + PostgreSQL driver
- **[Scikit-Learn](https://scikit-learn.org/)** — ML model and TF-IDF vectorization
- **[NLTK](https://www.nltk.org/)** — NLP preprocessing (tokenization, POS tagging, stopwords)
- **[Pydantic Settings](https://docs.pydantic.dev/latest/concepts/pydantic_settings/)** — Type-safe environment configuration
- **[Docker Compose](https://docs.docker.com/compose/)** — Multi-service orchestration
- **[Grafana](https://grafana.com/)** — Observability dashboards

---

## 📄 License

For educational use only. Not intended for production deployment without further hardening.
