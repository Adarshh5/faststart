from django.db import models


from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from django.db import models

class UserManager(BaseUserManager):
    """Custom manager for the user model."""

    def create_user(self, email, password=None, **extra_fields):
        """Create and return a regular user with the given email and password."""
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        # user.set_password(password)
        if password:
            user.set_password(password)
        else:
            user.set_unusable_password()  # 👈 this is perfect for Google login users

        user.is_active = True
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """Create and return a superuser with the given email and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        user = self.create_user(email, password, **extra_fields)
        user.is_active = False  # Superuser must also be activated manually
        user.save(using=self._db)
        return user

class User(AbstractBaseUser):
    """Custom user model where email is the unique identifier."""
    email = models.EmailField(unique=True, max_length=255)

    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    created_at  = models.DateTimeField(auto_now_add=True)  # Added tracking
    updated_at = models.DateTimeField(auto_now=True) 


    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = [] 

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        """Does the user have a specific permission?"""
        return self.is_superuser  # Only superusers have all permissions
    def has_module_perms(self, app_label):
        """Does the user have permissions to view the app `app_label`?"""
        return self.is_superuser 
    




class UserAgreement(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    agreed = models.BooleanField(default=False)
    agreed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.email} agreed at {self.agreed_at}"