# adminpanel/models.py
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    phone_no = models.CharField(max_length=15, blank=True, null=True)
    address_line_1 = models.CharField(max_length=255, blank=True, null=True)
    address_line_2 = models.CharField(max_length=255, blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)
    state = models.CharField(max_length=100, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    zipcode = models.CharField(max_length=10, blank=True, null=True)
    role = models.CharField(max_length=50, blank=True, null=True)
    photo = models.ImageField(upload_to='profile_photos/', blank=True, null=True)

    def __str__(self):
        return self.user.username

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    if hasattr(instance, 'profile'):
        instance.profile.save()

# category models
class Category(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class SubCategory(models.Model):
    category = models.ForeignKey(Category, related_name='subcategories', on_delete=models.CASCADE)
    subcat_name = models.CharField(max_length=255)

    def __str__(self):
        return self.subcat_name

class Field(models.Model):
    field_name = models.CharField(max_length=255)
    field_type = models.CharField(max_length=50)

    def __str__(self):
        return self.field_name

class SubCategoryField(models.Model):
    subcategory = models.ForeignKey(SubCategory, on_delete=models.CASCADE)
    field = models.ForeignKey(Field, on_delete=models.CASCADE)

    class Meta:
        unique_together = (('subcategory', 'field'),)

    def __str__(self):
        return f"{self.subcategory.subcat_name} - {self.field.field_name}"

class SubCategoryOptionField(models.Model):
    subcategory_field = models.ForeignKey(SubCategoryField, on_delete=models.CASCADE)
    option_value = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.subcategory_field.field.field_name} - {self.option_value}"