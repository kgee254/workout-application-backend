from flask import Blueprint, request, jsonify
from marshmallow import ValidationError
from sqlalchemy.exc import IntegrityError

from server.models import db, Workout, Exercise, WorkoutExercise
from server.schemas import (
    WorkoutSchema,
    ExerciseSchema,
    WorkoutExerciseSchema
)

api = Blueprint("api", __name__)

workout_schema = WorkoutSchema()
workouts_schema = WorkoutSchema(many=True)

exercise_schema = ExerciseSchema()
exercises_schema = ExerciseSchema(many=True)

workout_exercise_schema = WorkoutExerciseSchema()


def error(message, status):
    return jsonify({"error": message}), status


# ---------------- WORKOUT ROUTES ----------------

@api.route("/workouts", methods=["GET"])
def get_workouts():
    workouts = Workout.query.all()
    return jsonify(workouts_schema.dump(workouts)), 200


@api.route("/workouts/<int:workout_id>", methods=["GET"])
def get_workout(workout_id):
    workout = db.session.get(Workout, workout_id)

    if workout is None:
        return error("Workout not found", 404)

    return jsonify(workout_schema.dump(workout)), 200


@api.route("/workouts", methods=["POST"])
def create_workout():
    try:
        data = workout_schema.load(request.get_json() or {})
        workout = Workout(**data)

        db.session.add(workout)
        db.session.commit()

        return jsonify(workout_schema.dump(workout)), 201

    except ValidationError as exc:
        db.session.rollback()
        return jsonify({"errors": exc.messages}), 400

    except (ValueError, TypeError) as exc:
        db.session.rollback()
        return error(str(exc), 400)

    except IntegrityError:
        db.session.rollback()
        return error("Invalid workout data", 400)


@api.route("/workouts/<int:workout_id>", methods=["DELETE"])
def delete_workout(workout_id):
    workout = db.session.get(Workout, workout_id)

    if workout is None:
        return error("Workout not found", 404)

    db.session.delete(workout)
    db.session.commit()

    return "", 204


# ---------------- EXERCISE ROUTES ----------------

@api.route("/exercises", methods=["GET"])
def get_exercises():
    exercises = Exercise.query.all()
    return jsonify(exercises_schema.dump(exercises)), 200


@api.route("/exercises/<int:exercise_id>", methods=["GET"])
def get_exercise(exercise_id):
    exercise = db.session.get(Exercise, exercise_id)

    if exercise is None:
        return error("Exercise not found", 404)

    return jsonify(exercise_schema.dump(exercise)), 200


@api.route("/exercises", methods=["POST"])
def create_exercise():
    try:
        data = exercise_schema.load(request.get_json() or {})
        exercise = Exercise(**data)

        db.session.add(exercise)
        db.session.commit()

        return jsonify(exercise_schema.dump(exercise)), 201

    except ValidationError as exc:
        db.session.rollback()
        return jsonify({"errors": exc.messages}), 400

    except (ValueError, TypeError) as exc:
        db.session.rollback()
        return error(str(exc), 400)

    except IntegrityError:
        db.session.rollback()
        return error(
            "An exercise with this name and category already exists",
            400
        )


@api.route("/exercises/<int:exercise_id>", methods=["DELETE"])
def delete_exercise(exercise_id):
    exercise = db.session.get(Exercise, exercise_id)

    if exercise is None:
        return error("Exercise not found", 404)

    db.session.delete(exercise)
    db.session.commit()

    return "", 204


# ---------------- WORKOUT-EXERCISE ROUTE ----------------

@api.route(
    "/workouts/<int:workout_id>/exercises/<int:exercise_id>/workout_exercises",
    methods=["POST"]
)
def add_exercise_to_workout(workout_id, exercise_id):
    workout = db.session.get(Workout, workout_id)
    exercise = db.session.get(Exercise, exercise_id)

    if workout is None:
        return error("Workout not found", 404)

    if exercise is None:
        return error("Exercise not found", 404)

    try:
        data = workout_exercise_schema.load(request.get_json() or {})

        link = WorkoutExercise(
            workout_id=workout_id,
            exercise_id=exercise_id,
            **data
        )

        db.session.add(link)
        db.session.commit()

        return jsonify({
            "id": link.id,
            "workout_id": link.workout_id,
            "exercise_id": link.exercise_id,
            "sets": link.sets,
            "reps": link.reps,
            "duration_seconds": link.duration_seconds
        }), 201

    except ValidationError as exc:
        db.session.rollback()
        return jsonify({"errors": exc.messages}), 400

    except (ValueError, TypeError) as exc:
        db.session.rollback()
        return error(str(exc), 400)

    except IntegrityError:
        db.session.rollback()
        return error("Invalid workout exercise data", 400)