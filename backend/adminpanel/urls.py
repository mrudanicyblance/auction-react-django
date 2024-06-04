from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.admin_login, name='login'),
    path('index/', views.index, name='index'),
    path('logout/', views.admin_logout, name='logout'),
    path('categories/', views.view_category, name='view_category'),
    path('categories/add/', views.add_category, name='add_category'),
    path('subcategories/add/', views.add_subcategory, name='add_subcategory'),
    path('categories/delete/',views.delete_category, name='delete_category'),
    path('categories/update/',views.update_category, name='update_category'),
    path('view_fields/',views.view_fields,name="view_fields")
]