from django.db import models

# Create your models here.

class Guest(models.Model):
    guestEmail = models.EmailField()
    guestActive = models.BooleanField(default=True)
    guestDateLastUpdated = models.DateTimeField(auto_now=True)
    guestDateCreated = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.guestEmail
