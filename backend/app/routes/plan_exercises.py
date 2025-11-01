from typing import List

from app.database import get_current_user, get_db
from app.schemas import PlanExerciseCreate, PlanExerciseResponse, PlanExerciseUpdate
from fastapi import APIRouter, Depends, HTTPException, status
from prisma import Prisma

router = APIRouter(prefix="/plan-exercises", tags=["Plan Exercises"])


@router.post(
    "/", response_model=PlanExerciseResponse, status_code=status.HTTP_201_CREATED
)
async def create_plan_exercise(
    plan_exercise: PlanExerciseCreate,
    current_user=Depends(get_current_user),
    db: Prisma = Depends(get_db),
):
    # Verify plan training belongs to user
    plan_training = await db.plantraining.find_unique(
        where={"id": plan_exercise.planTrainingId},
        include={"planWeek": {"include": {"plan": True}}},
    )
    if not plan_training or plan_training.planWeek.plan.userId != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Plan training not found"
        )

    # Verify exercise exists and is accessible
    exercise = await db.exercise.find_first(
        where={
            "id": plan_exercise.exerciseId,
            "OR": [{"userId": current_user.id}, {"public": True}],
        }
    )
    if not exercise:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Exercise not found"
        )

    new_plan_exercise = await db.planexercise.create(
        data={
            "intensity": plan_exercise.intensity,
            "planTrainingId": plan_exercise.planTrainingId,
            "exerciseId": plan_exercise.exerciseId,
        }
    )
    return new_plan_exercise


@router.get("/training/{plan_training_id}", response_model=List[PlanExerciseResponse])
async def get_plan_exercises_by_training(
    plan_training_id: int,
    current_user=Depends(get_current_user),
    db: Prisma = Depends(get_db),
):
    # Verify plan training belongs to user or is public
    plan_training = await db.plantraining.find_unique(
        where={"id": plan_training_id},
        include={"planWeek": {"include": {"plan": True}}},
    )
    if not plan_training or (plan_training.planWeek.plan.userId != current_user.id and not plan_training.planWeek.plan.public):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Plan training not found"
        )

    plan_exercises = await db.planexercise.find_many(
        where={"planTrainingId": plan_training_id}, include={"exercise": True}
    )
    return plan_exercises


@router.get("/{plan_exercise_id}", response_model=PlanExerciseResponse)
async def get_plan_exercise(
    plan_exercise_id: int,
    current_user=Depends(get_current_user),
    db: Prisma = Depends(get_db),
):
    plan_exercise = await db.planexercise.find_unique(
        where={"id": plan_exercise_id},
        include={
            "planTraining": {"include": {"planWeek": {"include": {"plan": True}}}},
            "exercise": True
        },
    )
    # Allow access if plan belongs to user or is public
    if (
        not plan_exercise
        or (plan_exercise.planTraining.planWeek.plan.userId != current_user.id 
            and not plan_exercise.planTraining.planWeek.plan.public)
    ):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Plan exercise not found"
        )
    return plan_exercise


@router.put("/{plan_exercise_id}", response_model=PlanExerciseResponse)
async def update_plan_exercise(
    plan_exercise_id: int,
    plan_exercise_data: PlanExerciseUpdate,
    current_user=Depends(get_current_user),
    db: Prisma = Depends(get_db),
):
    plan_exercise = await db.planexercise.find_unique(
        where={"id": plan_exercise_id},
        include={
            "planTraining": {"include": {"planWeek": {"include": {"plan": True}}}}
        },
    )
    if (
        not plan_exercise
        or plan_exercise.planTraining.planWeek.plan.userId != current_user.id
    ):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Plan exercise not found"
        )

    update_data = plan_exercise_data.model_dump(exclude_unset=True)
    updated_plan_exercise = await db.planexercise.update(
        where={"id": plan_exercise_id}, data=update_data
    )
    return updated_plan_exercise


@router.delete("/{plan_exercise_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_plan_exercise(
    plan_exercise_id: int,
    current_user=Depends(get_current_user),
    db: Prisma = Depends(get_db),
):
    plan_exercise = await db.planexercise.find_unique(
        where={"id": plan_exercise_id},
        include={
            "planTraining": {"include": {"planWeek": {"include": {"plan": True}}}}
        },
    )
    if (
        not plan_exercise
        or plan_exercise.planTraining.planWeek.plan.userId != current_user.id
    ):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Plan exercise not found"
        )

    await db.planexercise.delete(where={"id": plan_exercise_id})
    return None
