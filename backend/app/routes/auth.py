from datetime import timedelta

from app.auth import create_access_token, get_password_hash, verify_password
from app.config import settings
from app.database import get_db
from app.schemas import Token, UserCreate, UserLogin, UserResponse
from fastapi import APIRouter, Depends, HTTPException, status
from prisma import Prisma

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post(
    "/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED
)
async def register(user: UserCreate, db: Prisma = Depends(get_db)):
    # Check if user already exists
    existing_user = await db.user.find_unique(where={"username": user.username})
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered",
        )

    # Hash the password
    hashed_password = get_password_hash(user.password)

    # Create new user
    new_user = await db.user.create(
        data={"username": user.username, "password": hashed_password}
    )

    return new_user


@router.post("/login", response_model=Token)
async def login(user_data: UserLogin, db: Prisma = Depends(get_db)):
    # Find user
    user = await db.user.find_unique(where={"username": user_data.username})

    if not user or not verify_password(user_data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Create access token
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )

    return {"access_token": access_token, "token_type": "bearer"}
