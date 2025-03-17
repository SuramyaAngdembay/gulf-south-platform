# Gulf South Scholars Hub

A full-stack web platform for the Center for the Study of the Gulf South (CSGS) at USM, facilitating research collaboration, event management, and resource sharing among scholars.

## Features

- User Authentication (Login/Register)
- Research Project Management
- Event and Conference Management
- Resource Library
- Member Profiles
- Real-time Messaging
- Notifications System
- Responsive Design

## Tech Stack

### Frontend
- Vue.js 3
- TypeScript
- Vuex for State Management
- Vue Router
- Element Plus UI Framework
- Axios for API calls

### Backend
- Python 3.8+
- FastAPI
- SQLAlchemy ORM
- MySQL Database
- JWT Authentication
- WebSocket for real-time features
- Alembic for database migrations

## Prerequisites

- Python 3.8 or higher
- MySQL 8.0 or higher
- Node.js 16 or higher (for frontend)
- npm or yarn

## Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/gulf-south-platform.git
cd gulf-south-platform
```

### 2. Backend Setup

```bash
cd backend

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
cp .env.example .env

# Update the following variables in .env:
DB_HOST=localhost
DB_USER=your_mysql_username
DB_PASSWORD=your_mysql_password
DB_NAME=gulf_south_platform
SECRET_KEY=your_secret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=11520  # 8 days

# Run database migrations
alembic upgrade head

# Start the development server
uvicorn app.main:app --reload --port 5000
```

### 3. Frontend Setup

```bash
cd frontend
npm install

# Create .env file
cp .env.example .env

# Update the following variables in .env:
VITE_API_URL=http://localhost:5000/api/v1
VITE_BASE_URL=/

# Start the development server
npm run dev
```

### 4. Database Setup

```sql
-- Create the database
CREATE DATABASE gulf_south_platform CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- Create user and grant privileges
CREATE USER 'gulf_south_user'@'localhost' IDENTIFIED BY 'your_password';
GRANT ALL PRIVILEGES ON gulf_south_platform.* TO 'gulf_south_user'@'localhost';
FLUSH PRIVILEGES;
```

## Environment Variables

### Backend (.env)
```
DB_HOST=localhost
DB_USER=gulf_south_user
DB_PASSWORD=your_password
DB_NAME=gulf_south_platform
SECRET_KEY=your_secret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=11520
BACKEND_CORS_ORIGINS=["http://localhost:5173"]
```

### Frontend (.env)
```
VITE_API_URL=http://localhost:5000/api/v1
VITE_BASE_URL=/
```

## Available Scripts

### Backend
- `uvicorn app.main:app --reload`: Start development server
- `alembic upgrade head`: Run database migrations
- `alembic downgrade -1`: Rollback last migration
- `pytest`: Run tests

### Frontend
- `npm run dev`: Start development server
- `npm run build`: Build for production
- `npm run preview`: Preview production build
- `npm run lint`: Run linter

## Project Structure

```
gulf-south-platform/
├── backend/
│   ├── alembic/
│   │   ├── versions/
│   │   └── env.py
│   ├── app/
│   │   ├── api/
│   │   ├── core/
│   │   ├── db/
│   │   ├── models/
│   │   └── schemas/
│   ├── tests/
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── views/
│   │   ├── store/
│   │   └── router/
│   └── package.json
└── docs/
    ├── api.md
    ├── database.md
    └── deployment.md
```

## Documentation

Detailed documentation is available in the `docs` directory:
- [API Documentation](docs/api.md)
- [Database Schema](docs/database.md)
- [Deployment Guide](docs/deployment.md)

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details. 