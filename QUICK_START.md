# Quick Start Commands

## 🚀 Backend Setup (PowerShell)

```powershell
# Navigate to backend
cd backend

# Create and activate virtual environment
python -m venv venv
.\venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt

# Copy environment file
Copy-Item .env.example .env

# Edit .env with your database credentials
notepad .env

# Generate Prisma client
prisma generate

# Push schema to database
prisma db push

# Start server
python main.py
```

## 📱 Frontend Setup (PowerShell)

```powershell
# Open new terminal and navigate to frontend
cd frontend

# Install dependencies
npm install

# Start Expo development server
npm start
```

## 🔧 Configuration

### Backend .env
```env
DATABASE_URL="postgresql://postgres:password@localhost:5432/training_app?schema=public"
JWT_SECRET="change-this-to-a-random-secret-key"
JWT_ALGORITHM="HS256"
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### Frontend API URL
Edit `frontend/src/services/api.ts`:

```typescript
// For Android Emulator
const API_URL = 'http://10.0.2.2:8000';

// For iOS Simulator
const API_URL = 'http://localhost:8000';

// For Physical Device (replace with your computer's IP)
const API_URL = 'http://192.168.1.100:8000';
```

## 🎯 First Test

1. **Backend**: Visit http://localhost:8000/docs
2. **Frontend**: Scan QR code with Expo Go app
3. **Register** a new user
4. **Login** with credentials
5. **Create** a plan or exercise

## 📦 One-Line Install (After Prerequisites)

### Backend
```powershell
cd backend; python -m venv venv; .\venv\Scripts\Activate.ps1; pip install -r requirements.txt; prisma generate
```

### Frontend
```powershell
cd frontend; npm install
```

## 🔍 Check if Running

```powershell
# Backend should respond
curl http://localhost:8000/health

# Should return: {"status":"healthy"}
```

## 🛑 Stop Servers

- **Backend**: `Ctrl+C` in terminal
- **Frontend**: `Ctrl+C` in terminal
- **Deactivate venv**: `deactivate`

## 📝 PostgreSQL Setup (if needed)

### Using Docker:
```powershell
docker run --name training-db -e POSTGRES_PASSWORD=password -e POSTGRES_DB=training_app -p 5432:5432 -d postgres:15
```

### Using Local Installation:
1. Install PostgreSQL from https://www.postgresql.org/download/
2. Create database: `CREATE DATABASE training_app;`
3. Update DATABASE_URL in .env

## 🐛 Common Issues

### "prisma command not found"
```powershell
pip install prisma
prisma --version
```

### "Cannot find module 'react'"
```powershell
cd frontend
rm -rf node_modules
npm install
```

### "Database connection failed"
- Ensure PostgreSQL is running
- Check DATABASE_URL in .env
- Verify database exists

### "Port 8000 already in use"
```powershell
# Find process
netstat -ano | findstr :8000

# Kill process (replace PID)
taskkill /PID <PID> /F
```

### "Can't connect to backend from phone"
- Use your computer's local IP address
- Ensure firewall allows connections on port 8000
- Both devices must be on same WiFi network

## ✅ Verify Setup

### Backend Check:
```powershell
# In browser, visit:
http://localhost:8000/docs
# Should see Swagger API documentation
```

### Frontend Check:
```powershell
# In terminal after 'npm start':
# Scan QR code with Expo Go app
# Should see login screen
```

## 🎉 You're Ready!

Backend API: http://localhost:8000
API Docs: http://localhost:8000/docs
Frontend: Expo development server

Happy coding! 🚀
