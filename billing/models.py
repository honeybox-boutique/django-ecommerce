from django.conf import settings
from django.db import models
from django.db.models.signals import post_save

User = settings.AUTH_USER_MODEL

# Create your models here.

class BillingProfile(models.Model):
    billingEmail = models.EmailField()
    active = models.BooleanField(default=True)
    lastUpdated = models.DateTimeField(auto_now=True)
    dateCreated = models.DateTimeField(auto_now_add=True)

    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    # billingToken = ? #Stripe token here, will be retrieved using sensors

    def __str__(self):
        return self.billingEmail

# Stripe tokenizer API request
# def billing_profile_created_receiver(sender, instance, created, *args, **kwargs):
    # if created:
        # print('Actual api request to Stripe to get token')
        # instance.customer_id = newID
        # instance.save()

# creates billing profile on user creation
def user_created_receiver(sender, instance, created, *args, **kwargs):
    if created and instance.email:
        BillingProfile.objects.get_or_create(user=instance, billingEmail=instance.email)
post_save.connect(user_created_receiver, sender=User)
