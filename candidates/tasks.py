from .models import Candidate
from .models import Candidate
from .models import Candidate
from ai_engine.resume_parser import extract_text_from_pdf
from ai_engine.skill_extractor import extract_skills
from ai_engine.matcher import calculate_match
from ai_engine.recommender import recommend

def process_resume(candidate_id):
    candidate = Candidate.objects.get(id=candidate_id)

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

    candidate.skill_score = result["skill_score"]
    candidate.experience_score = result["experience_score"]
    candidate.education_score = result["education_score"]
    candidate.semantic_score = result["semantic_score"]
    candidate.match_score = result["final_score"]

    candidate.ai_recommendation = recommend(candidate.match_score)

    candidate.save()