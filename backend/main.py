from app.database import prisma
from app.routes import (
    auth,
    declining_exercises,
    exercises,
    plan_exercises,
    plan_trainings,
    plan_weeks,
    plans,
    training_exercises,
    trainings,
)
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="Training App API",
    description="API for managing training plans, exercises, and workouts",
    version="1.0.0",
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Startup and shutdown events
@app.on_event("startup")
async def startup():
    await prisma.connect()


@app.on_event("shutdown")
async def shutdown():
    await prisma.disconnect()


# Root endpoint
@app.get("/")
async def root():
    return {"message": "Welcome to Training App API", "version": "1.0.0"}


# Health check
@app.get("/health")
async def health_check():
    return {"status": "healthy"}


# Include routers
app.include_router(auth.router)
app.include_router(plans.router)
app.include_router(plan_weeks.router)
app.include_router(plan_trainings.router)
app.include_router(plan_exercises.router)
app.include_router(exercises.router)
app.include_router(trainings.router)
app.include_router(training_exercises.router)
app.include_router(declining_exercises.router)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
