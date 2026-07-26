from django.db import models
from candidates.models import Candidate
from jobs.models import JobRole


class Interview(models.Model):

    MODE_CHOICES = [
        ("Online", "Online"),
        ("Offline", "Offline"),
    ]

    STATUS_CHOICES = [
        ("Scheduled", "Scheduled"),
        ("Completed", "Completed"),
        ("Cancelled", "Cancelled"),
    ]

    candidate = models.ForeignKey(
        Candidate,
        on_delete=models.CASCADE,
    )

    job = models.ForeignKey(
        JobRole,
        on_delete=models.CASCADE,
    )

    interview_date = models.DateField()

    interview_time = models.TimeField()

    interviewer_name = models.CharField(
        max_length=100
    )

    mode = models.CharField(
        max_length=20,
        choices=MODE_CHOICES,
    )

    meeting_link = models.URLField(
        blank=True
    )

    remarks = models.TextField(
        blank=True
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="Scheduled",
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.candidate.name} - {self.interview_date}"