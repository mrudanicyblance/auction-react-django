from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from .models import Profile

class EmailAuthenticationForm(AuthenticationForm):
    username = forms.EmailField(label='Email', max_length=254, required=True)

class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True, help_text='Required.')
    last_name = forms.CharField(max_length=30, required=True, help_text='Required.')
    email = forms.EmailField(max_length=254, required=True, help_text='Required. Enter a valid email address.')
    phone_no = forms.CharField(max_length=15, required=True)
    address_line_1 = forms.CharField(max_length=255, required=True)
    address_line_2 = forms.CharField(max_length=255, required=False)  # changed to required=True
    country = forms.CharField(max_length=100, required=True)
    state = forms.CharField(max_length=100, required=True)
    city = forms.CharField(max_length=100, required=True)
    zipcode = forms.CharField(max_length=10, required=True)
    photo = forms.ImageField(required=True)
    role = forms.CharField(max_length=50, required=True, initial='user', widget=forms.TextInput(attrs={'readonly': 'readonly'}))

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', 'first_name', 'last_name', 'phone_no', 'address_line_1', 'address_line_2', 'country', 'state', 'city', 'zipcode', 'photo')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("This email is already registered.")
        return email

    def save(self, commit=True):
        user = super(SignUpForm, self).save(commit=False)
        if commit:
            user.save()
            Profile.objects.create(
                user=user,
                phone_no=self.cleaned_data['phone_no'],
                address_line_1=self.cleaned_data['address_line_1'],
                address_line_2=self.cleaned_data['address_line_2'],
                country=self.cleaned_data['country'],
                state=self.cleaned_data['state'],
                city=self.cleaned_data['city'],
                zipcode=self.cleaned_data['zipcode'],
                role=self.cleaned_data['role'],
                photo=self.cleaned_data['photo']
            )
        return user

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('phone_no', 'address_line_1', 'address_line_2', 'country', 'state', 'city', 'zipcode', 'photo')

    def __init__(self, *args, **kwargs):
        super(UserProfileForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.required = True

class UserUpdateForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name')

    def __init__(self, *args, **kwargs):
        super(UserUpdateForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.required = True
