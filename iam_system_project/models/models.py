from django.contrib.auth.models import BaseUserManager, AbstractBaseUser,PermissionsMixin
from django.contrib.auth.password_validation import MinimumLengthValidator, CommonPasswordValidator, NumericPasswordValidator
from django.utils.translation import gettext_lazy as _
from django.core.validators import EmailValidator
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.db import models

def contains_uppercase_letter(password):
        for char in password:
            if char.isupper():  return True
        return False       

class CustomUserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifiers
    for authentication instead of usernames.
    """
    def validate_password(self, password, user=None):
        """
        Custom password validation based on specified criteria.
        """        
        # Minimum length of 10 characters
        MinimumLengthValidator(10).validate(password, user)

        # Include numbers, special characters, and uppercase letters        
        NumericPasswordValidator().validate(password, user) 
        CommonPasswordValidator().validate(password, user)

        # Password must contain at least one uppercase letter
        if not contains_uppercase_letter(password):
            raise ValidationError('Password must contain at least one uppercase letter.')          

    def create_user(self, email, password, **extra_fields):
        """
        Create and save a user with the given email and password.
        """       

        if not email: raise ValueError(_("The Email must be set"))
        self.validate_password(password)

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
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

    objects = CustomUserManager()

    USERNAME_FIELD  = 'email'
    REQUIRED_FIELDS = []    

    def __str__(self):
        return self.email

    # Add these lines to resolve the clash
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='customuser_set',
        related_query_name='customuser',
        blank=True,
        verbose_name='groups',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='customuser_set',
        related_query_name='customuser',
        blank=True,
        verbose_name='user permissions',
        help_text='Specific permissions for this user.',
    )    


# class Role(models.Model):
#     "Represents a user role."
#     name = models.CharField(max_length=255, unique=True)
#     description = models.TextField()

#     def __str__(self):
#         return self.name

# class UserRole(models.Model):
#     """Represents the relationship between users and roles."""
#     user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
#     role = models.ForeignKey(Role, on_delete=models.CASCADE)

#     def __str__(self):
#         return f"{self.user} - {self.role}"


# class Permission(models.Model):
#     name = models.CharField(max_length=255, unique=True)
#     codename = models.CharField(max_length=255, unique=True)
#     description = models.TextField()

#     def __str__(self):
#         return self.name


# class AuditLog(models.Model):
#     user = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True)
#     action = models.CharField(max_length=255)
#     timestamp = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return f"{self.user} - {self.action} - {self.timestamp}"

# class Session(models.Model):
#     user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
#     session_key = models.CharField(max_length=40, primary_key=True)
#     expire_date = models.DateTimeField()

#     def __str__(self):
#         return f"{self.user} - {self.session_key}"


