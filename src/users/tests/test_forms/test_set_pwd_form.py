from django.test import TestCase
from users.models import CustomUser
from users.forms import SetPasswordForm

class TestSetPasswordForm(TestCase):

    def setUp(self):
        #Setting up a default custom user to use to test the set password form
        self.user = CustomUser.objects.create(
            username="test_form_pwd",
            email="test_form_pwd@example.com",
            password="test_form_pwd"
        )

        self.client.login(username="test_form", email="test_form_pwd@example.com", password="test_form")
    
    def test_set_password_form_data(self):
        #Test used for set_password form
        form_password = {
            'new_password1': 'new_password',
            'new_password2': 'new_password',
        }

        form = SetPasswordForm(user=self.user,data=form_password)

        #Test if is a valid form
        self.assertTrue(form.is_valid())
    
    def test_mismatch_password_form_data(self):
        form_password = {
            'new_password1': 'new_password',
            'new_password2': 'new_passwo',
        }

        form = SetPasswordForm(user=self.user,data=form_password)

        #Test that is an invalid form
        self.assertFalse(form.is_valid())

        #Test that the error message is the fact that the passwords are not equals
        self.assertEqual(form.errors["new_password2"], ['The two password fields didn’t match.'])
