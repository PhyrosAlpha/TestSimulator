from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate
from re import match

@login_required(login_url='/login')
def dashboard(request):
    template = loader.get_template('dashboard.html')
    print("Executou o dashboard")
    return HttpResponse(template.render(request=request))

@login_required(login_url='/login')
def change_password(request):
    template = loader.get_template('change_password.html')
    return HttpResponse(template.render(request=request))

@login_required(login_url='/login')
def auth_change_password(request):
    if request.method == 'POST':
        current_password = request.POST['current_password']
        new_password = request.POST['new_password']
        confirm_password = request.POST['confirm_password']

    if new_password != confirm_password:
        return HttpResponseRedirect("/dashboard/change_password/?error=1")

    regex = "^(?=.*\d)(?=.*[!@#$%^&*])(?=.*[A-Z]).{9,}$"
    if match(regex, new_password) is None:
        return HttpResponseRedirect("/dashboard/change_password/?error=2")

    user = authenticate(request, username=request.user, password=current_password)
    if user is None:
        return HttpResponseRedirect("/dashboard/change_password/?error=3")

    user.set_password(new_password)
    user.save()

    return HttpResponseRedirect("/dashboard/change_password/?success=1")