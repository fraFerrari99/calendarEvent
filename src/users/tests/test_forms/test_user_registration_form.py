from django.test import TestCase
from django.contrib.auth import get_user_model
from users.forms import UserRegistrationForm


class TestUserRegistrationForm(TestCase):

    def setUp(self):
        """Setting up the user registration form data to test user registration form""" 
        self.form_data = {
            'email': 'test_user_registration@example.com',
            'password1': 'testpassword',
            'password2': 'testpassword',
            'g-recaptcha-response': 'test_recaptcha_response',
        }


    def test_invalid_email(self):
        form_data = self.form_data.copy()
        form_data['email'] = 'invalidemail'  # Invalid email format
        form = UserRegistrationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['email'], ['Enter a valid email address.'])

    def test_mismatching_passwords(self):
        form_data = self.form_data.copy()
        form_data['password2'] = 'differentpassword'  # Mismatching passwords
        form = UserRegistrationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['password2'], ['The two password fields didn’t match.'])


    def test_invalid_recaptcha(self):
        form_data = self.form_data.copy()
        form_data['g-recaptcha-response'] = ''  # Empty reCAPTCHA response
        form = UserRegistrationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['captcha'], ['This field is required.'])
 


