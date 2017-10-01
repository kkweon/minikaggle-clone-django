from django import forms
from .models import Competition


class CompetitionForm(forms.ModelForm):
    class Meta:
        model = Competition
        fields = ["title", "description", "training_file", "test_file", "test_answer_file"]
