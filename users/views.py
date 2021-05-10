from django.core.exceptions import ValidationError
from django.http import HttpResponseRedirect
from django.urls import reverse

from django.shortcuts import render
from django.contrib.auth.models import User

from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

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
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        form.fields['username'].widget.attrs['class'] = 'form-control'
        form.fields['password1'].widget.attrs['class'] = 'form-control'
        form.fields['password2'].widget.attrs['class'] = 'form-control'
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
