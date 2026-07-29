from django.shortcuts import render
from candidates.models import Candidate
from interview_management.models import Interview


def report_dashboard(request):

    candidates = Candidate.objects.all()
    interviews = Interview.objects.all()

    context = {
        "candidates": candidates,
        "interviews": interviews,
    }

    return render(request, "reports/report_dashboard.html", context)
