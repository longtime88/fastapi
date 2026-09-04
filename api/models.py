from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship
from .database import Base


# Viele-zu-Viele Verknuepfungstabelle zwischen Workouts und Routines
# Ein Workout kann in mehreren Routines vorkommen, eine Routine kann mehrere Workouts enthalten
workout_routine_association = Table(
    'workout_routine', Base.metadata,
    Column("workout_id", Integer, ForeignKey('workouts.id')),
    Column("routine_id", Integer, ForeignKey('routines.id'))
)


# Benutzer-Modell: Speichert Benutzername und gehashtes Passwort
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)


# Workout-Modell: Ein einzelnes Training (z.B. "Bankdruecken")
# Gehoert zu einem Benutzer und kann in mehreren Routines vorkommen
class Workout(Base):
    __tablename__ = "workouts"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    name = Column(String, index=True)
    description = Column(String, index=True)
    
  


# Routine-Modell: Eine Trainingsroutine (z.B. "Beintag")
# Besteht aus mehreren Workouts, gehoert zu einem Benutzer
class Routine(Base):
    __tablename__ = "routines"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    name = Column(String, index=True)
    description = Column(String, index=True)
   
    
    