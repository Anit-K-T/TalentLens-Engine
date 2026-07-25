import re

SKILLS = [
    "Python",
    "Java",
    "C",
    "C++",
    "SQL",
    "MySQL",
    "PostgreSQL",
    "MongoDB",
    "Machine Learning",
    "Deep Learning",
    "Artificial Intelligence",
    "Data Science",
    "TensorFlow",
    "PyTorch",
    "Scikit-learn",
    "Pandas",
    "NumPy",
    "Matplotlib",
    "Django",
    "Flask",
    "FastAPI",
    "HTML",
    "CSS",
    "JavaScript",
    "React",
    "Node.js",
    "Git",
    "Docker",
    "AWS",
    "Azure",
    "Power BI",
    "Excel",
]

def extract_skills(text):
    found_skills = []

    for skill in SKILLS:
        pattern = r"\b" + re.escape(skill) + r"\b"
        if re.search(pattern, text, re.IGNORECASE):
            found_skills.append(skill)

    return sorted(list(set(found_skills)))