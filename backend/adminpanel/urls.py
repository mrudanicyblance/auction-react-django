from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('login/', views.admin_login, name='login'),
    path('logout/', views.admin_logout, name='logout'),
    path('index/', views.index, name='index'),
    path('myprofile/', views.my_profile, name='myprofile'),
    path('forget-password/', views.forget_password, name='forget-password'),

    #USERS URL
    path('superadmin/users/', views.all_users, name='allusers'),
    path('superadmin/users/create', views.create_users, name='createusers'),
    path('superadmin/users/edit/<int:user_id>/', views.edit_user, name='editusers'),
    path('superadmin/users/delete/<int:user_id>/', views.delete_user, name='deleteuser'),

    # category subcategory urls
    path('categories/', views.view_category, name='view_category'),
    path('categories/add/', views.add_category, name='add_category'),
    path('subcategories/add/', views.add_subcategory, name='add_subcategory'),
    path('categories/delete/',views.delete_category, name='delete_category'),
    path('categories/update/',views.update_category, name='update_category'),

    # field urls
    path('fields/',views.view_fields,name="view_fields"),
    path('field/add/',views.add_field,name="add_field"),
    path('field/edit/',views.edit_field,name="edit_field"),
    path('field/delete/',views.delete_field,name="delete_field"),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)