from django import forms
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from . import models
from django.contrib.auth import get_user_model,authenticate

# user sign up form.
class AuctionUserCreationForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text='Required. Enter a valid email address.')
    class Meta:
        model = models.auctionUser
        fields = ['username', 'first_name', 'last_name', 'email', 'dob', 'role','mobile_number', 'password1', 'password2']

# user login form.
class AuctionUserAuthenticationForm(AuthenticationForm):
    def get_user(self):
        return self.user_cache

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if username and password:
            self.user_cache = authenticate(username=username, password=password)
            if self.user_cache is None:
                raise forms.ValidationError("Invalid username or password.")
            else:
                self.confirm_login_allowed(self.user_cache)

        return self.cleaned_data

    class Meta:
        model = models.auctionUser
        fields = ['username', 'password']