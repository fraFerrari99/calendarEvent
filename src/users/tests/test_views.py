from django.contrib.messages import get_messages
from django.test import TestCase, Client
from django.urls import reverse
from events.models import Event
from users.models import CustomUser
import json 
from datetime import datetime

 
class TestUsersViews(TestCase):
    """Test users views """

    def setUp(self):
        """
            This method is called every time before every tests are run, so it can be used to recreate some scenarios
        """
        self.client = Client()
        self.register = reverse('register')
        self.sign_out = reverse('sign_out')
        self.change_password = reverse('change_password')
        self.forgot_password = reverse('forgot_pwd')
        self.change_email = reverse('change_email')

        
        """Create a test custom user"""
        self.user_test = CustomUser.objects.create(
            username="test_user",
            email="test_user@gmail.com",
            password="test_password",
        )
       
        
        self.profile = reverse('profile', args=[self.user_test.email])

    def test_register_GET(self):
        response = self.client.get(self.register)
        """
        Check what response was returned and what template was returned
        """
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'user/register.html')
    
    
  
    def test_logout_view(self):

        """Test that see if he can logout"""
        self.client.login(username="test_user",email="test_user@gmail.com",password="test_password")
        response = self.client.post(self.sign_out)
        self.assertEquals(response.status_code, 302)
    
    def change_password_test_POST(self):
        """Test  change_password view"""

        self.client.login(username="test_user",email="test_user@gmail.com",password="test_password")
        
        # Make a POST request with valid form data
        form_data = {
            'new_password1': 'newpassword',
            'new_password2': 'newpassword'
        }
        response = self.client.post(self.change_password, form_data)

        # Check if the password has been changed and the user is redirected to the sign-in page
        self.assertRedirects(response, reverse('sign_in'))
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password('newpassword'))

        # Check if the success message is displayed
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(messages[0].level_tag, 'success')
        self.assertIn('your password has been changed', str(messages[0]))
    

    def update_profile_test(self):
        
        # Make a POST request with valid form data to update the profile (only the email)
        form_data = {
            'email': 'newemail@gmail.com',
        }

        response = self.client.post(self.profile, form_data, follow=True)

        # Check if the form is valid and the user profile is updated
        self.assertEqual(response.status_code, 200)
        self.user.refresh_from_db()
        self.assertEqual(self.user.email, 'newemail@gmail.com')

        # Check if the success message is displayed
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(messages[0].level_tag, 'success')
        self.assertIn('Your profile has been updated', str(messages[0]))
