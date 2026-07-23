from django.db import models

class Candidate(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15, blank=True)
    education = models.CharField(max_length=150)
    experience = models.FloatField(help_text="Experience in years")
    skills = models.TextField(help_text="Comma-separated skills")
    resume = models.FileField(upload_to="resumes/")
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name