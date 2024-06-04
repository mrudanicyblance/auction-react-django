from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.contrib import messages
from .forms import EmailAuthenticationForm, SignUpForm, UserAndProfileForm  # Import the custom form
from django.contrib.auth.models import User
from .models import Profile
import random
import string
from django.contrib import messages

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
    users_with_user_role = User.objects.filter(profile__role='user')

    # You can then pass this queryset to your template
    context = {
        'users': users_with_user_role
    }
    return render(request, 'adminpanel/users/index.html',context)

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
            # Send email to the user
            subject = 'Your account has been created'
            html_message = render_to_string('adminpanel/users/email.html', {'username': user.username, 'password': random_password})
            plain_message = strip_tags(html_message)
            from_email = 'urmish.cyblance@gmail.com'  # Change this to your email address
            to_email = user.email

            #send_mail(subject, plain_message, from_email, [to_email], html_message=html_message)

            messages.success(request, 'User created successfully and email sent')
            return redirect('allusers')
        else:
            print("Form errors:", form.errors.as_json())
            return render(request, 'adminpanel/users/create.html', {'form': form})
    else:
        form = SignUpForm()
    return render(request, 'adminpanel/users/create.html', {'form': form})

def edit_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    profile = user.profile

    if request.method == 'POST':
        form = UserAndProfileForm(request.POST, request.FILES, instance=user)
        if not request.FILES.get('photo'):
            form.fields['photo'].initial = profile.photo
        if form.is_valid():
            # Update User model fields
            user.email = form.cleaned_data['email']
            user.first_name = form.cleaned_data['first_name']
            user.last_name = form.cleaned_data['last_name']
            # Update Profile model fields
            profile.phone_no = form.cleaned_data['phone_no']
            profile.address_line_1 = form.cleaned_data['address_line_1']
            profile.address_line_2 = form.cleaned_data['address_line_2']
            profile.country = form.cleaned_data['country']
            profile.state = form.cleaned_data['state']
            profile.city = form.cleaned_data['city']
            profile.zipcode = form.cleaned_data['zipcode']
            profile.photo = form.cleaned_data['photo']
            profile.role = form.cleaned_data['role']
            # Save both models
            user.save()
            profile.save()
            messages.success(request, 'User updated successfully')
            return redirect('allusers')  # Replace 'all_users' with your desired redirect URL name
    else:
        form = UserAndProfileForm(instance=user)

    return render(request, 'adminpanel/users/edit.html', {'form': form, 'user': user, 'profile': profile})

def delete_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        user.delete()
        messages.success(request, 'User deleted successfully')
        return redirect('allusers')  # Redirect to the user list page
    else:
        messages.error(request, 'Somthing went wrong')
        return redirect('allusers')

def my_profile (request):
    return render(request, 'adminpanel/my-profile.html')
def forget_password (request):
    return render(request, 'adminpanel/forget-password.html')