from django import forms
from .models import Interview


class InterviewForm(forms.ModelForm):
    class Meta:
        model = Interview
        fields = "__all__"

        widgets = {
            "interview_date": forms.DateInput(
                attrs={"type": "date", "class": "form-control"}
            ),
            "interview_time": forms.TimeInput(
                attrs={"type": "time", "class": "form-control"}
            ),
            "interviewer_name": forms.TextInput(
                attrs={"class": "form-control"}
            ),
            "meeting_link": forms.URLInput(
                attrs={"class": "form-control"}
            ),
            "remarks": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 3,
                }
            ),
        }