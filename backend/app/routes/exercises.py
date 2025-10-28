from typing import List

from app.database import get_current_user, get_db
from app.schemas import ExerciseCreate, ExerciseResponse, ExerciseUpdate
from fastapi import APIRouter, Depends, HTTPException, status
from prisma import Prisma

router = APIRouter(prefix="/exercises", tags=["Exercises"])


@router.post("/", response_model=ExerciseResponse, status_code=status.HTTP_201_CREATED)
async def create_exercise(
    exercise: ExerciseCreate,
    current_user=Depends(get_current_user),
    db: Prisma = Depends(get_db),
):
    new_exercise = await db.exercise.create(
        data={
            "name": exercise.name,
            "description": exercise.description,
            "video": exercise.video,
            "image": exercise.image,
            "public": exercise.public,
            "userId": current_user.id,
        }
    )
    return new_exercise


@router.get("/", response_model=List[ExerciseResponse])
async def get_exercises(
    current_user=Depends(get_current_user), db: Prisma = Depends(get_db)
):
    # Get user's exercises and public exercises
    exercises = await db.exercise.find_many(
        where={"OR": [{"userId": current_user.id}, {"public": True}]}
    )
    return exercises


@router.get("/{exercise_id}", response_model=ExerciseResponse)
async def get_exercise(
    exercise_id: int,
    current_user=Depends(get_current_user),
    db: Prisma = Depends(get_db),
):
    exercise = await db.exercise.find_first(
        where={"id": exercise_id, "OR": [{"userId": current_user.id}, {"public": True}]}
    )
    if not exercise:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Exercise not found"
        )
    return exercise


@router.put("/{exercise_id}", response_model=ExerciseResponse)
async def update_exercise(
    exercise_id: int,
    exercise_data: ExerciseUpdate,
    current_user=Depends(get_current_user),
    db: Prisma = Depends(get_db),
):
    # Check if exercise exists and belongs to user
    exercise = await db.exercise.find_first(
        where={"id": exercise_id, "userId": current_user.id}
    )
    if not exercise:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Exercise not found"
        )

    # Update exercise
    update_data = exercise_data.model_dump(exclude_unset=True)
    updated_exercise = await db.exercise.update(
        where={"id": exercise_id}, data=update_data
    )
    return updated_exercise


@router.delete("/{exercise_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_exercise(
    exercise_id: int,
    current_user=Depends(get_current_user),
    db: Prisma = Depends(get_db),
):
    # Check if exercise exists and belongs to user
    exercise = await db.exercise.find_first(
        where={"id": exercise_id, "userId": current_user.id}
    )
    if not exercise:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Exercise not found"
        )

    await db.exercise.delete(where={"id": exercise_id})
    return None
