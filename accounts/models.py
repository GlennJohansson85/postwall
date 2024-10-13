from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


class ProfileManager(BaseUserManager):
    """
    Custom manager for the Profile model, extending the default UserManager
    to provide methods for creating user and superuser accounts.
    """

    def create_user(self, username, first_name, last_name, email, password=None, **extra_fields):
        """
        Creates and saves a regular user with the given
        username, first name, last name, email, and password.
        """

        # If an email address is provided;if not, raise an error
        if not email:
            raise ValueError('Email is required')

        # Normalize the email to ensure it is in a consistent format
        email = self.normalize_email(email)
        # Create a new user instance with the data below
        user = self.model(
            username = username,
            email  = email,
            first_name = first_name,
            last_name = last_name,
            **extra_fields
        )
        # Hash the user's password for security before saving
        user.set_password(password)
        # Save the user instance to the database
        user.save(using=self._db)
        # Return the newly created user instance
        return user


    def create_superuser(self, username, first_name, last_name, email, password=None, **extra_fields):
        """
        Creates and saves a superuser with the given username, first name,
        last name, email, and password, ensuring specific permissions are set.
        """

        # Set default values for superuser-specific fields
        extra_fields.setdefault('is_admin', True)
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_active', True)

        # Check if the "is_admin", "is_staff" fields is set to True; raise an error if not
        if extra_fields.get('is_admin') is not True:
            raise ValueError('Superuser must have is_admin=True.')

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')

        # Call the create_user method to create the superuser
        return self.create_user(username, first_name, last_name, email, password, **extra_fields)


class Profile(AbstractBaseUser):
    """
    Custom user model that extends AbstractBaseUser to create a user profile
    with specific fields and behavior for authentication.
    """

    username          = models.CharField(max_length=50, unique=True)
    first_name        = models.CharField(max_length=50)
    last_name         = models.CharField(max_length=50)
    email             = models.EmailField(max_length=100, unique=True)
    profile_picture   = models.ImageField(blank=True, upload_to='profile/')
    date_joined       = models.DateTimeField(auto_now_add=True)
    last_login        = models.DateTimeField(auto_now=True)
    is_admin          = models.BooleanField(default=False)
    is_staff          = models.BooleanField(default=True)
    is_active         = models.BooleanField(default=True)
    is_inactive       = models.BooleanField(default=True)
    is_published      = models.BooleanField(default=True)

    # Specifies the field used for user login (email instead of username)
    USERNAME_FIELD    = 'email'
    # Required fields when creating a user
    REQUIRED_FIELDS   = ['username', 'first_name', 'last_name']

    # Custom manager for the Profile model
    objects = ProfileManager()

    def full_name(self):
        """
        Returns the full name of the user by combining first and last names.
        """
        return f'{self.first_name} {self.last_name}'

    def __str__(self):
        """
        String representation of the Profile instance, returning the email.
        """
        return self.email

    def has_perm(self, perm, obj=None):
        """
        Returns whether the user has a specific permission. If admin = Returns True
        """
        return self.is_admin

    def has_module_perms(self, add_label):
        """
        Returns whether the user has permissions for a given module.
        Returns True for all modules
        """
        return True
