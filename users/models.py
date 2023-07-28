from typing import Any

from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.hashers import make_password
from django.db import models
from django.contrib.auth.models import AbstractUser, PermissionsMixin, User as BaseUser


class CustomUserManager(BaseUserManager):
    def _create_user(self, email, password, **extra_fields):  # type: ignore
        """Create and save a user with the given email and password."""
        if not email:
            raise ValueError("Please provide an email!")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.password = make_password(password)
        user.save(using=self._db)
        return user

    def create_user(
        self,
        email: Any,
        password: Any = None,
        **extra_fields: Any,
    ) -> BaseUser:
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(
        self,
        email: Any,
        password: Any = None,
        **extra_fields: Any,
    ) -> BaseUser:
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True, verbose_name="Email")
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    first_name = models.CharField(max_length=20, null=True, blank=True)
    last_name = models.CharField(max_length=20, null=True, blank=True)
    avatar = models.ImageField(upload_to="profile_images", null=True, blank=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
    objects = CustomUserManager()

    @property
    def is_complete(self) -> bool:
        return bool(self.first_name) and bool(self.last_name)

    def __str__(self) -> str:
        if self.is_complete:
            return f"{self.first_name} {self.last_name}"
        return f"{self.email}"
