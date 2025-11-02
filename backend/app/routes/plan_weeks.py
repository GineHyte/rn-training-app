from typing import List

from app.database import get_current_user, get_db
from app.schemas import PlanWeekCreate, PlanWeekResponse, PlanWeekUpdate
from fastapi import APIRouter, Depends, HTTPException, status
from prisma import Prisma

router = APIRouter(prefix="/plan-weeks", tags=["Plan Weeks"])


@router.post("/", response_model=PlanWeekResponse, status_code=status.HTTP_201_CREATED)
async def create_plan_week(
    plan_week: PlanWeekCreate,
    current_user=Depends(get_current_user),
    db: Prisma = Depends(get_db),
):
    # Verify plan belongs to user
    plan = await db.plan.find_first(
        where={"id": plan_week.planId, "userId": current_user.id}
    )
    if not plan:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Plan not found"
        )

    from datetime import datetime
    new_plan_week = await db.planweek.create(
        data={
            "startDate": plan_week.startDate if plan_week.startDate else datetime.now(),
            "planId": plan_week.planId
        }
    )
    return new_plan_week


@router.get("/plan/{plan_id}", response_model=List[PlanWeekResponse])
async def get_plan_weeks_by_plan(
    plan_id: int, current_user=Depends(get_current_user), db: Prisma = Depends(get_db)
):
    # Verify plan belongs to user or is public
    plan = await db.plan.find_first(
        where={"id": plan_id, "OR": [{"userId": current_user.id}, {"public": True}]}
    )
    if not plan:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Plan not found"
        )

    plan_weeks = await db.planweek.find_many(where={"planId": plan_id})
    return plan_weeks


@router.get("/{plan_week_id}", response_model=PlanWeekResponse)
async def get_plan_week(
    plan_week_id: int,
    current_user=Depends(get_current_user),
    db: Prisma = Depends(get_db),
):
    plan_week = await db.planweek.find_unique(
        where={"id": plan_week_id}, include={"plan": True}
    )
    # Allow access if plan belongs to user or is public
    if not plan_week or (plan_week.plan.userId != current_user.id and not plan_week.plan.public):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Plan week not found"
        )
    return plan_week


@router.put("/{plan_week_id}", response_model=PlanWeekResponse)
async def update_plan_week(
    plan_week_id: int,
    plan_week_data: PlanWeekUpdate,
    current_user=Depends(get_current_user),
    db: Prisma = Depends(get_db),
):
    plan_week = await db.planweek.find_unique(
        where={"id": plan_week_id}, include={"plan": True}
    )
    if not plan_week or plan_week.plan.userId != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Plan week not found"
        )

    update_data = plan_week_data.model_dump(exclude_unset=True)
    updated_plan_week = await db.planweek.update(
        where={"id": plan_week_id}, data=update_data
    )
    return updated_plan_week


@router.delete("/{plan_week_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_plan_week(
    plan_week_id: int,
    current_user=Depends(get_current_user),
    db: Prisma = Depends(get_db),
):
    plan_week = await db.planweek.find_unique(
        where={"id": plan_week_id}, include={"plan": True}
    )
    if not plan_week or plan_week.plan.userId != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Plan week not found"
        )

    await db.planweek.delete(where={"id": plan_week_id})
    return None
