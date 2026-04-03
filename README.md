# Habit Tracker

A daily habit tracking app for setting goals, checking off completions, and monitoring streaks and trends over time.

Built with Flask, PostgreSQL, Bootstrap 5, and Chart.js. Deployed with Docker Compose.

## Features

- **Daily habits** — create habits with custom names, descriptions, and colors
- **One-click check-off** — toggle completion for each habit daily
- **Dashboard** — 30-day completion rate, current/longest streaks, weekly and monthly trend charts
- **Dev login** — email-only sign-in when SSO is not configured
- **SSO-ready** — supports Microsoft Entra ID and Google Workspace when configured

## Quick Start

```bash
git clone git@github.com:BardSec/habit-tracker.git
cd habit-tracker
cp .env.example .env
# Edit .env with your settings
docker compose up -d --build
```

Run the initial database migration:

```bash
docker compose exec app flask db init
docker compose exec app flask db migrate -m "initial schema"
docker compose exec app flask db upgrade
```

The app will be available at `http://localhost:5000`.

## Environment Variables

| Variable | Required | Description |
|---|---|---|
| `SECRET_KEY` | Yes | Random string for session signing |
| `DATABASE_URL` | Yes | PostgreSQL connection string (default works with included Docker Compose) |
| `ADMIN_EMAILS` | Yes | Comma-separated list of emails that get admin role on first login |
| `AZURE_CLIENT_ID` | No | Microsoft Entra ID application (client) ID |
| `AZURE_CLIENT_SECRET` | No | Microsoft Entra ID client secret |
| `AZURE_TENANT_ID` | No | Microsoft Entra ID directory (tenant) ID |
| `GOOGLE_CLIENT_ID` | No | Google Workspace OAuth 2.0 client ID |
| `GOOGLE_CLIENT_SECRET` | No | Google Workspace OAuth 2.0 client secret |

When all SSO variables are unset, the app falls back to dev login (email-only, no password).

## SSO Configuration

### Microsoft Entra ID

1. Go to [Azure Portal > App registrations](https://portal.azure.com/#view/Microsoft_AAD_RegisteredApps/ApplicationsListBlade) and create a new registration
2. Set the **Redirect URI** to:
   - Type: **Web**
   - URI: `https://yourdomain.com/auth/callback/azure`
   - For local dev: `http://localhost:5000/auth/callback/azure`
3. Under **Certificates & secrets**, create a new client secret
4. Set the following in your `.env`:
   ```
   AZURE_CLIENT_ID=<Application (client) ID>
   AZURE_CLIENT_SECRET=<Client secret value>
   AZURE_TENANT_ID=<Directory (tenant) ID>
   ```

### Google Workspace

1. Go to [Google Cloud Console > Credentials](https://console.cloud.google.com/apis/credentials) and create an OAuth 2.0 Client ID
2. Set the **Authorized redirect URI** to:
   - `https://yourdomain.com/auth/callback/google`
   - For local dev: `http://localhost:5000/auth/callback/google`
3. Set the following in your `.env`:
   ```
   GOOGLE_CLIENT_ID=<Client ID>
   GOOGLE_CLIENT_SECRET=<Client secret>
   ```

### Redirect URI Summary

| Provider | Redirect URI |
|---|---|
| Microsoft Entra ID | `https://<yourdomain>/auth/callback/azure` |
| Google Workspace | `https://<yourdomain>/auth/callback/google` |
| Local dev (Entra) | `http://localhost:5000/auth/callback/azure` |
| Local dev (Google) | `http://localhost:5000/auth/callback/google` |

## Development

Use the dev compose file for hot reload:

```bash
docker compose -f docker-compose.dev.yml up --build
```

### Running Tests

Tests require a local PostgreSQL instance:

```bash
createdb habit_tracker_test
pytest
```

### Database Migrations

```bash
docker compose exec app flask db migrate -m "description of change"
docker compose exec app flask db upgrade
```

## Tech Stack

- Python 3.12 / Flask 3.1
- PostgreSQL 16 / SQLAlchemy 2.0 / Alembic
- Jinja2 / Bootstrap 5 / Chart.js
- Flask-Login / Flask-WTF / Flask-Session
- Docker / Docker Compose
- Gunicorn
