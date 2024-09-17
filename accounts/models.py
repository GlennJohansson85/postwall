
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

class ProfileManager(BaseUserManager):
      def create_user(self, username, first_name, last_name, email, password=None, **extra_fields):
            if not email:
                  raise ValueError('Email is required')
            
            email = self.normalize_email(email)
            user = self.model(
                  username=username,
                  email=email,
                  first_name=first_name,
                  last_name=last_name,
                  **extra_fields
            )
            user.set_password(password)
            user.save(using=self._db)
            return user
      
      def create_superuser(self, username, first_name, last_name, email, password=None, **extra_fields):
            extra_fields.setdefault('is_admin', True)
            extra_fields.setdefault('is_staff', True)
            extra_fields.setdefault('is_active', True)
            
            if extra_fields.get('is_admin') is not True:
                  raise ValueError('Superuser must have is_admin=True.')
            
            if extra_fields.get('is_staff') is not True:
                  raise ValueError('Superuser must have is_staff=True.')
            
            return self.create_user(username, first_name, last_name, email, password, **extra_fields)


class Profile(AbstractBaseUser):
      username          = models.CharField(max_length=50, unique=True)
      first_name        = models.CharField(max_length=50)
      last_name         = models.CharField(max_length=50)
      email             = models.EmailField(max_length=100, unique=True)
      profile_picture   = models.ImageField(blank=True, upload_to='profile/')
      date_joined       = models.DateTimeField(auto_now_add=True)
      last_login        = models.DateTimeField(auto_now_add=True)
      is_admin          = models.BooleanField(default=False)
      is_staff          = models.BooleanField(default=True)
      is_active         = models.BooleanField(default=True)
      is_inactive       = models.BooleanField(default=False)
      is_published      = models.BooleanField(default=True)
      
      # Login with email
      USERNAME_FIELD    = 'email'
      REQUIRED_FIELDS   = ['username', 'first_name', 'last_name']
      
      objects = ProfileManager()
      
      def full_name(self):
            return f'{self.first_name} {self.last_name}'
      
      def __str__(self):
            return self.email
      
      def has_perm(self, perm, obj=None):
            return self.is_admin
      
      def has_module_perms(self, add_label):
            return True