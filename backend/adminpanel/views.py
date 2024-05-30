from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponse

def admin_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('index')
            else:
                return HttpResponse("Invalid login")
        else:
            return HttpResponse("Invalid form")
    else:
        form = AuthenticationForm()
    return render(request, 'adminpanel/login.html', {'form': form})

@login_required
def index(request):
    username = request.user.username
    return render(request, 'adminpanel/index.html', {'username': username})