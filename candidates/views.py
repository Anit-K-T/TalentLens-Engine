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
            print("DEBUG: Form is valid")
            candidate = form.save()
            print("DEBUG: Candidate saved")

            # Get the uploaded resume path
            resume_path = candidate.resume.path

            # Extract text from the PDF
            parsed_text = extract_text_from_pdf(resume_path)
            skills = extract_skills(parsed_text)
            print("Resume path:", resume_path)
            print("Extracted characters:", len(parsed_text))
            candidate.parsed_resume = parsed_text
            candidate.matched_skills = ", ".join(skills)

            score, matched, missing = calculate_match(
            candidate.matched_skills,
            candidate.applied_job.required_skills
            )

            candidate.match_score = score
            candidate.ai_recommendation = recommend(score)

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
    candidate = get_object_or_404(Candidate, id=candidate_id)

    if request.method == "POST":
        form = CandidateForm(
            request.POST,
            request.FILES,
            instance=candidate,
        )

        if form.is_valid():
            candidate = form.save()

            # Only parse if a resume exists
            if candidate.resume:
                resume_path = candidate.resume.path
                parsed_text = extract_text_from_pdf(resume_path)
                skills = extract_skills(parsed_text)

                candidate.parsed_resume = parsed_text
                candidate.matched_skills = ", ".join(skills)

                score, matched, missing = calculate_match(
                candidate.matched_skills,
                candidate.applied_job.required_skills
                )

                candidate.match_score = score
                candidate.ai_recommendation = recommend(score)

                candidate.save()
            return redirect("candidate_list")

    else:
        form = CandidateForm(instance=candidate)

    return render(
        request,
        "candidates/add_candidate.html",
        {"form": form},
    )
def candidate_detail(request, candidate_id):
    candidate = get_object_or_404(Candidate, id=candidate_id)

    skills = []
    matched = []
    missing = []

    if candidate.matched_skills:
        skills = [
            skill.strip()
            for skill in candidate.matched_skills.split(",")
            if skill.strip()
        ]

        score, matched, missing = calculate_match(
            candidate.matched_skills,
            candidate.applied_job.required_skills
        )

    return render(
        request,
        "candidates/candidate_detail.html",
        {
            "candidate": candidate,
            "skills": skills,
            "matched": matched,
            "missing": missing,
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
