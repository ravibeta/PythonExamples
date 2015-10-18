from django import forms

class OForm(forms.Form):
    purpose = forms.CharField(label='purpose', max_length=100)
