def calculate_match(candidate_skills, required_skills):
    """
    Calculate match percentage between candidate skills and job required skills.
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
        return 0, []

    matched = candidate_set.intersection(required_set)

    score = round((len(matched) / len(required_set)) * 100, 2)

    return score, list(matched)