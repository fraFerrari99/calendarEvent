from typing import Any, Optional
from django.contrib import messages 
from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.base_user import AbstractBaseUser
from django.http.request import HttpRequest
# from captcha.fields import ReCaptchaField
# from captcha.widgets import ReCaptchaV2Checkbox

#create a custom authentication backend, in this way we can use the email to authenticate the users!

class EmailAuthBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
       UserModel = get_user_model()
       try:
           user = UserModel.objects.get(email=username)
       except UserModel.DoesNotExist:
           return None
       else:
           if user.check_password(password):
                messages.success(request, f'Welcome {user.username}! You are now logged in!')
                return user
       
       return None