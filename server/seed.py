from datetime import date

from server.app import app
from server.models import db, Workout, Exercise, WorkoutExercise


def seed_data():
    with app.app_context():
        db.create_all()

        workout1 = Workout(
            date=date(2026, 10, 31),
            duration_minutes=60,
            notes="Upper body strength"
        )

        workout2 = Workout(
            date=date(2026, 10, 30),
            duration_minutes=45,
            notes="Lower body training"
        )

        squat = Exercise(
            name="Squat",
            category="Legs",
            equipment_needed=False
        )

        pushup = Exercise(
            name="Push-up",
            category="Chest",
            equipment_needed=False
        )

        bench_press = Exercise(
            name="Bench Press",
            category="Chest",
            equipment_needed=True
        )

        db.session.add_all([
            workout1, workout2,
            squat, pushup, bench_press
        ])

        db.session.flush()

        db.session.add_all([
            WorkoutExercise(
                workout=workout1,
                exercise=pushup,
                sets=3,
                reps=12
            ),
            WorkoutExercise(
                workout=workout1,
                exercise=bench_press,
                sets=4,
                reps=8
            ),
            WorkoutExercise(
                workout=workout2,
                exercise=squat,
                sets=3,
                reps=10
            ),
        ])

        db.session.commit()
        print("Database seeded successfully!")


if __name__ == "__main__":
    seed_data()