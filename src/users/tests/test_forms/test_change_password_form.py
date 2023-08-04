from django.test import TestCase
from users.forms import ChangePasswordForm


class TestChangePasswordForm(TestCase):
    """Tests written for ChangePasswordForm"""
    def setUp(self):

        #Setting up a change password form data to use to test the change password form
        self.form_change_password_data = {
            'password1': 'newpassword',
            'password2': 'newpassword',
            'g-recaptcha-response': 'test_recaptcha_response',
        }


    def test_change_pwd_mismatching_passwords(self):
        form_data = self.form_change_password_data.copy()
        form_data['password2'] = 'differentpassword'  # Mismatching passwords
        form = ChangePasswordForm(data=form_data)
        self.assertFalse(form.is_valid())
        
    def test_change_pwd_short_password(self):
        form_data = self.form_change_password_data.copy()
        form_data['password1'] = 'short'  # Short password
        form = ChangePasswordForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_change_pwd_invalid_recaptcha(self):
        form_data = self.form_change_password_data.copy()
        form_data['g-recaptcha-response'] = ''  # Empty reCAPTCHA response
        form = ChangePasswordForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['captcha'], ['This field is required.'])