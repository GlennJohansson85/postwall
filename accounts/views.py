from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages, auth
from django.core.mail import EmailMessage, send_mail
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.decorators import login_required

import requests

from .forms import RegistrationForm, UserForm
from .models import Profile


def register(request):
    """
    Handles user registration. If the request method is POST, it processes the form data,
    creates a new user, and sends an account activation email. On successful registration,
    redirects the user to the login page.
    """

    # If request method is POST
    if request.method == 'POST':
        # Instantiate the RegistrationForm with the submitted data
        form = RegistrationForm(request.POST)

        # If form data is valid
        if form.is_valid():
            # Extract cleaned data from the form
            email       = form.cleaned_data['email']
            username    = email.split("@")[0] # Use the part before '@' in the email as the username
            password    = form.cleaned_data['password']
            first_name  = form.cleaned_data['first_name']
            last_name   = form.cleaned_data['last_name']

            # Create user by data input
            user = Profile.objects.create_user(
                email       = email,
                username    = username,
                password    = password,
                first_name  = first_name,
                last_name   = last_name,
            )
            # Save the user instance to the database
            user.save()

            # Get the current site instance for the activation link
            current_site = get_current_site(request)
            mail_subject = 'Postwall - Account Activation'

            # Render the activation email template with context
            message = render_to_string('verification_email.html', {
                'user': user,
                # Domain for the activation link
                'domain': current_site,
                # Encode user ID
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                # Generate activation token
                'token': default_token_generator.make_token(user),
            })
            # Set the recipient email
            to_email = email

            # Create EmailMessage instance to send the activation email
            send_email = EmailMessage(
                mail_subject,
                message,
                # Sender's email
                from_email='Postwall <glenncoding@gmail.com>',
                # Recipient's email
                to=[to_email]
            )

            # Specify the content type as HTML
            send_email.content_subtype = "html"
            # Send the email
            send_email.send()
            # Display a success message to the user
            messages.success(request, 'Activation link sent to your email')

            # Redirect the user to the login page after successful registration
            return redirect('/accounts/login/')

    # if registstration is not successful
    else:
        # instantiate an empty RegistrationForm
        form = RegistrationForm()

    # Prepare context for rendering the registration template
    context = {
        # Pass the form to the template
        'form': form,
    }

    # Render the registration template with the context
    return render(request, 'register.html', context)


def login(request):
    """
    Handles user login by checking the provided email and password against the database.
    If the credentials are valid, logs the user in and redirects to the postwall page.
    If invalid, an error message is shown and the user is redirected to the login page.
    """

    # If the request method is POST (i.e., the form has been submitted)
    if request.method == "POST":
        # Retrieve the email from the POST request data
        email = request.POST['email']
        # Retrieve the password from the POST request data
        password = request.POST['password']
        # Authenticate the user using the provided email and password
        user = auth.authenticate(email=email, password=password)

        # If the authentication was successful
        if user is not None:
            # Log the user into the session
            auth.login(request, user)
            # Display a success message for login
            messages.success(request, 'Login Successful!')
            # Redirect to the postwall page after successful login
            return redirect('postwall')

        # If the authentication was unsuccessful
        else:
            # Show an error message for invalid credentials
            messages.error(request, 'Invalid Login Credentials.')
            # Redirect back to the login page if credentials are invalid
            return redirect('login')

    # Render the login page for GET requests (when the form is first displayed)
    return render(request, 'login.html')


@login_required(login_url = 'login')
def logout(request):
    """
    Logs the user out if they are authenticated and redirects them to the login page.
    A success message is displayed after logout.
    """

    # Log the user out of the session
    auth.logout(request)
    # Display a success message for logout
    messages.success(request, 'Loggout Successful!')
    # Redirect to the login page after logging out
    return redirect('login')


