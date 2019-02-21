from django.conf import settings
from django.db import models
from django.db.models.signals import post_save, pre_save

from users.models import Guest
User = settings.AUTH_USER_MODEL


import stripe
stripe.api_key = "***REMOVED***"

class BillingProfileManager(models.Manager):
    def new_or_get(self, request):
        user = request.user
        guest_email_id = request.session.get('guest_email_id')
        created = False
        obj = None
        if user.is_authenticated:
            # user checkout
            print('user checkout')
            obj, created = self.model.objects.get_or_create(user=user, billingEmail=user.email)
            print('billing profile: ', obj.id)
        elif guest_email_id is not None:
            # guest checkout
            print('guest checkout')
            guest_obj = Guest.objects.get(id=guest_email_id)
            obj, created = self.model.objects.get_or_create(billingEmail=guest_obj.guestEmail)
            print(obj)
        else:
            # change: do we need error raise here?
            pass
        return obj, created

class BillingProfile(models.Model):
    billingEmail = models.EmailField()
    active = models.BooleanField(default=True)
    lastUpdated = models.DateTimeField(auto_now=True)
    dateCreated = models.DateTimeField(auto_now_add=True)

    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)

    # stripe token
    billingToken = models.CharField(max_length=120, null=True, blank=True)

    objects = BillingProfileManager()

    def __str__(self):
        return self.billingEmail

# Stripe tokenizer API request
def billing_profile_created_receiver(sender, instance, *args, **kwargs):
    if not instance.billingToken and instance.billingEmail:
        print('Actual api request to Stripe to get token')
        customer = stripe.Customer.create(
            email=instance.billingEmail
        )
        print(customer)
        instance.billingToken = customer.id
pre_save.connect(billing_profile_created_receiver, sender=BillingProfile)

# creates billing profile on user creation
def user_created_receiver(sender, instance, created, *args, **kwargs):
    if created and instance.email:
        BillingProfile.objects.get_or_create(user=instance, billingEmail=instance.email)
post_save.connect(user_created_receiver, sender=User)


class CardManager(models.Manager):
    def add_new(self, billing_profile, stripe_card_response):
        if str(stripe_card_response.object) == 'card':
            new_card = self.model(
                billingProfile=billing_profile,
                cardStripeID=stripe_card_response.id,
                cardBrand=stripe_card_response.brand,
                cardCountry=stripe_card_response.country,
                cardExpMonth=stripe_card_response.exp_month,
                cardExpYear=stripe_card_response.exp_year,
                cardLast4=stripe_card_response.last4,
            )
            new_card.save()
            return new_card
        return None

class Card(models.Model):
    billingProfile = models.ForeignKey(BillingProfile, on_delete=models.CASCADE)
    cardStripeID = models.CharField(max_length=120)
    cardBrand = models.CharField(max_length=120, null=True, blank=True)
    cardCountry = models.CharField(max_length=20, null=True, blank=True)
    cardExpMonth = models.IntegerField(null=True, blank=True)
    cardExpYear = models.IntegerField(null=True, blank=True)
    cardLast4 = models.CharField(max_length=4)
    cardDefault = models.BooleanField(default=False)

    objects = CardManager()

    def __str__(self):
        return '{} {}'.format(self.cardBrand, self.cardLast4)

    class Meta:
        db_table = 'card'