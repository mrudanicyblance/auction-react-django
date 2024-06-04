from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponseBadRequest
from django.contrib import messages
from .forms import EmailAuthenticationForm, SignUpForm, UserAndProfileForm  # Import the custom form
from django.contrib.auth.models import User
from .models import Profile, Category, SubCategory, Field, SubCategoryField, SubCategoryOptionField
import random
import string
from django.contrib import messages

# fields functions
def view_fields(request):
    fields = Field.objects.all()
    context = {'fields':fields}
    return render(request,'categories/view_fields.html',context=context)

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
        return JsonResponse({'status':'success'})
    except Exception as e:
        return JsonResponse({'status':'error','message':str(e)})

@require_POST
@csrf_exempt
def delete_field(request):
    try:
        field_id = request.POST.get('id')
        field = Category.objects.get(id=field_id)
        field.delete()
        return JsonResponse({'status':'success'})
    except:
        return JsonResponse({'status':'error'})

# category functions
def view_category(request):
    categories = Category.objects.all()
    context = {'categories':categories}
    return render(request,'categories/view_category.html',context=context)

def add_category(request):
    if request.method == 'POST':
        try:
            print('add_reached')
            name = request.POST.get('name')
            if not name:
                return HttpResponseBadRequest("Name is required")

            category = Category.objects.create(name=name)
            return JsonResponse({'id': category.id, 'name': category.name})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
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
def my_profile (request):
    return render(request, 'my-profile.html')

def forget_password (request):
    return render(request, 'forget-password.html')