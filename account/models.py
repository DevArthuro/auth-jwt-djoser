from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
from django.utils.translation import gettext_lazy as _

class UserManage(BaseUserManager):
    def create_user(self, email, name, password, **extra_fields):
        if not email: 
            raise ValueError(_('The Email field must be set'))
        
        if not name:
            raise ValueError(_('The Name field is to required'))
        
        email = self.normalize_email(email)
        user: User = self.model(email = email, name = name, **extra_fields)
        user.set_password(password)
        user.save()
        
        return user
    
    def create_superuser(self, email, name, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_superuser', True)
        
        return self.create_user(email, name, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_('email address'), max_length=250, unique=True)
    name: str = models.CharField(_('name'), max_length=250)
    
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']
    
    objects = UserManage()
    
    def __str__(self) -> str:
        return str(self.name)