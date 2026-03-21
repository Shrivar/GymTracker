from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Configuration for sets and reps per lift
SETS_PER_LIFT = 5
REPS_PER_SET = 5


class WorkoutSession(models.Model):
    WORKOUT_CHOICES = [
        ("A", "Workout A"),
        ("B", "Workout B"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    workout_type = models.CharField(max_length=1, choices=WORKOUT_CHOICES)
    date = models.DateTimeField(default=timezone.now)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-date"]

    def __str__(self):
        return f"Workout {self.workout_type} on {self.date.strftime('%Y-%m-%d')}"


class Lift(models.Model):
    LIFT_NAMES = [
        ("squat", "Squat"),
        ("bench", "Bench Press"),
        ("row", "Barbell Row"),
        ("deadlift", "Deadlift"),
        ("ohp", "Overhead Press"),
    ]

    workout_session = models.ForeignKey(WorkoutSession, on_delete=models.CASCADE, related_name="lifts")
    lift_name = models.CharField(max_length=20, choices=LIFT_NAMES)
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["created_at"]

    def __str__(self):
        return f"{self.get_lift_name_display()} - {self.workout_session}"


class Set(models.Model):
    lift = models.ForeignKey(Lift, on_delete=models.CASCADE, related_name="sets")
    set_number = models.IntegerField()
    weight = models.DecimalField(max_digits=6, decimal_places=2)  # in lbs
    reps = models.IntegerField()

    class Meta:
        ordering = ["set_number"]

    def __str__(self):
        return f"Set {self.set_number}: {self.weight}lbs x {self.reps}"

