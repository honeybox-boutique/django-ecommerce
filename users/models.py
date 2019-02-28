from django.db import models
from django.contrib.auth.models import AbstractUser

# class User(AbstractUser):
    # email = models.EmailField(unique=True)
    # send_promos = models.BooleanField(default=True)

class Guest(models.Model):
    guestEmail = models.EmailField()
    guestActive = models.BooleanField(default=True)
    guestDateLastUpdated = models.DateTimeField(auto_now=True)
    guestDateCreated = models.DateTimeField(auto_now_add=True)
    guestSendPromos = models.BooleanField(default=False)

    def __str__(self):
        return self.guestEmail
