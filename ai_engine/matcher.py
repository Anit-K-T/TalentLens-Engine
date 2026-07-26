def calculate_match(candidate_skills, required_skills):
    """
    Compare candidate skills with job required skills.
    Returns:
    score,
    matched_skills,
    missing_skills
    """

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

    if not required_set:
        return 0, [], []

    matched = sorted(candidate_set.intersection(required_set))
    missing = sorted(required_set - candidate_set)

    score = round((len(matched) / len(required_set)) * 100, 2)

    return score, matched, missing