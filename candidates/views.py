from django.shortcuts import render, redirect, get_object_or_404
from .models import Candidate
from .forms import CandidateForm, RecruiterEvaluationForm
from ai_engine.skill_extractor import extract_skills
from ai_engine.resume_parser import extract_text_from_pdf
from ai_engine.matcher import calculate_match
from ai_engine.recommender import recommend
from jobs.models import JobRole
from django.http import HttpResponse
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
import csv
from django.http import HttpResponse
from openpyxl import Workbook
from django.db.models import Avg, Count
from interview_management.models import Interview


def evaluate_candidate(request, pk):
    candidate = get_object_or_404(Candidate, pk=pk)

    if request.method == "POST":
        form = RecruiterEvaluationForm(
            request.POST,
            instance=candidate
        )

        if form.is_valid():
            form.save()
            return redirect("candidate_detail", pk=candidate.pk)

    else:
        form = RecruiterEvaluationForm(instance=candidate)

    return render(
        request,
        "candidates/evaluate_candidate.html",
        {
            "candidate": candidate,
            "form": form,
        },
    )

def candidate_list(request):

    candidates = Candidate.objects.all().order_by("-id")

    search = request.GET.get("search")
    status = request.GET.get("status")
    job = request.GET.get("job")
    min_score = request.GET.get("min_score")

    if search:
        candidates = candidates.filter(name__icontains=search)

    if status:
        candidates = candidates.filter(status=status)

    if job:
        candidates = candidates.filter(applied_job_id=job)

    if min_score:
        candidates = candidates.filter(match_score__gte=min_score)

    jobs = JobRole.objects.all()

    context = {
        "candidates": candidates,
        "jobs": jobs,
    }

    return render(
        request,
        "candidates/candidate_list.html",
        context,
    )


def add_candidate(request):

    if request.method == "POST":

        form = CandidateForm(request.POST, request.FILES)

        if form.is_valid():

            candidate = form.save()

            # Resume Path
            resume_path = candidate.resume.path

            # Extract Resume Text
            parsed_text = extract_text_from_pdf(resume_path)

            # Extract Skills
            skills = extract_skills(parsed_text)

            candidate.parsed_resume = parsed_text
            candidate.matched_skills = ", ".join(skills)

            # AI Matching
            result = calculate_match(
                candidate_skills=candidate.matched_skills,
                required_skills=candidate.applied_job.required_skills,
                candidate_experience=candidate.experience,
                required_experience=candidate.applied_job.minimum_experience,
                candidate_education=candidate.education,
                required_education=candidate.applied_job.education_required,
            )

            # Debug Prints (Optional)
            print("Candidate Experience:", candidate.experience)
            print("Required Experience:", candidate.applied_job.minimum_experience)
            print("Candidate Education:", candidate.education)
            print("Required Education:", candidate.applied_job.education_required)
            print("AI Result:", result)

            # Save AI Scores
            candidate.skill_score = result["skill_score"]
            candidate.experience_score = result["experience_score"]
            candidate.education_score = result["education_score"]
            candidate.semantic_score = result["semantic_score"]
            candidate.match_score = result["final_score"]

            # Recommendation
            candidate.ai_recommendation = recommend(candidate.match_score)

            candidate.save()

            return redirect("candidate_list")

    else:
        form = CandidateForm()

    return render(
        request,
        "candidates/add_candidate.html",
        {
            "form": form,
        },
    )
def edit_candidate(request, candidate_id):

    candidate = get_object_or_404(
        Candidate,
        id=candidate_id,
    )

    if request.method == "POST":

        form = CandidateForm(
            request.POST,
            request.FILES,
            instance=candidate,
        )

        if form.is_valid():

            candidate = form.save()

            if candidate.resume:

                resume_path = candidate.resume.path

                parsed_text = extract_text_from_pdf(
                    resume_path
                )

                skills = extract_skills(parsed_text)

                candidate.parsed_resume = parsed_text

                candidate.matched_skills = ", ".join(skills)

                result = calculate_match(
                    candidate_skills=candidate.matched_skills,
                    required_skills=candidate.applied_job.required_skills,
                    candidate_experience=candidate.experience,
                    required_experience=candidate.applied_job.minimum_experience,
                    candidate_education=candidate.education,
                    required_education=candidate.applied_job.education_required,
                )

                candidate.skill_score = result["skill_score"]

                candidate.experience_score = result["experience_score"]

                candidate.semantic_score = result["semantic_score"]

                candidate.education_score = result["education_score"]

                candidate.match_score = result["final_score"]

                candidate.ai_recommendation = recommend(
                    candidate.match_score
                )

                candidate.save()

            return redirect("candidate_list")

    else:

        form = CandidateForm(
            instance=candidate
        )

    return render(
        request,
        "candidates/add_candidate.html",
        {
            "form": form,
        },
    )
def candidate_detail(request, pk):

    candidate = get_object_or_404(
        Candidate,
        pk=pk
    )

    result = calculate_match(
        candidate_skills=candidate.matched_skills,
        required_skills=candidate.applied_job.required_skills,
        candidate_experience=candidate.experience,
        required_experience=candidate.applied_job.minimum_experience,
        candidate_education=candidate.education,
        required_education=candidate.applied_job.education_required,
    )

    return render(
        request,
        "candidates/candidate_detail.html",
        {
            "candidate": candidate,
            "matched": result["matched"],
            "missing": result["missing"],
        },
    )

