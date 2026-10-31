import pytest

from server.app import app
from server.models import db, Workout, Exercise, WorkoutExercise


@pytest.fixture
def client():
    app.config["TESTING"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite://"

    with app.app_context():
        db.drop_all()
        db.create_all()

        workout = Workout(
            date=__import__("datetime").date(2026, 10, 31),
            duration_minutes=60,
            notes="Test workout"
        )

        exercise = Exercise(
            name="Push-up",
            category="Chest",
            equipment_needed=False
        )

        db.session.add_all([workout, exercise])
        db.session.commit()

        db.session.add(
            WorkoutExercise(
                workout_id=workout.id,
                exercise_id=exercise.id,
                sets=3,
                reps=10
            )
        )
        db.session.commit()

        workout_id = workout.id
        exercise_id = exercise.id

    with app.test_client() as test_client:
        yield test_client, workout_id, exercise_id

    with app.app_context():
        db.session.remove()
        db.drop_all()


def test_get_workouts(client):
    test_client, _, _ = client

    response = test_client.get("/workouts")

    assert response.status_code == 200
    assert len(response.get_json()) == 1
    assert response.get_json()[0]["duration_minutes"] == 60


def test_get_single_workout(client):
    test_client, workout_id, _ = client

    response = test_client.get(f"/workouts/{workout_id}")

    assert response.status_code == 200
    assert response.get_json()["notes"] == "Test workout"


def test_get_missing_workout(client):
    test_client, _, _ = client

    response = test_client.get("/workouts/999")

    assert response.status_code == 404


def test_create_workout(client):
    test_client, _, _ = client

    response = test_client.post(
        "/workouts",
        json={
            "date": "2026-11-01",
            "duration_minutes": 45,
            "notes": "Cardio"
        }
    )

    assert response.status_code == 201
    assert response.get_json()["duration_minutes"] == 45


def test_reject_invalid_workout(client):
    test_client, _, _ = client

    response = test_client.post(
        "/workouts",
        json={
            "date": "2026-11-01",
            "duration_minutes": -10
        }
    )

    assert response.status_code == 400


def test_delete_workout(client):
    test_client, workout_id, _ = client

    response = test_client.delete(f"/workouts/{workout_id}")

    assert response.status_code == 204
    assert test_client.get(f"/workouts/{workout_id}").status_code == 404


def test_get_exercises(client):
    test_client, _, _ = client

    response = test_client.get("/exercises")

    assert response.status_code == 200
    assert len(response.get_json()) == 1
    assert response.get_json()[0]["name"] == "Push-up"


def test_get_single_exercise(client):
    test_client, _, exercise_id = client

    response = test_client.get(f"/exercises/{exercise_id}")

    assert response.status_code == 200
    assert response.get_json()["category"] == "Chest"


def test_create_exercise(client):
    test_client, _, _ = client

    response = test_client.post(
        "/exercises",
        json={
            "name": "Squat",
            "category": "Legs",
            "equipment_needed": False
        }
    )

    assert response.status_code == 201
    assert response.get_json()["name"] == "Squat"


def test_reject_duplicate_exercise(client):
    test_client, _, _ = client

    response = test_client.post(
        "/exercises",
        json={
            "name": "Push-up",
            "category": "Chest",
            "equipment_needed": False
        }
    )

    assert response.status_code == 400


def test_delete_exercise(client):
    test_client, _, exercise_id = client

    response = test_client.delete(f"/exercises/{exercise_id}")

    assert response.status_code == 204
    assert test_client.get(f"/exercises/{exercise_id}").status_code == 404


def test_add_exercise_to_workout(client):
    test_client, workout_id, exercise_id = client

    response = test_client.post(
        f"/workouts/{workout_id}/exercises/{exercise_id}/workout_exercises",
        json={"sets": 4, "reps": 12}
    )

    assert response.status_code == 201
    assert response.get_json()["sets"] == 4
    assert response.get_json()["reps"] == 12


def test_reject_invalid_sets(client):
    test_client, workout_id, exercise_id = client

    response = test_client.post(
        f"/workouts/{workout_id}/exercises/{exercise_id}/workout_exercises",
        json={"sets": -2, "reps": 12}
    )

    assert response.status_code == 400


def test_add_exercise_to_missing_workout(client):
    test_client, _, exercise_id = client

    response = test_client.post(
        f"/workouts/999/exercises/{exercise_id}/workout_exercises",
        json={"sets": 3, "reps": 10}
    )

    assert response.status_code == 404