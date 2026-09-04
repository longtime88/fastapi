from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import  sessionmaker


# SQLite-Datenbank-URL: Lokale Datei workout_app.db im Projektverzeichnis
SQL_ALCHEMY_DATABASE_URL = 'sqlite:///workout_app.db'

# SQLAlchemy Engine: Verbindung zur Datenbank
# check_same_thread=False ist fuer SQLite erforderlich bei Multi-Threading (z.B. FastAPI + Uvicorn)
engine = create_engine(SQL_ALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})

# SessionLocal: Factory fuer Datenbank-Sessions
# autocommit=False: Aenderungen muessen explizit committet werden
# autoflush=False: Kein automatisches Flush vor Queries
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base: Basisklasse fuer alle SQLAlchemy-Modelle (Tabellen-Definitionen)
Base = declarative_base()