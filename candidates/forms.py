from django import forms
from .models import Candidate

class CandidateForm(forms.ModelForm):
    class Meta:
        model = Candidate
        fields = [
            "name",
            "email",
            "phone",
            "education",
            "experience",
            "skills",
            "resume",
            "applied_job",
            "status",
        ]

        widgets = {
            "name": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Enter Candidate Name"
            }),

            "email": forms.EmailInput(attrs={
                "class": "form-control",
                "placeholder": "Enter Email"
            }),

            "phone": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Enter Phone Number"
            }),

            "education": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Highest Qualification"
            }),

            "experience": forms.NumberInput(attrs={
                "class": "form-control"
            }),

            "skills": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 3,
                "placeholder": "Python, SQL, Machine Learning"
            }),

            "resume": forms.ClearableFileInput(attrs={
                "class": "form-control"
            }),

            "applied_job": forms.Select(attrs={
                "class": "form-select"
            }),

            "status": forms.Select(attrs={
                "class": "form-select"
            }),
        }