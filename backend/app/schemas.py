from datetime import datetime
from typing import Optional

from pydantic import BaseModel


# User Schemas
class UserBase(BaseModel):
    username: str


class UserCreate(UserBase):
    password: str


class UserLogin(BaseModel):
    username: str
    password: str


class UserResponse(UserBase):
    id: int
    createdAt: datetime
    updatedAt: datetime

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str


# Plan Schemas
class PlanBase(BaseModel):
    name: str
    startDate: Optional[datetime] = None
    public: bool = False


class PlanCreate(PlanBase):
    pass


class PlanUpdate(BaseModel):
    name: Optional[str] = None
    startDate: Optional[datetime] = None
    public: Optional[bool] = None


class PlanResponse(PlanBase):
    id: int
    userId: int
    createdAt: datetime
    updatedAt: datetime

    class Config:
        from_attributes = True


# PlanWeek Schemas
class PlanWeekBase(BaseModel):
    startDate: Optional[datetime] = None


class PlanWeekCreate(PlanWeekBase):
    planId: int


class PlanWeekUpdate(BaseModel):
    startDate: Optional[datetime] = None


class PlanWeekResponse(PlanWeekBase):
    id: int
    planId: int
    createdAt: datetime
    updatedAt: datetime

    class Config:
        from_attributes = True


# PlanTraining Schemas
class PlanTrainingBase(BaseModel):
    name: str
    startTime: Optional[datetime] = None
    endTime: Optional[datetime] = None
    intensity: int


class PlanTrainingCreate(PlanTrainingBase):
    planWeekId: int


class PlanTrainingUpdate(BaseModel):
    name: Optional[str] = None
    startTime: Optional[datetime] = None
    endTime: Optional[datetime] = None
    intensity: Optional[int] = None


class PlanTrainingResponse(PlanTrainingBase):
    id: int
    planWeekId: int
    createdAt: datetime
    updatedAt: datetime

    class Config:
        from_attributes = True


# Exercise Schemas
class ExerciseBase(BaseModel):
    name: str
    description: Optional[str] = None
    video: Optional[str] = None
    image: Optional[str] = None
    public: bool = False


class ExerciseCreate(ExerciseBase):
    pass


class ExerciseUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    video: Optional[str] = None
    image: Optional[str] = None
    public: Optional[bool] = None


class ExerciseResponse(ExerciseBase):
    id: int
    userId: int
    createdAt: datetime
    updatedAt: datetime

    class Config:
        from_attributes = True


# PlanExercise Schemas
class PlanExerciseBase(BaseModel):
    intensity: int


class PlanExerciseCreate(PlanExerciseBase):
    planTrainingId: int
    exerciseId: int


class PlanExerciseUpdate(BaseModel):
    intensity: Optional[int] = None


class PlanExerciseResponse(PlanExerciseBase):
    id: int
    planTrainingId: int
    exerciseId: int
    exercise: Optional["ExerciseResponse"] = None
    createdAt: datetime
    updatedAt: datetime

    class Config:
        from_attributes = True


# Training Schemas
class TrainingBase(BaseModel):
    startTime: Optional[datetime] = None
    endTime: Optional[datetime] = None


class TrainingCreate(BaseModel):
    planTrainingId: int
    startTime: Optional[datetime] = None


class TrainingUpdate(BaseModel):
    endTime: Optional[datetime] = None


class TrainingResponse(TrainingBase):
    id: int
    planTrainingId: int
    createdAt: datetime
    updatedAt: datetime

    class Config:
        from_attributes = True


# TrainingExercise Schemas
class TrainingExerciseBase(BaseModel):
    reps: int
    kgs: float
    timestamp: datetime


class TrainingExerciseCreate(TrainingExerciseBase):
    trainingId: int
    planExerciseId: int


class TrainingExerciseUpdate(BaseModel):
    reps: Optional[int] = None
    kgs: Optional[float] = None


class TrainingExerciseResponse(TrainingExerciseBase):
    id: int
    trainingId: int
    planExerciseId: int
    createdAt: datetime
    updatedAt: datetime

    class Config:
        from_attributes = True


# DecliningTrainingExercise Schemas
class DecliningTrainingExerciseBase(BaseModel):
    timestamp: datetime


class DecliningTrainingExerciseCreate(BaseModel):
    planExerciseId: int
    timestamp: Optional[datetime] = None


class DecliningTrainingExerciseUpdate(BaseModel):
    timestamp: Optional[datetime] = None


class DecliningTrainingExerciseResponse(DecliningTrainingExerciseBase):
    id: int
    planExerciseId: int
    createdAt: datetime
    updatedAt: datetime

    class Config:
        from_attributes = True


# DecliningTrainingExercisePosition Schemas
class DecliningTrainingExercisePositionBase(BaseModel):
    kgs: float
    reps: int


class DecliningTrainingExercisePositionCreate(DecliningTrainingExercisePositionBase):
    decliningExerciseId: int


class DecliningTrainingExercisePositionUpdate(BaseModel):
    kgs: Optional[float] = None
    reps: Optional[int] = None


class DecliningTrainingExercisePositionResponse(DecliningTrainingExercisePositionBase):
    id: int
    decliningExerciseId: int
    createdAt: datetime
    updatedAt: datetime

    class Config:
        from_attributes = True


# Update forward references
PlanExerciseResponse.model_rebuild()
