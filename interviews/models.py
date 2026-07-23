from django.db import models
from candidates.models import Candidate

class Interview(models.Model):
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE)
    transcript = models.TextField()
    technical_score = models.FloatField(default=0)
    communication_score = models.FloatField(default=0)
    overall_score = models.FloatField(default=0)

    def __str__(self):
        return f"Interview - {self.candidate.name}"