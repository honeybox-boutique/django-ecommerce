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

    def charge(self, order_obj, card=None):
        return Charge.objects.do(self, order_obj, card)

    def get_cards(self):
        return self.card_set.all()

    @property
    def has_card(self):
        card_qs = self.get_cards()
        return card_qs.exists()

    @property
    def default_card(self):
        default_cards = self.get_cards().filter(cardDefault=True)
        if default_cards.exists():
            return default_cards.first()
        return None

    def __str__(self):
        return self.billingEmail

# Stripe tokenizer API request
def billing_profile_created_receiver(sender, instance, *args, **kwargs):
    if not instance.billingToken and instance.billingEmail:
        print('Actual api request to Stripe to get token')
        customer = stripe.Customer.create(
            email=instance.billingEmail,
            description=instance.user
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
    def add_new(self, billing_profile, token):
        if token:
            customer = stripe.Customer.retrieve(billing_profile.billingToken)
            stripe_card_response = customer.sources.create(source=token)
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
    cardDefault = models.BooleanField(default=True)

    objects = CardManager()

    def __str__(self):
        return '{} {}'.format(self.cardBrand, self.cardLast4)

    class Meta:
        db_table = 'card'

class ChargeManager(models.Manager):
    def do(self, billing_profile, sale_obj, card=None):
        card_obj = card
        if card_obj is None:
            cards = billing_profile.card_set.filter(cardDefault=True)
            if cards.exists():
                card_obj = cards.first()
        if card_obj is None:
            return False, 'No cards available'
        
        c = stripe.Charge.create(
            amount=int(sale_obj.saleTotal * 100), #amount in cents
            currency='usd',
            customer=billing_profile.billingToken,
            source=card_obj.cardStripeID,
            metadata={'order_id': sale_obj.saleStringID},
        )
        new_charge_obj = self.model(
            billingProfile=billing_profile,
            chargeStripeID=c.id,
            chargePaid=c.paid,
            chargeRefunded=c.refunded,
            chargeOutcome=c.outcome,
            chargeOutcomeType=c.outcome['type'],
            chargeSellerMessage=c.outcome.get('seller_message'),
            chargeRiskLevel=c.outcome.get('risk_level'),
        )
        new_charge_obj.save()
        return new_charge_obj.chargePaid, new_charge_obj.chargeSellerMessage

class Charge(models.Model):
    billingProfile = models.ForeignKey(BillingProfile, on_delete=models.CASCADE)
    chargeStripeID = models.CharField(max_length=120)
    chargePaid = models.BooleanField(default=False)
    chargeRefunded = models.BooleanField(default=False)
    chargeOutcome = models.TextField(max_length=255, blank=True, null=True)
    chargeOutcomeType = models.CharField(max_length=120, blank=True, null=True)
    chargeSellerMessage = models.CharField(max_length=120, blank=True, null=True)
    chargeRiskLevel = models.CharField(max_length=120, blank=True, null=True)

    objects = ChargeManager()

    class Meta:
        db_table = 'charge'