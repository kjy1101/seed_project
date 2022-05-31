from django import forms
from django.db.models import fields
from .models import Seed

class SeedForm(forms.ModelForm):
    class Meta:
        model = Seed
        fields = ['intro_num', 'family', 'genus', 'used_scientific_name', 'plant_name', 'microscope', 'seed_length', 'seed_length_error', 'seed_width', 'seed_width_error', 'note']