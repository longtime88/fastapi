# FastAPI-Backend

Das Backend stellt die Benutzerregistrierung und Authentifizierung für das Support-Portal bereit.

## Voraussetzungen

- Python 3.11 oder neuer

## Installation

```bash
cd fastapi
python -m venv .venv
source .venv/bin/activate       # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

Erstelle `fastapi/.env`:

```env
AUTH_SECRET_KEY=ein-langes-zufaelliges-geheimnis
AUTH_ALGORITHM=HS256
```

## Start

```bash
python -m uvicorn api.main:app --reload --port 8000
```

API: <http://localhost:8000>  
API-Dokumentation: <http://localhost:8000/docs>

## Endpunkte

- `POST /auth/` – Benutzer registrieren
- `POST /auth/token` – anmelden und JWT erhalten
- `GET /auth/me` – angemeldeten Benutzer abrufen

## Tests

```bash
python -m pytest
```

Die SQLite-Datenbank wird lokal als `workout_app.db` angelegt. Produktionssysteme sollten eine geeignete persistente Datenbank und Migrationen verwenden.
