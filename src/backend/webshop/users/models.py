from django.db import models
from django.contrib.auth.models import AbstractUser

from ckeditor.fields import RichTextField


class UserRBACRole(models.Model):
    """
    Class for user role level access
    """

    ROLES = (
        ("COMPANY_ADMINISTRATOR", "COMPANY_ADMINISTRATOR"),
        ("INVENTORY_MANAGER", "INVENTORY_MANAGER"),
        ("BUYER", "BUYER"),
    )

    role = models.CharField(max_length=100, choices=ROLES, default="BUYER")
    role_description = RichTextField()

    def __str__(self):
        return self.role

    class Meta:
        verbose_name = "Role"
        verbose_name_plural = "Roles"


class User(AbstractUser):
    avatar = models.ImageField(upload_to="images", null=True, default=None, blank=True)
    online = models.BooleanField(default=False)
    role = models.ForeignKey(
        UserRBACRole, on_delete=models.CASCADE, null=True, blank=True
    )
