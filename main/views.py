from django.contrib.auth.models import User
from django.db.models import Q
from django.http import HttpResponseRedirect, HttpResponseNotFound
from django.shortcuts import render, redirect, get_object_or_404
from .forms import CreateUserForm, OrganizationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
# from .models import Application, Timetable, Type_question, Type_employee
from django.views.generic import ListView
from django.contrib.auth import models
import random

from .models import Services


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


def services(request):

    return render(request, 'main/services.html')


def create_organization(request):
    if request.method == 'POST':
        f = OrganizationForm(request.POST)
        if f.is_valid():
            f.save()
    else:
        f = OrganizationForm()
    return render(request, 'main/create_organization.html', {'form': f})