def download_ai_report(request, candidate_id):

    candidate = get_object_or_404(Candidate, id=candidate_id)

    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = (
        f'attachment; filename="{candidate.name}_AI_Report.pdf"'
    )

    doc = SimpleDocTemplate(response)

    styles = getSampleStyleSheet()
    story = []

    story.append(Paragraph("<b>TalentLens Engine</b>", styles["Title"]))
    story.append(Paragraph("AI Candidate Evaluation Report", styles["Heading2"]))
    story.append(Paragraph("<br/>", styles["BodyText"]))

    story.append(Paragraph(f"<b>Name:</b> {candidate.name}", styles["BodyText"]))
    story.append(Paragraph(f"<b>Email:</b> {candidate.email}", styles["BodyText"]))
    story.append(Paragraph(f"<b>Applied Job:</b> {candidate.applied_job.title}", styles["BodyText"]))
    story.append(Paragraph(f"<b>Status:</b> {candidate.status}", styles["BodyText"]))
    story.append(Paragraph(f"<b>AI Match Score:</b> {candidate.match_score}%", styles["BodyText"]))
    story.append(Paragraph(f"<b>Recommendation:</b> {candidate.ai_recommendation}", styles["BodyText"]))
    story.append(Paragraph(f"<b>Matched Skills:</b> {candidate.matched_skills}", styles["BodyText"]))

    doc.build(story)

    return response
def delete_candidate(request, candidate_id):
    candidate = get_object_or_404(Candidate, id=candidate_id)
    candidate.delete()

    return redirect("candidate_list")


def export_candidates_csv(request):
    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = 'attachment; filename="candidates.csv"'

    writer = csv.writer(response)

    writer.writerow([
        "Name",
        "Email",
        "Phone",
        "Job Applied",
        "Match Score",
        "Status",
    ])

    candidates = Candidate.objects.all()

    for candidate in candidates:
        writer.writerow([
            candidate.name,
            candidate.email,
            candidate.phone,
            candidate.applied_job.title if candidate.applied_job else "",
            candidate.match_score,
            candidate.status,
        ])

    return response
def export_candidates_excel(request):
    workbook = Workbook()
    worksheet = workbook.active
    worksheet.title = "Candidates"

    worksheet.append([
        "Name",
        "Email",
        "Phone",
        "Job Applied",
        "Match Score",
        "Status",
    ])

    candidates = Candidate.objects.all()

    for candidate in candidates:
        worksheet.append([
            candidate.name,
            candidate.email,
            candidate.phone,
            candidate.applied_job.title if candidate.applied_job else "",
            candidate.match_score,
            candidate.status,
        ])

    response = HttpResponse(
        content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

    response["Content-Disposition"] = (
        'attachment; filename="candidates.xlsx"'
    )

    workbook.save(response)

    return response
from django.db.models import Avg, Count
from django.shortcuts import render

from candidates.models import Candidate
from jobs.models import JobRole
from interview_management.models import Interview


def dashboard(request):

    candidates = Candidate.objects.all()

    # -----------------------------
    # Dashboard Cards
    # -----------------------------
    total_candidates = candidates.count()
    total_jobs = JobRole.objects.count()
    total_interviews = Interview.objects.count()

    average_score = (
        candidates.aggregate(Avg("match_score"))["match_score__avg"] or 0
    )

    avg_score = round(average_score, 2)

    # -----------------------------
    # Candidate Status Counts
    # -----------------------------
    pending = candidates.filter(status="Pending").count()
    shortlisted = candidates.filter(status="Shortlisted").count()
    rejected = candidates.filter(status="Rejected").count()
    hired = candidates.filter(status="Hired").count()

    # -----------------------------
    # Hiring Funnel
    # -----------------------------
    applied_count = total_candidates
    shortlisted_count = shortlisted
    interview_count = Interview.objects.filter(
        status="Scheduled"
    ).count()
    hired_count = hired

    # -----------------------------
    # Recent Data
    # -----------------------------
    recent_candidates = candidates.order_by("-uploaded_at")[:5]

    recent_jobs = JobRole.objects.order_by("-id")[:5]

    upcoming_interviews = Interview.objects.filter(
        status="Scheduled"
    ).order_by(
        "interview_date",
        "interview_time"
    )[:5]

    top_candidates = candidates.order_by("-match_score")[:5]

    # -----------------------------
    # Score Distribution
    # -----------------------------
    score_0_40 = candidates.filter(match_score__lt=40).count()

    score_41_60 = candidates.filter(
        match_score__gte=40,
        match_score__lte=60
    ).count()

    score_61_80 = candidates.filter(
        match_score__gt=60,
        match_score__lte=80
    ).count()

    score_81_100 = candidates.filter(
        match_score__gt=80
    ).count()

    # -----------------------------
    # Job-wise Applications
    # -----------------------------
    job_application_stats = JobRole.objects.annotate(
        total_candidates=Count("candidates")
    )

    context = {
        # Cards
        "total_candidates": total_candidates,
        "total_jobs": total_jobs,
        "total_interviews": total_interviews,
        "avg_score": avg_score,

        # Status
        "pending": pending,
        "shortlisted": shortlisted,
        "rejected": rejected,
        "hired": hired,

        # Funnel
        "applied_count": applied_count,
        "shortlisted_count": shortlisted_count,
        "interview_count": interview_count,
        "hired_count": hired_count,

        # Lists
        "recent_candidates": recent_candidates,
        "recent_jobs": recent_jobs,
        "upcoming_interviews": upcoming_interviews,
        "top_candidates": top_candidates,

        # Charts
        "chart_pending": pending,
        "chart_shortlisted": shortlisted,
        "chart_rejected": rejected,
        "chart_hired": hired,

        "score_0_40": score_0_40,
        "score_41_60": score_41_60,
        "score_61_80": score_61_80,
        "score_81_100": score_81_100,

        "job_application_stats": job_application_stats,
    }

    return render(
        request,
        "dashboard.html",
        context,
    )