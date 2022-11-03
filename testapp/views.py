from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib import messages
from .forms import UploadForm
from .utils import collect_from_stored_files, collect_from_uploaded_files, add_users
from django.core.files.storage import FileSystemStorage
import os
from pathlib import Path

# Create your views here.
BASE_DIR = Path(__file__).resolve().parent.parent


def index(request):
    """view for home page"""
    user = get_user_model()
    if user.objects.all():
        return render(request, 'index.html', {'users': user.objects.all()})
    data = collect_from_stored_files()
    add_users(user, data)
    return render(request, 'index.html', {'users': user.objects.all()})


def user_login(request):
    """view for login page"""
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
    """view for logout"""
    logout(request)
    return HttpResponseRedirect(reverse('index'))


def upload_files(request):
    """view for uploading files"""
    if request.POST:
        form = UploadForm(request.POST, request.FILES)
        csv_file = request.FILES['upload_csv']
        xml_file = request.FILES['upload_xml']
        print(csv_file)
        print(xml_file)
        if form.is_valid():
            if not csv_file.name.endswith('.csv'):
                messages.error(request, 'Wrong file type')
                return HttpResponseRedirect(reverse('upload'))
            if not xml_file.name.endswith('.xml'):
                messages.error(request, 'Wrong file type')
                return HttpResponseRedirect(reverse('upload'))
            user = get_user_model()
            fss = FileSystemStorage()
            csv_file = fss.save(csv_file.name, csv_file)
            csv_url = fss.url(csv_file)
            print(os.path.join(BASE_DIR, csv_url))
            xml_file = fss.save(xml_file.name, xml_file)
            xml_url = fss.url(xml_file)
            data = collect_from_uploaded_files(csv_url, xml_url)
            add_users(user, data)
            return HttpResponseRedirect(reverse('index'))
    else:
        form = UploadForm()
    return render(request, 'upload.html', {'form': form})
