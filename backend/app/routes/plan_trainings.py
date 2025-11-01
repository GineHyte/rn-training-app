from typing import List

from app.database import get_current_user, get_db
from app.schemas import PlanTrainingCreate, PlanTrainingResponse, PlanTrainingUpdate
from fastapi import APIRouter, Depends, HTTPException, status
from prisma import Prisma

router = APIRouter(prefix="/plan-trainings", tags=["Plan Trainings"])


@router.post(
    "/", response_model=PlanTrainingResponse, status_code=status.HTTP_201_CREATED
)
async def create_plan_training(
    plan_training: PlanTrainingCreate,
    current_user=Depends(get_current_user),
    db: Prisma = Depends(get_db),
):
    # Verify plan week belongs to user's plan
    plan_week = await db.planweek.find_unique(
        where={"id": plan_training.planWeekId}, include={"plan": True}
    )
    if not plan_week or plan_week.plan.userId != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Plan week not found"
        )

    new_plan_training = await db.plantraining.create(
        data={
            "name": plan_training.name,
            "startTime": plan_training.startTime,
            "endTime": plan_training.endTime,
            "intensity": plan_training.intensity,
            "planWeekId": plan_training.planWeekId,
        }
    )
    return new_plan_training


@router.get("/week/{plan_week_id}", response_model=List[PlanTrainingResponse])
async def get_plan_trainings_by_week(
    plan_week_id: int,
    current_user=Depends(get_current_user),
    db: Prisma = Depends(get_db),
):
    # Verify plan week belongs to user's plan or is public
    plan_week = await db.planweek.find_unique(
        where={"id": plan_week_id}, include={"plan": True}
    )
    if not plan_week or (plan_week.plan.userId != current_user.id and not plan_week.plan.public):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Plan week not found"
        )

    plan_trainings = await db.plantraining.find_many(where={"planWeekId": plan_week_id})
    return plan_trainings


@router.get("/{plan_training_id}", response_model=PlanTrainingResponse)
async def get_plan_training(
    plan_training_id: int,
    current_user=Depends(get_current_user),
    db: Prisma = Depends(get_db),
):
    plan_training = await db.plantraining.find_unique(
        where={"id": plan_training_id},
        include={"planWeek": {"include": {"plan": True}}},
    )
    # Allow access if plan belongs to user or is public
    if not plan_training or (plan_training.planWeek.plan.userId != current_user.id and not plan_training.planWeek.plan.public):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Plan training not found"
        )
    return plan_training


@router.put("/{plan_training_id}", response_model=PlanTrainingResponse)
async def update_plan_training(
    plan_training_id: int,
    plan_training_data: PlanTrainingUpdate,
    current_user=Depends(get_current_user),
    db: Prisma = Depends(get_db),
):
    plan_training = await db.plantraining.find_unique(
        where={"id": plan_training_id},
        include={"planWeek": {"include": {"plan": True}}},
    )
    if not plan_training or plan_training.planWeek.plan.userId != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Plan training not found"
        )

    update_data = plan_training_data.model_dump(exclude_unset=True)
    updated_plan_training = await db.plantraining.update(
        where={"id": plan_training_id}, data=update_data
    )
    return updated_plan_training


@router.delete("/{plan_training_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_plan_training(
    plan_training_id: int,
    current_user=Depends(get_current_user),
    db: Prisma = Depends(get_db),
):
    plan_training = await db.plantraining.find_unique(
        where={"id": plan_training_id},
        include={"planWeek": {"include": {"plan": True}}},
    )
    if not plan_training or plan_training.planWeek.plan.userId != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Plan training not found"
        )

    await db.plantraining.delete(where={"id": plan_training_id})
    return None
