from django.contrib.auth.models import BaseUserManager, AbstractBaseUser,PermissionsMixin
from django.contrib.auth.password_validation import MinimumLengthValidator, CommonPasswordValidator, NumericPasswordValidator
from django.utils.translation import gettext_lazy as _
from django.core.validators import EmailValidator
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.db import models

class CustomUserManager(BaseUserManager):
    def validate_password(self, password, user=None):
        MinimumLengthValidator(10).validate(password, user)
        NumericPasswordValidator().validate(password, user)
        CommonPasswordValidator().validate(password, user)
        if not any(char.isupper() for char in password):
            raise ValidationError('Password must contain at least one uppercase letter.')

    def create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError(_("The Email must be set"))
        self.validate_password(password)

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError(_("Superuser must have is_staff=True."))
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(_("Superuser must have is_superuser=True."))
        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    """Represents a custom user model."""
    email = models.EmailField(unique=True,validators=[EmailValidator()])    
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)  
    roles = models.ManyToManyField('Role')  

    objects = CustomUserManager()

    USERNAME_FIELD  = 'email'
    REQUIRED_FIELDS = []    

    def __str__(self):
        return self.email


class Role(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField()
    permissions = models.ManyToManyField('auth.Permission')

    def __str__(self):
        return self.name

class UserRole(models.Model):    
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    role = models.ManyToManyField("Role")

    def __str__(self):
        return f"{self.user} - {self.role}"


class AuditLog(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True)
    action = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} - {self.action} - {self.timestamp}"


