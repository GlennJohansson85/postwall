from django.apps import AppConfig


class AccountsConfig(AppConfig):
    """
    Configuration class for the Accounts application.

    Defines the name of the application and specifies 
    the default field type for primary keys in models.
    """

    # Specify the default auto field type for model primary keys
    default_auto_field = 'django.db.models.BigAutoField'
     # Define the name of the application
    name = 'accounts'
