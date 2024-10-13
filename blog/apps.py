from django.apps import AppConfig


class BlogConfig(AppConfig):
    """
    Configuration for the Blog application.
    This class holds the configuration for the Blog app,
    including the default auto field type.
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'blog'
