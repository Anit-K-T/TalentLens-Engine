from django.shortcuts import render
from candidates.models import Candidate
from jobs.models import JobRole


def home(request):

    total_candidates = Candidate.objects.count()

    total_jobs = JobRole.objects.count()

    shortlisted = Candidate.objects.filter(
        status="Shortlisted"
    ).count()

    rejected = Candidate.objects.filter(
        status="Rejected"
    ).count()

    pending = Candidate.objects.filter(
        status="Pending"
    ).count()

    hired = Candidate.objects.filter(
        status="Hired"
    ).count()

    average_match = Candidate.objects.all()

    if average_match.exists():
        avg_score = round(
            sum(c.match_score for c in average_match)
            / average_match.count(),
            1,
        )
    else:
        avg_score = 0

    recent_candidates = Candidate.objects.order_by("-uploaded_at")[:5]

    context = {
    "total_candidates": total_candidates,
    "total_jobs": total_jobs,
    "shortlisted": shortlisted,
    "rejected": rejected,
    "pending": pending,
    "hired": hired,
    "avg_score": avg_score,
    "recent_candidates": recent_candidates,
    "chart_pending": pending,
    "chart_shortlisted": shortlisted,
    "chart_rejected": rejected,
    "chart_hired": hired,
}

    return render(request, "dashboard.html", context)