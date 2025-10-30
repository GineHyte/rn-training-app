# Training App

A complete training management web application with SvelteKit frontend and FastAPI backend.

## Project Structure

```
rn-training-app/
├── backend/           # FastAPI + Prisma ORM
│   ├── app/
│   │   ├── routes/   # API endpoints
│   │   ├── schemas.py
│   │   ├── auth.py
│   │   ├── config.py
│   │   └── database.py
│   ├── prisma/
│   │   └── schema.prisma
│   ├── main.py
│   ├── requirements.txt
│   └── README.md
│
└── frontend/         # SvelteKit Web App
    ├── src/
    │   ├── lib/      # Services, stores, API
    │   └── routes/   # Pages (file-based routing)
    ├── package.json
    ├── svelte.config.js
    └── README.md
```

## Features

### User Management
- User registration and authentication
- JWT-based authorization
- Secure password hashing

### Plans
- Create training plans
- Set start dates
- Public/private visibility
- Organize plans by weeks

### Plan Weeks
- Add weeks to plans
- Define week start dates
- Organize trainings within weeks

### Plan Trainings
- Schedule training sessions
- Set start/end times
- Define intensity levels
- Link to plan weeks

### Exercises
- Create custom exercises
- Add descriptions, videos, and images
- Public/private exercise library
- Share exercises with community

### Plan Exercises
- Link exercises to plan trainings
- Set exercise intensity
- Build workout routines

### Trainings
- Start training sessions
- Track start/end times
- Link to plan trainings
- Record actual workouts

### Training Exercises
- Log exercise sets
- Track reps and weight
- Timestamp each set
- Link to plan exercises

### Declining Training Exercises
- Track drop sets
- Multiple positions per set
- Record weight and rep progression
- Timestamp tracking

## Quick Start

### 🐳 Option 1: Using Docker (Recommended)

```bash
# Start everything with Docker Compose
docker-compose up -d

# Backend will be available at http://localhost:8000
# API docs at http://localhost:8000/docs
```

That's it! Docker will:
- Start PostgreSQL database
- Run migrations automatically
- Start the FastAPI backend
- Enable hot reload for development

See [DOCKER_GUIDE.md](DOCKER_GUIDE.md) for more details.

### 💻 Option 2: Manual Setup

#### Backend Setup

1. Navigate to backend directory:
```bash
cd backend
```

2. Create virtual environment:
```bash
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Configure environment:
```bash
copy .env.example .env
# Edit .env with your database credentials
```

5. Setup database:
```bash
prisma generate
prisma db push
```

6. Run server:
```bash
python main.py
```

Server will be available at `http://localhost:8000`

### Frontend Setup

1. Navigate to frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Create environment file:
```bash
cp .env.example .env
```

4. Start development server:
```bash
npm run dev
```

Web app will be available at `http://localhost:5173`

## API Documentation

Once the backend is running, visit:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Testing

### Quick Test
```bash
# With backend running, test all endpoints
cd backend
python run_tests.py
```

### Full Test Suite
```bash
cd backend
pytest -v
```

See [TESTING_GUIDE.md](TESTING_GUIDE.md) for comprehensive testing documentation.

## Docker Usage

```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Run tests in Docker
docker-compose exec backend pytest -v

# Stop all services
docker-compose down
```

See [DOCKER_GUIDE.md](DOCKER_GUIDE.md) for complete Docker documentation.

## Tech Stack

### Backend
- **Framework**: FastAPI
- **ORM**: Prisma (Python)
- **Database**: PostgreSQL
- **Authentication**: JWT (python-jose)
- **Password Hashing**: bcrypt (passlib)

### Frontend
- **Framework**: SvelteKit 2.0
- **Language**: TypeScript
- **Styling**: TailwindCSS
- **HTTP Client**: Axios
- **State**: Svelte Stores
- **Build Tool**: Vite

## Database Schema

The application uses a relational database with the following main entities:

- **User**: Authentication and ownership
- **Plan**: Training plans
- **PlanWeek**: Weekly organization
- **PlanTraining**: Scheduled training sessions
- **Exercise**: Exercise library
- **PlanExercise**: Exercises within trainings
- **Training**: Actual workout sessions
- **TrainingExercise**: Logged exercise sets
- **DecliningTrainingExercise**: Drop sets tracking
- **DecliningTrainingExercisePosition**: Individual drop set positions

All models have proper foreign key relationships with cascade deletion configured.

## Development

### Backend Development
- API runs on port 8000
- Hot reload enabled with `--reload` flag
- Check logs for errors
- Use Swagger UI for API testing

### Frontend Development
- SvelteKit dev server on port 5173
- Hot reload (HMR) enabled by default
- TypeScript type checking
- TailwindCSS for styling
- Access at http://localhost:5173

## Production Deployment

### Backend
1. Set up PostgreSQL database
2. Configure production environment variables
3. Run database migrations
4. Deploy using:
   - Docker
   - Cloud providers (AWS, GCP, Azure)
   - PaaS (Heroku, Render)

### Frontend
1. Update `VITE_API_URL` to production backend
2. Build production app:
```bash
npm run build
```
3. Deploy to:
   - Vercel (recommended)
   - Netlify
   - AWS S3 + CloudFront
   - Any static hosting

## Security Notes

- Change `JWT_SECRET` in production
- Use HTTPS for production API
- Implement rate limiting
- Add input validation
- Enable CORS only for trusted origins
- Regular security audits

## Future Enhancements

- [ ] Progress tracking and analytics
- [ ] Social features (follow users, share workouts)
- [ ] Exercise video streaming
- [ ] Workout reminders and notifications
- [ ] Integration with fitness trackers
- [ ] Meal planning integration
- [ ] Export workout data
- [ ] Offline mode support (PWA)
- [ ] Real-time collaboration on plans
- [ ] Mobile app version (Capacitor/React Native)

## License

MIT License - feel free to use this project for learning or production.

## Support

For issues or questions:
1. Check the README files in backend/ and frontend/
2. Review API documentation at /docs
3. Check console/logs for errors
4. Refer to Prisma and FastAPI documentation
