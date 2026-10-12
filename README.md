# 🦅 OZARK

> A full-stack intelligent data platform powered by relational + graph databases, a Python ML pipeline, and a modern Next.js frontend.

---

## 📐 Architecture Overview

```
OZARK/
├── frontend/          # Next.js 15 + TypeScript + Tailwind + ShadCN UI
├── backend/           # FastAPI REST & WebSocket API
├── database/          # PostgreSQL schema migrations & seeds
├── connectors/        # Data ingestion connectors (ETL)
├── ml/                # Machine learning pipeline
├── docker/            # Docker Compose configurations
└── docs/              # Architecture docs & API specs
```

---

## 🛠️ Tech Stack

| Layer       | Technology                              |
|-------------|------------------------------------------|
| Frontend    | Next.js 15, TypeScript, Tailwind CSS, ShadCN UI |
| Backend     | FastAPI, Python 3.12, Pydantic v2        |
| Relational  | PostgreSQL 16                            |
| Graph DB    | Neo4j 5                                  |
| Connectors  | Custom Python ETL                        |
| ML          | Python, scikit-learn / PyTorch           |
| DevOps      | Docker, Docker Compose                   |

---

## 🚀 Quick Start

### Prerequisites

- [Docker](https://docs.docker.com/get-docker/) & Docker Compose v2
- [Node.js](https://nodejs.org/) >= 20.x
- [Python](https://www.python.org/) >= 3.12
- [pnpm](https://pnpm.io/) >= 9.x

### 1. Clone & Configure

```bash
git clone https://github.com/your-org/ozark.git
cd ozark
cp .env.example .env
# Edit .env with your secrets
```

### 2. Start All Services via Docker

```bash
docker compose -f docker/docker-compose.yml up --build
```

This starts:
- **PostgreSQL** on `localhost:5432`
- **Neo4j** on `localhost:7474` (HTTP) / `localhost:7687` (Bolt)
- **FastAPI backend** on `localhost:8000`
- **Next.js frontend** on `localhost:3000`

### 3. Frontend Only (Dev)

```bash
cd frontend
pnpm install
pnpm dev
```

### 4. Backend Only (Dev)

```bash
cd backend
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

### 5. Run Migrations

```bash
cd database
alembic upgrade head
```

---

## 🗂️ Detailed Structure

See [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md) for the full architectural breakdown.

---

## 🌍 Environment Variables

See [`.env.example`](.env.example) for all required environment variables.

---

## 📖 API Documentation

Once the backend is running, visit:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

---

## 📄 License

MIT © OZARK Team
