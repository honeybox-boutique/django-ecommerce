from django.conf import settings
from django.db import models
from django.db.models.signals import post_save, pre_save
from django.urls import reverse

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
            obj, created = self.model.objects.get_or_create(
                user=user, 
                billingEmail=user.email,
                profileType='user',
            )
        elif guest_email_id is not None:
            # guest checkout
            guest_obj = Guest.objects.get(id=guest_email_id)
            # query for guest profile thats active, has email, and profile type is guest
            profile_qs = self.get_queryset().filter(
                billingEmail=guest_obj.guestEmail,
                active=True,
                profileType='guest',
            )
            if profile_qs.count() == 1:
                obj = profile_qs.first()
            elif profile_qs.count() == 0:
                # create new billing profile if guest
                created = True
                obj = self.model.objects.create(
                    billingEmail=guest_obj.guestEmail,
                    profileType='guest',
                )
        else:
            # change: do we need error raise here?
            pass
        return obj, created

class BillingProfile(models.Model):
    billingEmail = models.EmailField()# make this a related field to user.email or guest.email
    active = models.BooleanField(default=True)
    lastUpdated = models.DateTimeField(auto_now=True)
    dateCreated = models.DateTimeField(auto_now_add=True)
    PROFILE_TYPES = (
        ('guest', 'Guest'),
        ('user', 'User'),
    )
    profileType = models.CharField(max_length=120, choices=PROFILE_TYPES)

    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)

    # stripe token
    billingToken = models.CharField(max_length=120, null=True, blank=True)

    objects = BillingProfileManager()

    def charge(self, sale_obj):
        card = sale_obj.salePaymentCard
        return Charge.objects.do(self, sale_obj, card)

    def get_cards(self):
        return self.card_set.all()

    def get_payment_method_url(self):
        return reverse('billing:payment_method')

    @property
    def has_card(self):
        card_qs = self.get_cards()
        return card_qs.exists()

    @property
    def default_card(self):
        default_cards = self.get_cards().filter(cardActive=True, cardDefault=True)
        if default_cards.exists():
            return default_cards.first()
        return None

    def set_inactive(self):
        self.active = False
        self.save()
        self.set_cards_inactive()
        return self.active

    def set_cards_inactive(self):
        card_qs = self.get_cards()
        card_qs.update(cardActive=False)
        return card_qs.filter(cardActive=True).count()

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
        BillingProfile.objects.get_or_create(
            user=instance,
            billingEmail=instance.email,
            profileType='user'
        )
post_save.connect(user_created_receiver, sender=User)


class CardManager(models.Manager):
    def all(self, *args, **kwargs):
        return self.get_queryset().filter(cardActive=True)

    def add_new(self, billing_profile, token, address_obj=None, remember=False):
        if token:
            customer = stripe.Customer.retrieve(billing_profile.billingToken)
            stripe_card = customer.sources.create(source=token)
            if address_obj:
                # set new info on card
                stripe_card.address_city = address_obj.addressCity
                stripe_card.address_country = address_obj.addressCountry 
                stripe_card.address_line1 = address_obj.addressLine1 
                stripe_card.address_line2 = address_obj.addressLine2 
                stripe_card.address_state = address_obj.addressState
                stripe_card.address_zip = address_obj.addressPostalCode
                stripe_card.name = address_obj.addressName
                stripe_card.save()

            print(remember)
            if remember:
                new_card = self.model(
                    billingProfile=billing_profile,
                    cardStripeID=stripe_card.id,
                    cardBrand=stripe_card.brand,
                    cardCountry=stripe_card.country,
                    cardExpMonth=stripe_card.exp_month,
                    cardExpYear=stripe_card.exp_year,
                    cardLast4=stripe_card.last4,
                    cardAddressLine1=stripe_card.address_line1,
                    cardAddressLine2=stripe_card.address_line2,
                    cardCity=stripe_card.address_city,
                    cardState=stripe_card.address_state,
                    cardPostalCode=stripe_card.address_zip,
                    cardName=stripe_card.name,
                )
            else:
                new_card = self.model(
                    billingProfile=billing_profile,
                    cardStripeID=stripe_card.id,
                    cardBrand=stripe_card.brand,
                    cardCountry=stripe_card.country,
                    cardExpMonth=stripe_card.exp_month,
                    cardExpYear=stripe_card.exp_year,
                    cardLast4=stripe_card.last4,
                    cardAddressLine1=stripe_card.address_line1,
                    cardAddressLine2=stripe_card.address_line2,
                    cardCity=stripe_card.address_city,
                    cardState=stripe_card.address_state,
                    cardPostalCode=stripe_card.address_zip,
                    cardName=stripe_card.name,
                    cardActive=False,
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
    cardActive = models.BooleanField(default=True)
    cardDateAdded = models.DateTimeField(auto_now_add=True)

    cardName = models.CharField(max_length=120, null=True, blank=True)
    cardCity= models.CharField(max_length=120, null=True, blank=True)
    cardAddressLine1 = models.CharField(max_length=120, null=True, blank=True)
    cardAddressLine2 = models.CharField(max_length=120, null=True, blank=True)
    cardState= models.CharField(max_length=120, null=True, blank=True)
    cardPostalCode= models.CharField(max_length=120, null=True, blank=True)


    objects = CardManager()

    def __str__(self):
        return '{} {}'.format(self.cardBrand, self.cardLast4)

    class Meta:
        db_table = 'card'

# creates billing profile on user creation
def new_card_post_save_receiver(sender, instance, created, *args, **kwargs):
    if instance.cardDefault:
        billing_profile = instance.billingProfile
        qs = Card.objects.filter(billingProfile=billing_profile).exclude(pk=instance.pk)
        qs.update(cardDefault=False)
post_save.connect(new_card_post_save_receiver, sender=Card)

class ChargeManager(models.Manager):
    def do(self, billing_profile, sale_obj, card):
        card_obj = card
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