from django.core.exceptions import ValidationError
from django.http import HttpResponseRedirect
from django.urls import reverse

from django.shortcuts import render
from django.contrib.auth.models import User

from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

import re

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        form = AuthenticationForm(request.POST, initial={'username' : username})
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return HttpResponseRedirect(reverse('index'))
        else:
            form.error_message = 'Please enter a correct username and password. Note that both fields are case-sensitive.'
            
    else:
        form = AuthenticationForm()
        
    form.fields['username'].widget.attrs['class'] = "form-control"
    form.fields['password'].widget.attrs['class'] = "form-control"

    context = {'form':form}
    return render(request, 'users/login.html', context)

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))

def register_view(request):
    def check_if_username_is_valid():
        username = form.__dict__['data']['username']
        invalid_usernames = ['search','new_album','new_media']
        if not (re.match(r'^[a-zA-Z0-9_]*$', username)) or len(username) > 18:
            form.errors['username'] = form.error_class()
            form.add_error('username', '18 characters or fewer. Letters and digits only.')
        
        if username in invalid_usernames:
            form.errors['username'] = form.error_class()
            form.add_error('username', 'Please choose a different username')
        
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        form.fields['username'].widget.attrs['class'] = 'form-control'
        form.fields['password1'].widget.attrs['class'] = 'form-control'
        form.fields['password2'].widget.attrs['class'] = 'form-control'
        
        check_if_username_is_valid()
        
        if form.is_valid():
            new_user = form.save()
            authenticated_user = authenticate(username=new_user.username, password=request.POST['password1'])
            login(request, authenticated_user)
            return HttpResponseRedirect(reverse('index'))
    else:
        form = UserCreationForm()
        form.fields['username'].widget.attrs['class'] = 'form-control'
        form.fields['password1'].widget.attrs['class'] = 'form-control'
        form.fields['password2'].widget.attrs['class'] = 'form-control'
    
    context = {'form': form}
    return render(request, 'users/register.html', context)
