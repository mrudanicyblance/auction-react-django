from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.admin_login, name='login'),
    path('index/', views.index, name='index'),
    path('logout/', views.admin_logout, name='logout'),
]