from django import forms
from django.db.models import fields
from .models import Family

class FamilyForm(forms.ModelForm):
    class Meta:
        model = Family
        fields = ['family_ko', 'family_en']
        widgets = {
            'family_ko': forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "ex)"
            }),
            'family_en': forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "ex)"
            })
        }