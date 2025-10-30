# React Native Training App Workspace Instructions

## Project Structure
- `backend/` - FastAPI + Prisma ORM (Python)
- `frontend/` - SvelteKit web application (TypeScript)
- `frontend-react-native-backup/` - Original React Native app (backup)

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
- [x] **Migrate frontend from React Native to SvelteKit**

## Tech Stack
- **Backend**: FastAPI, Prisma (Python), JWT authentication, PostgreSQL
- **Frontend**: SvelteKit 2.0, TypeScript, TailwindCSS, Axios, Svelte Stores
- **Auth**: JWT tokens, bcrypt password hashing

## Quick Start

### With Docker (Recommended)
```bash
docker-compose up -d
```

### Backend
```bash
cd backend
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac
pip install -r requirements.txt
prisma generate
prisma db push
python main.py
```

### Frontend
```bash
cd frontend
npm install
cp .env.example .env
npm run dev
```

## Documentation
- `README.md` - Main project overview
- `SETUP_GUIDE.md` - Detailed setup instructions
- `DATA_MODEL.md` - Data relationships and flow
- `MIGRATION.md` - Frontend migration details
- `FRONTEND_MIGRATION.md` - Complete migration summary
- `backend/README.md` - Backend API documentation
- `frontend/README.md` - Frontend app documentation
