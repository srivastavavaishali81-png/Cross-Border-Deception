# OZARK — Setup Guide

## 1. Prerequisites

| Tool | Version | Install |
|------|---------|---------|
| Docker | >= 24.x | https://docs.docker.com/get-docker/ |
| Docker Compose | >= 2.x | Bundled with Docker Desktop |
| Node.js | >= 20.x | https://nodejs.org/ |
| pnpm | >= 9.x | `npm install -g pnpm` |
| Python | >= 3.12 | https://www.python.org/ |

---

## 2. Environment Configuration

```bash
# Copy the template
cp .env.example .env

# Required values to update in .env:
#   APP_SECRET_KEY       — generate with: python -c "import secrets; print(secrets.token_hex(32))"
#   POSTGRES_PASSWORD    — strong random password
#   NEO4J_PASSWORD       — strong random password (min 8 chars)
```

---

## 3. Start Everything with Docker

```bash
# Build and start all services
docker compose -f docker/docker-compose.yml up --build

# Or run in detached mode
docker compose -f docker/docker-compose.yml up -d --build

# View logs
docker compose -f docker/docker-compose.yml logs -f
```

**Service URLs after startup:**

| Service | URL |
|---------|-----|
| Frontend | http://localhost:3000 |
| API Docs (Swagger) | http://localhost:8000/docs |
| API Docs (ReDoc) | http://localhost:8000/redoc |
| Neo4j Browser | http://localhost:7474 |

---

## 4. Local Development (Native)

For faster iteration, run databases in Docker and services natively.

### 4a. Start databases only

```bash
docker compose -f docker/docker-compose.db.yml up -d
```

### 4b. Backend

```bash
cd backend

# Create virtual environment
python -m venv .venv
source .venv/bin/activate    # Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run migrations
cd ../database
alembic upgrade head
cd ../backend

# Start dev server
uvicorn app.main:app --reload --port 8000
```

### 4c. Frontend

```bash
cd frontend

# Install dependencies
pnpm install

# Start dev server
pnpm dev
```

---

## 5. Database Migrations

```bash
# Create a new migration
cd database
alembic revision --autogenerate -m "describe your change"

# Apply migrations
alembic upgrade head

# Roll back one step
alembic downgrade -1
```

---

## 6. Neo4j Setup

1. Open Neo4j Browser at http://localhost:7474
2. Connect with username `neo4j` and your `NEO4J_PASSWORD`
3. Run initial constraints:

```bash
cypher-shell -u neo4j -p <password> -f database/neo4j/001_initial_constraints.cypher
```

---

## 7. Running Tests

```bash
# Backend tests
cd backend
pytest

# Frontend type check
cd frontend
pnpm type-check

# Frontend lint
pnpm lint
```

---

## 8. Adding ShadCN Components

```bash
cd frontend
npx shadcn@latest add button
npx shadcn@latest add card
npx shadcn@latest add dialog
# ... etc
```

---

## 9. Stopping All Services

```bash
docker compose -f docker/docker-compose.yml down

# Remove volumes (⚠ deletes all data)
docker compose -f docker/docker-compose.yml down -v
```
