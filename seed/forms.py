from tkinter import Widget
from django import forms
from django.db.models import fields
from .models import Seed

class SeedForm(forms.ModelForm):
    class Meta:
        model = Seed
        fields = ['intro_num', 'family', 'genus', 'used_scientific_name', 'plant_name', 'microscope', 'seed_length', 'seed_length_error', 'seed_width', 'seed_width_error', 'note', 'grain']
        widgets = {
            'intro_num' : forms.TextInput(attrs={
                "class" : "form-control",
                "placeholder" : "ex) 2020-001492"
            }),
            'family' : forms.Select(attrs={
                "class" : "form-select"
            }),
            'genus' : forms.Select(attrs={
                "class" : "form-select"
            }),
            'used_scientific_name' : forms.TextInput(attrs={
                "class" : "form-control",
                "placeholder" : "ex) Aster maackii Regel"
            }),
            'plant_name' : forms.TextInput(attrs={
                "class" : "form-control",
                "placeholder" : "ex) 좀개미취"
            }),
            'microscope' : forms.CheckboxInput(attrs={
                "class" : "form-check-input",
                "style" : "margin-left: 15px;"
            }),
            'seed_length' : forms.NumberInput(attrs={
                "class" : "form-control",
                "placeholder" : "ex) 2.71"
            }),
            'seed_length_error' : forms.TextInput(attrs={
                "class" : "form-control",
                "placeholder" : "ex) 0.05"
            }),
            'seed_width' : forms.TextInput(attrs={
                "class" : "form-control",
                "placeholder" : "ex) 1.01"
            }),
            'seed_width_error' : forms.TextInput(attrs={
                "class" : "form-control",
                "placeholder" : "ex) 0.02"
            }),
            'note' : forms.Textarea(attrs={
                "class" : "form-control",
                "placeholder" : "ex) 1차"
            }),
            'grain' : forms.Select(attrs={
                "class" : "form-select"
            })
        }