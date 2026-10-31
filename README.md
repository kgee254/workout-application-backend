# Workout Application Backend

## Description

A Flask REST API for tracking workouts and exercises. The application allows users to create, view, and delete workouts and exercises, as well as associate exercises with individual workouts.

The project uses Flask, Flask-SQLAlchemy, Flask-Migrate, Marshmallow, and SQLite.

## Features

- Create, view, and delete workouts.
- Create, view, and delete exercises.
- Add exercises to workouts with sets, repetitions, or duration.
- Validate incoming request data.
- Enforce database constraints and model validations.
- Serialize model data into JSON responses.
- Manage database schema changes with Flask-Migrate.

## Requirements

- Python 3.8.13 or later
- Pipenv
- Git

## Installation

Clone the repository and enter the project directory:

```bash
git clone git@github.com:kgee254/workout-application-backend.git
cd workout-application-backend
```

Install the project dependencies:

```bash
pipenv install
```

Activate the virtual environment:

```bash
pipenv shell
```

## Database Setup

Initialize migrations if the migrations directory does not already exist:

```bash
flask --app server.app db init
```

Generate and apply migrations:

```bash
flask --app server.app db migrate -m "Create workout and exercise models"
flask --app server.app db upgrade
```

Seed the database with sample records:

```bash
python -m server.seed
```

**Note:** The seed script adds sample data. Run it against a development database, and avoid running it repeatedly unless you want additional sample records.

## Running the Application

Start the development server:

```bash
flask --app server.app run --port 5555
```

The API will be available at:

`http://127.0.0.1:5555`

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/workouts` | Retrieve all workouts |
| GET | `/workouts/<workout_id>` | Retrieve one workout |
| POST | `/workouts` | Create a workout |
| DELETE | `/workouts/<workout_id>` | Delete a workout |
| GET | `/exercises` | Retrieve all exercises |
| GET | `/exercises/<exercise_id>` | Retrieve one exercise |
| POST | `/exercises` | Create an exercise |
| DELETE | `/exercises/<exercise_id>` | Delete an exercise |
| POST | `/workouts/<workout_id>/exercises/<exercise_id>/workout_exercises` | Add an exercise to a workout |

## Example Requests

### Create a workout

```bash
curl -X POST http://127.0.0.1:5555/workouts \
-H "Content-Type: application/json" \
-d '{"date":"2026-11-01","duration_minutes":45,"notes":"Upper body workout"}'
```

### Create an exercise

```bash
curl -X POST http://127.0.0.1:5555/exercises \
-H "Content-Type: application/json" \
-d '{"name":"Squat","category":"Legs","equipment_needed":true}'
```

### Add an exercise to a workout

Replace `1` in the URL with the relevant workout and exercise IDs.

```bash
curl -X POST http://127.0.0.1:5555/workouts/1/exercises/1/workout_exercises \
-H "Content-Type: application/json" \
-d '{"sets":3,"reps":10}'
```

### Retrieve workouts

```bash
curl http://127.0.0.1:5555/workouts
```

## Validation and Error Handling

The API validates required fields, data types, positive durations, sets and repetitions, and non-empty exercise names and categories. Duplicate exercises with the same name and category are rejected.

Typical response codes include:

- `200 OK` — successful retrieval.
- `201 Created` — successful creation.
- `204 No Content` — successful deletion.
- `400 Bad Request` — invalid request data.
- `404 Not Found` — requested workout or exercise does not exist.

## Running Tests

Install development dependencies and run:

```bash
pipenv install --dev pytest
pipenv run pytest -v
```

## Project Structure

```text
server/
    app.py
    models.py
    routes.py
    schemas.py
    seed.py
migrations/
tests/
    test_api.py
Pipfile
Pipfile.lock
README.md
.gitignore
```

## Technologies

- Python
- Flask
- Flask-SQLAlchemy
- Flask-Migrate
- Marshmallow
- SQLite
- Pytest
- Git and GitHub