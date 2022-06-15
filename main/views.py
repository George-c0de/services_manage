from django.contrib.auth.models import User
from django.db.models import Q
from django.http import HttpResponseRedirect, HttpResponseNotFound, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from .forms import CreateUserForm, OrganizationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
# from .models import Application, Timetable, Type_question, Type_employee
from django.views.generic import ListView
from django.contrib.auth import models
import random
from hashlib import sha1
from django.contrib.auth.hashers import check_password
import random
from .models import Services, Get_Password, Organization


def loginPage(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                messages.info(request, 'имя пользователя и пароль неверный.')

        context = {}
        return render(request, 'main/login.html', context)


def logoutUser(request):
    logout(request)
    return redirect('login')


def RegisterPage(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        form = CreateUserForm()
        if request.method == 'POST':
            form = CreateUserForm(request.POST)
            if form.is_valid():
                form.save()
                user = form.cleaned_data.get('username')
                messages.success(request, 'Аккаунт создан,' + user)
                return redirect('login')

        context = {'form': form}
        return render(request, 'main/register.html', context)


# @login_required(login_url='login')
def index(request):
    service = Services.objects.filter(ip_address=request.GET.get('search'))
    service_name = Services.objects.filter(organization__name=request.GET.get('search'))
    search = request.GET.get('search')
    if request.method == 'GET' and search is not None:
        if not service:
            if not service_name:
                context = {
                    'services': None,
                    'title': 'Главная страница1',
                }
            else:
                context = {
                    'services': service_name,
                    'title': 'Главная страница2',
                }
        else:
            context = {
                'services': service,
                'title': 'Главная страница3',
            }
    else:
        service = Services.objects.all()
        context = {
            'services': service,
            'title': 'Главная страница4',
        }
    template = 'main/index.html'
    return render(request, template, context=context)


def services(request, services_id):
    service = Services.objects.get(id=services_id)
    password = None
    if request.method == 'POST':
        id_services = request.POST.get('id_services')
        id_user = request.user.id
        user = User.objects.get(id=id_user)
        if check_password(request.POST.get('password'), user.password) and user.username == request.POST.get('login'):
            get_password = Get_Password()
            service1 = Services.objects.get(id=id_services)
            get_password.id_services = service1
            get_password.id_user = user
            get_password.save()
            chars = '-_abcdefghijklnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890'
            number = 1
            length = 10
            for n in range(number):
                password = ''
                for i in range(length):
                    password += random.choice(chars)
            password = service1.password
        else:
            get_password = None

    else:
        get_password = None
    context = {
        'service': service,
        'get_password': get_password,
        'password': password
    }
    return render(request, 'main/services.html', context=context)


def create_organization(request):
    if request.user.groups.filter(name='Admin').exists():
        if request.method == 'POST':
            f = OrganizationForm(request.POST)
            if f.is_valid():
                f.save()
                return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))
        else:
            f = OrganizationForm()
        return render(request, 'main/create_organization.html', {'form': f})
    else:
        return HttpResponse("Вкладка доступна только для администрации")


def create_services(request):
    organizations = Organization.objects.all()
    services1 = Services.objects.all()
    g=0
    if request.method == 'POST' and request.POST.get('services1') is not None:
        serv = Services.objects.get(id=request.POST.get('services1'))

        if request.POST.get('ip_address') is not None:
            serv.ip_address = request.POST.get('ip_address')
        if request.POST.get('login') is not None:
            serv.login = request.POST.get('login')
        if request.POST.get('password') is not None:
            serv.password = request.POST.get('password')
        serv.save()
        g = serv.login
        context = {
            'organizations': organizations,
            'services1': services1,
            'g': g
        }
        return render(request, 'main/create_services.html', context=context)
    elif request.method == 'POST':
        services = Services()
        organization = Organization.objects.get(id=request.POST.get('organization'))
        services.organization = organization
        services.ip_address = request.POST.get('id_address')
        services.ip_address = request.POST.get('login')
        services.ip_address = request.POST.get('password')
        services.save()
        return HttpResponseRedirect('/services/' + str(services.id))
    else:
        context = {
            'organizations': organizations,
            'services1': services1,
            'g': g
        }
        return render(request, 'main/create_services.html', context=context)


def report(request):
    context = {

    }
    return render(request, 'main/report.html', context=context)