# OZARK — Makefile
# Convenience aliases for common development tasks.
# Requires: Docker, pnpm, Python 3.12+

.PHONY: help up down up-db up-db-down backend frontend migrate lint test

COMPOSE      = docker compose -f docker/docker-compose.yml
COMPOSE_DB   = docker compose -f docker/docker-compose.db.yml

help:          ## Show this help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-18s\033[0m %s\n", $$1, $$2}'

# ── Docker ────────────────────────────────────────────────────────────────────
up:            ## Start all services (Docker)
	$(COMPOSE) up --build

up-d:          ## Start all services detached
	$(COMPOSE) up -d --build

down:          ## Stop all services
	$(COMPOSE) down

down-v:        ## Stop all services and remove volumes ⚠
	$(COMPOSE) down -v

up-db:         ## Start databases only (dev mode)
	$(COMPOSE_DB) up -d

down-db:       ## Stop databases
	$(COMPOSE_DB) down

logs:          ## Tail all service logs
	$(COMPOSE) logs -f

# ── Backend ───────────────────────────────────────────────────────────────────
backend:       ## Run FastAPI dev server
	cd backend && uvicorn app.main:app --reload --port 8000

migrate:       ## Apply Alembic migrations
	cd database && alembic upgrade head

migrate-new:   ## Create a new migration (set MSG= to describe it)
	cd database && alembic revision --autogenerate -m "$(MSG)"

seed:          ## Seed database with 50 companies (Python)
	cd backend && python -m app.db.seed

seed-sql:      ## Seed database with 50 companies (SQL)
	docker exec -i ozark-postgres psql -U ozark_user -d ozark < database/seeds/002_seed_50_companies.sql

# ── Frontend ──────────────────────────────────────────────────────────────────
frontend:      ## Run Next.js dev server
	cd frontend && pnpm dev

install:       ## Install frontend dependencies
	cd frontend && pnpm install

# ── Quality ───────────────────────────────────────────────────────────────────
lint:          ## Run all linters
	cd backend && ruff check app/ && mypy app/
	cd frontend && pnpm lint && pnpm type-check

format:        ## Auto-format code
	cd backend && ruff format app/
	cd frontend && pnpm format

test:          ## Run all tests
	cd backend && pytest
