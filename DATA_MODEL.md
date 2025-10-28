# Training App - Data Model & Flow

## Entity Relationships

```
User
 ├─── Plans (1:N)
 │     └─── PlanWeeks (1:N)
 │           └─── PlanTrainings (1:N)
 │                 ├─── PlanExercises (1:N)
 │                 │     ├─── Exercise (N:1)
 │                 │     ├─── TrainingExercises (1:N)
 │                 │     └─── DecliningTrainingExercises (1:N)
 │                 │           └─── DecliningTrainingExercisePositions (1:N)
 │                 │
 │                 └─── Trainings (1:N)
 │                       └─── TrainingExercises (1:N)
 │
 └─── Exercises (1:N)
```

## Typical User Flow

### 1. Setup Phase
```
User registers/logs in
  ↓
Creates Exercises
  ↓
Creates a Plan
  ↓
Adds Plan Weeks to Plan
  ↓
Adds Plan Trainings to each Week
  ↓
Adds Plan Exercises to each Training
```

### 2. Workout Phase
```
User starts Training (links to Plan Training)
  ↓
Performs exercises from Plan Training
  ↓
Logs Training Exercises (reps, weight, timestamp)
  OR
Logs Declining Training Exercise with positions
  ↓
Ends Training (sets end timestamp)
```

## Data Model Details

### User
- **Purpose**: Authentication and ownership
- **Relations**: Owns Plans and Exercises
- **Fields**: username, password (hashed)

### Plan
- **Purpose**: High-level training program
- **Example**: "Summer Cut 2024", "Strength Building"
- **Fields**: name, startDate, public
- **Relations**: Belongs to User, has PlanWeeks

### PlanWeek
- **Purpose**: Organize plan by weeks
- **Example**: "Week 1", "Week 2"
- **Fields**: startDate
- **Relations**: Belongs to Plan, has PlanTrainings

### PlanTraining
- **Purpose**: Scheduled training session
- **Example**: "Monday - Chest & Triceps", "Wednesday - Legs"
- **Fields**: name, startTime, endTime, intensity (1-10)
- **Relations**: Belongs to PlanWeek, has PlanExercises and Trainings

### Exercise
- **Purpose**: Exercise library/catalog
- **Example**: "Bench Press", "Squats", "Pull-ups"
- **Fields**: name, description, video, image, public
- **Relations**: Belongs to User, used in PlanExercises
- **Note**: Can be shared (public) or private

### PlanExercise
- **Purpose**: Exercise instance in a training plan
- **Example**: "3x10 Bench Press at 70% intensity"
- **Fields**: intensity
- **Relations**: Links Exercise to PlanTraining

### Training
- **Purpose**: Actual workout session
- **Example**: User performs "Monday Workout" on Jan 15, 2024
- **Fields**: startTime, endTime
- **Relations**: Links to PlanTraining, has TrainingExercises
- **Note**: This is the ACTUAL workout, not the plan

### TrainingExercise
- **Purpose**: Individual set logged during workout
- **Example**: "Set 1: 10 reps at 100kg at 10:30 AM"
- **Fields**: reps, kgs, timestamp
- **Relations**: Belongs to Training and references PlanExercise

### DecliningTrainingExercise
- **Purpose**: Drop set tracking
- **Example**: "Declining Bench Press - 3 drops"
- **Fields**: timestamp
- **Relations**: References PlanExercise, has Positions
- **Note**: For exercises with progressive weight reduction

### DecliningTrainingExercisePosition
- **Purpose**: Individual position in a drop set
- **Example**: "Position 1: 100kg x 10 reps", "Position 2: 80kg x 8 reps"
- **Fields**: kgs, reps
- **Relations**: Belongs to DecliningTrainingExercise

## Example Workout Session

### Setup (Done Once)
```
1. User creates Exercise: "Bench Press"
2. User creates Plan: "Strength Program"
3. User adds PlanWeek: "Week 1"
4. User adds PlanTraining: "Monday - Upper Body"
5. User adds PlanExercise: Links "Bench Press" to "Monday - Upper Body"
```

