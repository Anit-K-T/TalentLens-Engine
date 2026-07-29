# TalentLens Engine

## AI-Powered Candidate Evaluation Platform

TalentLens Engine is an AI-powered recruitment platform developed as part of the **InfoCreon Solutions 14-Day Technical Internship Challenge**. The system automates resume screening, candidate-job matching, interview evaluation, and recruiter decision-making using Artificial Intelligence, Natural Language Processing (NLP), and Machine Learning techniques.

The platform enables recruiters to upload candidate resumes, evaluate them against predefined job roles, conduct AI-assisted interview assessments, and make informed hiring decisions through an explainable scoring system.

---
![Python](https://img.shields.io/badge/Python-3.13-blue)
![Django](https://img.shields.io/badge/Django-5.x-green)
![MySQL](https://img.shields.io/badge/MySQL-Database-orange)
![AI](https://img.shields.io/badge/AI-Whisper%20%7C%20Gemini-red)

# Project Objectives

- Parse and process PDF resumes.
- Extract candidate skills, experience, and education.
- Match candidates with predefined job roles.
- Calculate an explainable Hire-Fit Score.
- Schedule and evaluate interviews using AI.
- Generate recruiter evaluation reports.
- Support recruiter decision-making through an interactive dashboard.

---

# Features

### Resume Processing

- Upload candidate resumes in PDF format
- Automatic resume parsing
- Candidate information extraction
- Skill extraction using NLP
- Resume data stored in MySQL database

### AI Candidate Matching

- Match candidates against predefined job roles
- AI-based weighted scoring
- Skill matching
- Experience evaluation
- Education matching
- Semantic similarity using TF-IDF and Cosine Similarity
- Candidate ranking
- AI recommendation

### Recruiter Dashboard

- View all candidates
- Search and filter candidates
- Candidate score breakdown
- Approve / Reject candidates
- Recruiter evaluation notes

### Interview Intelligence

- Schedule interviews
- Upload interview audio
- Speech-to-text transcription using OpenAI Whisper
- Interview evaluation using Google Gemini
- AI-generated feedback
- Overall interview score

### Reports

- PDF evaluation report generation
- CSV export
- Excel export

---

# AI Scoring Methodology

The Hire-Fit Score is calculated using a weighted evaluation model.

| Criteria | Weight |
|----------|---------|
| Skills Match | 40% |
| Experience Match | 30% |
| Semantic Similarity (TF-IDF + Cosine Similarity) | 20% |
| Education Match | 10% |

Final Score = Skills + Experience + Semantic Similarity + Education

---

# Project Workflow

```
Resume Upload
        │
        ▼
PDF Resume Parsing
        │
        ▼
Skill Extraction
        │
        ▼
Candidate Database
        │
        ▼
AI Job Matching
        │
        ▼
Hire-Fit Score Calculation
        │
        ▼
Recruiter Dashboard
        │
        ▼
Interview Scheduling
        │
        ▼
Speech-to-Text (Whisper)
        │
        ▼
Interview Evaluation (Gemini)
        │
        ▼
PDF Report Generation
```

---

# Technology Stack

## Backend

- Python
- Django
- Django REST Framework

## Frontend

- HTML5
- CSS3
- Bootstrap
- JavaScript

## Database

- MySQL

## Artificial Intelligence

- Google Gemini API
- OpenAI Whisper
- TF-IDF
- Cosine Similarity
- Scikit-Learn
- NLP-based Skill Extraction

## Python Libraries

- PyPDF2
- spaCy
- Pandas
- NumPy
- ReportLab
- Scikit-learn

---

# Project Structure

```
TalentLens-Engine/

├── accounts/
├── ai_engine/
├── candidates/
├── interviews/
├── jobs/
├── reports/
├── static/
├── templates/
├── media/
├── manage.py
├── requirements.txt
└── README.md
```

---

# Installation

## Clone Repository

```bash
git clone <repository-url>
```

## Navigate to Project

```bash
cd TalentLens-Engine
```

## Create Virtual Environment

```bash
python -m venv venv
```

## Activate Virtual Environment

Windows

```bash
venv\Scripts\activate
```

Linux / macOS

```bash
source venv/bin/activate
```

## Install Dependencies

```bash
pip install -r requirements.txt
```

## Apply Migrations

```bash
python manage.py migrate
```

## Run the Development Server

```bash
python manage.py runserver
```

The application will be available at:

```
http://127.0.0.1:8000/
```

---

# Modules

- Authentication
- Candidate Management
- Resume Processing
- AI Matching Engine
- Job Management
- Interview Scheduling
- AI Interview Evaluation
- Recruiter Dashboard
- Reports

---

# API Overview

| Module | Purpose |
|---------|----------|
| Authentication | User Login |
| Candidates | Resume Upload & Management |
| Jobs | Job Role Management |
| Interviews | Schedule & Evaluate Interviews |
| Reports | Generate Candidate Reports |

---

# Unit Testing

Run all unit tests using:

```bash
python manage.py test
```

---

# Future Enhancements

- Cloud Deployment
- Real-Time Notifications
- AI Chat Interview Assistant
- Video Interview Emotion Analysis
- Resume Recommendation Engine
- Email Notifications
- Advanced Analytics Dashboard

---

# Screenshots

(Add application screenshots here before submission.)

Example:

- Login Page
- Dashboard
- Candidate List
- Resume Upload
- Job Roles
- Interview Evaluation
- PDF Report

---

# Developer

**Anit K T**

B.Tech Computer Science and Engineering

Developed as part of the **InfoCreon Solutions Private Limited - 14-Day Technical Internship Challenge (TalentLens Engine)**.

---

# License

This project is developed for educational and internship assessment purposes.