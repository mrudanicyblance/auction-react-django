from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.contrib import messages
from .forms import EmailAuthenticationForm, SignUpForm  # Import the custom form
from .models import Profile
import random
import string

#ADMIN LOGIN PAGE
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

def admin_logout(request):
    logout(request)
    return redirect('login')

#INDEX PAGE
@login_required
def index(request):
    username = request.user.username
    return render(request, 'adminpanel/index.html', {'username': username})

#USERS PAGE
def all_users(request):
    return render(request, 'adminpanel/users/index.html')

def generate_random_username():
    return 'user_' + ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))

def generate_random_password(length=10):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for i in range(length))

def create_users(request):
    if request.method == 'POST':
        # Generate random username and password
        random_username = generate_random_username()
        random_password = generate_random_password()

        # Assign random username and password to the request.POST data
        request.POST = request.POST.copy()
        request.POST['username'] = random_username
        request.POST['password1'] = random_password
        request.POST['password2'] = random_password

        form = SignUpForm(request.POST, request.FILES)

        if form.is_valid():
            user = form.save(commit=False)
            user.save()

            # Create profile with form data
            Profile.objects.create(
                user=user,
                phone_no=form.cleaned_data['phone_no'],
                address_line_1=form.cleaned_data['address_line_1'],
                address_line_2=form.cleaned_data['address_line_2'],
                country=form.cleaned_data['country'],
                state=form.cleaned_data['state'],
                city=form.cleaned_data['city'],
                zipcode=form.cleaned_data['zipcode'],
                role=form.cleaned_data['role'],
                photo=form.cleaned_data['photo']
            )

            return redirect('allusers')
        else:
            print("Form errors:", form.errors.as_json())
            return render(request, 'adminpanel/users/create.html', {'form': form})
    else:
        form = SignUpForm()
    return render(request, 'adminpanel/users/create.html', {'form': form})
def edit_users(request):
    #if request.method == 'POST':
    #    user_form = UserUpdateForm(request.POST, instance=request.user)
     #   profile_form = UserProfileForm(request.POST, instance=request.user.profile)
     #   if user_form.is_valid() and profile_form.is_valid():
      #      user_form.save()
     ##       profile_form.save()
      #      return redirect('profile')
   # else:
     #   user_form = UserUpdateForm(instance=request.user)
     #   profile_form = UserProfileForm(instance=request.user.profile)
     return render(request, 'adminpanel/users/edit.html', {
            #'user_form': user_form,
           # 'profile_form': profile_form
        })