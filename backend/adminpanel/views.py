from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponseBadRequest
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.contrib import messages
from django.urls import reverse  # Import reverse from django.urls
from django.template.loader import render_to_string
from django.http import HttpResponse


from .forms import EmailAuthenticationForm, SignUpForm, UserAndProfileForm, ForgotPasswordForm  # Import the custom form
from django.contrib.auth.models import User
from .models import Profile, Category, SubCategory, Field, SubCategoryField, SubCategoryOptionField
import random
import string
from django.contrib import messages

# fields functions
def view_fields(request):
    fields = Field.objects.all()
    context = {'fields':fields}
    return render(request,'categories/fields.html',context=context)

@require_POST
@csrf_exempt
def add_field(request):
    if request.method == 'POST':
        try:
            print('add fields')
            field_name = request.POST.get('field_name')
            field_type = request.POST.get('field_type')
            print(field_name,field_type)
            field = Field.objects.create(field_name=field_name,field_type=field_type)
            return JsonResponse({'status':'success','field_name':field_name})
        except Exception as e:
            print('error occurred:',e)
            return JsonResponse({'status':'error'})

@require_POST
@csrf_exempt
def edit_field(request):
    try:
        field_id = request.POST.get('id')
        field_name = request.POST.get('field_name')
        field_type = request.POST.get('field_type')

        field = Field.objects.get(id=field_id)
        field.field_name = field_name
        field.field_type = field_type
        field.save()
        return JsonResponse({'status':'success','field_name':field_name})
    except Exception as e:
        return JsonResponse({'status':'error','message':str(e)})

@require_POST
@csrf_exempt
def delete_field(request):
    try:
        field_id = request.POST.get('fieldId')
        print(field_id)
        field = Field.objects.get(id=field_id)
        field.delete()
        return JsonResponse({'status':'success'})
    except Exception as e:
        print(e)
        return JsonResponse({'status':'error'})

# category functions
def view_category(request):
    categories = Category.objects.all()
    context = {'categories':categories}
    return render(request,'categories/category.html',context=context)

def add_category(request):
    if request.method == 'POST':
        try:
            print('add_reached')
            name = request.POST.get('name')
            if not name:
                return HttpResponseBadRequest("Name is required")

            category = Category.objects.create(name=name)
            return JsonResponse({'status':'success','id': category.id, 'name': category.name})
        except Exception as e:
            return JsonResponse({'status':'error','error': str(e)}, status=500)
    else:
        return HttpResponseBadRequest("Invalid request method")

@require_POST
@csrf_exempt
def update_category(request):
    try:
        category_id = request.POST.get('id')
        category_name = request.POST.get('name')
        if not category_name:
            return JsonResponse({'status': 'error', 'message': 'Category name cannot be empty'})

        category = Category.objects.get(id=category_id)
        category.name = category_name
        category.save()

        return JsonResponse({'status': 'success'})
    except Category.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Category does not exist'})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)})

@require_POST
@csrf_exempt
def delete_category(request):
    try:
        category_id = request.POST.get('id')
        category = Category.objects.get(id=category_id)
        category.delete()
        return JsonResponse({'status': 'success'})
    except Category.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Category does not exist'})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)})

# subcategory functions
def add_subcategory(request):
    if request.method == 'POST':
        print('add_reached_sub')
        print(request.POST)
        subcat_name = request.POST.get('subcat_name')
        category_id = request.POST.get('category_id')
        category = get_object_or_404(Category, id=category_id)
        subcategory = SubCategory.objects.create(category=category, subcat_name=subcat_name)
        return JsonResponse({'status': 'success'})
    else:
        return JsonResponse({'status':'error'})

def view_subcategory(request,id):
    subcategory = SubCategory.objects.get(pk=id)
    fields_of_subcategory = SubCategoryField.objects.filter(subcategory=subcategory)
    all_fields = Field.objects.all()
    context = {'subcategory':subcategory,'fields_of_subcategory':fields_of_subcategory,'all_fields':all_fields}
    return render(request,'categories/subcategory.html',context=context)

# linking subcategory and field
def link_subcat_field(request):
    if request.method == 'POST':
        selected_fields = request.POST.getlist('fieldchoice')
        subcat_id = request.POST.get('subcategory_id')

        try:
            subcategory = get_object_or_404(SubCategory, id=subcat_id)

            for field_id in selected_fields:
                field = get_object_or_404(Field, id=field_id)
                SubCategoryField.objects.get_or_create(subcategory=subcategory, field=field)

            return JsonResponse({'status': 'success'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})

    return JsonResponse({'status': 'error', 'message': 'Invalid request method'})

