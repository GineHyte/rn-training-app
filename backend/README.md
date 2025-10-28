# Training App Backend

FastAPI backend with Prisma ORM for the Training App.

## Features

- User authentication with JWT
- Complete CRUD operations for:
  - Plans
  - Plan Weeks
  - Plan Trainings
  - Plan Exercises
  - Exercises
  - Trainings
  - Training Exercises
  - Declining Training Exercises
  - Declining Training Exercise Positions

## Setup

### Prerequisites

- Python 3.8+
- PostgreSQL database

### Installation

1. Create a virtual environment:
```bash
python -m venv venv
```

2. Activate the virtual environment:
```bash
# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Copy `.env.example` to `.env` and configure your database:
```bash
copy .env.example .env
```

5. Update the `.env` file with your PostgreSQL connection string:
```
DATABASE_URL="postgresql://user:password@localhost:5432/training_app?schema=public"
JWT_SECRET="your-secret-key-change-this-in-production"
```

6. Generate Prisma client:
```bash
prisma generate
```

7. Run migrations:
```bash
prisma db push
```

## Running the Server

```bash
python main.py
```

Or using uvicorn directly:
```bash
uvicorn main:app --reload
```

The API will be available at `http://localhost:8000`

## API Documentation

Once the server is running, visit:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## API Endpoints

### Authentication
- `POST /auth/register` - Register new user
- `POST /auth/login` - Login user

### Plans
- `POST /plans/` - Create plan
- `GET /plans/` - Get all user plans
- `GET /plans/{id}` - Get plan by ID
- `PUT /plans/{id}` - Update plan
- `DELETE /plans/{id}` - Delete plan

### Plan Weeks
- `POST /plan-weeks/` - Create plan week
- `GET /plan-weeks/plan/{plan_id}` - Get plan weeks by plan
- `GET /plan-weeks/{id}` - Get plan week by ID
- `PUT /plan-weeks/{id}` - Update plan week
- `DELETE /plan-weeks/{id}` - Delete plan week

### Plan Trainings
- `POST /plan-trainings/` - Create plan training
- `GET /plan-trainings/week/{plan_week_id}` - Get plan trainings by week
- `GET /plan-trainings/{id}` - Get plan training by ID
- `PUT /plan-trainings/{id}` - Update plan training
- `DELETE /plan-trainings/{id}` - Delete plan training

### Exercises
- `POST /exercises/` - Create exercise
- `GET /exercises/` - Get all exercises (user's + public)
- `GET /exercises/{id}` - Get exercise by ID
- `PUT /exercises/{id}` - Update exercise
- `DELETE /exercises/{id}` - Delete exercise

### Plan Exercises
- `POST /plan-exercises/` - Create plan exercise
- `GET /plan-exercises/training/{plan_training_id}` - Get plan exercises by training
- `GET /plan-exercises/{id}` - Get plan exercise by ID
- `PUT /plan-exercises/{id}` - Update plan exercise
- `DELETE /plan-exercises/{id}` - Delete plan exercise

### Trainings
- `POST /trainings/` - Start training
- `GET /trainings/` - Get all user trainings
- `GET /trainings/{id}` - Get training by ID
- `PUT /trainings/{id}` - Update training
- `POST /trainings/{id}/end` - End training
- `DELETE /trainings/{id}` - Delete training

### Training Exercises
- `POST /training-exercises/` - Create training exercise
- `GET /training-exercises/training/{training_id}` - Get training exercises
- `GET /training-exercises/{id}` - Get training exercise by ID
- `PUT /training-exercises/{id}` - Update training exercise
- `DELETE /training-exercises/{id}` - Delete training exercise

### Declining Exercises
- `POST /declining-exercises/` - Create declining exercise
- `GET /declining-exercises/plan-exercise/{plan_exercise_id}` - Get declining exercises
- `GET /declining-exercises/{id}` - Get declining exercise by ID
- `PUT /declining-exercises/{id}` - Update declining exercise
- `DELETE /declining-exercises/{id}` - Delete declining exercise
- `POST /declining-exercises/{id}/positions` - Add position
- `GET /declining-exercises/{id}/positions` - Get positions
- `PUT /declining-exercises/positions/{id}` - Update position
- `DELETE /declining-exercises/positions/{id}` - Delete position

## Database Schema

The Prisma schema includes the following models:
- User
- Plan
- PlanWeek
- PlanTraining
- PlanExercise
- Exercise
- Training
- TrainingExercise
- DecliningTrainingExercise
- DecliningTrainingExercisePosition

All models have proper relations and cascade deletion configured.

## Authentication

All endpoints (except `/auth/register` and `/auth/login`) require authentication via Bearer token.

Include the token in the Authorization header:
```
Authorization: Bearer <your_token>
```
