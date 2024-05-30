from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
# main user class defined
class auctionUser(AbstractUser):
    dob = models.DateField(null=True, blank=True)
    mobile_number = models.CharField(max_length=15, blank=True)
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('buyer', 'Buyer'),
        ('seller', 'Seller')
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='user')

    # constraints to make a user unique
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['email'], name='unique_email_constraint'),
            models.UniqueConstraint(fields=['username'], name='unique_username_constraint'),
        ]

    # groups and permissions are the needed fields of a user in django
    # this creates custom auction user group and permission table
    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name='groups',
        blank=True,
        related_name='auction_users_groups'
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name='user permissions',
        blank=True,
        related_name='auction_users_permissions'
    )

    # what will this class return on call.
    def __str__(self):
        return self.username