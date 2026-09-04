import os

from datetime import datetime, timedelta, timezone
from typing import Annotated

from dotenv import load_dotenv
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from jose import jwt
from passlib.context import CryptContext
from pydantic import BaseModel
from sqlalchemy.orm import Session

from api.deps import bcrypt_context, get_current_user, get_db
from api.models import User

load_dotenv()

# Router fuer alle Auth-Endpunkte mit Prefix /auth
router = APIRouter(
    prefix="/auth",
    tags=["auth"],
)

# JWT-Konfiguration aus Umgebungsvariablen
SECRET_KEY = os.getenv("AUTH_SECRET_KEY")
ALGORITHM = os.getenv("AUTH_ALGORITHM")


# Pydantic-Modell fuer Registrierungs-Request (username + password)
class UserCreateRequest(BaseModel):
    username: str
    password: str


# Pydantic-Modell fuer Login-Response (JWT-Token)
class Token(BaseModel):
    access_token: str
    token_type: str


# Pydantic-Modell fuer Token-Payload (wird in JWT codiert)
class TokenData(BaseModel):
    username: str | None = None
    id: int | None = None
    exp: datetime | None = None


# Pydantic-Modell fuer User-Response (ohne Passwort)
class UserResponse(BaseModel):
    username: str
    id: int


# Authentifiziere User anhand von username und password
# Gibt das User-Objekt zurueck oder False bei Fehler
def authenticate_user(username: str, password: str, db: Session):
    user = db.query(User).filter(User.username == username).first()
    if not user:
        return False
    if not bcrypt_context.verify(password, user.hashed_password):
        return False
    return user


# Erstelle einen JWT-Access-Token mit username, user_id und Ablaufzeit
def create_access_token(username: str, user_id: int, expires_delta: timedelta):
    encoded_data = {"sub": username, "id": user_id}
    expires = datetime.now(timezone.utc) + expires_delta
    encoded_data.update({"exp": expires})
    return jwt.encode(encoded_data, SECRET_KEY, algorithm=ALGORITHM)


# POST /auth/ - Registriere einen neuen Benutzer
@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_user(request: UserCreateRequest, db: Session = Depends(get_db)):
    # Pruefe, ob Username bereits existiert
    existing_user = db.query(User).filter(User.username == request.username).first()
    if existing_user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Username already exists")

    # Erstelle neuen User mit gehashtem Passwort
    create_user_model = User(
        username=request.username,
        hashed_password=bcrypt_context.hash(request.password),
    )
    db.add(create_user_model)
    db.commit()
    db.refresh(create_user_model)
    return {"username": create_user_model.username, "id": create_user_model.id}


# POST /auth/token - Login: Erstelle JWT-Token fuer eingeloggten User
@router.post("/token", response_model=Token)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Session = Depends(get_db),
):
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect username or password")
    # Token ist 30 Minuten gueltig
    token = create_access_token(username=user.username, user_id=user.id, expires_delta=timedelta(minutes=30))
    return Token(access_token=token, token_type="bearer")


# GET /auth/me - Gibt die Daten des aktuell eingeloggten Users zurueck
# Benoetigt gueltigen JWT-Token im Authorization-Header
@router.get("/me", response_model=UserResponse)
async def get_current_user(user: dict = Depends(get_current_user)):
    return {"username": user["username"], "id": user["id"]}


