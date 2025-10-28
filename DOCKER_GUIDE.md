# Docker Setup for Training App

## Quick Start with Docker Compose

### Start Everything
```bash
docker-compose up -d
```

This will:
- Start PostgreSQL database on port 5432
- Start FastAPI backend on port 8000
- Automatically run migrations
- Enable hot reload for development

### Check Status
```bash
docker-compose ps
```

### View Logs
```bash
# All services
docker-compose logs -f

# Backend only
docker-compose logs -f backend

# Database only
docker-compose logs -f postgres
```

### Stop Everything
```bash
docker-compose down
```

### Stop and Remove Data
```bash
docker-compose down -v
```

## Access the Application

- **API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **Database**: localhost:5432
  - User: `postgres`
  - Password: `postgres`
  - Database: `training_app`

## Development Workflow

### Rebuild After Changes
```bash
docker-compose up -d --build
```

### Run Backend Commands
```bash
# Access backend container
docker-compose exec backend bash

# Run Prisma commands
docker-compose exec backend prisma generate
docker-compose exec backend prisma db push

# Run tests
docker-compose exec backend pytest
```

### Database Management
```bash
# Access PostgreSQL
docker-compose exec postgres psql -U postgres -d training_app

# Backup database
docker-compose exec postgres pg_dump -U postgres training_app > backup.sql

# Restore database
docker-compose exec -T postgres psql -U postgres training_app < backup.sql
```

## Configuration

### Environment Variables
Edit `docker-compose.yml` to change:
- `POSTGRES_PASSWORD`: Database password
- `JWT_SECRET`: Secret key for JWT tokens
- `ACCESS_TOKEN_EXPIRE_MINUTES`: Token expiration time

### Ports
If ports are already in use, edit `docker-compose.yml`:
```yaml
ports:
  - "5433:5432"  # Change PostgreSQL port
  - "8001:8000"  # Change backend port
```

## Production Deployment

For production, create `docker-compose.prod.yml`:

```yaml
version: '3.8'

services:
  postgres:
    image: postgres:15-alpine
    environment:
      POSTGRES_USER: ${POSTGRES_USER}
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD}
      POSTGRES_DB: ${POSTGRES_DB}
    volumes:
      - postgres_data:/var/lib/postgresql/data
    restart: always

  backend:
    build:
      context: ./backend
      dockerfile: Dockerfile
    environment:
      DATABASE_URL: ${DATABASE_URL}
      JWT_SECRET: ${JWT_SECRET}
      JWT_ALGORITHM: HS256
      ACCESS_TOKEN_EXPIRE_MINUTES: ${ACCESS_TOKEN_EXPIRE_MINUTES}
    ports:
      - "8000:8000"
    depends_on:
      - postgres
    restart: always
    command: uvicorn main:app --host 0.0.0.0 --port 8000

volumes:
  postgres_data:
```

Then run:
```bash
docker-compose -f docker-compose.prod.yml up -d
```

## Troubleshooting

### Port Already in Use
```bash
# Check what's using port 5432
netstat -ano | findstr :5432

# Check what's using port 8000
netstat -ano | findstr :8000
```

### Database Connection Issues
```bash
# Check if database is ready
docker-compose exec postgres pg_isready -U postgres

# View database logs
docker-compose logs postgres
```

### Backend Not Starting
```bash
# View backend logs
docker-compose logs backend

# Restart backend
docker-compose restart backend
```

### Reset Everything
```bash
# Stop and remove all containers and volumes
docker-compose down -v

# Remove images
docker-compose down --rmi all -v

# Start fresh
docker-compose up -d --build
```

## Testing with Docker

### Run All Tests
```bash
docker-compose exec backend pytest -v
```

### Run Specific Test
```bash
docker-compose exec backend pytest test_api.py::test_login_user -v
```

### Run with Coverage
```bash
docker-compose exec backend pytest --cov=app --cov-report=html
```

## Frontend Development with Docker Backend

If you're developing the frontend and using Docker for backend:

1. Start backend with Docker:
   ```bash
   docker-compose up -d
   ```

2. Update frontend API URL to `http://localhost:8000`

3. Run frontend normally:
   ```bash
   cd frontend
   npm start
   ```

## Benefits of Using Docker

✅ No need to install Python, PostgreSQL locally
✅ Consistent environment across team
✅ Easy database reset for testing
✅ Isolated from local system
✅ Easy deployment to production
✅ Automatic dependency management
