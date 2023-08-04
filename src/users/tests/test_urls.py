from django.test import SimpleTestCase
from django.urls import reverse, resolve
from users.views import register, logout_view, profile, activate, change_password, change_email, forgot_password, password_reset_confirm

class TestUsersUrls(SimpleTestCase):

    """
    Class that contains all the tests for the urls of users django app
    Simple test urls to check if at that specific url, it is called the correct view!
    """

    def test_register_url_is_resolved(self):
        url = reverse('register')
        self.assertEquals(resolve(url).func, register)

    
    def test_sign_out_url_is_resolved(self):
        url = reverse('sign_out')
        self.assertEquals(resolve(url).func, logout_view)
    
    def test_profile_url_is_resolved(self):
        """
        It has an argument that is the email of the user, so we need to pass it!
        """
        url = reverse('profile', args=['test_profile@gmail.com'])
        self.assertEquals(resolve(url).func, profile)
    
    def test_activate_url_is_resolved(self):
        url = reverse('activate', args=["test_uidb64","test_token"])
        self.assertEquals(resolve(url).func, activate)
        

    def test_change_password_url_is_resolved(self):
        url = reverse('change_password')
        self.assertEquals(resolve(url).func, change_password)
    
    def test_forgot_pwd_url_is_resolved(self):
        url = reverse('forgot_pwd')
        self.assertEquals(resolve(url).func, forgot_password)
    
    def test_password_reset_url_is_resolved(self):
        url = reverse('password_reset_confirm', args=["test_uidb64","test_token"])
        self.assertEquals(resolve(url).func, password_reset_confirm)
        
    def test_change_email_url_is_resolved(self):
        url = reverse('change_email')
        self.assertEquals(resolve(url).func, change_email)
    