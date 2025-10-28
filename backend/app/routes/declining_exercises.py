from datetime import datetime
from typing import List

from app.database import get_current_user, get_db
from app.schemas import (
    DecliningTrainingExerciseCreate,
    DecliningTrainingExercisePositionCreate,
    DecliningTrainingExercisePositionResponse,
    DecliningTrainingExercisePositionUpdate,
    DecliningTrainingExerciseResponse,
    DecliningTrainingExerciseUpdate,
)
from fastapi import APIRouter, Depends, HTTPException, status
from prisma import Prisma

router = APIRouter(prefix="/declining-exercises", tags=["Declining Training Exercises"])


@router.post(
    "/",
    response_model=DecliningTrainingExerciseResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_declining_training_exercise(
    declining_exercise: DecliningTrainingExerciseCreate,
    current_user=Depends(get_current_user),
    db: Prisma = Depends(get_db),
):
    # Verify plan exercise belongs to user
    plan_exercise = await db.planexercise.find_unique(
        where={"id": declining_exercise.planExerciseId},
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

    timestamp = (
        declining_exercise.timestamp if declining_exercise.timestamp else datetime.now()
    )

    new_declining_exercise = await db.decliningtrainingexercise.create(
        data={
            "timestamp": timestamp,
            "planExerciseId": declining_exercise.planExerciseId,
        }
    )
    return new_declining_exercise


@router.get(
    "/plan-exercise/{plan_exercise_id}",
    response_model=List[DecliningTrainingExerciseResponse],
)
async def get_declining_exercises_by_plan_exercise(
    plan_exercise_id: int,
    current_user=Depends(get_current_user),
    db: Prisma = Depends(get_db),
):
    # Verify plan exercise belongs to user
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

    declining_exercises = await db.decliningtrainingexercise.find_many(
        where={"planExerciseId": plan_exercise_id}
    )
    return declining_exercises


@router.get(
    "/{declining_exercise_id}", response_model=DecliningTrainingExerciseResponse
)
async def get_declining_training_exercise(
    declining_exercise_id: int,
    current_user=Depends(get_current_user),
    db: Prisma = Depends(get_db),
):
    declining_exercise = await db.decliningtrainingexercise.find_unique(
        where={"id": declining_exercise_id},
        include={
            "planExercise": {
                "include": {
                    "planTraining": {
                        "include": {"planWeek": {"include": {"plan": True}}}
                    }
                }
            }
        },
    )
    if (
        not declining_exercise
        or declining_exercise.planExercise.planTraining.planWeek.plan.userId
        != current_user.id
    ):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Declining training exercise not found",
        )
    return declining_exercise


@router.put(
    "/{declining_exercise_id}", response_model=DecliningTrainingExerciseResponse
)
async def update_declining_training_exercise(
    declining_exercise_id: int,
    declining_exercise_data: DecliningTrainingExerciseUpdate,
    current_user=Depends(get_current_user),
    db: Prisma = Depends(get_db),
):
    declining_exercise = await db.decliningtrainingexercise.find_unique(
        where={"id": declining_exercise_id},
        include={
            "planExercise": {
                "include": {
                    "planTraining": {
                        "include": {"planWeek": {"include": {"plan": True}}}
                    }
                }
            }
        },
    )
    if (
        not declining_exercise
        or declining_exercise.planExercise.planTraining.planWeek.plan.userId
        != current_user.id
    ):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Declining training exercise not found",
        )

    update_data = declining_exercise_data.model_dump(exclude_unset=True)
    updated_declining_exercise = await db.decliningtrainingexercise.update(
        where={"id": declining_exercise_id}, data=update_data
    )
    return updated_declining_exercise


@router.delete("/{declining_exercise_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_declining_training_exercise(
    declining_exercise_id: int,
    current_user=Depends(get_current_user),
    db: Prisma = Depends(get_db),
):
    declining_exercise = await db.decliningtrainingexercise.find_unique(
        where={"id": declining_exercise_id},
        include={
            "planExercise": {
                "include": {
                    "planTraining": {
                        "include": {"planWeek": {"include": {"plan": True}}}
                    }
                }
            }
        },
    )
    if (
        not declining_exercise
        or declining_exercise.planExercise.planTraining.planWeek.plan.userId
        != current_user.id
    ):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Declining training exercise not found",
        )

    await db.decliningtrainingexercise.delete(where={"id": declining_exercise_id})
    return None


