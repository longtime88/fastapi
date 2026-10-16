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


# Routine-Modell: Eine Trainingsroutine (z.B. "Beintag")
# Besteht aus mehreren Workouts, gehoert zu einem Benutzer
class Routine(Base):
    __tablename__ = "routines"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    name = Column(String, index=True)
    description = Column(String, index=True)
    
    workouts = relationship("Workout", secondary=workout_routine_association, back_populates="routines")


# Add back_populates to Workout
class Workout(Base):
    __tablename__ = "workouts"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    name = Column(String, index=True)
    description = Column(String, index=True)
    
    routines = relationship("Routine", secondary=workout_routine_association, back_populates="workouts")
   
    
    