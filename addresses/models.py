from django.db import models

from billing.models import BillingProfile

ADDRESS_TYPES = (
    ('billing', 'Billing'),
    ('shipping', 'Shipping'),
)

class Address(models.Model):
    addressBillingProfile = models.ForeignKey(BillingProfile, on_delete=models.CASCADE)
    addressType = models.CharField(max_length=120, choices=ADDRESS_TYPES)
    addressLine1 = models.CharField(max_length=120)
    addressLine2 = models.CharField(max_length=120, null=True, blank=True)
    addressCity = models.CharField(max_length=120)
    COUNTRY_CHOICES = (
        ('United States', 'United States'),
    )
    addressCountry = models.CharField(max_length=120, default='United States', choices=COUNTRY_CHOICES)
    STATE_CHOICES = (
        ('AL', 'Alabama'), 
        ('AK', 'Alaska'), 
        ('AZ', 'Arizona'), 
        ('AR', 'Arkansas'), 
        ('CA', 'California'),
        ('CO', 'Colorado'),
        ('CT', 'Connecticut'), 
        ('DE', 'Delaware'), 
        ('FL', 'Florida'), 
        ('GA', 'Georgia'), 
        ('HI', 'Hawaii'), 
        ('ID', 'Idaho'), 
        ('IL', 'Illinois'), 
        ('IN', 'Indiana'), 
        ('IA', 'Iowa'), 
        ('KS', 'Kansas'), 
        ('KY', 'Kentucky'), 
        ('LA', 'Louisiana'), 
        ('ME', 'Maine'), 
        ('MD', 'Maryland'), 
        ('MA', 'Massachusetts'), 
        ('MI', 'Michigan'), 
        ('MN', 'Minnesota'), 
        ('MS', 'Mississippi'), 
        ('MO', 'Missouri'), 
        ('MT', 'Montana'), 
        ('NE', 'Nebraska'), 
        ('NV', 'Nevada'), 
        ('NH', 'New Hampshire'), 
        ('NJ', 'New Jersey'),
        ('NM', 'New Mexico'),
        ('NY', 'New York'),
        ('NC', 'North Carolina'),
        ('ND', 'North Dakota'),
        ('OH', 'Ohio'), 
        ('OK', 'Oklahoma'), 
        ('OR', 'Oregon'), 
        ('PA', 'Pennsylvania'), 
        ('RI', 'Rhode Island'), 
        ('SC', 'South Carolina'),
        ('SD', 'South Dakota'), 
        ('TN', 'Tennessee'), 
        ('TX', 'Texas'), 
        ('UT', 'Utah'), 
        ('VT', 'Vermont'), 
        ('VA', 'Virginia'), 
        ('WA', 'Washington'), 
        ('WV', 'West Virginia'),
        ('WI', 'Wisconsin'),
        ('WY', 'Wyoming'), 
        ('AS', 'American Samoa'),
        ('DC', 'District of Columbia'),
        ('FM', 'Federated States of Micronesia'),
        ('GU', 'Guam'),
        ('MH', 'Marshall Islands'),
        ('MP', 'Northern Mariana Islands'),
        ('PW', 'Palau'),
        ('PR', 'Puerto Rico'),
        ('VI', 'Virgin Islands'),
    )
    addressState = models.CharField(max_length=120, choices=STATE_CHOICES)
    addressPostalCode = models.CharField(max_length=120)

    addressName = models.CharField(max_length=150, null=True, blank=True)

    addressActive = models.BooleanField(default=True)

    addressEasyPostID = models.CharField(max_length=120, blank=True, null=True)


    def __str__(self):
        return str(self.addressBillingProfile) + ' ' + self.addressLine1
