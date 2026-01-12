# Management System

Opinionated starter for a management system application with a Django backend and a Vite + React frontend. This repository includes a Docker-based development setup and convenience scripts for local development.

---

## Contents / Quick overview

- Backend: Django (project: `Management_system`) — located in `backend/`  
- Frontend: Vite + React — located in `frontend/`  
- Orchestration: `docker-compose.yml` to run the Django app and a Postgres database  
- Python requirements: `backend/requirements.txt`  
- Node dependencies: `frontend/package.json`

---

## Features (inferred)
- REST API via Django REST Framework
- PostgreSQL database (Postgres 13 in docker-compose)
- JWT authentication dependency listed (`djangorestframework-simplejwt`)
- API documentation/developer utilities listed (`drf-spectacular`, `drf-yasg`)
- Separately packaged frontend (Vite + React)

---

## Tech stack
- Python 3.9 (Dockerfile uses `python:3.9-alpine3.13`)
- Django 3.2.x
- Django REST Framework
- PostgreSQL 13 (Docker)
- Node (for frontend) with Vite and React

---

## Prerequisites

- Docker & docker-compose (recommended for quick start)
- OR for local development:
  - Python 3.9
  - pip
  - Node.js (recommend Node 18+)
  - npm or yarn

---

## Quick start (recommended — Docker)

From the repository root:

1. Build and start containers:
   ```bash
   docker-compose up --build
   ```
2. Services:
   - Backend (Django) will be available on http://localhost:8000
   - Postgres DB is created by docker-compose (DB user/db name/password set in `docker-compose.yml`)

The compose file runs:
- `python manage.py wait_for_db` (script referenced in the Docker command)
- `python manage.py migrate`
- `python manage.py runserver 0.0.0.0:8000`

If you need to run the containers in the background:
```bash
docker-compose up --build -d
```

To stop and remove containers:
```bash
docker-compose down
```

---

## Backend — Local development (without Docker)

1. Create and activate virtual environment:
   ```bash
   cd backend
   python -m venv .venv
   source .venv/bin/activate   # macOS/Linux
   .venv\Scripts\activate      # Windows (PowerShell)
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set required environment variables (example):
   ```bash
   export DB_HOST=localhost
   export DB_NAME=devdb
   export DB_USER=devuser
   export DB_PASS=changeme
   export DJANGO_SETTINGS_MODULE=Management_system.settings
   export DEBUG=1
   ```

   Note: `DJANGO_SETTINGS_MODULE` in this project is `Management_system.settings` (capital `M` and underscore).

4. Run migrations and start the dev server:
   ```bash
   python manage.py migrate
   python manage.py runserver 0.0.0.0:8000
   ```

If you use a local Postgres instance, ensure a database/user matching the environment variables exists (or adjust env vars accordingly).

---

## Frontend — Local development

1. Install node dependencies:
   ```bash
   cd frontend
   npm install
   ```

2. Start dev server (Vite):
   ```bash
   npm run dev
   ```

3. Build for production:
   ```bash
   npm run build
   ```

4. Preview production build:
   ```bash
   npm run preview
   ```

The frontend package.json declares React 19 and Vite; ensure your Node version is compatible (Node 18+ recommended).

---

## Environment variables (summary)

Used in docker-compose and referenced by the project:

- Backend / Django:
  - DJANGO_SETTINGS_MODULE=Management_system.settings
  - DB_HOST (e.g., `DB` when using docker-compose)
  - DB_NAME
  - DB_USER
  - DB_PASS
  - DEBUG (0/1)

- Database (when using docker-compose):
  - POSTGRES_DB
  - POSTGRES_USER
  - POSTGRES_PASSWORD

Adjust values as needed in your environment or CI.

---

## Project structure (top-level)
- backend/          — Django project (settings, apps, manage.py)
  - requirements.txt
  - requirements.dev.txt
  - Dockerfile
  - manage.py
- frontend/         — Vite + React frontend
- docker-compose.yml
- package.json      — root (some deps), plus frontend/package.json
- node_modules/     — present in repo (typically this is gitignored in most projects)

---

## Notes, gotchas & troubleshooting

- DJANGO_SETTINGS_MODULE is set to `Management_system.settings` (capitalization matters). If you see settings import errors, check the environment variable spelling and case.
- If migrations fail against the DB, ensure that Postgres is reachable from Django and that DB credentials match.
- In Docker, the backend uses a Python virtual environment inside the image (`/py`) — the Dockerfile installs dependencies listed in backend/requirements.txt.
- If static/media files are required for production, run `python manage.py collectstatic` and configure static file serving (nginx or whitenoise) as needed.
- node_modules is present in the repo — for clean local setup you can remove it and run `npm ci` or `npm install`.

---

## Tests
No tests are present in the repository (none detected). Add backend tests (Django `manage.py test`) and frontend tests (Jest/Vitest) as desired.

---

## Contributing
- Fork the repository, create a branch, make changes, open a PR.
- Please include tests for new features and run linters:
  - Backend dev requirements include `flake8` in `requirements.dev.txt`.
  - Frontend has eslint configured; run `npm run lint` in `frontend`.

---

## License
No license file detected. Add a LICENSE file (e.g., MIT, Apache-2.0) to make the repository license explicit.

---

## Contact / Author
Project owner: Nozima (GitHub: [Nozima-Rustamova](https://github.com/Nozima-Rustamova))

---

If you'd like, I can:
- Commit this README.md to the repository,
- Add a CONTRIBUTING.md or LICENSE file,
- Generate simple example environment files (.env.example) and/or a Makefile for common tasks.
Tell me which you'd prefer next.
