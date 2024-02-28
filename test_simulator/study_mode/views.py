from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from tests.models import Test, Question, UserQuestionData
from django.core.paginator import Paginator
from django.core.exceptions import ObjectDoesNotExist as DoesNotExist
from django.core.paginator import EmptyPage
from json import dumps
from django.http import Http404
from . import forms
from django.contrib import messages

def study_mode(request):

    print(request.GET)
    if request.GET.__contains__('test'):
        test = request.GET['test']
        return HttpResponseRedirect('test/' + test)

    form = forms.SelectTestForm()
    print(form.is_bound)
    print(form.is_valid)

    #form.renderer()
    context = {"form": form}

    template = loader.get_template('study_mode.html')
    return HttpResponse(template.render(context, request))

def selected_test(request, test):
    request_page = request.GET.get('page') or 1
    request_tag = request.GET.get('tag') or 'TODOS'

    print(request.GET)

    form = forms.SelectTag(request.GET)

    try:
        test = Test.objects.get(id=test)
        template = loader.get_template('selected_test.html')
        if(request.GET.get('tag') != None and request.GET.get('tag') != 'TODOS'):
            if request.user.is_authenticated:
                questions = []
                result = UserQuestionData.objects.filter(user=request.user, tag=request_tag, question__test=test)
                for i in result:
                    questions.append(i.question)
                page = Paginator(questions, 10)
                context = {
                    'form': form,
                    'test': test,
                    'current_page': page.page(request_page)
                }
                return HttpResponse(template.render(context, request)) 


        questions = test.question_set.all()
        page = Paginator(questions, 20)
        context = {
            'form': form,
            'test': test,
            'current_page': page.page(request_page),
        }
        return HttpResponse(template.render(context, request))
        
    except DoesNotExist :
        raise Http404()
    
    except EmptyPage:
        raise Http404()

def selected_question(request, test, question):
    result = Question.objects.filter(id=question)
    if len(result) == 0:
        raise Http404()
    question = result[0]

    if request.method == "POST":
        try:
            userData = UserQuestionData.objects.get(user=request.user, question=question)    

        except DoesNotExist:
            userData = UserQuestionData(user=request.user, question=question)

        form = forms.QuestionModelForm(request.POST, instance=userData)
        if(form.is_valid()):
            form.save()
            messages.success(request, "Os dados foram salvos com sucesso!")
    else:
        try:
            userData = UserQuestionData.objects.get(user=request.user, question=question)    
            form = forms.QuestionModelForm(instance=userData)
            
        except DoesNotExist:
            form = forms.QuestionModelForm()

    context = {
        'test':test,
        'question': question,
        'form': form
    }

    template = loader.get_template('selected_question.html')
    return HttpResponse(template.render(context, request))