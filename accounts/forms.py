from django import forms
from .models import Profile


class RegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Choose a strong password',
        'class': 'form-control',
    }))
    
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Same as you just created'
    }))
    class Meta:
        model  = Profile
        fields = ['username', 'first_name', 'last_name', 'email', 'password']
    
    def clean(self):
        cleaned_data = super(RegistrationForm, self).clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        if password != confirm_password:
            raise forms.ValidationError(
                "Passwords do not match."
            )
    
    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['placeholder'] = 'Hoffmeister'
        self.fields['first_name'].widget.attrs['placeholder'] = 'David'
        self.fields['last_name'].widget.attrs['placeholder'] = 'Hasselhoff'
        self.fields['email'].widget.attrs['placeholder'] = 'David.Hasselhoff@hotmail.com'
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'

class UserForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['first_name', 'last_name', 'email', 'username', 'profile_picture']