def activate(request, uidb64, token):
    """
    Activates a user account based on the provided unique user ID (uid) and token.
    Decodes the uid, retrieves the user, and verifies the token. If valid, the user's
    account is activated and they are redirected to the login page. If invalid, an
    error message is shown and the user is redirected to the registration page.
    """

    try:
        # Decode the user ID from the base64 format
        uid = urlsafe_base64_decode(uidb64).decode()
        # Retrieve the user associated with the decoded user ID
        user = Profile._default_manager.get(pk=uid)

    # If there's an error, set user to None
    except(TypeError, ValueError, OverflowError, Profile.DoesNotExist):
        user = None

    # If the user exists and the token is valid
    if user is not None and default_token_generator.check_token(user, token):
        # Activate the user's account
        user.is_active = True
        # Save the changes to the user account
        user.save()
        # Display a success message for account activation
        messages.success(request, 'Account is activated!')
        # Redirect to the login page after activation
        return redirect('login')

    # If not valid
    else:
        # Show an error message for invalid activation link
        messages.error(request, 'invalid activation link')
    # Redirect to the registration page
    return redirect('register')


@login_required(login_url='login')
def dashboard(request):
    """
    Displays the user's dashboard page. The current authenticated user's profile
    is passed to the template for rendering. If the user is not logged in, they
    are redirected to the login page.
    """

    # Retrieve the current authenticated user's profile
    profile = request.user
    # Prepare the context to pass to the template
    context = {
        'profile': profile,
    }
    # Render the dashboard template with the user's profile
    return render(request, 'dashboard.html', context)


@login_required(login_url='login')
def edit_profile(request):
    """
    Allows the authenticated user to edit their profile information.
    Handles both GET and POST requests to display the form and process updates.
    If the form is valid and changes are made, the profile is updated,
    and a success message is displayed. If no changes are made or if
    there are form errors, appropriate messages are shown.
    """

    # If the request method is POST (i.e., the form has been submitted)
    if request.method == 'POST':
        # Create a form instance with the submitted data and the current user's data
        user_form = UserForm(request.POST, request.FILES, instance=request.user)

        # If the form is valid
        if user_form.is_valid():
            # If changes has been made to the form
            if user_form.has_changed():
                # Save the updated profile informatio
                user_form.save()
                # Display a success message for profile update
                messages.success(request, 'Your profile has been updated')

            # If no changes have been made to the form
            else:
                # Show an error message indicating that no changes were made
                messages.error(request, 'No changes has been made')
            # Redirect to the profile page to avoid resubmission on refresh
            return redirect('edit_profile')

        # If the form is not valid
        else:
            # Handle invalid form errors if needed
            messages.error(request, 'There was an error with your submission')

    # If the request method is GET (i.e., the form has not been submitted)
    else:
        # Create a form instance with the current user's data to pre-fill the form fields
        user_form = UserForm(instance=request.user)

    # Render the edit profile template with the user form
    return render(request, 'edit_profile.html', {'user_form': user_form})


@login_required(login_url='login')
def change_password(request):
    """
    Allows the authenticated user to change their password. It verifies the current
    password, checks if the new password and confirmation match, and updates the
    password if everything is correct. Appropriate success or error messages are displayed.
    """

    # If the request method is POST (i.e., the form has been submitted)
    if request.method == 'POST':
        # Retrieve the data submitted by the user associated with the current session
        current_password        = request.POST['current_password']
        new_password            = request.POST['new_password']
        confirm_new_password    = request.POST['confirm_new_password']
        user                    = Profile.objects.get(username__exact=request.user.username)

        # If the new password match the confirmation password
        if new_password == confirm_new_password:
            # Verify if the current password is correct
            success = user.check_password(current_password)

            # If match
            if success:
                # Update the user's password
                user.set_password(new_password)
                # Save the changes to the user account
                user.save()
                # Display a success message
                messages.success(request, 'Password is now updated!')
                # Redirect to the dashboard
                return redirect('dashboard')

            # If current password is incorrect
            else:
                # Display error message
                messages.error(request, 'Your current password is not correct!')

        # If no match
        else:
            # Display error message
            messages.error(request, 'Passwords do not match!')
            # Redirect to the same page
            return redirect('change_password')

    # Render the change password template for GET requests
    return render(request, 'change_password.html')


