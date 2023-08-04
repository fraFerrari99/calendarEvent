from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model, login, logout, get_user_model
from django.contrib import messages #messages are used to display messages to the user
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm

from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage #to send the email confirmation message

from django.db.models.query_utils import Q

from django.template.loader import render_to_string #used to render a template and return a string!
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes, force_str


from .forms import UserRegistrationForm, UserUpdateForm, SetPasswordForm, ChangePasswordForm, ChangeEmailForm
from .tokens import account_activation_token
from events.models import Event

# Create your views here.

def activate(request, uidb64, token):
    User = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except:
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()

        messages.success(request, "Thank you for the email confirmation! Now you can login your account.")
        return redirect('sign_in')
    else:
        messages.error(request, "Activation link is invalid!")

    return redirect('/')

def activate_email(request, user, to_email):
    mail_subject = "Activate your user account email!"
    domain = get_current_site(request).domain
    message = render_to_string("activate_account_template.html", {
        'user': user.email,
        'domain': get_current_site(request).domain + ":8000",
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': account_activation_token.make_token(user),
        'protocol': 'https' if request.is_secure() else 'http'
    })

    email = EmailMessage(mail_subject, message, to=[to_email])
    if email.send():
        username = to_email.split('@')[0]
        messages.success(request, f"Dear <b>{username}</b>, please go to your email <b>{to_email}</b> inbox and click on \
                        the activation link you received to complete your registration. <b> Note: </b> Please check your <b>spam</b> folder!")
    else:
        messages.error(request, f'Problem sending email to {to_email}, check if you typed it correctly.')
                
    
def register(request):
    if request.user.is_authenticated:
        #is already logged in
        return redirect('/')

    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False #user is not active since he needs to confirm with the email
            user.save()
            activate_email(request, user, form.cleaned_data["email"])
            login(request, user)
            return redirect('/')
        else:
            #there can be a lot of errors, so we print them out
            for error in list(form.errors.values()):
                #!display the error messages to the user
                messages.error(request, error)
    
    else: #if it not a POST request, when the user enters for the first time, we show him the form
        form = UserRegistrationForm()
    
    
    return render(request, "user/register.html", {"form": form})



@login_required
def logout_view(request):
    #logout the user printing a message to the user!
    logout(request)
    messages.success(request, f'You are now logged out!')
    return redirect('/')

@login_required
def change_password(request):
    #change the password of the user
    user = request.user
    if request.method == 'POST':
        form = SetPasswordForm(user, request.POST)
        if form.is_valid():
            #form is valid so we can change the password of the user
            form.save()
            messages.success(request, f'{user.email}, your password has been changed!')
            return redirect('sign_in')
        else:
            for error in list(form.error.values()):
                messages.error(request, error) #print all the errors

    form = SetPasswordForm(user)
    return render(request, 'password_reset_confirm.html',{'form':form})

def profile(request, email):
    if request.method == 'POST':
        user = request.user
        form = UserUpdateForm(request.POST, instance=user)
        if form.is_valid():
            user_form = form.save()
            messages.success(request, f'{user_form.email}, Your profile has been updated!')
            return redirect("profile", user_form.email)

        for error in list(form.errors.values()):
            messages.error(request, error)

    user = get_user_model().objects.filter(email=email).first() #check the user in the db to edit it
    if user:
        form = UserUpdateForm(instance=user)
         #here we pass to the profile page, the user object that can be edited!
        return render(request, "user/profile.html", {"form": form})
    
    return redirect('/')


"""
    View to change the password of a user if he doesn't remember it!
"""
def forgot_password(request):
    if request.method == 'POST':
        form = ChangePasswordForm(request.POST)
        if form.is_valid():
            user_email = form.cleaned_data["email"] #get the email
            """
            Check if the user email exists in the database
            """
            user_associated = get_user_model().objects.filter(Q(email=user_email)).first()
            if user_associated:
                #if user exists in the database, send him an email through which he can change the password
                    mail_subject = "Password Reset Request"
                    message = render_to_string("change_password_template.html", {
                        'user': user_associated.email,
                        'domain': get_current_site(request).domain + ":8000",
                        'uid': urlsafe_base64_encode(force_bytes(user_associated.pk)),
                        'token': account_activation_token.make_token(user_associated),
                        'protocol': 'https' if request.is_secure() else 'http'
                    })

                    email = EmailMessage(mail_subject, message, to=[user_associated.email])
                    if email.send():
                        username = user_associated.email.split('@')[0]
                        messages.success(request, f"<h2>Password Reset Confirm</h2><br>Dear <b>{username}</b>, please go to your email <b>{user_associated.email}</b> inbox and click on \
                                        the reset password link you received to reset your password. <b> Note: </b> Please check your <b>spam</b> folder!")
                    else:
                        messages.error(request, f'Problem sending reset password email to {user_associated.email}, check if you typed it correctly.')
            """
            User does not exist in the database, so return to the homepage
            """
            return redirect('/')
        """
        If form is not valid, there can be a problem with the captcha!
        """
        for key, error in list(form.errors.items()):
            if key == 'captcha' and error[0] == 'This field is required.':
                messages.error(request, "You must pass the reCAPTCHA test")
                continue

    form = ChangePasswordForm()
    return render(request, "password_change.html", {"form": form})


""" View to confirm the reset of the password to the link that will be sent to the user's email"""
def password_reset_confirm(request, uidb64, token):
    User = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except:
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        if request.method == 'POST':
            form = SetPasswordForm(user, request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, "New password was saved successfully! You can now <b>login</b> again.")
                return redirect('sign_in')
            else:
                for error in list(form.errors.values()):
                    messages.error(request, error)
        
        form = SetPasswordForm(user)
        return render(request, 'password_reset_confirm.html', {'form': form})
    else:
        messages.error(request, "Activation link is invalid!")

    messages.error(request, "Something went wrong, redirecting to the homepage!")
    return redirect('/')

@login_required
def change_email(request):
    """Change the email address"""
    if request.method == 'POST':
        user = request.user
        form = ChangeEmailForm(request.POST)
        if form.is_valid():
            user_email = form.cleaned_data["email"] #get the new email
            """
            Check if new the user email already exists in the database
            """
            user_associated = get_user_model().objects.filter(Q(email=user_email)).first()
            if user_associated:
                """
                User exists in the database, so print the error message and return to the homepage
                """
                messages.error(request, f'User {user_email} already exists, make sure it is <b>yours</b> and in case change your password!')
                return redirect('/')
            else:

                #if user email does not exist in the database, change the email to the new one
                update_event_owner_email(user, user_email)
                user.email = user_email
                user.save()
                
                messages.success(request, f"Email changed to {user_email} successfully!")
                return redirect('/')
 
    
        """
        If form is not valid, there can be a problem with the captcha!
        """
        for key, error in list(form.errors.items()):
            messages.error(request, error)
            if key == 'captcha' and error[0] == 'This field is required.':
                messages.error(request, "You must pass the reCAPTCHA test")
                continue

    form = ChangeEmailForm()
    return render(request, "change_email_confirm.html", {"form": form})

def update_event_owner_email(user, new_email):
    """
        Get all events owned by the user and change the owner of each event if he changes his email address     
    """
    user_events = Event.objects.filter(owner=user)

    # Update the email for each event
    for event in user_events:
        event.owner_email = new_email
        event.owner_username = new_email
        event.save()





