# Habit Tracker

Single-tenant Flask app for daily habit tracking with streaks and trend dashboards.

## Stack

- Python 3.12 / Flask 3.1 / Gunicorn
- PostgreSQL 16 / SQLAlchemy 2.0 / Alembic (Flask-Migrate)
- Jinja2 / Bootstrap 5 / Chart.js
- Flask-Login / Flask-WTF / Flask-Session
- Docker Compose (prod + dev with hot reload)

## Project Layout

```
app/
├── __init__.py          # create_app() factory
├── config.py            # Config from env vars
├── extensions.py        # db, migrate, login_manager, csrf
├── models/              # User, Habit, CheckIn
├── services/            # Business logic (auth, habits, dashboard)
├── blueprints/
│   ├── auth/            # Login/logout, dev login fallback
│   ├── habits/          # CRUD + daily toggle
│   └── dashboard/       # Streaks, trends, charts
├── templates/           # Jinja2 + Bootstrap 5
└── static/css/
```

## Key Patterns

- Routes are thin — business logic lives in `app/services/`
- Auth: dev login (email-only, no password) when SSO env vars are unset
- Check-ins use a unique constraint on (habit_id, date) — one check-in per habit per day
- Dashboard stats are computed from CheckIn records (streaks, rates, trends)

## Deploy (docker-home)

```bash
ssh andylombardo@docker-home "cd /home/andylombardo/habit-tracker && git pull && docker compose up -d --build"
```

If models change, run migrations after deploy:
```bash
docker compose exec app flask db migrate -m "description"
docker compose exec app flask db upgrade
```

## SSO (not yet implemented)

Callback routes needed at:
- `/auth/callback/azure` (Microsoft Entra ID)
- `/auth/callback/google` (Google Workspace)
