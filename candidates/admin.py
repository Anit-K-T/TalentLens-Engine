from django.contrib import admin
from .models import Candidate

@admin.register(Candidate)
class CandidateAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "email",
        "applied_job",
        "status",
        "match_score",
    )

    readonly_fields = (
        "parsed_resume",
        "matched_skills",
        "match_score",
        "ai_recommendation",
    )