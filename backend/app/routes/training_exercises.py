from typing import List

from app.database import get_current_user, get_db
from app.schemas import (
    TrainingExerciseCreate,
    TrainingExerciseResponse,
    TrainingExerciseUpdate,
)
from fastapi import APIRouter, Depends, HTTPException, status
from prisma import Prisma

router = APIRouter(prefix="/training-exercises", tags=["Training Exercises"])


@router.post(
    "/", response_model=TrainingExerciseResponse, status_code=status.HTTP_201_CREATED
)
async def create_training_exercise(
    training_exercise: TrainingExerciseCreate,
    current_user=Depends(get_current_user),
    db: Prisma = Depends(get_db),
):
    # Verify training belongs to user
    training = await db.training.find_unique(
        where={"id": training_exercise.trainingId},
        include={
            "planTraining": {"include": {"planWeek": {"include": {"plan": True}}}}
        },
    )
    if not training or training.planTraining.planWeek.plan.userId != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Training not found"
        )

    # Verify plan exercise belongs to the same plan training
    plan_exercise = await db.planexercise.find_unique(
        where={"id": training_exercise.planExerciseId}, include={"planTraining": True}
    )
    if not plan_exercise or plan_exercise.planTrainingId != training.planTrainingId:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Plan exercise does not belong to this training's plan",
        )

    new_training_exercise = await db.trainingexercise.create(
        data={
            "reps": training_exercise.reps,
            "kgs": training_exercise.kgs,
            "timestamp": training_exercise.timestamp,
            "trainingId": training_exercise.trainingId,
            "planExerciseId": training_exercise.planExerciseId,
        }
    )
    return new_training_exercise


@router.get("/training/{training_id}", response_model=List[TrainingExerciseResponse])
async def get_training_exercises_by_training(
    training_id: int,
    current_user=Depends(get_current_user),
    db: Prisma = Depends(get_db),
):
    # Verify training belongs to user
    training = await db.training.find_unique(
        where={"id": training_id},
        include={
            "planTraining": {"include": {"planWeek": {"include": {"plan": True}}}}
        },
    )
    if not training or training.planTraining.planWeek.plan.userId != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Training not found"
        )

    training_exercises = await db.trainingexercise.find_many(
        where={"trainingId": training_id}
    )
    return training_exercises


@router.get("/{training_exercise_id}", response_model=TrainingExerciseResponse)
async def get_training_exercise(
    training_exercise_id: int,
    current_user=Depends(get_current_user),
    db: Prisma = Depends(get_db),
):
    training_exercise = await db.trainingexercise.find_unique(
        where={"id": training_exercise_id},
        include={
            "training": {
                "include": {
                    "planTraining": {
                        "include": {"planWeek": {"include": {"plan": True}}}
                    }
                }
            }
        },
    )
    if (
        not training_exercise
        or training_exercise.training.planTraining.planWeek.plan.userId
        != current_user.id
    ):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Training exercise not found"
        )
    return training_exercise


@router.put("/{training_exercise_id}", response_model=TrainingExerciseResponse)
async def update_training_exercise(
    training_exercise_id: int,
    training_exercise_data: TrainingExerciseUpdate,
    current_user=Depends(get_current_user),
    db: Prisma = Depends(get_db),
):
    training_exercise = await db.trainingexercise.find_unique(
        where={"id": training_exercise_id},
        include={
            "training": {
                "include": {
                    "planTraining": {
                        "include": {"planWeek": {"include": {"plan": True}}}
                    }
                }
            }
        },
    )
    if (
        not training_exercise
        or training_exercise.training.planTraining.planWeek.plan.userId
        != current_user.id
    ):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Training exercise not found"
        )

    update_data = training_exercise_data.model_dump(exclude_unset=True)
    updated_training_exercise = await db.trainingexercise.update(
        where={"id": training_exercise_id}, data=update_data
    )
    return updated_training_exercise


@router.delete("/{training_exercise_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_training_exercise(
    training_exercise_id: int,
    current_user=Depends(get_current_user),
    db: Prisma = Depends(get_db),
):
    training_exercise = await db.trainingexercise.find_unique(
        where={"id": training_exercise_id},
        include={
            "training": {
                "include": {
                    "planTraining": {
                        "include": {"planWeek": {"include": {"plan": True}}}
                    }
                }
            }
        },
    )
    if (
        not training_exercise
        or training_exercise.training.planTraining.planWeek.plan.userId
        != current_user.id
    ):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Training exercise not found"
        )

    await db.trainingexercise.delete(where={"id": training_exercise_id})
    return None
