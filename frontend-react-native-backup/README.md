# Training App Frontend

React Native application for the Training App using Expo.

## Features

- User authentication (login/register)
- Plans management
- Exercises library
- Training tracking
- Real-time workout recording

## Setup

### Prerequisites

- Node.js 16+
- npm or yarn
- Expo CLI (optional, for easier development)

### Installation

1. Install dependencies:
```bash
npm install
```

2. Update API URL in `src/services/api.ts`:
```typescript
const API_URL = 'http://your-backend-url:8000';
```

For local development:
- Android emulator: `http://10.0.2.2:8000`
- iOS simulator: `http://localhost:8000`
- Physical device: `http://YOUR_COMPUTER_IP:8000`

## Running the App

### Start the development server:
```bash
npm start
```

### Run on specific platform:
```bash
# Android
npm run android

# iOS
npm run ios

# Web
npm run web
```

## Project Structure

```
frontend/
├── App.tsx                 # Main app component with navigation
├── src/
│   ├── screens/           # Screen components
│   │   ├── LoginScreen.tsx
│   │   ├── RegisterScreen.tsx
│   │   ├── PlansScreen.tsx
│   │   ├── CreatePlanScreen.tsx
│   │   ├── ExercisesScreen.tsx
│   │   └── CreateExerciseScreen.tsx
│   └── services/          # API service layer
│       ├── api.ts         # Axios configuration
│       ├── authService.ts # Authentication
│       ├── planService.ts # Plans CRUD
│       ├── exerciseService.ts # Exercises CRUD
│       └── trainingService.ts # Training operations
├── app.json               # Expo configuration
├── package.json
└── tsconfig.json
```

## Features Implementation

### Authentication
- JWT-based authentication
- Token stored in AsyncStorage
- Automatic token injection in API requests
- Auto-logout on 401 responses

### Plans
- Create, read, update, delete plans
- Public/private plan visibility
- Start date tracking

### Exercises
- Create custom exercises
- Browse user and public exercises
- Add descriptions, videos, and images
- Public/private exercise visibility

### Training (Structure Ready)
- Start/end training sessions
- Track exercise sets (reps, weight)
- Link trainings to plan trainings
- Real-time workout recording

## API Services

All API calls are centralized in the `src/services/` directory:

- **api.ts**: Base Axios configuration with interceptors
- **authService.ts**: Login, register, logout
- **planService.ts**: Plans CRUD operations
- **exerciseService.ts**: Exercises CRUD operations
- **trainingService.ts**: Training and training exercises operations

## State Management

Currently using React hooks (useState, useEffect). For production, consider:
- Redux Toolkit
- Zustand
- React Query for server state

## Styling

Basic React Native StyleSheet. Consider adding:
- React Native Paper
- NativeBase
- Styled Components

## Next Steps

1. Add remaining screens:
   - Plan detail with weeks
   - Training session screen
   - Exercise detail view
   - Training history

2. Implement declining exercise tracking
3. Add form validation library (Formik, React Hook Form)
4. Add loading states and better error handling
5. Implement proper navigation flow
6. Add image picker for exercise images
7. Add video player for exercise demos
8. Implement search and filtering
9. Add analytics and progress tracking

## Development Notes

- TypeScript errors are expected until dependencies are installed
- Run `npm install` to resolve module imports
- Ensure backend is running before testing API calls
- Use Expo Go app for quick testing on physical devices

## Building for Production

### Android:
```bash
expo build:android
```

### iOS:
```bash
expo build:ios
```

Or use EAS Build:
```bash
eas build --platform android
eas build --platform ios
```
