from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, SetPasswordForm, PasswordResetForm
from django.contrib.auth import get_user_model
from captcha.fields import ReCaptchaField
from captcha.widgets import ReCaptchaV2Checkbox
  

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(help_text="Enter a valid email address", required=True)
    captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox()) #this is the captcha

    class Meta:
        model = get_user_model()
        fields = ['email', 'password1', 'password2']
    
    def save(self, commit=True):
        user = super(UserRegistrationForm, self).save(commit=False)
        user.email = self.cleaned_data['email'] #get the email the user entered
        user.username = self.cleaned_data['email'].split("@")[0] #get the username the user entered
        if commit:
            user.save() #save the new user in the database

        return user

class UserLoginForm(AuthenticationForm):
    """form that is used to make the user login"""
    def __init__(self, *args, **kwargs):
        super(UserLoginForm, self).__init__(*args, **kwargs)
        

    captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox())

#user update form to update the user profile
class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = get_user_model()
        fields = ['email']

#form used to set a new password of the user
class SetPasswordForm(SetPasswordForm):
    class Meta:
        model = get_user_model()
        # Form to set a new password
        fields = ['new_password1', 'new_password2']

#form used to change the password of the user
class ChangePasswordForm(PasswordResetForm):
    def __init__(self, *args, **kwargs):
        super(PasswordResetForm, self).__init__(*args, **kwargs)
        

    captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox())

class ChangeEmailForm(forms.ModelForm):
    """
    Form that it is used to change the email!
    """
    email = forms.EmailField(help_text="Enter a new email address", required=True)
    captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox()) 

    class Meta:
        model = get_user_model()
        fields = ['email']
    