def delete_link(request):
    if request.method == 'POST':
        linkId = request.POST.get('linkId')
        subcatlink = get_object_or_404(SubCategoryField, id=linkId)
        if subcatlink:
            subcatlink.delete()
            return JsonResponse({'status':'success'})
        else:
            return JsonResponse({'status':'error'})

# account functions
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
    return render(request, 'login.html', {'form': form})

def admin_logout(request):
    logout(request)
    return redirect('login')

#INDEX PAGE
@login_required(login_url='login')
def index(request):
    username = request.user.username
    return render(request, 'index.html', {'username': username})

#USERS PAGE
@login_required(login_url='login')
def all_users(request):
    users_with_user_role = User.objects.filter(profile__role='user')

    # You can then pass this queryset to your template
    context = {
        'users': users_with_user_role
    }
    return render(request, 'users/index.html',context)

def generate_random_username():
    return 'user_' + ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))

def generate_random_password(length=10):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for i in range(length))

@login_required(login_url='login')
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
            #subject = 'Your account has been created'
            #html_message = render_to_string('users/email.html', {'username': user.username, 'password': random_password})
            #plain_message = strip_tags(html_message)
            #from_email = 'urmish.cyblance@gmail.com'  # Change this to your email address
            #to_email = user.email

            #send_mail(subject, plain_message, from_email, [to_email], html_message=html_message)

            messages.success(request, 'User created successfully and email sent')
            return redirect('allusers')
        else:
            print("Form errors:", form.errors.as_json())
            return render(request, 'users/create.html', {'form': form})
    else:
        form = SignUpForm()
    return render(request, 'users/create.html', {'form': form})


@login_required(login_url='login')
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

    return render(request, 'users/edit.html', {'form': form, 'user': user, 'profile': profile})

@login_required(login_url='login')
def delete_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        user.delete()
        messages.success(request, 'User deleted successfully')
        return redirect('allusers')  # Redirect to the user list page
    else:
        messages.error(request, 'Somthing went wrong')
        return redirect('allusers')

@login_required(login_url='login')
def my_profile(request):
    user = request.user  # Get the current user object
    try:
        profile = user.profile  # Try to get the user's profile
    except Profile.DoesNotExist:
        profile = None  # If the profile doesn't exist, set it to None

    if request.method == 'POST':
        form = UserAndProfileForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            # Update User model fields
            user.email = form.cleaned_data['email']
            user.first_name = form.cleaned_data['first_name']
            user.last_name = form.cleaned_data['last_name']

            if not profile:
                # If the profile doesn't exist, create it
                profile = Profile(user=user)

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

            messages.success(request, 'Your profile has been updated successfully.')
            return redirect('myprofile')  # Redirect to the user's profile page
        else:
            messages.error(request, 'There was an error updating your profile. Please check the form.')
    else:
        form = UserAndProfileForm(instance=user)
        profile = Profile.objects.get(user=request.user)

    return render(request, 'my-profile.html', {'form': form, 'profile': profile})

def forget_password(request):
    if request.method == 'POST':
        form = ForgotPasswordForm(request.POST)
        if form.is_valid():
            UserModel = get_user_model()
            email = form.cleaned_data['email']
            users = UserModel.objects.filter(email=email)
            if users.exists():
                for user in users:
                    uid = urlsafe_base64_encode(force_bytes(user.pk))
                    token = default_token_generator.make_token(user)
                    reset_link = request.build_absolute_uri(reverse('password-reset-confirm', args=[uid, token]))
                    subject = 'Password Reset Request'
                    message = render_to_string('password-reset-email-template.html', {
                        'email': user.email,
                        'fullname': user.first_name+' '+user.last_name,
                        'reset_link': reset_link,
                        'protocol': request.scheme,
                        'domain': request.get_host(),
                        'uid': uid,  # Pass uid to the template context
                        'token': token,  # Pass token to the template context
                    })
                    return HttpResponse(message)

            #send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user.email], html_message=message)
            #return redirect('password_reset_done')  # Redirect to the 'password_reset_done' view
            else:
                error_message = "No user found with the provided email address."
                return render(request, 'forget-password.html', {'form': form, 'error_message': error_message})
    else:
        form = ForgotPasswordForm()
    return render(request, 'forget-password.html', {'form': form})