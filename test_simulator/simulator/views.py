from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from tests.models import Test
from django.contrib.auth import authenticate, login as login_now, logout
from json import dumps, loads
from . import test_generator
from . import test_corrector
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers
from .forms import SelectSimulationTestForm
#from django.contrib import messages


def home(request):
    template = loader.get_template('home.html')
    return HttpResponse(template.render())

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

        #messages.error(request, "Senha incorreta")
        return HttpResponseRedirect('/login?error=1')

    return HttpResponseRedirect('/')

def auth_logout(request):
    logout(request)
    return HttpResponseRedirect('/')

def simulator(request):
    print("Usuário logado: " + str(request.user.username))
    size = request.GET.get('size')
    form = SelectSimulationTestForm()
    if request.GET.__contains__('test'):
        test = request.GET['test']
        return HttpResponseRedirect('test/' + test + '?size=' + size)
    
    tests = Test.objects.all()
    context = {
        'form': form,
        'tests': tests
    }

    template = loader.get_template('simulator.html')
    return HttpResponse(template.render(context, request))

def start_simulator(request, test):
    print("Usuário logado: " + str(request.user.username))
    size = request.GET.get('size')
    print(size)
    if request.user.is_authenticated:
        username = request.user.username
        print(username)

    result = Test.objects.filter(id=test)
    test = result[0]
    context = {
        'test': test,
        'size': size
    }
        
    template = loader.get_template('start_simulator.html')
    return HttpResponse(template.render(context, request))


def get_test(request, test):
    size = request.GET.get('size')
    print('aquiiiii - ' + size)
    generator = test_generator.TestGenerator(test, int(size))
    data = generator.generateTest()
    return HttpResponse(data, content_type='application/json')


@csrf_exempt
def correct_test(request):
    print("SEND TEST")
    print(loads(request.body))

    #Cria gabarito do Usuário
    test_user_dict = loads(request.body)
    user_answer_sheet = test_corrector.AnswerSheetFactory.get_user_answer_sheet(test_user_dict, request.user)

    #Cria gabarito do Sistema, com as respostas corretas
    questions_list = user_answer_sheet.get_questions_list()
    system_answer_sheet = test_corrector.AnswerSheetFactory.get_system_answer_sheet(test_user_dict['test_id'], questions_list)


    #Corrigi o teste gerando o gabarito corrigido
    instance_test_corrector = test_corrector.TestCorrector(user_answer_sheet, system_answer_sheet)
    corrected_answer_sheet_user = instance_test_corrector.init_correction()

    #print("DEPOIS DE CORRIGIR")
    #print("Corretas:{}    Incorretas:{}".format(corrected_answer_sheet_user.get_corrects(), corrected_answer_sheet_user.get_incorrects()))
    #print(corrected_answer_sheet_user)
    #for question in corrected_answer_sheet_user.questions:
    #    print(question)
    
    data = corrected_answer_sheet_user.serialize_to_json()
    print(data)
    return HttpResponse(data, content_type='application/json')

"""
@csrf_exempt
def correct_test(request):
    print("SEND TEST")
    print(loads(request.body))

    test_user_json = loads(request.body)
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
"""