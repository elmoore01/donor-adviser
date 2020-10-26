from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, DeleteView
from django.contrib.auth.views import LoginView
from django.contrib.auth import get_user_model
from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.urls import reverse_lazy

import uuid
import boto3

from .forms import LoginForm, RegisterForm
from .models import CustomUser

S3_BASE_URL = 'https://s3.us-west-1.amazonaws.com/'
BUCKET = 'lifeprep-academy'

# Create your views here.
class AccountLoginView(LoginView):
    form_class = LoginForm
    template_name = 'accounts/login.html'

class AccountRegisterView(CreateView):
    form_class = RegisterForm
    template_name = 'accounts/signup.html'
    success_url = reverse_lazy('account_login')

@login_required
def account_profile(request):
    return render(request, 'accounts/profile.html', {'user': request.user})

@login_required
def account_profile_update(request):
    return render(request, 'accounts/update.html', {'user': request.user})

@login_required
def account_profile_save(request):
    if request.method == 'POST':
        user = request.user
        user.first_name = request.POST.get('first_name', '')
        user.last_name = request.POST.get('last_name', '')
        user.description = request.POST.get('description', '')
        photo_file = request.FILES.get('photo-file', None)
        if photo_file:
            s3 = boto3.client('s3')
            key = uuid.uuid4().hex[:6] + '-' + photo_file.name[photo_file.name.rfind('.'):]
            try:
                s3.upload_fileobj(photo_file, BUCKET, key)
                url = f'{S3_BASE_URL}{BUCKET}/{key}'
                user.profile_url = url
            except:
                print('An error occurred uploading a file to S3')
        user.save()
    return redirect('account_profile')

@login_required
def account_profile_delete(request):
    user = request.user
    user.delete()
    return redirect('account_logout')

def account_logout(request):
    logout(request)
    return redirect('home')
