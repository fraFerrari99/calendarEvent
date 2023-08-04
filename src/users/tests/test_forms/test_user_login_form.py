from django.test import TestCase
from users.forms import UserLoginForm

class TestUserLoginForm(TestCase):
    """Tests written for UserLoginForm"""
    def setUp(self):

        #Setting up a user login form data to use to test the user login form
        self.form_login_data = {
            "email": 'login@example.com',
            'password': 'password',
            'g-recaptcha-response': 'test_recaptcha_response',
        }
  

    def test_invalid_login_form_email(self):
        form_data = self.form_login_data.copy()
        form_data['email'] = ''  # Empty email field
        form = UserLoginForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['username'], ['This field is required.'])

    def test_invalid_login_form_password(self):
        form_data = self.form_login_data.copy()
        form_data['password'] = ''  # Empty password
        form = UserLoginForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['password'], ['This field is required.'])

    def test_invalid_login_form_recaptcha(self):
        form_data = self.form_login_data.copy()
        form_data['g-recaptcha-response'] = ''  # Empty reCAPTCHA response
        form = UserLoginForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['captcha'], ['This field is required.'])