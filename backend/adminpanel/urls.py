from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views


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

    # Categories & Subcategories URL
    path('categories/', views.view_category, name='categories'),
    path('categories/add/', views.add_category, name='createcategories'),
    path('categories/delete/',views.delete_category, name='deletecategory'),
    path('categories/edit/',views.update_category, name='updatecategory'),
    path('subcategories/add/', views.add_subcategory, name='createsubcategory'),
    path('subcategories/<int:id>/',views.view_subcategory,name="subcategories"),

    # Subcategory & Fields link
    path('subcategories/link-create/',views.link_subcat_field,name='link_subfields'),
    path('subcategories/link-delete/',views.delete_link, name="delete_link"),

    # Field urls
    path('fields/',views.view_fields,name="fields"),
    path('field/add/',views.add_field,name="add_field"),
    path('field/edit/',views.edit_field,name="edit_field"),
    path('field/delete/',views.delete_field,name="delete_field"),
    path('field-option/<int:field_id>/', views.field_option_view, name='field-option'),
    path('field-option/<int:field_id>/add-option/', views.add_option, name='add-option'),
    path('field-option/update-option/', views.update_option, name='update-option'),
    path('field-option/delete-option/', views.delete_option, name='delete-option'),


    path('reset-password/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('reset-password/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="password-reset-confirm.html"), name='password-reset-confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)