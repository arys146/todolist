# Project: Todo & Habits

## Description

Simple todo list with habits. Backend and frontend implemented.

## Features

- Create and manage tasks and habits
- Tags and priority for tasks/habits
- User authentication
- Flexible habit schedules
- Custom end-of-day time (not fixed to 00:00)

## Tech Stack

**Backend**

- Async FastAPI
- SQLAlchemy for data access
- PostgreSQL as the database
- Alembic for migrations
- Redis for session checks and instant access-token invalidation
- JWT authentication with access and refresh tokens

  - Refresh-token rotation
  - Refresh-token hash stored in DB for logging, analytics, and suspicious-activity prevention

- Code structure approximates Clean Architecture within current experience level

**Frontend**

- React
- Axios for HTTP requests
- Tailwind CSS for styling

## Installation

- Install [Git](https://git-scm.com/install/) to clone project
- Install [Docker Desktop](https://docs.docker.com/get-started/get-docker/) to build project container
- Open place in terminal where project folder will be copied (replace [path] with yours)
  ```
  cd [path]
  ```
- Clone the repository

  ```
  git clone https://github.com/arys146/todolist.git
  cd todolist
  ```

- Create `.env` file in project folder and copy following there

  ```
  ACCESS_SECRET_KEY=access__on_prod__token_hex__or__urlsafe
  REFRESH_TOKEN_PEPPER=refresh__on_prod__token_hex__or__urlsafe
  JWT_ALGORITHM=HS256
  JWT_ACCESS_EXPIRE_MINUTES=5
  REFRESH_EXPIRE_DAYS=7
  JWT_ACCESS_NAME=access_token
  REFRESH_TOKEN_NAME=refresh_token
  REDIS_URL=redis://redis:6379/0

  POSTGRES_USER=postgres
  POSTGRES_PASSWORD=postgres
  POSTGRES_DB=todolist

  PGHOST=localhost
  PGPORT=5432

  DATABASE_URL=postgresql+psycopg://postgres:postgres@db:5432/todolist
  ```

- Build and start container
  ```
  docker compose up -d --build
  ```
- Run migrations to update db

  ```
  docker compose exec web alembic revision --autogenerate -m "initial"
  docker compose exec web alembic upgrade head
  ```

  - If there were no errors, the frontend should be available at http://localhost:5173, and the API and documentation at http://localhost:8000/docs.

## Roadmap

### Backend

- [ ] Add **Exercise** as the third entity
- [ ] Stop querying the user on each request; trust the access token. Store required user fields in JWT and invalidate access tokens on updates
- [ ] Normalize time handling: keep server time in UTC and account for the user’s time zone in calculations
- [ ] Revisit helper utilities to ensure they do not leak into business logic
- [ ] Do not expose ORM models outside business logic; return only schemas/DTOs
- [ ] Restructure the repository and organize modules/folders
- [ ] Add an endpoint for user statistics and streaks
- [ ] Return active user sessions and allow revoking a single session or signing out of all sessions

### Frontend

- [ ] Split large/duplicated code into reusable components
- [ ] Add update flows for habits and tasks
- [ ] Add deletion for habits and tasks
- [ ] Allow users to set a custom start-of-day in settings
- [ ] Multi-tab support: broadcast in-memory access token across tabs to avoid race conditions and redundant calls to the refresh endpoint
- [ ] Display tags for habits and tasks
- [ ] Session management UI: sign out from a single session or all sessions
- [ ] Add **Exercise** UI
- [ ] Add a tab to view all habits or all tasks
- [ ] Proper display of completed/past tasks
- [ ] Loading animations for checking a task or habit
- [ ] Form validation everywhere and intuitive toast errors
