# Flight Management UI

Modern React-based frontend for the Flight Management System with authentication and user management.

## Features

- **Authentication**: JWT-based login/register with account lockout protection
- **User Management**: Profile viewing and editing
- **Modern UI**: Black theme with purple accents
- **Responsive**: Mobile-friendly design
- **DDD Architecture**: Clean, modular code structure

## Tech Stack

- React 19
- TypeScript
- React Router
- Axios
- Vite

## Project Structure

```
src/
├── application/          # Application layer
│   ├── components/       # Protected route wrapper
│   └── context/          # Auth context
├── domain/              # Domain layer
│   ├── dtos/            # Data transfer objects
│   ├── enums/           # Enumerations (Gender, Role)
│   └── models/          # Domain models
├── infrastructure/      # Infrastructure layer
│   ├── api/             # API client
│   └── services/        # Auth and user services
└── presentation/        # Presentation layer
    ├── layouts/         # Layout components
    ├── pages/           # Page components
    └── shared/          # Shared UI components
```

## Environment Configuration

Create a `.env` file in the root directory:

```env
VITE_API_URL=http://localhost:5000
```

## Getting Started

### Development

```bash
# Install dependencies
npm install

# Start development server
npm run dev
```

### Production Build

```bash
# Build for production
npm run build

# Preview production build
npm run preview
```

### Docker

```bash
# Build image
docker build -t flight-management-ui .

# Run container
docker run -p 80:80 flight-management-ui
```

## Available Routes

- `/login` - User login
- `/register` - User registration
- `/` - Dashboard (protected)
- `/account` - Account settings (protected)

## API Integration

The frontend connects to the backend API at the URL specified in `VITE_API_URL`. The API client automatically:

- Adds JWT token to requests
- Handles 401 errors by redirecting to login
- Provides clean error handling

## Theme

The application uses a modern dark theme with:
- Background: `#0f0f0f` (near black)
- Cards: `#18181b` (dark gray)
- Borders: `#27272a` (gray)
- Primary: `#8b5cf6` (purple)
- Text: `#fafafa` (off-white)

This template provides a minimal setup to get React working in Vite with HMR and some ESLint rules.

Currently, two official plugins are available:

- [@vitejs/plugin-react](https://github.com/vitejs/vite-plugin-react/blob/main/packages/plugin-react) uses [Babel](https://babeljs.io/) (or [oxc](https://oxc.rs) when used in [rolldown-vite](https://vite.dev/guide/rolldown)) for Fast Refresh
- [@vitejs/plugin-react-swc](https://github.com/vitejs/vite-plugin-react/blob/main/packages/plugin-react-swc) uses [SWC](https://swc.rs/) for Fast Refresh

## React Compiler

The React Compiler is not enabled on this template because of its impact on dev & build performances. To add it, see [this documentation](https://react.dev/learn/react-compiler/installation).

## Expanding the ESLint configuration

If you are developing a production application, we recommend updating the configuration to enable type-aware lint rules:

```js
export default defineConfig([
  globalIgnores(['dist']),
  {
    files: ['**/*.{ts,tsx}'],
    extends: [
      // Other configs...

      // Remove tseslint.configs.recommended and replace with this
      tseslint.configs.recommendedTypeChecked,
      // Alternatively, use this for stricter rules
      tseslint.configs.strictTypeChecked,
      // Optionally, add this for stylistic rules
      tseslint.configs.stylisticTypeChecked,

      // Other configs...
    ],
    languageOptions: {
      parserOptions: {
        project: ['./tsconfig.node.json', './tsconfig.app.json'],
        tsconfigRootDir: import.meta.dirname,
      },
      // other options...
    },
  },
])
```

You can also install [eslint-plugin-react-x](https://github.com/Rel1cx/eslint-react/tree/main/packages/plugins/eslint-plugin-react-x) and [eslint-plugin-react-dom](https://github.com/Rel1cx/eslint-react/tree/main/packages/plugins/eslint-plugin-react-dom) for React-specific lint rules:

```js
// eslint.config.js
import reactX from 'eslint-plugin-react-x'
import reactDom from 'eslint-plugin-react-dom'

export default defineConfig([
  globalIgnores(['dist']),
  {
    files: ['**/*.{ts,tsx}'],
    extends: [
      // Other configs...
      // Enable lint rules for React
      reactX.configs['recommended-typescript'],
      // Enable lint rules for React DOM
      reactDom.configs.recommended,
    ],
    languageOptions: {
      parserOptions: {
        project: ['./tsconfig.node.json', './tsconfig.app.json'],
        tsconfigRootDir: import.meta.dirname,
      },
      // other options...
    },
  },
])
```
