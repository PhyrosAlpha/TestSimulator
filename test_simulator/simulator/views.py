from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound
from django.template import loader
from django.core import serializers
from tests.models import Test, Question, Option

from json import dumps

def login(request):
    template = loader.get_template('login.html')
    return HttpResponse(template.render())

def home(request):
    template = loader.get_template('home.html')
    return HttpResponse(template.render())

def simulator(request):
    if request.GET.__contains__('test'):
        test = request.GET['test']
        print(test)
        return HttpResponseRedirect('test/' + test)
    
    tests = Test.objects.all()
    context = {
        'tests': tests
    }

    template = loader.get_template('simulator.html')
    return HttpResponse(template.render(context, request))

def start_simulator(request, test):
    print("Usuário logado: " + str(request.user.username))
    if request.user.is_authenticated:
        username = request.user.username
        print(username)

    result = Test.objects.filter(id=test)
    
    test = result[0]
    context = {
        'test': test
    }
        
    template = loader.get_template('start_simulator.html')
    return HttpResponse(template.render({'test': test}, request))


def get_test(request, test):
    result = Test.objects.filter(id=test)[0]
    
    dict_data = {'test_id': result.id, 
                 'name': result.name,
                 'questions': []
                 }
    
    questions = result.getQuestionsToTest()
    for question in questions:
        dict_question = {'id': question.id,
                         'question_text': question.question_text,
                         'options': []
                         }
        options = question.getOptions()
        for option in options:
            dict_option = {'id': option.id,
                           'option_text': option.option_text,
                           }
            dict_question['options'].append(dict_option)
        dict_data['questions'].append(dict_question)
    
    # print(dict_data)
    # data = serializers.serialize('json', dict_data)
    data = dumps(dict_data)
    return HttpResponse(data, content_type='application/json')


def send_test(request):
    pass