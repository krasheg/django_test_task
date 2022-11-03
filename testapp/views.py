from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate,login,logout
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib import messages

# Create your views here.


def index(request):
    return render(request, 'index.html')


def user_login(request):

    if request.POST:
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse('index'))
            else:
                messages.error(request, "Account isn`t active!")
                return HttpResponseRedirect(reverse('login'))
        else:
            messages.error(request, "Incorrect username or password!")
            return HttpResponseRedirect(reverse('login'))
    else:
        return render(request, "login.html")


@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))
