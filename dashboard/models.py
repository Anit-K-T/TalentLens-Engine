from django.db import models
from candidates.models import Candidate
from jobs.models import JobRole

class Evaluation(models.Model):

    STATUS_CHOICES = [
        ("Pending", "Pending"),
        ("Approved", "Approved"),
        ("Rejected", "Rejected"),
    ]

    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE)
    job_role = models.ForeignKey(JobRole, on_delete=models.CASCADE)

    skill_score = models.FloatField(default=0)
    experience_score = models.FloatField(default=0)
    education_score = models.FloatField(default=0)
    semantic_score = models.FloatField(default=0)

    final_score = models.FloatField(default=0)

    recommendation = models.TextField(blank=True)

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="Pending"
    )

    def __str__(self):
        return f"{self.candidate.name} - {self.job_role.title}"