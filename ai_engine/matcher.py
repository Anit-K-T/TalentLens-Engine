from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
def calculate_match(
    candidate_skills,
    required_skills,
    candidate_experience,
    required_experience,
    candidate_education,
    required_education,
):
    """
    AI Matching Engine

    Weightage:
    Skills              40%
    Experience          30%
    Semantic Similarity 20%
    Education           10%
    """

    # -----------------------------
    # Skills Matching (40 Marks)
    # -----------------------------

    candidate_set = {
        skill.strip().lower()
        for skill in candidate_skills.split(",")
        if skill.strip()
    }

    required_set = {
        skill.strip().lower()
        for skill in required_skills.split(",")
        if skill.strip()
    }

    matched = sorted(candidate_set.intersection(required_set))
    missing = sorted(required_set - candidate_set)

    if len(required_set) == 0:
        skill_score = 0
    else:
        skill_score = round(
            (len(matched) / len(required_set)) * 40,
            2
        )

    # -----------------------------
    # Experience Matching (30 Marks)
    # -----------------------------

    if required_experience <= 0:
        experience_score = 30

    elif candidate_experience >= required_experience:
        experience_score = 30

    else:
        experience_score = round(
            (candidate_experience / required_experience) * 30,
            2
        )

    # -----------------------------
    # Education Matching (10 Marks)
    # -----------------------------

    if candidate_education.strip().lower() == required_education.strip().lower():
        education_score = 10
    else:
        education_score = 5

    # -----------------------------
# Semantic Similarity (20 Marks)
# TF-IDF + Cosine Similarity
# -----------------------------

    candidate_text = candidate_skills.lower()
    job_text = required_skills.lower()

    documents = [candidate_text, job_text]

    vectorizer = TfidfVectorizer()

    tfidf_matrix = vectorizer.fit_transform(documents)

    similarity = cosine_similarity(
    tfidf_matrix[0:1],
    tfidf_matrix[1:2]
    )[0][0]

    semantic_score = round(similarity * 20, 2)
    # -----------------------------
    # Final Weighted Score
    # -----------------------------

    final_score = round(
        skill_score
        + experience_score
        + education_score
        + semantic_score,
        2
    )

    return {
        "skill_score": skill_score,
        "experience_score": experience_score,
        "education_score": education_score,
        "semantic_score": semantic_score,
        "final_score": final_score,
        "matched": matched,
        "missing": missing,
    }