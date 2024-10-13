from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Profile
from django.utils.html import format_html


class ProfileAdmin(UserAdmin):
    """
    Admin interface for the Profile model, extending the default UserAdmin
    to include custom fields and functionality.
    """

    # Specify the model this admin interface is for
    model = Profile
    # Fields to display in the admin list view
    list_display = (
        'thumbnail',
        'email',
        'first_name',
        'last_name',
        'last_login',
        'date_joined',
        'is_admin',
        'is_staff',
        'is_active',
        'is_inactive'
    )

    # Fields that are clickable links in the list view
    list_display_links = ('thumbnail', 'email',)
    # Fields that are read-only in the admin interface
    readonly_fields = ('last_login', 'date_joined',)
    # Define the ordering of the list view
    ordering = ('-date_joined',)


    # Define the fieldsets for the admin form layout
    fieldsets = (
        # Default fields
        (None, {'fields': ('email', 'password')}),
        # Personal info fields
        ('Personal Info', {'fields': ('first_name', 'last_name', 'profile_picture')}),
        # Permission fields
        ('Permissions', {'fields': ('is_admin', 'is_staff', 'is_active', 'is_inactive', 'is_published')}),
    )

    # Horizontal filters (none)
    filter_horizontal = ()
    # List of filters for the admin list view (none)
    list_filter = ()


    def thumbnail(self, obj):
        """
        User Profile Picture visible as a thumbnail in the admin interface
        """

        # If user have a profile picture, return the picture in the style - row 60
        if obj.profile_picture:
            return format_html('<img src="{}" width="50" style="border-radius: 50%;" />'.format(obj.profile_picture.url))
        # If not, show none
        else:
            return None

    # Column for the thumbnails in the admin interface
    thumbnail.short_description = 'Profile Picture'

# Register the Profile model with the custom ProfileAdmin interface
admin.site.register(Profile, ProfileAdmin)
