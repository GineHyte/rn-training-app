from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from datetime import datetime
from prisma import Prisma
from app.schemas import TrainingCreate, TrainingUpdate, TrainingResponse
from app.database import get_db, get_current_user

router = APIRouter(prefix="/trainings", tags=["Trainings"])


@router.post("/", response_model=TrainingResponse, status_code=status.HTTP_201_CREATED)
async def create_training(
    training: TrainingCreate,
    current_user = Depends(get_current_user),
    db: Prisma = Depends(get_db)
):
    # Verify plan training belongs to user
    plan_training = await db.plantraining.find_unique(
        where={"id": training.planTrainingId},
        include={"planWeek": {"include": {"plan": True}}}
    )
    if not plan_training or plan_training.planWeek.plan.userId != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Plan training not found"
        )
    
    new_training = await db.training.create(
        data={
            "startTime": training.startTime if training.startTime else datetime.now(),
            "planTrainingId": training.planTrainingId
        }
    )
    return new_training


@router.get("/", response_model=List[TrainingResponse])
async def get_trainings(
    current_user = Depends(get_current_user),
    db: Prisma = Depends(get_db)
):
    # Get all trainings for user's plan trainings
    trainings = await db.training.find_many(
        where={
            "planTraining": {
                "is": {
                    "planWeek": {
                        "is": {
                            "plan": {
                                "is": {
                                    "userId": current_user.id
                                }
                            }
                        }
                    }
                }
            }
        }
    )
    return trainings


@router.get("/{training_id}", response_model=TrainingResponse)
async def get_training(
    training_id: int,
    current_user = Depends(get_current_user),
    db: Prisma = Depends(get_db)
):
    training = await db.training.find_unique(
        where={"id": training_id},
        include={"planTraining": {"include": {"planWeek": {"include": {"plan": True}}}}}
    )
    if not training or training.planTraining.planWeek.plan.userId != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Training not found"
        )
    return training


@router.put("/{training_id}", response_model=TrainingResponse)
async def update_training(
    training_id: int,
    training_data: TrainingUpdate,
    current_user = Depends(get_current_user),
    db: Prisma = Depends(get_db)
):
    training = await db.training.find_unique(
        where={"id": training_id},
        include={"planTraining": {"include": {"planWeek": {"include": {"plan": True}}}}}
    )
    if not training or training.planTraining.planWeek.plan.userId != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Training not found"
        )
    
    update_data = training_data.model_dump(exclude_unset=True)
    updated_training = await db.training.update(
        where={"id": training_id},
        data=update_data
    )
    return updated_training


@router.post("/{training_id}/end", response_model=TrainingResponse)
async def end_training(
    training_id: int,
    current_user = Depends(get_current_user),
    db: Prisma = Depends(get_db)
):
    training = await db.training.find_unique(
        where={"id": training_id},
        include={"planTraining": {"include": {"planWeek": {"include": {"plan": True}}}}}
    )
    if not training or training.planTraining.planWeek.plan.userId != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Training not found"
        )
    
    updated_training = await db.training.update(
        where={"id": training_id},
        data={"endTime": datetime.now()}
    )
    return updated_training


@router.delete("/{training_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_training(
    training_id: int,
    current_user = Depends(get_current_user),
    db: Prisma = Depends(get_db)
):
    training = await db.training.find_unique(
        where={"id": training_id},
        include={"planTraining": {"include": {"planWeek": {"include": {"plan": True}}}}}
    )
    if not training or training.planTraining.planWeek.plan.userId != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Training not found"
        )
    
    await db.training.delete(where={"id": training_id})
    return None
