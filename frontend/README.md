# Training App Frontend - SvelteKit

A modern web application for training management built with SvelteKit, TypeScript, and TailwindCSS.

## Tech Stack

- **Framework**: SvelteKit 2.0
- **Language**: TypeScript
- **Styling**: TailwindCSS
- **HTTP Client**: Axios
- **State Management**: Svelte Stores

## Features

- ✅ User authentication (login/register)
- ✅ JWT token management
- ✅ Training plans management
- ✅ Exercise library management
- ✅ Responsive design
- ✅ Protected routes
- ✅ Modern UI with TailwindCSS

## Project Structure

```
frontend/
├── src/
│   ├── lib/
│   │   ├── api.ts                 # Axios configuration
│   │   ├── stores/
│   │   │   └── auth.ts            # Authentication store
│   │   └── services/
│   │       ├── planService.ts     # Plans API
│   │       └── exerciseService.ts # Exercises API
│   ├── routes/
│   │   ├── +layout.svelte         # Root layout
│   │   ├── +page.svelte           # Home (redirect)
│   │   ├── login/
│   │   │   └── +page.svelte       # Login page
│   │   ├── register/
│   │   │   └── +page.svelte       # Register page
│   │   ├── plans/
│   │   │   ├── +page.svelte       # Plans list
│   │   │   └── create/
│   │   │       └── +page.svelte   # Create plan
│   │   └── exercises/
│   │       ├── +page.svelte       # Exercises list
│   │       └── create/
│   │           └── +page.svelte   # Create exercise
│   ├── app.html                   # HTML template
│   └── app.css                    # Global styles
├── package.json
├── svelte.config.js
├── vite.config.ts
├── tailwind.config.js
└── tsconfig.json
```

## Setup

### Prerequisites

- Node.js 18+ 
- npm or pnpm
- Backend API running on http://localhost:8000

### Installation

1. Install dependencies:
```bash
cd frontend
npm install
```

2. Create environment file:
```bash
cp .env.example .env
```

3. Update `.env` with your API URL:
```env
VITE_API_URL=http://localhost:8000
```

### Development

Start the development server:
```bash
npm run dev
```

The app will be available at: http://localhost:5173

### Building for Production

Build the app:
```bash
npm run build
```

Preview the production build:
```bash
npm run preview
```

## Features Detail

### Authentication

- JWT-based authentication
- Token stored in localStorage
- Automatic token injection in API requests
- Auto-redirect on 401 errors
- Login and registration pages

### Plans Management

- View all training plans
- Create new plans
- Delete plans
- Public/private visibility
- Start date configuration

### Exercises Management

- View all exercises (personal + public)
- Create new exercises
- Delete exercises
- Add descriptions, videos, and images
- Public/private visibility

### Navigation

- Responsive navigation bar
- Quick access to Plans and Exercises
- Logout functionality
- Protected routes (requires authentication)

## API Integration

The frontend communicates with the FastAPI backend through:

- **Base URL**: Configured via `VITE_API_URL` environment variable
- **Authentication**: JWT Bearer token in Authorization header
- **Error Handling**: Automatic logout on 401, error messages displayed

### API Endpoints Used

- `POST /auth/login` - User login
- `POST /auth/register` - User registration
- `GET /plans/` - Get all plans
- `POST /plans/` - Create plan
- `DELETE /plans/{id}` - Delete plan
- `GET /exercises/` - Get all exercises
- `POST /exercises/` - Create exercise
- `DELETE /exercises/{id}` - Delete exercise

## Styling

The app uses TailwindCSS for styling with:

- Responsive design (mobile-first)
- Modern UI components
- Indigo color scheme
- Form validation states
- Loading states
- Error messages

## State Management

- **Authentication Store**: Manages user authentication state
- **Svelte Stores**: Reactive state management
- **localStorage**: Persistent token storage

## Development Tips

### Hot Reload

Vite provides instant hot module replacement (HMR) during development.

### Type Safety

TypeScript is configured for strict type checking. All services and stores are fully typed.

### Code Organization

- **lib/api.ts**: Centralized Axios configuration
- **lib/stores/**: Svelte stores for global state
- **lib/services/**: API service layer
- **routes/**: File-based routing (SvelteKit convention)

## Deployment

### Vercel (Recommended)

```bash
npm install -g vercel
vercel
```

### Netlify

```bash
npm run build
# Deploy the 'build' directory
```

### Docker

```dockerfile
FROM node:18-alpine
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build
EXPOSE 3000
CMD ["node", "build"]
```

## Browser Support

- Chrome/Edge (latest)
- Firefox (latest)
- Safari (latest)
- Mobile browsers

## Troubleshooting

### Port Already in Use

Change the port in `vite.config.ts`:
```ts
server: {
  port: 3000
}
```

### Cannot Connect to Backend

1. Ensure backend is running on http://localhost:8000
2. Check CORS configuration in backend
3. Verify `VITE_API_URL` in `.env`

### Build Errors

```bash
# Clear cache and rebuild
rm -rf .svelte-kit node_modules
npm install
npm run build
```

## Contributing

1. Create a feature branch
2. Make your changes
3. Test thoroughly
4. Submit a pull request

## License

MIT
