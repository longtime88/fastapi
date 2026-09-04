from pydantic import BaseModel
from typing import Optional

from fastapi import APIRouter, status, Depends
from sqlalchemy.orm import Session

from api.deps import get_current_user, get_db
from api.models import Workout

# Router fuer alle Workout-Endpunkte mit Prefix /workouts
router = APIRouter(
    prefix="/workouts",
    tags=["Workout"],
)


# Basis-Modell fuer Workout-Daten (wird von Create geerbt)
class WorkoutBase(BaseModel):
    name: str
    description: Optional[str] = None


# Modell fuer das Erstellen eines neuen Workouts
class WorkoutCreate(WorkoutBase):
    pass



# GET /workouts/ - Hole ein einzelnes Workout anhand der ID
@router.get("/")
def get_workout(workout_id: int, db: Session = Depends(get_db), user: dict = Depends(get_current_user)):
    return db.query(Workout).filter(Workout.id == workout_id).first()


# GET /workouts/all - Hole alle Workouts des eingeloggten Users
@router.get("/all")
def get_workouts(db: Session = Depends(get_db), user: dict = Depends(get_current_user)):
    return db.query(Workout).all()


# POST /workouts - Erstelle ein neues Workout fuer den eingeloggten User
@router.post("", status_code=status.HTTP_201_CREATED)
def create_workout(work: WorkoutCreate, db: Session = Depends(get_db), user: dict = Depends(get_current_user)):
    db_workout = Workout(**work.model_dump(), user_id=user.get("id"))
    db.add(db_workout)
    db.commit()
    db.refresh(db_workout)
    return db_workout


# DELETE /workouts/ - Loesche ein Workout anhand der ID
@router.delete("/")
def delete_workout(workout_id: int, db: Session = Depends(get_db), user: dict = Depends(get_current_user)):
    db_workout = db.query(Workout).filter(Workout.id == workout_id).first()
    if db_workout:
        db.delete(db_workout)
        db.commit()
    return db_workout

