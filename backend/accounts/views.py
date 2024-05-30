from django.shortcuts import render, redirect
from . import forms,models
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required

# Create your views here.
# logged in account cannot access these pages.
def anonymous_required(view_func):
    def wrapped_view(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home')
        return view_func(request, *args, **kwargs)
    return wrapped_view

# login / authentication function. works only on username and password.
@anonymous_required
def loginaccounts(request):
    if request.method == 'POST':
        form = forms.AuctionUserAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            # print('form is valid', request.POST)
            user = form.get_user()
            login(request, user)
            # print('user role:',user.role)
            role = user.role
            if role == 'admin':
                return redirect('admin_home')
            else:
                return redirect('home')
        else:
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is None:
                messages.error(request, "Invalid username or password.")
            else:
                messages.error(request, "Authentication failed.")
    else:
        form = forms.AuctionUserAuthenticationForm()

    return render(request, 'login.html', {'form': form})

# signup form takes in fields to register a user
@anonymous_required
def signupaccounts(request):
    if request.method == 'POST':
        form = forms.AuctionUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
        else:
            print("Form errors:", form.errors)
    else:
        form = forms.AuctionUserCreationForm()

    return render(request, 'signup.html', {'form': form})

# session logout.
def logout_view(request):
    logout(request)
    return redirect('login_account')