from django import forms
from .models import Interview


class InterviewForm(forms.ModelForm):
    class Meta:
        model = Interview
        fields = [
            "candidate",
            "job",
            "interview_date",
            "interview_time",
            "interviewer_name",
            "mode",
            "meeting_link",
            "remarks",
            "status",
            "interview_recording",
        ]

        widgets = {
            "candidate": forms.Select(attrs={
                "class": "form-select"
            }),

            "job": forms.Select(attrs={
                "class": "form-select"
            }),

            "interview_date": forms.DateInput(
                attrs={
                    "type": "date",
                    "class": "form-control"
                }
            ),

            "interview_time": forms.TimeInput(
                attrs={
                    "type": "time",
                    "class": "form-control"
                }
            ),

            "interviewer_name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter interviewer name"
                }
            ),

            "mode": forms.Select(attrs={
                "class": "form-select"
            }),

            "meeting_link": forms.URLInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "https://meet.google.com/..."
                }
            ),

            "remarks": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 3,
                    "placeholder": "Interview remarks..."
                }
            ),

            "status": forms.Select(attrs={
                "class": "form-select"
            }),

            "interview_recording": forms.ClearableFileInput(
                attrs={
                    "class": "form-control"
                }
            ),
        }