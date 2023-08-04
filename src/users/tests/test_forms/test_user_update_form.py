from django.test import TestCase
from users.models import CustomUser
from users.forms import UserUpdateForm

class TestUserUpdateForm(TestCase):

    def setUp(self):
        #Setting up a default custom user to use to test the user update form
        self.user = CustomUser.objects.create(
            username="test_form_update",
            email="test_form_update@example.com",
            password="test_form"
        )

        self.client.login(username="test_form_update", email="test_form_update@example.com", password="test_form")

    def test_valid_user_update_form_data(self):

        #Test that form data for user update form is valid
        form_data = {
            "email": "new_email@example.com",
        }

        #

        #Use as instance self.user and as data the form data created
        form = UserUpdateForm(data=form_data, instance=self.user)
        self.assertTrue(form.is_valid())
    
    def test_invalid_user_update_form_data(self):

        #Test that form data for user update form is invalid
        form_data = {
            "email": "new_email",
        }

        #Use as instance self.user and as data the form data created
        form = UserUpdateForm(data=form_data, instance=self.user)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors["email"], ['Enter a valid email address.'])
    
