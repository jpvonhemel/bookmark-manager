# Bookmark Manager

A self-hosted bookmark manager with a dark-themed web UI. Save, organize, and access your bookmarks from any device on your network.

## Branches

| Branch | Database | Use case |
|--------|----------|----------|
| `main` | SQLite | Simple single-host setup |
| `postgres-backend` | PostgreSQL | Multi-host shared database |

## Quick Start (SQLite — single host)

```bash
git clone https://github.com/jpvonhemel/bookmark-manager.git
cd bookmark-manager
docker compose up -d --build
```

Open `http://<your-host>:5000`

## PostgreSQL Setup (multi-host)

### Primary host (runs the database)

```bash
git clone -b postgres-backend https://github.com/jpvonhemel/bookmark-manager.git
cd bookmark-manager
```

Edit `docker-compose.yml` and change `changeme_secure_password` to a real password (both `DB_PASS` and `POSTGRES_PASSWORD` must match).

```bash
docker compose up -d --build
```

Open `http://<your-host>:5001`

### Additional hosts (connect to existing database)

```bash
git clone -b postgres-backend https://github.com/jpvonhemel/bookmark-manager.git
cd bookmark-manager
```

Edit `docker-compose.remote.yml`:
- Set `DB_HOST` to the IP or hostname of your primary host
- Set `DB_PASS` to match the password on the primary host

```bash
docker compose -f docker-compose.remote.yml up -d --build
```

Open `http://<your-host>:5001`

All instances share the same database — bookmarks added on any host appear everywhere.

## Updating

On any host:

```bash
cd bookmark-manager
git pull
docker compose up -d --build
```

## Ports

| Branch | App port | Database port |
|--------|----------|---------------|
| main | 5000 | — |
| postgres-backend | 5001 | 5432 |

## Features

- Add bookmarks with title, URL, and category
- Click anywhere on a card to open the link
- Delete bookmarks with the X button
- Responsive grid layout adapts to screen width
- Default bookmarks seeded on fresh install
- Dark theme with lime green accents

## Tech Stack

- Python / Flask
- SQLite (main branch) or PostgreSQL 16 (postgres-backend branch)
- HTML / CSS
- Docker / Docker Compose
