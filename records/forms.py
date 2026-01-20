from django import forms
from .models import PlayerJudgement

class JudgementForm(forms.ModelForm):
    class Meta:
        model = PlayerJudgement
        fields = ["judgement"]
        widgets = {
            'judgement': forms.RadioSelect()
        }
