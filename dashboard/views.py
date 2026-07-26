from django.shortcuts import render,redirect
from candidates.models import Candidate
from jobs.models import JobRole
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import LoginForm

@login_required(login_url="login")
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

            if user:
                login(request, user)
                return redirect("dashboard")

    return render(
        request,
        "login.html",
        {"form": form},
    )


def logout_view(request):

    logout(request)

    return redirect("login")