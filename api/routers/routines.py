from pydantic import BaseModel
from typing import List, Optional
from fastapi import APIRouter, status, Depends
from sqlalchemy.orm import joinedload, Session

from api.deps import get_current_user, get_db
from api.models import Routine, Workout

# Router fuer alle Routine-Endpunkte mit Prefix /routines
router = APIRouter(
    prefix="/routines",
    tags=["Routine"],
)

# Basis-Modell fuer Routine-Daten (wird von Create geerbt)
class RoutineBase(BaseModel):
    name: str
    description: Optional[str] = None


# Modell fuer das Erstellen einer neuen Routine
# Erwartet eine Liste von Workout-IDs, die der Routine hinzugefuegt werden
class RoutineCreate(RoutineBase):
    workouts: List[int]


# GET /routines/ - Hole alle Routines des eingeloggten Users
# joinedload laedt die zugehoerigen Workouts gleich mit (Eager Loading)
@router.get("/")
def get_routine(routine_id: int, db: Session = Depends(get_db), user: dict = Depends(get_current_user)):
    return db.query(Routine).options(joinedload(Routine.workouts)).filter(Routine.user_id == user.get('id')).all()
    


# GET /routines/ - Erstelle eine neue Routine fuer den eingeloggten User
# Erwartet RoutineCreate mit name, description und Liste von Workout-IDs
@router.get("/")
def create_routine(routine: RoutineCreate, db: Session = Depends(get_db), user: dict = Depends(get_current_user)):
    # Erstelle die Routine
    db_routine = Routine(name = routine.name, description = routine.description, user_id = user.get("id"))
    # Fuege alle angegebenen Workouts zur Routine hinzu
    for workout_id in routine.workouts: 
        workout = db.query(Workout).filter(Workout.id == workout_id).first()
        if workout:
            db_routine.workouts.append(workout)
    db.add(db_routine)
    db.commit()
    db.refresh(db_routine)
    # Lade die Routine nochmal mit den zugehoerigen Workouts fuer die Response
    db_routine = db.query(Routine).options(joinedload(Routine.workouts)).filter(Routine.id == db_routine.id).first()
    return db_routine


# DELETE /routines/ - Loesche eine Routine anhand der ID
@router.delete("/")
def delete_routine(routine_id: int, db: Session = Depends(get_db), user: dict = Depends(get_current_user)):
    db_routine = db.query(Routine).filter(Routine.id == routine_id, ).first()
    if db_routine:
        db.delete(db_routine)
        db.commit()
        return db_routine


