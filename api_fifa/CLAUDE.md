# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Context

This is a Django 6.0 teaching project for the IFPI TDS 386 Backend Web Programming course (2026.1). It models a FIFA World Cup management API, currently serving HTML templates (not a REST API yet).

- Python 3.13.1 (managed via pyenv)
- Django 6.0.5 with SQLite
- Virtual environment at `.venv/`

## Commands

All commands must be run from `api_fifa/` with the venv activated:

```bash
source .venv/bin/activate
```

| Task | Command |
|---|---|
| Run dev server | `python manage.py runserver` |
| Run tests | `python manage.py test` |
| Run a single test | `python manage.py test core.tests.TestClassName.test_method` |
| Make migrations | `python manage.py makemigrations` |
| Apply migrations | `python manage.py migrate` |
| Open Django shell | `python manage.py shell` |
| Create superuser | `python manage.py createsuperuser` |

## Architecture

Single Django app (`core`) inside the `api_fifa` project package.

**Request flow:** `api_fifa/urls.py` → `core/urls.py` → `core/views.py` → Django template (`core/templates/`)

**Key URLs:**
- `GET /selecoes/` — lists all registered national teams (renders `selecoes.html`)
- `GET /painel/` — Django admin panel

**Data model (`core/models.py`):**
- `Selecao` — national team with `pais` (country), `tecnico` (coach), `grupo_fase1` (group A–G)

**Database:** SQLite (`db.sqlite3`), already migrated. Admin panel has `Selecao` registered for data entry.
