from django.urls import path
from . import views as v

# url defined for accounts and user based functionality.
urlpatterns = [
    path('',v.loginaccounts,name="login_account"),
    path('sign-up/',v.signupaccounts,name='signup_account'),
    path('logout/',v.logout_view,name='logout_account')
]