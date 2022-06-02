from django import forms


class SearchForm(forms.Form):
    intro_num = forms.CharField(
        widget=forms.TextInput
    )
