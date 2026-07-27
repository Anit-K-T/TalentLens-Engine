from django.shortcuts import render, redirect, get_object_or_404
from .models import Candidate
from .forms import CandidateForm
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

            resume_path = candidate.resume.path

            parsed_text = extract_text_from_pdf(resume_path)

            skills = extract_skills(parsed_text)

            candidate.parsed_resume = parsed_text

            candidate.matched_skills = ", ".join(skills)
            
            print("Candidate experience =", candidate.experience)
            print("Required experience =", candidate.applied_job.minimum_experience)
            print("Candidate education =", candidate.education)
            print("Required education =", candidate.applied_job.education_required)
            print("RESULT =", result)

            result = calculate_match(
                candidate_skills=candidate.matched_skills,
                required_skills=candidate.applied_job.required_skills,
                candidate_experience=candidate.experience,
                required_experience=candidate.applied_job.minimum_experience,
                candidate_education=candidate.education,
                required_education=candidate.applied_job.education_required,
            )
           

            

            candidate.save()

            return redirect("candidate_list")

    else:
        form = CandidateForm()

    return render(
        request,
        "candidates/add_candidate.html",
        {"form": form},
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