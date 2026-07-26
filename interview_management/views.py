from django.shortcuts import render, redirect, get_object_or_404

from .models import Interview
from .forms import InterviewForm


def interview_list(request):

    interviews = Interview.objects.all().order_by("interview_date")

    return render(
        request,
        "interviews/interview_list.html",
        {"interviews": interviews},
    )


def interview_create(request):

    if request.method == "POST":

        form = InterviewForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect("interview_list")

    else:
        form = InterviewForm()

    return render(
        request,
        "interviews/interview_form.html",
        {"form": form},
    )