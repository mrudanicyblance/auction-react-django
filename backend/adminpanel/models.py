from django.db import models

# Create your models here.
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