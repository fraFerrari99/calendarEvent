#test_forms.py
from django.test import TestCase
from events.forms import EventForm

class TestEventForm(TestCase):
    #Test the event form 

    def test_event_form_valid_data(self):
        #Populate the event form with valid data and see the results
        form_data = {
            "title": "Test form event",
            "description": "Test description form event",
            "date": "2023-08-13T12:00"
        }

        form = EventForm(data=form_data)

        #Check if the event form created is valid or not
        self.assertTrue(form.is_valid())
    
    def test_event_form_empty_is_invalid(self):
        #Check if an empty event form is an invalid form
        form = EventForm(data={})

        #Check if the event form is invalid
        self.assertFalse(form.is_valid())

    def test_event_form_invalid_date(self):
        #Check if the event form date is invalid
        form_data = {
            "title": "Test form event",
            "description": "Test description form event",
            "date": "2023-08-1312:00" #Incorrect date format
        }

        form = EventForm(data=form_data)

        #Check if the event form is invalid
        self.assertFalse(form.is_valid())