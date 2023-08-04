from django.test import SimpleTestCase
from django.urls import reverse, resolve
from events.views import create_event, edit_event, change_num

class TestEventUrls(SimpleTestCase):

    """
    Class that contains all the tests for the urls of events django app
    Simple test urls to check if at that specific url, it is called the correct view!
    """

    def test_create_event_url_is_resolved(self):
        url = reverse('create_event')
        self.assertEquals(resolve(url).func, create_event)

    
    def test_edit_event_url_is_resolved(self):
        """
        It has an argument that is the pk of the event, so we need to pass it!
        """
        url = reverse('edit_event', args=['test_edit_event'])
        self.assertEquals(resolve(url).func, edit_event)
    
    def test_change_num_url_is_resolved(self):
        url = reverse('change_num', args=['test_change_num'])
        self.assertEquals(resolve(url).func, change_num)