### Execution (Each Workout)
```
1. User starts Training (links to "Monday - Upper Body")
   - Creates Training record with startTime

2. User performs Bench Press:
   - Set 1: Logs TrainingExercise (100kg, 10 reps, 10:30 AM)
   - Set 2: Logs TrainingExercise (100kg, 8 reps, 10:32 AM)
   - Set 3: Logs TrainingExercise (100kg, 6 reps, 10:34 AM)

3. User performs Drop Set:
   - Creates DecliningTrainingExercise
   - Position 1: 100kg x 10 reps
   - Position 2: 80kg x 8 reps
   - Position 3: 60kg x 12 reps

4. User ends Training
   - Updates Training record with endTime
```

## Key Concepts

### Plans vs Trainings
- **Plan**: The program/schedule (what you PLAN to do)
- **Training**: The actual workout (what you DID)

### Public vs Private
- **Public Exercises**: Shared library everyone can use
- **Private Exercises**: Personal custom exercises
- **Public Plans**: Shareable workout programs
- **Private Plans**: Personal training programs

### Intensity
- Scale of 1-10
- Used in PlanTraining (overall session intensity)
- Used in PlanExercise (exercise-specific intensity)

### Timestamps
- **Plan dates**: When to start the program
- **Training times**: Actual workout start/end
- **Exercise timestamps**: When each set was performed

## API Usage Patterns

### Creating a Complete Plan
```
1. POST /plans/ - Create plan
2. POST /plan-weeks/ - Add weeks
3. POST /plan-trainings/ - Add trainings to weeks
4. POST /exercises/ - Create exercises (if needed)
5. POST /plan-exercises/ - Add exercises to trainings
```

### Starting a Workout
```
1. GET /plan-trainings/{id} - Get today's training
2. POST /trainings/ - Start training session
3. GET /plan-exercises/training/{id} - Get exercises to perform
4. POST /training-exercises/ - Log each set
5. POST /trainings/{id}/end - End workout
```

### Tracking Progress
```
1. GET /trainings/ - Get all workouts
2. GET /training-exercises/training/{id} - Get sets for workout
3. Analyze: reps, weight, timestamp data
4. Compare: against plan expectations
```

## Frontend Screen Flow

```
Login Screen
  ↓
Plans List Screen
  ├─→ Create Plan Screen
  └─→ Plan Detail Screen
       ├─→ Add Week Screen
       └─→ Week Detail Screen
            ├─→ Add Training Screen
            └─→ Training Detail Screen
                 ├─→ Add Exercise Screen
                 └─→ Start Workout Screen
                      ├─→ Log Exercise Screen
                      └─→ Complete Workout Screen

Exercise Library Screen
  ├─→ Create Exercise Screen
  └─→ Exercise Detail Screen
```

## Backend Route Structure

```
/auth
  POST /register
  POST /login

/plans
  CRUD operations

/plan-weeks
  CRUD operations
  GET /plan/{plan_id}

/plan-trainings
  CRUD operations
  GET /week/{week_id}

/exercises
  CRUD operations

/plan-exercises
  CRUD operations
  GET /training/{training_id}

/trainings
  CRUD operations
  POST /{id}/end

/training-exercises
  CRUD operations
  GET /training/{training_id}

/declining-exercises
  CRUD operations
  Positions sub-routes
```

## Common Queries

### "What exercises are in my Monday workout?"
```
GET /plan-trainings/{monday_training_id}
  includes: plan-exercises -> exercise
```

### "What did I lift last Monday?"
```
GET /trainings/?filter=last_monday
GET /training-exercises/training/{training_id}
```

### "What's my progress on Bench Press?"
```
GET /training-exercises/?exercise=bench_press
  sort by timestamp
  analyze weight/reps trends
```

### "Who can see my workout plan?"
```
Check Plan.public field
  true = Everyone can see
  false = Only you can see
```

This structure provides maximum flexibility while maintaining data integrity and clear relationships!
