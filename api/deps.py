import os
from dotenv import load_dotenv
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from .database import SessionLocal

# Lade Umgebungsvariablen aus .env-Datei
load_dotenv()

# Konfiguration fuer JWT-Token und Datenbank
SECRET_KEY = os.getenv("AUTH_SECRET_KEY")
ALGORITHM = os.getenv("AUTH_ALGORITHM")
DATABASE_URL = os.getenv("DATABASE_URL")


# Dependency: Stellt eine Datenbank-Session fuer jeden Request bereit
# Wird automatisch am Ende des Requests geschlossen
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Passwort-Verschluesselung mit bcrypt
# Using sha256_crypt as fallback to avoid bcrypt version issues
bcrypt_context = CryptContext(
    schemes=["bcrypt", "sha256_crypt"],
    deprecated="auto",
    bcrypt__rounds=12,
)

# OAuth2 Password Bearer: Extrahiert Token aus dem Authorization-Header
oauth2_bearer = OAuth2PasswordBearer(tokenUrl="auth/token")


# Dependency: Extrahiert und verifiziert den JWT-Token aus dem Request
# Gibt den eingeloggten User (username + id) zurueck oder wirft 401
async def get_current_user(token: str = Depends(oauth2_bearer)):
    try:
        # Token decodieren und Payload auslesen
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        user_id: int = payload.get("id")
        if username is None or user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate user")
        return {"username": username, "id": user_id}
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate user")
