from django import forms
from django.forms import Select, Textarea
from tests.models import Test, UserQuestionData

modified_select_widget = Select(attrs={'class':'form-select'})
modified_text_area_widget = Textarea(attrs={'class': 'form-control'})

class QuestionModelForm(forms.ModelForm):
    class Meta:
        model = UserQuestionData
        fields = ["tag", "annotation"]
        widgets = {
            'tag': modified_select_widget,
            'annotation': modified_text_area_widget
}

class SelectTestForm(forms.Form):
    result = Test.objects.all()
    options = []
    for option in result:
        options.append((option.id, option.name))

    test = forms.ChoiceField(
        required=True, 
        label="Escolha um Teste", 
        choices=options,
        widget=modified_select_widget)

class SelectTag(forms.Form):
    tags = UserQuestionData.TAGS
    tags.insert(0, ('TODOS', 'Todos'))

    tag = forms.ChoiceField(
        choices=tags,
        widget=modified_select_widget,
        initial='TODOS'
    )

class QuestionForm(forms.Form):
    tag = forms.ChoiceField(required=False, widget=modified_select_widget)
    annotation = forms.CharField(required=False, widget=modified_text_area_widget)


