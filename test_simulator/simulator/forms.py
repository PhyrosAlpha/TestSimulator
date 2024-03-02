from django import forms
from django.forms import Select, Textarea
from tests.models import Test, UserQuestionData

modified_select_widget = Select(attrs={'class':'form-select'})
modified_text_area_widget = Textarea(attrs={'class': 'form-control'})

class SelectSimulationTestForm(forms.Form):
    result = Test.objects.all()
    options = []
    for option in result:
        options.append((option.id, option.name))

    test = forms.ChoiceField(
        required=True, 
        label="Escolha um Teste", 
        choices=options,
        widget=modified_select_widget)
    
    sizes = []
    for n in range(1, 11):
        sizes.append((n*10, str(n*10)))

    size = forms.ChoiceField(
        required=True, 
        label="Quantas questões?", 
        choices=sizes,
        widget=modified_select_widget)
