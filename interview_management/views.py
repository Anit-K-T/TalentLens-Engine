from django.shortcuts import render, redirect, get_object_or_404
from .models import Interview
from .forms import InterviewForm
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages
from django.http import HttpResponse


def interview_list(request):

    interviews = Interview.objects.all().order_by("interview_date")

    return render(
        request,
        "interviews/interview_list.html",
        {"interviews": interviews},
    )


def interview_create(request):

    candidate_id = request.GET.get("candidate")

    if request.method == "POST":

        form = InterviewForm(request.POST,request.FILES)

        if form.is_valid():

            interview = form.save()

            candidate = interview.candidate

            print("Sending email to:", candidate.email)

            send_mail(
                subject="Interview Invitation - TalentLens Engine",

                message=f"""
Dear {candidate.name},

Congratulations!

Your interview has been scheduled.

Job Role: {interview.job.title}
Date: {interview.interview_date}
Time: {interview.interview_time}

Interviewer: {interview.interviewer_name}
Mode: {interview.mode}

Meeting Link:
{interview.meeting_link}

Best wishes!

TalentLens Recruitment Team
""",

                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[candidate.email],
                fail_silently=False,
            )

            messages.success(
                request,
                "Interview scheduled and email invitation sent successfully!"
            )

            return redirect("interview_list")

    else:

        if candidate_id:
            form = InterviewForm(
                initial={"candidate": candidate_id}
            )
        else:
            form = InterviewForm()

    return render(
        request,
        "interviews/interview_form.html",
        {"form": form},
    )
def interview_update(request, pk):

    interview = get_object_or_404(Interview, pk=pk)

    if request.method == "POST":
        form = InterviewForm(request.POST,request.FILES, instance=interview)

        if form.is_valid():
            form.save()
            return redirect("interview_list")

    else:
        form = InterviewForm(instance=interview)

    return render(
        request,
        "interviews/interview_form.html",
        {"form": form},
    )


def interview_delete(request, pk):

    interview = get_object_or_404(Interview, pk=pk)

    if request.method == "POST":
        interview.delete()
        return redirect("interview_list")

    return render(
        request,
        "interviews/interview_confirm_delete.html",
        {"interview": interview},
    )
def analyze_interview(request, pk):

    interview = get_object_or_404(
        Interview,
        pk=pk
    )

    return render(
        request,
        "interviews/interview_analysis.html",
        {
            "interview": interview,
        },
    )