from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin, UserManager
from django.db import models
from django.utils.translation import gettext_lazy as _
from ..dependencies import Project
from ..choices import UserPositions


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(_("username"), max_length=50, unique=True)
    first_name = models.CharField(_("first name"), max_length=40)
    last_name = models.CharField(_("last name"), max_length=40)
    email = models.EmailField(_("email address"), max_length=150, unique=True)
    phone = models.CharField(max_length=75, null=True, blank=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)
    deleted = models.BooleanField(default=False)
    position = models.CharField(max_length=15, choices=UserPositions.choices, default=UserPositions.PROGRAMMER)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="users", null=True, blank=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username", "first_name", "last_name", "position"]

    objects = UserManager()

    def __str__(self):
        return f"{self.last_name} {self.first_name}"
