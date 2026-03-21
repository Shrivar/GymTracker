from django.contrib import admin
from .models import WorkoutSession, Lift, Set

class SetInline(admin.TabularInline):
    model = Set
    extra = 0

class LiftInline(admin.TabularInline):
    model = Lift
    extra = 0
    inlines = [SetInline]

@admin.register(WorkoutSession)
class WorkoutSessionAdmin(admin.ModelAdmin):
    list_display = ["user", "workout_type", "date"]
    list_filter = ["workout_type", "date"]
    search_fields = ["user__username"]
    inlines = [LiftInline]

@admin.register(Lift)
class LiftAdmin(admin.ModelAdmin):
    list_display = ["lift_name", "workout_session", "created_at"]
    list_filter = ["lift_name", "created_at"]
    inlines = [SetInline]

@admin.register(Set)
class SetAdmin(admin.ModelAdmin):
    list_display = ["lift", "set_number", "weight", "reps"]
    list_filter = ["lift__lift_name"]

