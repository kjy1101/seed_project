from django import forms
from django.db.models import fields
from .models import Genus

class GenusForm(forms.ModelForm):
    class Meta:
        model = Genus
        fields = ['genus_ko', 'genus_en']