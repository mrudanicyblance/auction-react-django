from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.contrib import messages
from .forms import EmailAuthenticationForm  # Import the custom form

#For Admin Login
def admin_login(request):
    if request.method == 'POST':
        form = EmailAuthenticationForm(request, data=request.POST)  # Use custom form
        if form.is_valid():
            email = form.cleaned_data.get('username')  # Use 'username' field for email
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=email, password=password)
            if user is not None:
                login(request, user)
                return redirect('index')
            else:
                messages.error(request, "Invalid email or password")
        else:
            # Handle form errors
            if form.non_field_errors():
                messages.error(request, form.non_field_errors())
            else:
                for field, errors in form.errors.items():
                    for error in errors:
                        messages.error(request, f"{field}: {error}")
    else:
        form = EmailAuthenticationForm()  # Use custom form
    return render(request, 'adminpanel/login.html', {'form': form})

@login_required
def index(request):
    username = request.user.username
    return render(request, 'adminpanel/index.html', {'username': username})

def admin_logout(request):
    logout(request)
    return redirect('login')