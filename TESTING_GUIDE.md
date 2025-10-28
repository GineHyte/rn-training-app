# Testing Guide

## Prerequisites

Before testing, ensure you have:
- Python 3.8+ installed
- PostgreSQL running (or use Docker)
- Virtual environment activated
- Dependencies installed

## Setup Test Environment

### Option 1: Using Docker (Recommended)
```bash
# Start PostgreSQL only
docker run --name test-db -e POSTGRES_PASSWORD=postgres -e POSTGRES_DB=training_app -p 5432:5432 -d postgres:15-alpine

# Wait for database to be ready
timeout /t 5

# Set test environment variables
$env:DATABASE_URL="postgresql://postgres:postgres@localhost:5432/training_app?schema=public"
$env:JWT_SECRET="test-secret-key"
$env:JWT_ALGORITHM="HS256"
$env:ACCESS_TOKEN_EXPIRE_MINUTES="30"

# Run migrations
cd backend
prisma generate
prisma db push

# Run tests
pytest -v
```

### Option 2: Using Local PostgreSQL
```bash
# Create test database
createdb training_app

# Or using psql
psql -U postgres -c "CREATE DATABASE training_app;"

# Set environment variables
$env:DATABASE_URL="postgresql://postgres:yourpassword@localhost:5432/training_app?schema=public"
$env:JWT_SECRET="test-secret-key"

# Run migrations
cd backend
prisma generate
prisma db push

# Run tests
pytest -v
```

## Running Tests

### Run All Tests
```bash
cd backend
pytest -v
```

### Run Specific Test File
```bash
pytest test_api.py -v
```

### Run Specific Test Function
```bash
pytest test_api.py::test_login_user -v
```

### Run with Coverage
```bash
pytest --cov=app --cov-report=html
```

### Run and Show Print Statements
```bash
pytest -v -s
```

## Test Categories

### 1. Health Check Tests
- `test_root_endpoint` - Tests root API endpoint
- `test_health_check` - Tests health check endpoint

### 2. Authentication Tests
- `test_register_user` - Tests user registration
- `test_register_duplicate_user` - Tests duplicate username handling
- `test_login_user` - Tests successful login
- `test_login_wrong_password` - Tests login with wrong password

### 3. Authorization Tests
- `test_create_plan_requires_auth` - Tests protected endpoints
- `test_create_plan_with_auth` - Tests authenticated requests

### 4. CRUD Tests
- `test_create_plan_with_auth` - Tests plan creation
- `test_get_plans_with_auth` - Tests plan retrieval
- `test_create_exercise_with_auth` - Tests exercise creation

### 5. Documentation Tests
- `test_api_documentation` - Tests API docs availability
- `test_openapi_schema` - Tests OpenAPI schema

## Manual Testing with curl

### 1. Check Health
```bash
curl http://localhost:8000/health
```

### 2. Register User
```bash
curl -X POST http://localhost:8000/auth/register `
  -H "Content-Type: application/json" `
  -d '{\"username\":\"testuser\",\"password\":\"password123\"}'
```

### 3. Login
```bash
curl -X POST http://localhost:8000/auth/login `
  -H "Content-Type: application/json" `
  -d '{\"username\":\"testuser\",\"password\":\"password123\"}'
```

Save the token from response:
```bash
$token = "your_token_here"
```

### 4. Create Plan (Authenticated)
```bash
curl -X POST http://localhost:8000/plans/ `
  -H "Content-Type: application/json" `
  -H "Authorization: Bearer $token" `
  -d '{\"name\":\"My Plan\",\"startDate\":\"2024-01-01T00:00:00\",\"public\":false}'
```

### 5. Get Plans
```bash
curl http://localhost:8000/plans/ `
  -H "Authorization: Bearer $token"
```

### 6. Create Exercise
```bash
curl -X POST http://localhost:8000/exercises/ `
  -H "Content-Type: application/json" `
  -H "Authorization: Bearer $token" `
  -d '{\"name\":\"Bench Press\",\"description\":\"Chest exercise\",\"public\":true}'
```

## Using Swagger UI for Testing

1. Start the backend:
   ```bash
   cd backend
   python main.py
   ```

2. Open browser: http://localhost:8000/docs

3. Test endpoints:
   - Click on an endpoint
   - Click "Try it out"
   - Fill in the parameters
   - Click "Execute"

4. For authenticated endpoints:
   - First login via `/auth/login`
   - Copy the `access_token`
   - Click "Authorize" button at top
   - Enter: `Bearer your_token_here`
   - Now all requests will include the token

## Test Results

Expected output:
```
test_api.py::test_root_endpoint PASSED
test_api.py::test_health_check PASSED
test_api.py::test_register_user PASSED
test_api.py::test_register_duplicate_user PASSED
test_api.py::test_login_user PASSED
test_api.py::test_login_wrong_password PASSED
test_api.py::test_create_plan_requires_auth PASSED
test_api.py::test_create_plan_with_auth PASSED
test_api.py::test_get_plans_with_auth PASSED
test_api.py::test_create_exercise_with_auth PASSED
test_api.py::test_api_documentation PASSED
test_api.py::test_openapi_schema PASSED

============ 12 passed in 2.34s ============
```

## Troubleshooting Tests

### "prisma not found"
```bash
pip install prisma
prisma generate
```

### "Database connection failed"
```bash
# Check PostgreSQL is running
# For Docker:
docker ps

# For local:
pg_isready -U postgres
```

### "Module not found"
```bash
pip install -r requirements.txt
```

### Tests Fail Due to Existing Data
```bash
# Reset database
prisma db push --force-reset

# Or drop and recreate
dropdb training_app
createdb training_app
prisma db push
```

### "Port 8000 already in use"
```bash
# Find process
netstat -ano | findstr :8000

# Kill process
taskkill /PID <PID> /F
```

## Continuous Integration

### GitHub Actions Example
Create `.github/workflows/test.yml`:

```yaml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    
    services:
      postgres:
        image: postgres:15
        env:
          POSTGRES_PASSWORD: postgres
          POSTGRES_DB: training_app
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
        ports:
          - 5432:5432
    
    steps:
      - uses: actions/checkout@v3
      
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      
      - name: Install dependencies
        run: |
          cd backend
          pip install -r requirements.txt
      
      - name: Run migrations
        run: |
          cd backend
          prisma generate
          prisma db push
        env:
          DATABASE_URL: postgresql://postgres:postgres@localhost:5432/training_app
      
      - name: Run tests
        run: |
          cd backend
          pytest -v
        env:
          DATABASE_URL: postgresql://postgres:postgres@localhost:5432/training_app
          JWT_SECRET: test-secret-key
```

## Performance Testing

### Using Apache Bench
```bash
# Test health endpoint
ab -n 1000 -c 10 http://localhost:8000/health

# Test with authentication (after getting token)
ab -n 100 -c 5 -H "Authorization: Bearer $token" http://localhost:8000/plans/
```

### Using pytest-benchmark
```bash
pip install pytest-benchmark
pytest --benchmark-only
```

## Best Practices

✅ Run tests before committing
✅ Keep test database separate from development
✅ Use fixtures for common setup
✅ Test both success and failure cases
✅ Mock external dependencies
✅ Aim for >80% code coverage
✅ Run tests in CI/CD pipeline
