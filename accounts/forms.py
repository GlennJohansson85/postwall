from django import forms
from .models import Profile


class RegistrationForm(forms.ModelForm):
    """
    For user registration, allowing users to enter their details and set a password.
    Includes fields for username, first name, last name, email, password, and password confirmation.
    Custom validation ensures the two passwords match.
    """

    # Define the password field with a password input widget
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Choose a strong password',
        'class': 'form-control',
    }))

    # Define the confirm password field with a password input widget
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Same as you just created'
    }))

    class Meta:
        # Specify the model to use
        model  = Profile
        # Define the fields to include in the form
        fields = ['username', 'first_name', 'last_name', 'email', 'password']

    def clean(self):
        """
        Custom validation method to ensure the password and confirm password fields match.
        Raises a ValidationError if they do not.
        """

        # Call the parent clean method
        cleaned_data = super(RegistrationForm, self).clean()
        # Get the password value
        password = cleaned_data.get('password')
        # Get the confirm password value
        confirm_password = cleaned_data.get('confirm_password')

        # If passwords match - confirm
        if password != confirm_password:
            # If not - raise validation error
            raise forms.ValidationError(
                # Error message
                "Passwords do not match."
            )

    def __init__(self, *args, **kwargs):
        """
        Initializes the Form with custom attributes for form fields.

        This method is called when an instance of RegistrationForm is created.
        It allows us to set initial attributes such as placeholder text and CSS classes for each field.
        """

        # Call the parent class's __init__ method to ensure that the form is properly initialized
        super(RegistrationForm, self).__init__(*args, **kwargs)

        # Set placeholder text for the fields to guide the user
        self.fields['username'].widget.attrs['placeholder'] = 'Hoffmeister'
        self.fields['first_name'].widget.attrs['placeholder'] = 'David'
        self.fields['last_name'].widget.attrs['placeholder'] = 'Hasselhoff'
        self.fields['email'].widget.attrs['placeholder'] = 'David.Hasselhoff@hotmail.com'

        # Loop through all fields in the form to add a CSS class for styling
        for field in self.fields:
            # Add the 'form-control' class to each field to apply Bootstrap styling
            self.fields[field].widget.attrs['class'] = 'form-control'


class UserForm(forms.ModelForm):
    """
    For updating user profile information incl. first name, last name, email, username and profile picture.
    """

    class Meta:
        # Specify the model that the form is associated with
        model = Profile
        # Define the fields that will be included in the form
        fields = ['first_name', 'last_name', 'email', 'username', 'profile_picture']
