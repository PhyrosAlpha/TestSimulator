from django import forms

class QuestionForm(forms.Form):
    annotation = forms.CharField(label='Anotação', required=False, widget=forms.Textarea(attrs={'class': 'form-control'}))