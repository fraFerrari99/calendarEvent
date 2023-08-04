from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.core import serializers
from .forms import EventForm
from .models import Event
from datetime import datetime
import json


# Create your views here.
def homepage(request):
    all_events = Event.objects.all()
    #passing all the possible events to the homepage template
    context = {
        "events": all_events
    }
    return render(request, "event/homepage.html", context)


def create_event(request):
    #!this function is used to give the user the option to create a new event
    if request.method == "POST":
        #it's a post request, so we need to get the form data
        #we need to add request.FILES to get the image that the user uploaded
        event_form = EventForm(request.POST, request.FILES)
        if event_form.is_valid():
            event = event_form.save(commit=False) #to get the new event 
            request.user.username = request.user.username.split("@")[0]
            event.owner = request.user #!set the owner of the new event to the user that made
            event.owner.username = request.user.username #!split the username out of the email address
            event.save() #!save the new event to the database
            messages.success(request, f'New event created {event.title}')
            return redirect("/")
        else:
            #there can be a lot of errors, so we print them out
            for error in list(event_form.errors.values()):
                #!display the error messages to the user
                messages.error(request, error)
    else:
        #here is the form to create a new event since it's not a post request
        event_form = EventForm()
    
    context = {
        "form": event_form
    }
    return render(request, "event/create_event.html", context)


def edit_event(request, event_id):
    #!this function is used to give the user the option to edit an event he created
    event = get_object_or_404(Event, id=event_id, owner=request.user)
    if request.method == "POST":
        #it's a post request, so we need to get the form data
        #we need to add request.FILES to get the image that the user uploaded
        event_form = EventForm(request.POST, request.FILES, instance=event )
        if event_form.is_valid():
            num_of_participants = event.num_of_participants
            event = event_form.save(commit=False) #to get the new event 
            event.owner = request.user #!set the owner of the new event to the user that made
            event.owner.username = request.user.username.split('@')[0] #!split the username out of the email address
            event.num_of_participants = num_of_participants
            event.save() #!save the new event to the database
            messages.success(request, f'Event {event.title} edited successfully!')
            return redirect("/")
        else:
            #there can be a lot of errors, so we print them out
            for error in list(event_form.errors.values()):
                #!display the error messages to the user
                messages.error(request, error)
    else:
        event = EventForm(instance=event)

    return render(request, "event/edit_event.html", {"event": event})


def change_num(request, event_id):
    """
        If the user is in the participants, we will remove from them, reducing the number of participants
        else we will add to the participants and increase the number of participants
    """
    
    event = get_object_or_404(Event, id=event_id)

    if request.user in event.participants.all() and len(event.participants.all()) > 0:
        event.num_of_participants -= 1
        event.participants.remove(request.user)
        event.save()
        response = {
            "response": {
            "success": True,
            "num_of_participants": event.num_of_participants,
            "is_in_participant": False,
            "event_id": event.id,
            }
        }

        return JsonResponse(response, status=200)
    else:
        event.num_of_participants += 1
        event.participants.add(request.user)
        event.save()    
        response = {
            "response": {
            "success": True,
            "num_of_participants": event.num_of_participants,
            "is_in_participant": True,
            "event_id": event.id,
            }
        }

        return JsonResponse(response, status=200)