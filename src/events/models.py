# Create your models here.
from django.db import models
from users.models import CustomUser

# Create your models here.
class Event(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=200)
    description = models.TextField()
    num_of_participants = models.IntegerField(default=0)
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="owner_event")
    date = models.DateTimeField()
    

    #I added the image field so that the user can upload the image of the event
    image = models.ImageField(upload_to='media/', null=True, blank=True)

    """
    I added this field to save all the users that participated to the event
    This way, if they already participated to the event they will see another button that will make them opt out of the event!
    """
    participants = models.ManyToManyField(CustomUser, blank=True, related_name="participant_event")


    def __str__(self):
        #method that returns the string representation of the object
        #title and date of the event
        return self.title + ", " + self.date.strftime("%d-%m-%Y")
    
    def split_username(self):
        """
        This function is used to split the username and recover only the part before the @ of the email
        This is done for the task:  
        List view shows the owner of the event (as the part of the email before the "@").
        """
        return self.owner.username.split("@")[0].capitalize()
    
    class Meta:
        """
        I made two fields unique together that are date and title!
        I sorted by date in ascending order:
        this way upcoming events are first without using order_by() everywhere
        """
        unique_together = ('date', 'title')
        ordering = ['date']
    