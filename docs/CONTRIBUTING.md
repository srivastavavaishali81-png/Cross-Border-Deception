# Contributing to OZARK

Thank you for contributing! Please follow these guidelines.

---

## Branch Strategy

```
main          — production-ready code only
develop       — integration branch
feature/*     — new features (branch from develop)
fix/*         — bug fixes (branch from develop)
hotfix/*      — critical production fixes (branch from main)
```

---

## Commit Convention

We follow [Conventional Commits](https://www.conventionalcommits.org/):

```
feat(backend): add user authentication endpoint
fix(frontend): correct API client error handling
docs(arch): update port map in ARCHITECTURE.md
refactor(connectors): abstract base connector interface
test(backend): add health check tests
chore(docker): update postgres image to 16.2
```

---

## Code Standards

### Backend (Python)
- **Formatter**: `ruff format`
- **Linter**: `ruff check`
- **Type checker**: `mypy`
- Run all: `ruff format . && ruff check . && mypy app/`

### Frontend (TypeScript)
- **Formatter**: `prettier`
- **Linter**: `eslint`
- **Type checker**: `tsc --noEmit`
- Run all: `pnpm format && pnpm lint && pnpm type-check`

---

## Pull Request Checklist

- [ ] Tests pass (`pytest` / `pnpm test`)
- [ ] No type errors (`mypy` / `tsc`)
- [ ] Lint clean (`ruff` / `eslint`)
- [ ] Migration created if schema changed
- [ ] Docs updated if API changed
- [ ] PR title follows conventional commit format
