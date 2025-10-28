# React Native Training App Workspace Instructions

## Project Structure
- `backend/` - FastAPI + Prisma ORM (Python)
- `frontend/` - React Native + Expo application

## ✅ Completed Steps
- [x] Create workspace structure
- [x] Create copilot-instructions.md
- [x] Setup backend with Prisma schema (10 models)
- [x] Create FastAPI CRUD endpoints (all entities)
- [x] Setup React Native frontend structure
- [x] Configure JWT authentication
- [x] Create API service layer
- [x] Implement basic screens (Login, Register, Plans, Exercises)
- [x] Create comprehensive documentation

## Tech Stack
- **Backend**: FastAPI, Prisma (Python), JWT authentication, PostgreSQL
- **Frontend**: React Native, Expo, React Navigation, Axios, AsyncStorage
- **Auth**: JWT tokens, bcrypt password hashing

## Quick Start
See `SETUP_GUIDE.md` for complete setup instructions.

### Backend
```bash
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
prisma generate
prisma db push
python main.py
```

### Frontend
```bash
cd frontend
npm install
npm start
```

## Documentation
- `README.md` - Main project overview
- `SETUP_GUIDE.md` - Detailed setup instructions
- `DATA_MODEL.md` - Data relationships and flow
- `backend/README.md` - Backend API documentation
- `frontend/README.md` - Frontend app documentation
