from django import forms
from django.db.models import fields
from .models import Genus

class GenusForm(forms.ModelForm):
    class Meta:
        model = Genus
        fields = ['genus_ko', 'genus_en']
        widgets = {
            'genus_ko' : forms.TextInput(attrs={
                "class" : "form-control",
                "placeholder" : "ex)"
            }),
            'genus_en': forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "ex)"
            })
        }