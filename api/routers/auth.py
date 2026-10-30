from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from ..deps import get_current_user, get_db
from ..schemas.auth import Token, UserCreateRequest, UserResponse
from ..services import auth_service

# Router fuer alle Auth-Endpunkte mit Prefix /auth
router = APIRouter(
    prefix="/auth",
    tags=["auth"],
)

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=UserResponse)
def create_user(request: UserCreateRequest, db: Session = Depends(get_db)):
    try:
        user = auth_service.register_user(db, request.username, request.password)
    except auth_service.UserAlreadyExistsError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Username already exists",
        )

    return {"username": user.username, "id": user.id}


# POST /auth/token - Login: Erstelle JWT-Token fuer eingeloggten User
@router.post("/token", response_model=Token)
def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Session = Depends(get_db),
):
    try:
        access_token = auth_service.login(
            db,
            form_data.username,
            form_data.password,
        )
    except auth_service.InvalidCredentialsError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )

    return Token(access_token=access_token, token_type="bearer")


# GET /auth/me - Gibt die Daten des aktuell eingeloggten Users zurueck
# Benoetigt gueltigen JWT-Token im Authorization-Header
@router.get("/me", response_model=UserResponse)
def get_me(current_user: dict = Depends(get_current_user)):
    return current_user


