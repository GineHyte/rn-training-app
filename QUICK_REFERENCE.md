# Quick Reference Card

## 🚀 Start the App

### With Docker (Recommended)
```bash
docker-compose up -d
```

### Without Docker
```bash
cd backend
venv\Scripts\activate  # Windows
python main.py
```

## 🧪 Run Tests

### Simple Test
```bash
cd backend
python run_tests.py
```

### Full Test Suite
```bash
cd backend
pytest -v
```

### With Docker
```bash
docker-compose exec backend pytest -v
```

## 📖 Access Documentation

- **API Docs**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **Health**: http://localhost:8000/health

## 🛑 Stop the App

### With Docker
```bash
docker-compose down
```

### Without Docker
```bash
Ctrl + C
```

## 🗑️ Clean Reset

### Docker - Remove Everything
```bash
docker-compose down -v
docker-compose up -d
```

### Manual - Reset Database
```bash
cd backend
prisma db push --force-reset
```

## 📊 View Logs

### Docker
```bash
docker-compose logs -f
docker-compose logs -f backend
docker-compose logs -f postgres
```

### Manual
Check terminal output

## 🔍 Check Status

### Docker
```bash
docker-compose ps
```

### Manual
```bash
curl http://localhost:8000/health
```

## 💾 Database Access

### Docker
```bash
docker-compose exec postgres psql -U postgres -d training_app
```

### Manual
```bash
psql -U postgres -d training_app
```

## 📦 Common Commands

### Backend
```bash
# Install dependencies
pip install -r requirements.txt

# Generate Prisma client
prisma generate

# Push database schema
prisma db push

# Create migration
prisma migrate dev --name migration_name

# View database
prisma studio
```

### Docker
```bash
# Start services
docker-compose up -d

# Stop services
docker-compose down

# View logs
docker-compose logs -f

# Rebuild
docker-compose up -d --build

# Execute command
docker-compose exec backend <command>

# Remove volumes
docker-compose down -v
```

## 🧪 Testing Commands

```bash
# Simple test
python run_tests.py

# All tests
pytest -v

# Specific test
pytest test_api.py::test_login_user -v

# With coverage
pytest --cov=app

# Show print statements
pytest -v -s
```

## 🌐 API Testing

### Register User
```bash
curl -X POST http://localhost:8000/auth/register \
  -H "Content-Type: application/json" \
  -d '{"username":"user","password":"pass"}'
```

### Login
```bash
curl -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"user","password":"pass"}'
```

### Create Plan (with token)
```bash
curl -X POST http://localhost:8000/plans/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -d '{"name":"Plan","startDate":"2024-01-01T00:00:00","public":false}'
```

## 🔧 Troubleshooting

### Port in use
```bash
# Find process
netstat -ano | findstr :8000

# Kill process
taskkill /PID <PID> /F
```

### Database connection failed
```bash
# Check PostgreSQL
docker ps
pg_isready -U postgres
```

### Module not found
```bash
pip install -r requirements.txt
prisma generate
```

## 📚 Documentation Files

- `README.md` - Project overview
- `SETUP_GUIDE.md` - Detailed setup
- `QUICK_START.md` - Quick commands
- `DOCKER_GUIDE.md` - Docker documentation
- `TESTING_GUIDE.md` - Testing documentation
- `DATA_MODEL.md` - Data structure
- `DOCKER_TESTING.md` - What was added

## 🎯 URLs

- Backend API: http://localhost:8000
- Swagger Docs: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc
- Health Check: http://localhost:8000/health

## 📱 Frontend Setup

```bash
cd frontend
npm install
npm start
```

Update API URL in `frontend/src/services/api.ts`:
- Android Emulator: `http://10.0.2.2:8000`
- iOS Simulator: `http://localhost:8000`
- Physical Device: `http://YOUR_IP:8000`
