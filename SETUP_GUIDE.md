# Training App - Setup Guide

## ✅ What Has Been Created

### Backend (FastAPI + Prisma)
✅ Complete Prisma schema with all 10 models
✅ User authentication with JWT
✅ CRUD routes for all entities:
  - Plans
  - Plan Weeks
  - Plan Trainings
  - Plan Exercises
  - Exercises
  - Trainings
  - Training Exercises
  - Declining Training Exercises
  - Declining Training Exercise Positions
✅ Proper authorization and ownership checks
✅ Cascade deletion configured
✅ Environment configuration
✅ Documentation

### Frontend (React Native + Expo)
✅ Navigation setup with React Navigation
✅ Authentication screens (Login/Register)
✅ Plans management screens
✅ Exercises management screens
✅ API service layer with Axios
✅ JWT token management
✅ TypeScript interfaces
✅ Documentation

## 🚀 Getting Started

### 🐳 Quick Start with Docker (Easiest)

```bash
# Clone or navigate to project
cd rnTrainingsApp

# Start everything
docker-compose up -d

# Check if running
docker-compose ps

# View logs
docker-compose logs -f
```

**That's it!** Your backend is now running at:
- API: http://localhost:8000
- Docs: http://localhost:8000/docs

See [DOCKER_GUIDE.md](DOCKER_GUIDE.md) for more Docker commands.

### 💻 Manual Setup

#### Step 1: Backend Setup

```bash
# Navigate to backend
cd backend

# Create virtual environment
python -m venv venv

# Activate (Windows)
venv\Scripts\activate

# Activate (Linux/Mac)
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
copy .env.example .env
# Edit .env with your PostgreSQL credentials

# Generate Prisma client
prisma generate

# Push schema to database
prisma db push

# Start server
python main.py
```

Backend will run on: http://localhost:8000
API Docs: http://localhost:8000/docs

### Step 2: Frontend Setup

```bash
# Navigate to frontend
cd frontend

# Install dependencies
npm install

# Update API URL in src/services/api.ts
# For Android emulator: http://10.0.2.2:8000
# For iOS simulator: http://localhost:8000
# For physical device: http://YOUR_IP:8000

# Start Expo
npm start
```

## 📊 Database Models

1. **User** - Authentication
2. **Plan** - Training plans
3. **PlanWeek** - Weekly structure
4. **PlanTraining** - Scheduled sessions
5. **PlanExercise** - Exercises in training
6. **Exercise** - Exercise library
7. **Training** - Actual workout sessions
8. **TrainingExercise** - Logged sets
9. **DecliningTrainingExercise** - Drop sets
10. **DecliningTrainingExercisePosition** - Drop set positions

## 🔧 Next Steps

### Immediate
1. Install backend dependencies: `pip install -r requirements.txt`
2. Setup PostgreSQL database
3. Configure .env file
4. Run Prisma migrations
5. Install frontend dependencies: `npm install`
6. Update API URL in frontend

### Development
1. Add remaining screens for trainings
2. Implement training session flow
3. Add form validation
4. Improve error handling
5. Add loading states
6. Implement search/filtering

### Production
1. Deploy backend (Docker/Cloud)
2. Configure production database
3. Build mobile apps
4. Enable HTTPS
5. Add analytics
6. Implement CI/CD

## 🧪 Testing

### Quick Test (No Setup Required)
```bash
# Ensure backend is running, then:
cd backend
python run_tests.py
```

This will test all major endpoints and show results.

### Full Test Suite
```bash
cd backend
pytest -v
```

### Test with Docker
```bash
docker-compose exec backend pytest -v
```

See [TESTING_GUIDE.md](TESTING_GUIDE.md) for comprehensive testing documentation.

### Authentication
- POST `/auth/register` - Register user
- POST `/auth/login` - Login user

### Plans
- GET/POST `/plans/`
- GET/PUT/DELETE `/plans/{id}`

### Plan Weeks
- POST `/plan-weeks/`
- GET `/plan-weeks/plan/{plan_id}`
- GET/PUT/DELETE `/plan-weeks/{id}`

### Plan Trainings
- POST `/plan-trainings/`
- GET `/plan-trainings/week/{plan_week_id}`
- GET/PUT/DELETE `/plan-trainings/{id}`

### Exercises
- GET/POST `/exercises/`
- GET/PUT/DELETE `/exercises/{id}`

### Plan Exercises
- POST `/plan-exercises/`
- GET `/plan-exercises/training/{plan_training_id}`
- GET/PUT/DELETE `/plan-exercises/{id}`

### Trainings
- GET/POST `/trainings/`
- GET/PUT/DELETE `/trainings/{id}`
- POST `/trainings/{id}/end`

### Training Exercises
- POST `/training-exercises/`
- GET `/training-exercises/training/{training_id}`
- GET/PUT/DELETE `/training-exercises/{id}`

### Declining Exercises
- GET/POST/PUT/DELETE `/declining-exercises/`
- GET/POST `/declining-exercises/{id}/positions`
- PUT/DELETE `/declining-exercises/positions/{id}`

## 🔒 Security

- JWT authentication required for all endpoints (except login/register)
- Passwords hashed with bcrypt
- User-based ownership validation
- Cascade deletion for data integrity
- CORS configured (update for production)

## 🎯 Features Implemented

✅ User registration and login
✅ JWT token management
✅ Plans CRUD (with public/private)
✅ Exercises CRUD (with public/private)
✅ Trainings tracking
✅ Exercise logging (reps, weight)
✅ Drop sets (declining exercises)
✅ Full relational data model
✅ API documentation
✅ TypeScript support (frontend)
✅ Async storage for tokens
✅ Navigation flow
✅ Error handling

## 📦 Technologies

**Backend:**
- FastAPI - Web framework
- Prisma - ORM
- PostgreSQL - Database
- python-jose - JWT
- passlib - Password hashing
- Uvicorn - ASGI server

**Frontend:**
- React Native - Mobile framework
- Expo - Development platform
- React Navigation - Routing
- Axios - HTTP client
- AsyncStorage - Local storage
- TypeScript - Type safety

## 💡 Tips

1. **Backend errors?** Check Prisma is generated: `prisma generate`
2. **Frontend errors?** Run `npm install` to get dependencies
3. **Can't connect?** Verify API URL in `src/services/api.ts`
4. **Database issues?** Check PostgreSQL is running
5. **Auth not working?** Verify JWT_SECRET in .env

## 📚 Documentation

- Backend README: `backend/README.md`
- Frontend README: `frontend/README.md`
- Main README: `README.md`
- API Docs: http://localhost:8000/docs (when running)

## 🐛 Troubleshooting

**"prisma not found"**
```bash
pip install prisma
```

**"Cannot find module 'react'"**
```bash
cd frontend && npm install
```

**"Database connection failed"**
- Check PostgreSQL is running
- Verify DATABASE_URL in .env
- Ensure database exists

**"401 Unauthorized"**
- Check token in AsyncStorage
- Try logging out and back in
- Verify JWT_SECRET matches backend

## 🎉 You're Ready!

Your training app is fully structured with:
- Complete backend API
- Mobile frontend
- Database schema
- Authentication
- CRUD operations for all features

Just install dependencies and start building! 🚀
