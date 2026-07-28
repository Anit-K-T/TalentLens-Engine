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

    RECOMMENDATION_CHOICES = [
        ("Strong Hire", "Strong Hire"),
        ("Hire", "Hire"),
        ("Hold", "Hold"),
        ("Reject", "Reject"),
    ]

    # -----------------------------
    # Interview Details
    # -----------------------------
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

    # -----------------------------
    # Interview Recording
    # -----------------------------
    interview_recording = models.FileField(
        upload_to="interview_recordings/",
        blank=True,
        null=True
    )

    # -----------------------------
    # AI Transcript
    # -----------------------------
    transcript = models.TextField(
        blank=True,
        null=True
    )

    # -----------------------------
    # AI Evaluation Scores
    # -----------------------------
    communication_score = models.FloatField(
        default=0
    )

    technical_score = models.FloatField(
        default=0
    )

    confidence_score = models.FloatField(
        default=0
    )

    overall_score = models.FloatField(
        default=0
    )

    # -----------------------------
    # AI Feedback
    # -----------------------------
    ai_feedback = models.TextField(
        blank=True,
        null=True
    )

    hiring_recommendation = models.CharField(
        max_length=20,
        choices=RECOMMENDATION_CHOICES,
        blank=True,
        null=True
    )
    # -----------------------------
# AI Analysis
# -----------------------------
    summary = models.TextField(
    blank=True,
    null=True)

    strengths = models.JSONField(
    default=list,
    blank=True)

    weaknesses = models.JSONField(
    default=list,
    blank=True)

    # -----------------------------
    # Metadata
    # -----------------------------
    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return f"{self.candidate.name} - {self.job.title} ({self.interview_date})"