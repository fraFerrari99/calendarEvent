from django.test import TestCase
from users.models import CustomUser
from events.models import Event
from datetime import datetime


class TestEventModel(TestCase):

    def setUp(self):
        # Here we create a test user for the owner of the event
        self.user = CustomUser.objects.create(username="test_user1",email='test_user1@gmail.com', password='testpassword')
        self.participant1 = CustomUser.objects.create(username="user1", email='user1@gmail.com', password='testpassword1')
        self.participant2 = CustomUser.objects.create(username="user2", email='user2@gmail.com', password='testpassword2')
    
    def test_event_creation(self):
        
        # Create an event with all the required fields
        event = Event.objects.create(
            title='The Beatles Test',
            description='This is a test event of the beatles.',
            num_of_participants=1000000,
            owner=self.user,
            date=datetime(2023, 8, 23)
        )

        self.assertEqual(Event.objects.count(), 1)
        self.assertEqual(event.title, 'The Beatles Test')
        self.assertEqual(event.description, 'This is a test event of the beatles.')
        self.assertEqual(event.num_of_participants, 1000000)
        self.assertEqual(event.owner, self.user)
        self.assertEqual(event.date,datetime(2023, 8, 23))
        self.assertIsNone(event.image.name) #There is no image file name
        self.assertFalse(event.participants.exists()) #There are no participants

    def test_event_split_username(self):
        # Create an event with a specific owner username
        event = Event.objects.create(
            title='Test Beatles',
            description='This is a test event description of the beatles.',
            num_of_participants=1000000,
            owner=self.user,
            date=datetime(2023, 8, 23)
        )

        # Test the split_username() method that will return the part before @ and capitalize it!
        self.assertEqual(event.split_username(), 'Test_user1')

    def test_event_ordering_by_date(self):
        #Check if the events are ordered by date with ordering field defined!
        # Create events with different dates
        event1 = Event.objects.create(
            title='The beatles 1',
            description='This is event of the beatles number 1.',
            num_of_participants=5000000,
            owner=self.user,
            date=datetime(2023, 8, 15)
        )

        event2 = Event.objects.create(
            title='The beatles 2',
            description='This is event of the beatles number 1',
            num_of_participants=700000,
            owner=self.user,
            date=datetime(2023, 8, 10)
        )

        event3 = Event.objects.create(
            title='The beatles 3',
            description='This is event of the beatles number 1',
            num_of_participants=90000000,
            owner=self.user,
            date=datetime(2023, 8, 20)
        )

        # Check the events are ordered by date in ascending order
        ordered_events = Event.objects.all()
        self.assertEqual(list(ordered_events), [event2, event1, event3])


    def test_event_participants(self):
        # Create an event and add participants
        
        event = Event.objects.create(
            title='The Rolling Stones',
            description='This is a test of the rolling stones.',
            num_of_participants=100,
            owner=self.user,
            date=datetime(2023, 8, 15)
        )
        event.participants.add(self.participant1, self.participant2)

        self.assertEqual(event.participants.count(), 2)
        self.assertTrue(event.participants.filter(email='user1@gmail.com').exists())
        self.assertTrue(event.participants.filter(email='user2@gmail.com').exists())
