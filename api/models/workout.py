from sqlalchemy import Column, ForeignKey, Integer, String, Table
from sqlalchemy.orm import relationship

from ..database import Base


workout_routine_association = Table(
    "workout_routine",
    Base.metadata,
    Column("workout_id", Integer, ForeignKey("workouts.id")),
    Column("routine_id", Integer, ForeignKey("routines.id")),
)


class Routine(Base):
    __tablename__ = "routines"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    name = Column(String, index=True)
    description = Column(String, index=True)

    workouts = relationship(
        "Workout",
        secondary=workout_routine_association,
        back_populates="routines",
    )


class Workout(Base):
    __tablename__ = "workouts"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    name = Column(String, index=True)
    description = Column(String, index=True)

    routines = relationship(
        "Routine",
        secondary=workout_routine_association,
        back_populates="workouts",
    )
