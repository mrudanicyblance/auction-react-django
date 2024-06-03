from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.admin_login, name='login'),
    path('logout/', views.admin_logout, name='logout'),
    path('index/', views.index, name='index'),

    #USERS URL
    path('supadmin/users/', views.all_users, name='allusers'),
    path('supadmin/users/create', views.create_users, name='createusers'),
    path('supadmin/users/edit', views.edit_users, name='editusers'),
]