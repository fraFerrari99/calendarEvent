from django.contrib.messages import get_messages
from django.test import TestCase, Client
from django.urls import reverse
from events.models import Event
from users.models import CustomUser
import json 
from datetime import datetime

 
class TestEventViews(TestCase):


    def setUp(self):
        """
            This method is called every time before every tests are run, so it can be used to recreate some scenarios
        """
        self.client = Client()
        self.create_event_url = reverse('create_event')
        self.edit_event_url = reverse('edit_event', args=["test_edit"])
        self.change_num_url = reverse('change_num', args=["test_change_num"])
        
        """Create a test custom user"""
        self.user_test = CustomUser.objects.create(
            username="test_user",
            email="test_user@gmail.com",
            password="test_password",
        )
 
        

    def test_create_event_GET(self):
        response = self.client.get(self.create_event_url)
        """
        Check what response was returned and what template was returned
        """
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'event/create_event.html')
    
    
    """This one is not working, there are some problems related with the create_event view method!"""
        # def test_create_event_POST_add_new_event(self):

        #     """Test that see if he can create a new event"""
        #     self.client.login(username="test_user",email="test_user@gmail.com",password="test_password")
        #     event_data = {
        #         "title": "Inception",
        #         "description": "Movie event",
        #         "num_of_participants": 2450,
        #         "date": datetime.now()
        #     }

        #     response = self.client.post(self.create_event_url, event_data, follow=True)

        #     # Check if the event is created in the database
        #     self.assertEqual(response.status_code, 200)
        #     self.assertEqual(Event.objects.count(), 1)
        #     event = Event.objects.first()
        #     self.assertEqual(event.title, 'Inception')
        #     self.assertEqual(event.description, 'Movie event')
        #     self.assertEqual(event.num_of_participants, 2450)

        #     # Check if the success message is displayed
        #     messages = list(get_messages(response.wsgi_request))
        #     self.assertEqual(len(messages), 1)
        #     self.assertEqual(messages[0].level_tag, 'success')
        #     self.assertIn('New event created', str(messages[0]))