# Declining Training Exercise Positions
@router.post(
    "/{declining_exercise_id}/positions",
    response_model=DecliningTrainingExercisePositionResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_declining_exercise_position(
    declining_exercise_id: int,
    position: DecliningTrainingExercisePositionCreate,
    current_user=Depends(get_current_user),
    db: Prisma = Depends(get_db),
):
    # Verify declining exercise belongs to user
    declining_exercise = await db.decliningtrainingexercise.find_unique(
        where={"id": declining_exercise_id},
        include={
            "planExercise": {
                "include": {
                    "planTraining": {
                        "include": {"planWeek": {"include": {"plan": True}}}
                    }
                }
            }
        },
    )
    if (
        not declining_exercise
        or declining_exercise.planExercise.planTraining.planWeek.plan.userId
        != current_user.id
    ):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Declining training exercise not found",
        )

    new_position = await db.decliningtrainingexerciseposition.create(
        data={
            "kgs": position.kgs,
            "reps": position.reps,
            "decliningExerciseId": declining_exercise_id,
        }
    )
    return new_position


@router.get(
    "/{declining_exercise_id}/positions",
    response_model=List[DecliningTrainingExercisePositionResponse],
)
async def get_declining_exercise_positions(
    declining_exercise_id: int,
    current_user=Depends(get_current_user),
    db: Prisma = Depends(get_db),
):
    # Verify declining exercise belongs to user
    declining_exercise = await db.decliningtrainingexercise.find_unique(
        where={"id": declining_exercise_id},
        include={
            "planExercise": {
                "include": {
                    "planTraining": {
                        "include": {"planWeek": {"include": {"plan": True}}}
                    }
                }
            }
        },
    )
    if (
        not declining_exercise
        or declining_exercise.planExercise.planTraining.planWeek.plan.userId
        != current_user.id
    ):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Declining training exercise not found",
        )

    positions = await db.decliningtrainingexerciseposition.find_many(
        where={"decliningExerciseId": declining_exercise_id}
    )
    return positions


@router.put(
    "/positions/{position_id}", response_model=DecliningTrainingExercisePositionResponse
)
async def update_declining_exercise_position(
    position_id: int,
    position_data: DecliningTrainingExercisePositionUpdate,
    current_user=Depends(get_current_user),
    db: Prisma = Depends(get_db),
):
    position = await db.decliningtrainingexerciseposition.find_unique(
        where={"id": position_id},
        include={
            "decliningExercise": {
                "include": {
                    "planExercise": {
                        "include": {
                            "planTraining": {
                                "include": {"planWeek": {"include": {"plan": True}}}
                            }
                        }
                    }
                }
            }
        },
    )
    if (
        not position
        or position.decliningExercise.planExercise.planTraining.planWeek.plan.userId
        != current_user.id
    ):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Position not found"
        )

    update_data = position_data.model_dump(exclude_unset=True)
    updated_position = await db.decliningtrainingexerciseposition.update(
        where={"id": position_id}, data=update_data
    )
    return updated_position


@router.delete("/positions/{position_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_declining_exercise_position(
    position_id: int,
    current_user=Depends(get_current_user),
    db: Prisma = Depends(get_db),
):
    position = await db.decliningtrainingexerciseposition.find_unique(
        where={"id": position_id},
        include={
            "decliningExercise": {
                "include": {
                    "planExercise": {
                        "include": {
                            "planTraining": {
                                "include": {"planWeek": {"include": {"plan": True}}}
                            }
                        }
                    }
                }
            }
        },
    )
    if (
        not position
        or position.decliningExercise.planExercise.planTraining.planWeek.plan.userId
        != current_user.id
    ):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Position not found"
        )

    await db.decliningtrainingexerciseposition.delete(where={"id": position_id})
    return None
