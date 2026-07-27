from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Avg,Count
from django.utils import timezone

from .forms import LoginForm
from candidates.models import Candidate
from jobs.models import JobRole
from interview_management.models import Interview


def login_view(request):

    if request.user.is_authenticated:
        return redirect("dashboard")

    form = LoginForm()

    if request.method == "POST":

        form = LoginForm(request.POST)

        if form.is_valid():

            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]

            user = authenticate(
                request,
                username=username,
                password=password,
            )

            if user is not None:
                login(request, user)
                return redirect("dashboard")

    return render(
        request,
        "login.html",
        {"form": form},
    )


@login_required(login_url="login")
def home(request):

    total_candidates = Candidate.objects.count()
    total_jobs = JobRole.objects.count()
    total_interviews = Interview.objects.count()

    pending = Candidate.objects.filter(status="Pending").count()
    shortlisted = Candidate.objects.filter(status="Shortlisted").count()
    rejected = Candidate.objects.filter(status="Rejected").count()
    hired = Candidate.objects.filter(status="Hired").count()

    avg_score = Candidate.objects.aggregate(
        Avg("match_score")
    )["match_score__avg"]

    if avg_score is None:
        avg_score = 0

    avg_score = round(avg_score, 1)

    recent_candidates = Candidate.objects.order_by(
        "-uploaded_at"
    )[:5]

    recent_jobs = JobRole.objects.order_by(
        "-id"
    )[:5]

    upcoming_interviews = Interview.objects.filter(
        interview_date__gte=timezone.now().date()
    ).order_by(
        "interview_date",
        "interview_time"
    )[:5]

    top_candidates = Candidate.objects.order_by(
        "-match_score"
    )[:5]
    job_application_stats = (
    JobRole.objects
    .annotate(total_applications=Count("candidates"))
    .order_by("-total_applications")
    )
    score_0_40 = Candidate.objects.filter(match_score__lte=40).count()

    score_41_60 = Candidate.objects.filter(
    match_score__gt=40,
    match_score__lte=60
    ).count()

    score_61_80 = Candidate.objects.filter(
    match_score__gt=60,
    match_score__lte=80
    ).count()

    score_81_100 = Candidate.objects.filter(
        match_score__gt=80
    ).count()
    applied_count = Candidate.objects.count()

    shortlisted_count = Candidate.objects.filter(status="Shortlisted").count()

    interview_count = Interview.objects.count()

    hired_count = Candidate.objects.filter(status="Hired").count()
    context = {
        "total_candidates": total_candidates,
        "total_jobs": total_jobs,
        "total_interviews": total_interviews,
        "job_application_stats": job_application_stats,
        "pending": pending,
        "shortlisted": shortlisted,
        "rejected": rejected,
        "hired": hired,
        "score_0_40": score_0_40,
        "score_41_60": score_41_60,
        "score_61_80": score_61_80,
        "score_81_100": score_81_100,
        "avg_score": avg_score,
    "applied_count": applied_count,
    "shortlisted_count": shortlisted_count,
    "interview_count": interview_count,
    "hired_count": hired_count,
        "recent_candidates": recent_candidates,
        "recent_jobs": recent_jobs,
        "upcoming_interviews": upcoming_interviews,
        "top_candidates": top_candidates,

        "chart_pending": pending,
        "chart_shortlisted": shortlisted,
        "chart_rejected": rejected,
        "chart_hired": hired,
    }

    return render(
        request,
        "dashboard.html",
        context,
    )


def logout_view(request):

    logout(request)

    return redirect("login")