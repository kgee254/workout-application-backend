from marshmallow import Schema, fields, validate, validates_schema, ValidationError


class WorkoutExerciseSchema(Schema):
    id = fields.Int(dump_only=True)
    workout_id = fields.Int(dump_only=True)
    exercise_id = fields.Int(dump_only=True)

    reps = fields.Int(allow_none=True, validate=validate.Range(min=1))
    sets = fields.Int(allow_none=True, validate=validate.Range(min=1))
    duration_seconds = fields.Int(
        allow_none=True,
        validate=validate.Range(min=1)
    )


class ExerciseSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(
        required=True,
        validate=validate.Length(min=1, max=100)
    )
    category = fields.Str(
        required=True,
        validate=validate.Length(min=1, max=50)
    )
    equipment_needed = fields.Bool(load_default=False)

    workouts = fields.Method("get_workouts", dump_only=True)

    def get_workouts(self, obj):
        return [
            {
                "id": workout.id,
                "date": workout.date.isoformat(),
                "duration_minutes": workout.duration_minutes
            }
            for workout in obj.workouts
        ]

    @validates_schema
    def validate_strings(self, data, **kwargs):
        for field in ("name", "category"):
            if field in data and not data[field].strip():
                raise ValidationError({field: ["Cannot be blank"]})


class WorkoutSchema(Schema):
    id = fields.Int(dump_only=True)
    date = fields.Date(required=True)
    duration_minutes = fields.Int(
        required=True,
        validate=validate.Range(min=1)
    )
    notes = fields.Str(allow_none=True)

    workout_exercises = fields.Method(
        "get_workout_exercises",
        dump_only=True
    )

    def get_workout_exercises(self, obj):
        return [
            {
                "id": link.exercise.id,
                "name": link.exercise.name,
                "category": link.exercise.category,
                "sets": link.sets,
                "reps": link.reps,
                "duration_seconds": link.duration_seconds
            }
            for link in obj.workout_exercises
        ]

    @validates_schema
    def validate_notes(self, data, **kwargs):
        if data.get("notes") is not None and len(data["notes"]) > 2000:
            raise ValidationError({
                "notes": ["Notes cannot exceed 2000 characters"]
            })