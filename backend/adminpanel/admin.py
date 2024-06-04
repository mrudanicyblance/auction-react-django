from django.contrib import admin
from .models import Category, SubCategory, Profile, Field, SubCategoryField, SubCategoryOptionField

# Register your models here.
admin.site.register(Category)
admin.site.register(SubCategory)
admin.site.register(Profile)
admin.site.register(Field)
admin.site.register(SubCategoryField)
admin.site.register(SubCategoryOptionField)