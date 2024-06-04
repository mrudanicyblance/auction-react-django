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
    path('supadmin/users/', views.all_users, name='allusers'),
    path('supadmin/users/create', views.create_users, name='createusers'),
    path('supadmin/users/edit/<int:user_id>/', views.edit_user, name='editusers'),
    path('supadmin/users/delete/<int:user_id>/', views.delete_user, name='deleteuser'),

    # Categories & Subcategories URL
    path('categories/', views.view_category, name='categories'),
    path('categories/add/', views.add_category, name='createcategories'),
    path('subcategories/add/', views.add_subcategory, name='createsubcategory'),
    path('categories/delete/',views.delete_category, name='deletecategory'),
    path('categories/edit/',views.update_category, name='updatecategory'),

    # Field urls
    path('fields/',views.view_fields,name="fields"),
    path('field/add/',views.add_field,name="createfield"),
    path('field/edit/',views.edit_field,name="editfield"),
    path('field/delete/',views.delete_field,name="deletefield"),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)