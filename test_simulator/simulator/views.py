from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from tests.models import Test
from django.contrib.auth import authenticate, login as login_now, logout
from json import dumps, loads
from . import test_generator
from . import test_corrector
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers


def home(request):
    template = loader.get_template('home.html')
    return HttpResponse(template.render(request=request))

def login(request):
    if(request.user.is_authenticated):
        return HttpResponseRedirect('/')

    template = loader.get_template('login.html')
    return HttpResponse(template.render(request=request))

def auth_login(request):
    if(request.user.is_authenticated):
        return HttpResponseRedirect('/')

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None: 
            login_now(request, user)
            if(request.GET.__contains__('next')):
                return HttpResponseRedirect(request.GET['next'])

            return HttpResponseRedirect('/dashboard')

        return HttpResponseRedirect('/login?error=1')

    return HttpResponseRedirect('/')

def auth_logout(request):
    logout(request)
    return HttpResponseRedirect('/')

def simulator(request):
    if request.GET.__contains__('test'):
        test = request.GET['test']
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
    print(test)
    context = {
        'test': test
    }
        
    template = loader.get_template('start_simulator.html')
    return HttpResponse(template.render(context, request))


def get_test(request, test):
    generator = test_generator.TestGenerator(test, 5)
    data = generator.generateTest()
    return HttpResponse(data, content_type='application/json')


@csrf_exempt
def correct_test(request):
    print("SEND TEST")
    print(loads(request.body)['current'])

    test_user_json = loads(request.body)['current']
    answer_sheet_user = test_corrector.AnswerSheetUser(test_user_json, request.user)

    questions_list = answer_sheet_user.get_questions_list()
    generator_answer_sheet_test = test_corrector.GeneratorAnswerSheetTest(questions_list)
    answer_sheet_test = generator_answer_sheet_test.generate()
    intance_test_corrector = test_corrector.TestCorrector(answer_sheet_user, answer_sheet_test)
    corrected_answer_sheet_user = intance_test_corrector.init_correction()

    print("DEPOIS DE CORRIGIR")
    print("Corretas:{}    Incorretas:{}".format(corrected_answer_sheet_user.get_corrects(), corrected_answer_sheet_user.get_incorrects()))
    print(corrected_answer_sheet_user)
    for question in corrected_answer_sheet_user.questions:
        print(question)
    
    data = corrected_answer_sheet_user.serialize_to_json()
    print(data)
    return HttpResponse(data, content_type='application/json')