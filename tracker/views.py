from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.db.models import Max
from django.utils import timezone
from datetime import timedelta
from .models import WorkoutSession, Lift, Set, SETS_PER_LIFT, REPS_PER_SET

WORKOUT_A_LIFTS = ["squat", "bench", "row"]
WORKOUT_B_LIFTS = ["squat", "deadlift", "ohp"]


def get_next_workout_type(user):
    """Determine which workout (A or B) should be done next."""
    last_session = WorkoutSession.objects.filter(user=user).order_by("-date").first()
    if last_session is None:
        return "A"
    return "B" if last_session.workout_type == "A" else "A"


@login_required
def workout_form(request):
    """Display the workout entry form and handle submissions."""
    next_workout = get_next_workout_type(request.user)
    lifts = WORKOUT_A_LIFTS if next_workout == "A" else WORKOUT_B_LIFTS

    if request.method == "POST":
        # Create workout session
        session = WorkoutSession.objects.create(
            user=request.user,
            workout_type=next_workout,
            date=timezone.now()
        )

        # Process each lift
        for lift_name in lifts:
            lift = Lift.objects.create(
                workout_session=session,
                lift_name=lift_name,
                notes=request.POST.get(f"notes_{lift_name}", "")
            )

            # Process sets for this lift
            for set_num in range(1, SETS_PER_LIFT + 1):
                weight = request.POST.get(f"weight_{lift_name}_set_{set_num}")
                reps = request.POST.get(f"reps_{lift_name}_set_{set_num}")

                if weight and reps:
                    Set.objects.create(
                        lift=lift,
                        set_number=set_num,
                        weight=weight,
                        reps=reps
                    )

        return redirect("history")

    context = {
        "next_workout": next_workout,
        "lifts": lifts,
        "sets_per_lift": SETS_PER_LIFT,
        "reps_per_set": REPS_PER_SET,
    }
    return render(request, "tracker/workout_form.html", context)


@login_required
def history(request):
    """Display all workout sessions."""
    sessions = WorkoutSession.objects.filter(user=request.user).prefetch_related("lifts__sets")
    context = {"sessions": sessions}
    return render(request, "tracker/history.html", context)


@login_required
def progress(request):
    """Display weekly progress view."""
    # Get all sessions for the user
    sessions = WorkoutSession.objects.filter(user=request.user).prefetch_related("lifts__sets")

    # Group by week
    weeks = {}
    for session in sessions:
        week_start = session.date.date() - timedelta(days=session.date.weekday())
        if week_start not in weeks:
            weeks[week_start] = []
        weeks[week_start].append(session)

    # Sort weeks in reverse chronological order
    sorted_weeks = sorted(weeks.items(), reverse=True)

    context = {"weeks": sorted_weeks}
    return render(request, "tracker/progress.html", context)

