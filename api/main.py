from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers import auth, workouts, routines
from .database import Base, engine


app = FastAPI()


# Erstelle alle Tabellen in der SQLite-Datenbank beim Start
Base.metadata.create_all(bind=engine)

# CORS-Konfiguration: Erlaubt Anfragen von allen Origins
# Wichtig fuer Frontend-Anwendungen, die auf einem anderen Port laufen
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=["*"],
)

# Health-Check-Endpunkt zum Ueberpruefen, ob der Server laeuft



@app.get("/")
def health_check():
    return {"message": "Health check complete"}

@app.get("/")
def get_error():
    return {"message": "An error occurred"}    

# Registriere alle Router (API-Endpunkte)
app.include_router(auth.router)
app.include_router(workouts.router)
app.include_router(routines.router)




