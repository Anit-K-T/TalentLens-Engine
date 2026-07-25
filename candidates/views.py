from django.shortcuts import render, redirect, get_object_or_404
from .models import Candidate
from .forms import CandidateForm
from ai_engine.skill_extractor import extract_skills
from ai_engine.resume_parser import extract_text_from_pdf
from ai_engine.matcher import calculate_match
from ai_engine.recommender import recommend



def candidate_list(request):
    candidates = Candidate.objects.all().order_by("-id")
    return render(
        request,
        "candidates/candidate_list.html",
        {"candidates": candidates},
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

            score, matched = calculate_match(
            candidate.matched_skills,
            candidate.applied_job.required_skills)

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

# Calculate AI match score
                score, matched = calculate_match(
                candidate.matched_skills,
                candidate.applied_job.required_skills)

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
def delete_candidate(request, candidate_id):
    candidate = get_object_or_404(Candidate, id=candidate_id)
    candidate.delete()

    return redirect("candidate_list")