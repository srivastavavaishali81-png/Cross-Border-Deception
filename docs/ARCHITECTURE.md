# OZARK — Architecture

## System Overview

```
┌──────────────────────────────────────────────────────────────────┐
│                         CLIENT BROWSER                           │
└─────────────────────────────┬────────────────────────────────────┘
                              │ HTTP / WebSocket
┌─────────────────────────────▼────────────────────────────────────┐
│               FRONTEND  (Next.js 15 + Tailwind + ShadCN)         │
│   /app (App Router)  │  /components  │  /lib/api-client.ts       │
└─────────────────────────────┬────────────────────────────────────┘
                              │ REST / JSON  (via rewrites or direct)
┌─────────────────────────────▼────────────────────────────────────┐
│                   BACKEND  (FastAPI + Python 3.12)                │
│  /api/v1/router  │  /models (ORM)  │  /schemas (Pydantic)        │
│  /services       │  /db/postgres   │  /db/neo4j                  │
└──────────┬──────────────────────────────────┬────────────────────┘
           │ asyncpg / SQLAlchemy             │ neo4j driver
┌──────────▼──────────┐            ┌──────────▼──────────────────┐
│   PostgreSQL 16      │            │        Neo4j 5               │
│   (relational data)  │            │   (graph / relationships)    │
└──────────────────────┘            └──────────────────────────────┘

     ▲ ETL                                      ▲ Graph loads
┌────┴──────────────┐             ┌─────────────┴────────────────┐
│  CONNECTORS       │             │  ML PIPELINE                  │
│  (Python ETL)     │             │  (scikit-learn / PyTorch)     │
└───────────────────┘             └──────────────────────────────-┘
```

---

## Directory Reference

| Path | Purpose |
|------|---------|
| `frontend/` | Next.js 15 SPA — App Router, Tailwind, ShadCN UI |
| `frontend/src/app/` | Pages and layouts (App Router) |
| `frontend/src/components/` | Reusable React components |
| `frontend/src/lib/` | Utilities, API client, helpers |
| `frontend/src/types/` | TypeScript type definitions |
| `backend/` | FastAPI application |
| `backend/app/main.py` | App factory + lifespan |
| `backend/app/core/` | Config, logging, security |
| `backend/app/db/` | PostgreSQL + Neo4j sessions |
| `backend/app/api/v1/` | Versioned REST endpoints |
| `backend/app/models/` | SQLAlchemy ORM models |
| `backend/app/schemas/` | Pydantic request/response schemas |
| `backend/app/services/` | Business logic (no DB coupling) |
| `database/` | Alembic migrations + SQL seeds + Cypher scripts |
| `connectors/` | ETL connectors (CSV, REST, etc.) |
| `ml/` | Machine learning pipeline |
| `ml/pipeline/` | Abstract + concrete ML pipeline classes |
| `ml/models/` | Saved model artifacts (gitignored) |
| `docker/` | Dockerfiles + Docker Compose files |
| `docs/` | Project documentation |

---

## Data Flow

### Write Path
```
External Source → Connector → Transform → PostgreSQL / Neo4j
```

### Query Path
```
Browser → Next.js → FastAPI → PostgreSQL (SQL) or Neo4j (Cypher) → JSON response
```

### ML Path
```
PostgreSQL → ML Pipeline → Trained Model (.pkl / .pt) → FastAPI inference endpoint
```

---

## Technology Decisions

### Why FastAPI?
- Native async support for PostgreSQL (asyncpg) and Neo4j
- Pydantic v2 for zero-overhead validation
- Auto-generated OpenAPI docs

### Why Next.js 15 App Router?
- React Server Components for reduced client bundle
- Built-in API rewrites eliminating CORS issues in development
- Turbopack for fast HMR

### Why both PostgreSQL AND Neo4j?
- PostgreSQL: structured relational data (users, entities, transactions)
- Neo4j: relationship traversal and graph queries that would be expensive in SQL

### Why Alembic?
- Version-controlled schema changes
- Async migration runner (compatible with asyncpg)

---

## Port Map

| Service | Port |
|---------|------|
| Frontend (Next.js) | 3000 |
| Backend (FastAPI) | 8000 |
| PostgreSQL | 5432 |
| Neo4j HTTP | 7474 |
| Neo4j Bolt | 7687 |
