from django import forms
from .models import JobRole

class JobRoleForm(forms.ModelForm):
    class Meta:
        model = JobRole
        fields = [
            "title",
            "description",
            "required_skills",
            "minimum_experience",
            "education_required",
        ]

        widgets = {
            "title": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Enter Job Title"
            }),

            "description": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 4,
                "placeholder": "Enter Job Description"
            }),

            "required_skills": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 3,
                "placeholder": "Python, SQL, Machine Learning..."
            }),

            "minimum_experience": forms.NumberInput(attrs={
                "class": "form-control",
                "placeholder": "Years of Experience"
            }),

            "education_required": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "B.Tech, MCA..."
            }),
        }