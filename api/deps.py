from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from .core.config import ALGORITHM, SECRET_KEY
from .database import SessionLocal


# Dependency: Stellt eine Datenbank-Session fuer jeden Request bereit
# Wird automatisch am Ende des Requests geschlossen
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Passwort-Verschluesselung mit einem stabilen Backend.
# bcrypt kann in einigen Python-/passlib-Kombinationen fehlschlagen.
# PBKDF2 ist kompatibel und ausreichend fuer die lokale Anmeldung.
# sha256_crypt bleibt als Fallback fuer bereits gespeicherte Hashes erhalten.
bcrypt_context = CryptContext(
    schemes=["pbkdf2_sha256", "sha256_crypt"],
    deprecated="auto",
    pbkdf2_sha256__rounds=200000,
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
