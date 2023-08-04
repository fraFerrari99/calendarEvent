#test_models.py
from django.test import TestCase
from users.models import CustomUser

class TestUsersModel(TestCase):

    def setUp(self):
        """
        Set up the test models creating a test user that will be used for each case
        """
        self.user = CustomUser.objects.create(
            username="user_test",
            email="user_test@gmail.com",
            password="user_test123"
        )
    
    def test_str_method_returns_email(self):
        #Check if the __str__ method returns the email of the user
        self.assertEquals(str(self.user),"user_test@gmail.com")

    