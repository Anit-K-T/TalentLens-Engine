from django.db import models

class JobRole(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    required_skills = models.TextField(help_text="Comma-separated skills")
    minimum_experience = models.FloatField()
    education_required = models.CharField(max_length=100)
    summary = models.TextField(blank=True)

    strengths = models.JSONField(default=list, blank=True)

    weaknesses = models.JSONField(default=list, blank=True)

    def __str__(self):
        return self.title
