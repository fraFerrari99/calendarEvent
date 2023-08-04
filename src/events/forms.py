from django import forms
from .models import Event

#Create the form related to the event
class EventForm(forms.ModelForm):
    
    #it extends the Event model since it is a form that is used to create a new event
    class Meta:
        model = Event
        fields = ['title', 'description', 'date', 'image']

        """
        With the use of widgets field, we can create an input of type date for the date field!
        """
        widgets = {
            'date': forms.TextInput(attrs={'type': 'datetime-local'}),
        }