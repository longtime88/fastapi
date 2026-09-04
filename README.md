# Email-Support-Client

A full-stack workout application with a FastAPI backend and Nuxt 4 frontend.

## Architecture

```
.
├── fastapi/          # Backend (FastAPI + SQLAlchemy + SQLite)
│   ├── api/
│   │   ├── main.py           # FastAPI app entry point
│   │   ├── database.py       # Database connection
│   │   ├── models.py         # SQLAlchemy models
│   │   └── routers/          # API route handlers
│   │       ├── auth.py       # Authentication endpoints
│   │       ├── workouts.py   # Workout endpoints
│   │       └── routines.py   # Routine endpoints
│   ├── requirements.txt
│   ├── workout_app.db        # SQLite database
│   └── .env
├── frontend/         # Frontend (Nuxt 4 + Tailwind CSS)
│   ├── app/
│   │   ├── app.vue           # Root component
│   │   ├── pages/            # Route pages
│   │   └── ...
│   ├── composables/            # Pinia-style composables
│   │   ├── useAuth.js
│   │   └── useSupport.js
│   ├── components/             # Vue components
│   └── nuxt.config.ts
└── .github/
    └── workflows/
        └── ci.yml 
        
                    # CI pipeline
```

## Development

### Prerequisites

- Python 3.11+
- Node.js 20+
- pip / npm

### Backend

```bash
cd fastapi
pip install -r requirements.txt
python -m uvicorn api.main:app --host 0.0.0.0 --port 8000 --reload
```

API docs: http://localhost:8000/docs

### Frontend

```bash
cd frontend
npm install
npm run dev
```

App: http://localhost:3000

### Environment Variables

**Frontend** (`frontend/.env`):
```
NUXT_PUBLIC_API_BASE=http://localhost:8000
NUXT_PUBLIC_SUPPORT_API_BASE=http://localhost:5000
```

**Backend** (`fastapi/.env`):
```
AUTH_SECRET_KEY=your-secret-key
AUTH_ALGORITHM=HS256
API_URL=http://localhost:3000
```

## Testing

### Frontend

```bash
cd frontend
npm run lint      # ESLint
npm run build     # Production build
```

### Backend

```bash
cd fastapi
pytest
```

## Deployment

```bash
# Build frontend
cd frontend
npm run build
# Output is in .output/

# Run backend
cd fastapi
python -m uvicorn api.main:app --host 0.0.0.0 --port 8000
```

## License
