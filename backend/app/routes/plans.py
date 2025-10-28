from typing import List

from app.database import get_current_user, get_db
from app.schemas import PlanCreate, PlanResponse, PlanUpdate
from fastapi import APIRouter, Depends, HTTPException, status
from prisma import Prisma

router = APIRouter(prefix="/plans", tags=["Plans"])


@router.post("/", response_model=PlanResponse, status_code=status.HTTP_201_CREATED)
async def create_plan(
    plan: PlanCreate,
    current_user=Depends(get_current_user),
    db: Prisma = Depends(get_db),
):
    new_plan = await db.plan.create(
        data={
            "name": plan.name,
            "startDate": plan.startDate,
            "public": plan.public,
            "userId": current_user.id,
        }
    )
    return new_plan


@router.get("/", response_model=List[PlanResponse])
async def get_plans(
    current_user=Depends(get_current_user), db: Prisma = Depends(get_db)
):
    plans = await db.plan.find_many(where={"userId": current_user.id})
    return plans


@router.get("/{plan_id}", response_model=PlanResponse)
async def get_plan(
    plan_id: int, current_user=Depends(get_current_user), db: Prisma = Depends(get_db)
):
    plan = await db.plan.find_first(where={"id": plan_id, "userId": current_user.id})
    if not plan:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Plan not found"
        )
    return plan


@router.put("/{plan_id}", response_model=PlanResponse)
async def update_plan(
    plan_id: int,
    plan_data: PlanUpdate,
    current_user=Depends(get_current_user),
    db: Prisma = Depends(get_db),
):
    # Check if plan exists and belongs to user
    plan = await db.plan.find_first(where={"id": plan_id, "userId": current_user.id})
    if not plan:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Plan not found"
        )

    # Update plan
    update_data = plan_data.model_dump(exclude_unset=True)
    updated_plan = await db.plan.update(where={"id": plan_id}, data=update_data)
    return updated_plan


@router.delete("/{plan_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_plan(
    plan_id: int, current_user=Depends(get_current_user), db: Prisma = Depends(get_db)
):
    # Check if plan exists and belongs to user
    plan = await db.plan.find_first(where={"id": plan_id, "userId": current_user.id})
    if not plan:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Plan not found"
        )

    await db.plan.delete(where={"id": plan_id})
    return None
