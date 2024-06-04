from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, JsonResponse, HttpResponseBadRequest
from django.contrib import messages
from .forms import EmailAuthenticationForm  # Import the custom form
from .models import Category, SubCategory

# fields functions
def view_fields(request):
    return render(request,'cforms/view_fields.html')

# category functions
def view_category(request):
    categories = Category.objects.all()
    context = {'categories':categories}
    return render(request,'cforms/view_category.html',context=context)

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
        category.delete()  # This will also delete subcategories due to on_delete=models.CASCADE
        return JsonResponse({'status': 'success'})
    except Category.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Category does not exist'})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)})

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
#For Admin Login
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
    return render(request, 'adminpanel/users/edit.html', {
        #'user_form': user_form,
        #'profile_form': profile_form
    })