def reset_password(request, uidb64, token):
    """
    Resets the user's password based on the provided UID and token. If the token is valid,
    it checks if the new password and confirmation match, updates the password, and
    provides appropriate messages. If the link is
      invalid, it redirects to the request
    password reset page.
    """

    try:
        # Decode the user ID from the base64 format
        uid = urlsafe_base64_decode(uidb64).decode()
        # Retrieve the user associated with the decoded user ID
        user = Profile._default_manager.get(pk=uid)
    except (TypeError, ValueError, OverflowError, Profile.DoesNotExist):
        # If there's an error, set user to None
        user = None

    # If the user exists and the token is valid
    if user is not None and default_token_generator.check_token(user, token):

        # If the request method is POST (i.e., the form has been submitted)
        if request.method == 'POST':
            # Retrieve the user´s input from the POST request data
            new_password         = request.POST.get('new_password')
            confirm_new_password = request.POST.get('confirm_new_password')

            # If the new password and confirmation match
            if new_password == confirm_new_password:
                # Update the user's password with the new password
                user.set_password(new_password)
                # Save the changes to the user account
                user.save()
                # Display a success message
                messages.success(request, 'Your password has been reset successfully. You can now log in.')
                # Redirect to the login page
                return redirect('login')

            # if the passwords do not match
            else:
                # Show an error message
                messages.error(request, 'Passwords do not match!')
        # Render the reset password template with the uid and token
        return render(request, 'reset_password.html', {'uidb64': uidb64, 'token': token})

    # If the reset link is invalid
    else:
        # Show an error message
        messages.error(request, 'The password reset link is invalid.')
        # Redirect to the request password reset page
        return redirect('request_password_reset')


def request_password_reset(request):
    """
    Requests a password reset by sending a reset link to the user's email.
    The user submits their email, and if it exists in the database, an email
    with the reset link is sent. Success and error messages are displayed
    based on the outcome.
    """

    # If the request method is POST (i.e., the form has been submitted)
    if request.method == 'POST':
        # Retrieve the email from the POST request data
        email = request.POST['email']

        # Try to find a user with the provided email
        try:
            # Using the user's email to find the user
            user = Profile.objects.get(email=email)
            # Get the current site domain for the email
            current_site = get_current_site(request)
            # Subject of the email
            mail_subject = 'Reset your password'
            # Render the email template with user details, domain, uid, and token
            message = render_to_string('request_password_reset.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })

             # Prepare the recipient email address
            to_email = email

            # Create and send the email
            email_message = EmailMessage(
                mail_subject,
                message,
                from_email='Postwall <glenncoding@gmail.com>',
                to=[to_email]
            )
            # Ensure the email is sent as HTML
            email_message.content_subtype = "html"
            email_message.send()

            # Show a success message and redirect to the login page
            messages.success(request, 'A password reset link has been sent to your email.')

            # Redirect after sending email
            return redirect('login')

        # If no user exists with the provided email
        except Profile.DoesNotExist:
            # Display a error message
            messages.error(request, 'No account found with this email address.')

    # If the request method is GET (i.e., form not submitted), render the reset password form
    return render(request, 'reset_password.html')


def create_new_password(request, uidb64, token):
    """
    Allows the user to create a new password after verifying the reset link.
    If the new password and confirmation match, it updates the user's password
    and redirects them to the login page. Displays an error message for invalid
    reset links or mismatched passwords.
    """

    # If the request is a POST (i.e., form submission)
    if request.method == 'POST':
        # Retrieve new password and confirmation from the form
        new_password = request.POST.get('new_password')
        confirm_new_password = request.POST.get('confirm_new_password')

        # If the new passwords match
        if new_password == confirm_new_password:
            try:
                # Decode the user's unique ID from the URL-safe base64 string
                uid = force_bytes(urlsafe_base64_decode(uidb64))
                # Fetch the user (Profile model used instead of Django's default User model)
                user = Profile.objects.get(pk=uid)
                # Set the new password and save the user
                user.set_password(new_password)
                user.save()
                # Display a success message
                messages.success(request, 'Your password has been updated!')
                return redirect('login')

            # If an error occurs, set user to None and show an error message
            except (TypeError, ValueError, OverflowError, Profile.DoesNotExist):
                user = None
                messages.error(request, 'Invalid reset link')

    # Render the create new password form with UID and token context passed
    return render(request, 'create_new_password.html', {'uidb64': uidb64, 'token': token})
