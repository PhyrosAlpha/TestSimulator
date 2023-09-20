from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound
from django.template import loader
from tests.models import Test, Question, Option, UserQuestionData
from django.core.paginator import Paginator
from django.core.exceptions import ObjectDoesNotExist as DoesNotExist
from django.core.paginator import EmptyPage
from json import dumps

def study_mode(request):
    if request.GET.__contains__('test'):
        test = request.GET['test']
        return HttpResponseRedirect('test/' + test)

    tests = Test.objects.all()
    context = {
        'tests': tests
    }
    template = loader.get_template('study_mode.html')
    return HttpResponse(template.render(context, request))


def selected_test(request, test):
    page_int = 1
    request_page = request.GET.get('page')
    if request_page != None:
        page_int = int(request_page)

    try:
        test = Test.objects.get(id=test)  
        questions = test.question_set.all()
        page = Paginator(questions, 20)
        context = {
            'test': test,
            'current_page': page.page(page_int),
        }

        template = loader.get_template('selected_test.html')
        return HttpResponse(template.render(context, request))
    
    except DoesNotExist :
        return HttpResponseNotFound("Opa esse test não existe! x.x")
    
    except EmptyPage:
        return HttpResponseNotFound("Opa essa página não existe! x.x")

def selected_question(request, question):
    result = Question.objects.filter(id=question)

    if len(result) == 0:
        return HttpResponseNotFound("Opa essa questão não existe! x.x")
    
    question = result[0]
    context = {
        'question': question
    }
    template = loader.get_template('selected_question.html')
    return HttpResponse(template.render(context, request))

def save_user_question_data(request, question):
    print(request.POST)

    question = Question.objects.get(id=question)
    try:
        userData = UserQuestionData.objects.get(user=request.user, question=question)
        userData.annotation = request.POST['annotation']
        userData.tag = request.POST['tag']
        userData.save()
        
    except DoesNotExist:
        userData = UserQuestionData(user=request.user, question=question, annotation=request.POST['annotation'])
        userData.save()

    response = request.POST
    return HttpResponse(dumps(response), content_type='application/json')


