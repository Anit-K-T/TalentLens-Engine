from django.db import models
from jobs.models import JobRole

class Candidate(models.Model):

    STATUS_CHOICES = [
        ("Pending", "Pending"),
        ("Shortlisted", "Shortlisted"),
        ("Rejected", "Rejected"),
        ("Hired", "Hired"),
    ]

    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15, blank=True)

    education = models.CharField(max_length=150)
    experience = models.FloatField(help_text="Experience in years")
    skills = models.TextField(help_text="Comma-separated skills")

    resume = models.FileField(upload_to="resumes/")

    # ✅ AI fields
    parsed_resume = models.TextField(blank=True)
    matched_skills = models.TextField(blank=True)
    match_score = models.FloatField(default=0)
    ai_recommendation = models.CharField(max_length=100, blank=True)

    applied_job = models.ForeignKey(
        JobRole,
        on_delete=models.CASCADE,
        related_name="candidates"
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="Pending"
    )

    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name