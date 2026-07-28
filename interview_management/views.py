from django.shortcuts import render, redirect, get_object_or_404
from .models import Interview
from .forms import InterviewForm
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages
from django.http import HttpResponse
from .ai.transcriber import generate_transcript
from .ai.evaluator import evaluate_interview


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
    interview = get_object_or_404(Interview, pk=pk)

    if not interview.interview_recording:
        messages.error(request, "Please upload an interview recording first.")
        return redirect("interview_list")

    try:
        # Generate transcript if missing
        if not interview.transcript:
            interview.transcript = generate_transcript(
                interview.interview_recording.path
            )

        # Generate AI evaluation if any AI field is missing
        if (
            not interview.ai_feedback
            or not interview.summary
            or not interview.strengths
            or not interview.weaknesses
        ):

            result = evaluate_interview(interview.transcript)

            interview.communication_score = result.get("communication_score", 0)
            interview.technical_score = result.get("technical_score", 0)
            interview.confidence_score = result.get("confidence_score", 0)
            interview.overall_score = result.get("overall_score", 0)

            interview.hiring_recommendation = result.get(
                "hiring_recommendation", ""
            )

            interview.ai_feedback = result.get("ai_feedback", "")
            interview.summary = result.get("summary", "")
            interview.strengths = result.get("strengths", [])
            interview.weaknesses = result.get("weaknesses", [])

            interview.save()

        messages.success(
            request,
            "AI interview analysis completed successfully!"
        )

    except Exception as e:
        print("ERROR:", e)
        messages.error(request, f"AI analysis failed: {e}")

    return render(
        request,
        "interviews/interview_analysis.html",
        {
            "interview": interview,
        },
    )