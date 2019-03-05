# Clothing Store e-commerce site

Created using https://www.youtube.com/playlist?list=PLV2_Iivd4jxYVDWCcxmccusNaUx2kWCg1 as a guide. If I did anything weird look here to get some perspective on my methodology. I do cart stuff, and pricing differently to preserve historical data, allow for time based pricing, and allow for inventory management. Some other stuff might also be slightly different.

## Note on variable naming in this project

When I started this project I was unaware of best practices when naming variables in Python. As a result, the variable names are inconsistent in style. For the most part, I have used conventional Python styling in everything except the names of the model fields. Those use camelCase with the exception of some stuff in BillingProfile (I'm so sorry).

## Environment Setup  

### Have postgresql server setup

Install postgresql  

Create a database and database user.  
Give all permissions on database for user.  


### Install virtualenv and setup create app environment

install python 3  
install virtualenv  https://pypi.org/project/virtualenv/  
     
     pip install virtualenv
create virtualenv  
     
     virtualenv myenv

### Clone repo in environment

cd into virtualenv and clone

     cd myenv
     git clone https://github.com/honeybox-boutique/django-ecommerce.git
cd into project and install requirements.txt
     
     pip install -r requirements.txt
       
create copy of base_keys.template and rename to base_keys.py  
enter db info from database created earlier into base_keys.py. Include API test keys if testing API functionality.

     required: 
     DB_NAME = 'dbname'
     DB_USER = 'dbuser'
     DB_PASSWORD = 'dbpass'
     DB_HOST = '127.0.0.1'
     DB_PORT = '5432'
     
     
     need api keys to test payment processing functionality and shipping label creation
     need valid gmail account to test email sending functionality
set static root and media root in speedtest/settings/base.py to file path where static files will be collected. The file paths must end with static/ and media/ respectively.

     STATIC_ROOT = 'C:/Users/Jondoe/Path/To/local/static-cdn/static/'

     MEDIA_ROOT = 'C:/Users/Jondoe/Path/To/local/static-cdn/media/'
     
make database migrations

     python manage.py migrate
collect static files

     python manage.py collectstatic
run it 

     python manage.py runserver  

## Apps

*addresses - manages addresses  
*billing - manages stripe stuff, payment info  
coupons - used to process coupon codes  
*emails - manage contact us page functionality  
homepage - manage home page images  
pricing - manage product pricing and discounts  
products - manage products  
-purchases	- manage product inventory purchases  
*sales - manage sales creation and stuff  
*shipping - manage easypost stuff, send shipping emails  
*shopcart - manage user shopcart as well as checkout home view  
speedtest - main appp. want to rename to eccomerce, haven't had time to figure out how  
tax - manages sales tax charged to customer based on shipping address and jurisdictions  
*users - manages users and guests, django.conrtib.auth mainly  

## Things I need help with in order of importance:
     billing
          make sure adding payment methods adding/removing is seamless and error messages appear appropriately
     addresses
          make sure addresses application is running as expected
     shopcart
          fix add to cart stuff by adding model manager method to do it correctly (for details on bug scroll down to 'Thing to note...'> 'Shopping Cart')
          make sure that when purchitems becomes unavailable that user carts will add the next available purchitem matching criteria
          add quantity to add to cart form and add that logic to everywhere else
     sales
          make sure historical data is preserved
          optimize checkout process so it isn't re-adding everything from cart, checking for discounts, checking sales tax stuff, etc.  every time the page is reloaded in checkout process
     users
          I want to make emails unique for users since that is the main way to identify unique customers via stripe
          
     This stuff isn't as important-------------------------------------------------------------------------
     models settings stuff
          When should I set null=True, blank=True, etc. on model?
          When to set models.CASCADE=PROTECT or other?
     testing apps in general
          best software/way to test stuff in Django?
     make admin more usable
          how to show other fields other than self in listview of admin site
          change purchases > purchaseitems so that it uses quantity field
     emails
          can we just attach images to emails and send them without worry? Have read warnings about transactional emails getting blocked by gmail servers.
          why would we use email sending service like mailchimp?
     shipping
          make multi-shipment orders possible (will require saleid to be editable for shipment on admin site)
          do error handling
     image/static content delivery optimization
          inform me of best practices in django with AWS s3



## Things to note about functionality of site     

### All

     The admin site has NOT been tested with invalid inputs at all. For the time being I'm going to save this for later and assume admin of site will enter everything correctly
     The public-facing stuff has been LIGHTLY tested. I haven't had time to do more. 
     I know for a fact there a couple views that are using uncleaned post data for things. Couldn't figure out how to add needed field to form and put it through cleaned_data method.

### Products  
     
          make sure you have added the following to display a product for sale:  
               -add the product itself to products  
               -add active pricing for product  
               -productcolors imageset  
               -applicable discounts  

### Billing Profiles  
     
          a billing profile is supposed to represent a stripe customer.  
          It is created when clicking on 'checkout' in cart view and then continuing as guest or as user.  
          
          There are 'user' billing profiles and 'guest' billing profiles  
          user  
               a billing profile can only be associated with one user  
          guest  
               same as user billing profile except profile type is guest and user association is null   
               will be marked inactive if guest navigates away from checkout or upon checkout finish  
### Shopping Carts

     Currently a user can have multiple shopping cart per the model, but I have written the code intending to make it a one-to-one relationship
     Currently, shopcart status does absolutely nothing
     Currently, adding a product to shopping cart adds the first purchaseitem from inventory that matches post criteria. 
          This is causing issues when the item eventually gets purchased. 
          Any other shoppers who have that purchase item in their cart will have it removed automatically by the model manager as it is no longer available.
          Need to fix this somehow
### Sales
     
     -When user clicks checkout and continues as either guest or user, a sale gets created with a status of 'created'.
          The users shopcart items get copied into the saleitems as well. 
          Every request in the checkout process (even refreshing page)  will recopy items from cart. 
          This is to recheck the availability of the items in the cart. 
          If the item is no longer available, the item is automatically removed from the cart and the user is redirected to cart home.
               Want to change this so it will check if another purchitem is available with same product attributes
     -Sale status determines whether or not the saleitems, salediscounts and other related items will be modified.
     -Upon checkout completion sale gets marked payed. as a result it is no longer changed by my code (I think)
### Shipping

     Currently, a sale can have one to many shipments
     Currently, a shipment can have one to many parcels
     Easypost api calls do not have error handling currently
     I have only tested making one shipment with a single parcel per sale. 
          Will need to make it so admin can create additional shipments if items can't fit in 1 shipment
          
## Data models  

### addresses  

    address
        addressBillingProfile - billing profile associated with address  
        addressType - address type (billing or shipping)  
        addressLine1  
        addressLine2  
        addressCity  
        addressCountry  
        addressState  
        addressPostalCode  
        addressName - Full name of individual associated with address  
        addressActive - used to determine if address should be shown in existing addresses for user that is logged in  
        addressEasyPostID - easypost address token  

### billing 

    billingprofile - represents stripe customer
        billingEmail = email associated with billing profile  
        active = status of billing profile  
        lastUpdated  
        dateCreated  
        profileType - either 'user' billing profile or 'guest'. guest billing profiles get marked inactive after transaction  
        user = user associated with billing profile if any  
        billingToken = stripe customer token. generated from pre save signal if token doesn't exist and email isn't blank 
    card
        billingProfile = billing profile associated with card
        cardStripeID = cards stripe id. Generated in model manager method add_new
        cardBrand = brand of card
        cardCountry = models.CharField(max_length=20, null=True, blank=True)
        cardExpMonth = probably removing this, can't think of reason to store it
        cardExpYear = probably removing this, can't think of reason to store it
        cardLast4 = last 4 of card
        cardDefault = i don't think this currently does anything. Would like to allow setting one default card in user dashboard eventually 
        cardActive = determines if card shows up in existing payment methods when user is authenticated. Inactive cards can still be charged I think.
        cardDateAdded = models.DateTimeField(auto_now_add=True)
        
        This stuff is pretty much the billing address. creating a relation between card and addresses posed to much of a problem so I just duplicated the data on the card model. Not sure what happens if customer removes (makes inactive) the address associated with the card. 
        cardName = full name on card
        cardCity= city on card
        cardAddressLine1 = models.CharField(max_length=120, null=True, blank=True)
        cardAddressLine2 = models.CharField(max_length=120, null=True, blank=True)
        cardState= models.CharField(max_length=120, null=True, blank=True)
        cardPostalCode= models.CharField(max_length=120, null=True, blank=True)
    charge - represents an attempt to charge a card. currently only saving successful charges to model
        billingProfile = billing profile associated with charge
        chargeStripeID = charge stripe id
        chargePaid = was charge paid successfully?
        chargeRefunded = was charge refunded?
        chargeOutcome = charge outcome from stripe
        chargeOutcomeType = outcome type from stripe
        chargeSellerMessage = seller message from stripe
        chargeRiskLevel = risk level from stripe
        
### homepage

    homepageimage - smaller images displayed on home page 
        homePageImagePath - 
        homePageImageAltText = 
        homePageImageLink =
    bighomepageimage - banner image on home page
        bigHomePageImagePath = 
        bigHomePageImageAltText = 
        bigHomePageImageLink = 
### pricing

    pricing - a pricing for specific period of time for specific product
        pricingBasePrice = base price of product, not including any discounts.
        pricingDateCreated = models.DateTimeField('date created', auto_now_add=True)
        pricingValidFrom = models.DateTimeField('start date')
        pricingValidUntil = models.DateTimeField('end date')
        pricingNote = notes. currently what is being displayed in admin listview
        pricingIsActive = calculated field. calculated on pre_save signal for pricing based on dates
        
        productID = product the pricing is for
    
    pdiscount
        pDiscountID = primary key  
        pDiscountName = name of discount. displayed in checkout cart display  
        pDiscountDescription = description of discount
        pDiscountType = dollar amount or percentage discount
        pDiscountValue = discount value
        pDiscountDateCreated = models.DateTimeField('date created', auto_now_add=True)  
        pDiscountDateValidFrom = models.DateTimeField('valid from')  
        pDiscountDateValidUntil = models.DateTimeField('valid until')  
        pDiscountCouponCode = coupon code. currently not used, all product discounts are applied automatically. will eventually allow for non-automatic pdiscounts.  
        pDiscountMaxDiscount = currently doesn't do anything. was thinking of adding something like this to make sure things remain profitable.
        pDiscountMinOrderValue = currently doesn't do anything. was thinking of adding something like this to make sure things remain profitable. 
        pDiscountIsActive = calculated field. calculated on pre_save signal for pdiscount based on dates

        productID = product discount is associated with
    cdiscount
        cDiscountID = primary key
        cDiscountName = discount name
        cDiscountDescription = discount description
        cDiscountType = dollar amount or percent
        cDiscountValue = discount value
        cDiscountDateCreated = models.DateTimeField('date created', auto_now_add=True)
        cDiscountDateValidFrom = models.DateTimeField('valid from')
        cDiscountDateValidUntil = models.DateTimeField('valid until')
        cDiscountCouponCode = coupon code. currently not used, all product discounts are applied automatically. will eventually allow for non-automatic pdiscounts.  
        cDiscountMaxDiscount = models.DecimalField(max_digits=12, decimal_places=2)
        cDiscountMinOrderValue = models.DecimalField(max_digits=12, decimal_places=2)
        cDiscountIsActive = calculated field. calculated on pre_save signal for cdiscount based on dates
        categoryID = category discount applies to
        
    sdiscount  
        sDiscountID = primary key
        sDiscountName = discount name
        sDiscountDescription = discount description
        sDiscountMessage = message displayed in checkout when discount applied  
        sDiscountType = dollar amount or percent
        sDiscountValue = discount value
        sDiscountDateCreated = models.DateTimeField('date created')  
        sDiscountDateValidFrom = models.DateTimeField('valid from')  
        sDiscountDateValidUntil = models.DateTimeField('valid until')  
        sDiscountCouponCode = coupon code. used to lookup active discounts when user attempts to add discount with coupon code
        sDiscountMaxAmount = maximum discount for sale.
        sDiscountMinSaleValue = minimum sale subtotal value
        sDiscountAutomatic = determines if discount is automatically applied  
        sDiscountIsShippingDiscount = is this a shipping cost discount? if so won't be displayed in discount in checkout
        sDiscountIsActive = calculated field. calculated on pre_save signal for sdiscount based on dates
    sdiscountcondition - conditions to check before adding applying sdiscount to sale
        sDCID = primary key
        sDCName = condition name
        sDCFailMessage = message user sees if order doesn't meet conditions
        sDCType = is condition based on an product attribute, sale attribute, or user attribute. User attribute based conditions don't currently work  
        sDCFieldName = name of attribute field for product, sale or user
        sDCCompareOperator = comparison operator to use in condition check
        sDCValue = attribute value that needs to be set for condition check to pass 
        sDCNumRequired = minimum number of items that need to pass condition check for discount to be applied

        sDiscountID = sale discount condition is associated with  
    


### products
    
    color  
        colorID = models.AutoField(primary_key=True)
        colorName = models.CharField(max_length=50)
        colorDescription = models.TextField(max_length=200)
    
    category  
        categoryName = models.CharField(max_length=200)
        categoryDescription = models.CharField(max_length=200)
    
    categoryimage  
        categoryImageID = models.AutoField(primary_key=True)
        categoryImagePath = models.ImageField(upload_to='categories')
        categoryID = models.ForeignKey(Category, on_delete=models.CASCADE)
    
    size  
        sizeID = models.AutoField(primary_key=True)
        sizeName = models.CharField(max_length=200)
        sizeDescription = models.TextField(max_length=200)
        sizeNotes = models.TextField(max_length=255)
    
    product  
        productID = models.AutoField(primary_key=True)
        productName = models.CharField(max_length=200)
        productDescription = models.TextField(max_length=200)
        productSlug = models.SlugField(unique=True)
        productCategories = models.ManyToManyField(Category)
        productSizes = models.ManyToManyField(Size)
        #Calculated fields
        productDiscountAmount = models.DecimalField(null=True, max_digits=12, decimal_places=2)
        productSalePrice = models.DecimalField(null=True, max_digits=12, decimal_places=2)
        productBasePrice = models.DecimalField(null=True, max_digits=12, decimal_places=2)
        productDiscountType = models.CharField(null=True, max_length=40)
        productDiscountValue = models.DecimalField(null=True, max_digits=12, decimal_places=2)
        colorID = models.ManyToManyField(Color, through='ProductColor')
        
    productcolor  
        productColorID = models.AutoField(primary_key=True)
        productColorName = models.CharField(max_length=120)

        productID = models.ForeignKey(Product, on_delete=models.CASCADE)
        colorID = models.ForeignKey(Color, on_delete=models.CASCADE)
    productimage  
        productImageID = models.AutoField(primary_key=True)
        productImagePath = models.ImageField(upload_to='products')
        # will Add alt text field here - productImageAltText = models.CharField(max_length=40)
        productColorID = models.ForeignKey(ProductColor, on_delete=models.CASCADE)
### purchases  

    vendor
        vendorID = models.AutoField(primary_key=True)
        vendorName = models.CharField(max_length=40)
        vendorDescription = models.TextField(max_length=200)
        vendorNotes = models.TextField(max_length=200)
        vendorWebsite = models.URLField(max_length=200)
    purchase  
        purchaseID = models.AutoField(primary_key=True)
        purchaseDate = models.DateTimeField('date purchased')
        purchaseNote = models.TextField(max_length=200)
        purchaseStatus = models.CharField(max_length=40)

        productID = models.ManyToManyField(Product, through='PurchaseItems')
        userID = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    purchaseitems  
        prodStockID = models.AutoField(primary_key=True)
        piPrice = models.DecimalField(max_digits=8, decimal_places=3)
        piCondition = models.CharField(max_length=50)
        piNotes = models.TextField(max_length=200)
        piBarcode = models.ImageField(upload_to='barcodes', blank=True, null=True)
        piSize = models.ForeignKey(Size, on_delete=models.CASCADE)
        piColor = models.ForeignKey(Color, on_delete=models.CASCADE)
        purchaseID = models.ForeignKey(Purchase, on_delete=models.CASCADE)
        productID = models.ForeignKey(Product, on_delete=models.CASCADE)
        vendorID = models.ForeignKey(Vendor, on_delete=models.CASCADE)
        # field to determine if item is available for sale
        piIsAvailable = models.BooleanField(default=True)
### sales	

    customershipmethod  
        cSMID = models.AutoField(primary_key=True)
        cSMName = models.CharField(max_length=120)
        cSMDescription = models.TextField(max_length=200)
        cSMChargeAmount = models.DecimalField(default=0.00, max_digits=12, decimal_places=2)
        
    sale  
        saleID = models.AutoField(primary_key=True)
        saleStringID = models.CharField(max_length=120, blank=True)
        saleDate = models.DateTimeField('sale date', auto_now_add=True)
        saleNote = models.CharField(max_length=120, default='Sale')
        saleStatus = models.CharField(max_length=120, default='created', choices=SALE_STATUS_CHOICES) # purchaseDate = models.DateTimeField('date purchased')
        saleSubTotal = models.DecimalField(default=0.00, max_digits=12, decimal_places=2)# Amount should be sum(saleitemprice - p-cDiscount)
        saleDiscountAmount = models.DecimalField(default=0.00, max_digits=12, decimal_places=2)
        saleTaxAmount = models.DecimalField(default=0.00, max_digits=12, decimal_places=2)

        # change: add saleShippingMethod
        customerShipMethodID = models.ForeignKey(CustomerShipMethod, on_delete=models.PROTECT, null=True, blank=True)
        # customer shipping and total
        saleShipCostAmountCharged = models.DecimalField(default=0.00, max_digits=12, decimal_places=2)# change: integrate shipping API
        # saleCustomerTotal - not inclusive of shipping cost that we are paying

        # actual total
        saleTotal = models.DecimalField(default=0.00, max_digits=12, decimal_places=2)
        # saleTotalShippingCost - total shipping cost including portion we are paying

        saleShippingAddress = models.ForeignKey(Address, related_name='saleShippingAddress', null=True, blank=True, on_delete=models.PROTECT)
        saleBillingAddress = models.ForeignKey(Address, related_name='saleBillingAddress', null=True, blank=True, on_delete=models.PROTECT)
        saleDiscounts = models.ManyToManyField(SDiscount, blank=True)
        saleItems = models.ManyToManyField(PurchaseItems, through='SaleItems')
        saleBillingProfile = models.ForeignKey(BillingProfile, on_delete=models.CASCADE)
        salePaymentCard = models.ForeignKey(Card, on_delete=models.CASCADE, blank=True, null=True)
        
    saleitems  
        saleItemID = models.AutoField(primary_key=True)
        siBasePrice = models.DecimalField(default=0.00, max_digits=12, decimal_places=2)
        siDiscountAmount = models.DecimalField(default=0.00, max_digits=12, decimal_places=2)
        siSalePrice = models.DecimalField(default=0.00, max_digits=12, decimal_places=2)# change: add sensor to calculate this
        siNote = models.CharField(default='SaleItem', max_length=120, blank=True)# change: add sensor to populate this

        saleID = models.ForeignKey(Sale, on_delete=models.CASCADE)
        prodStockID = models.ForeignKey(PurchaseItems, on_delete=models.PROTECT)
### shipping	

    warehouse  
        warehouseID = models.AutoField(primary_key=True)
        warehouseName = models.CharField(max_length=120)
        warehouseAddress = models.ForeignKey(Address, on_delete=models.PROTECT)
        
    shipment  
        shipmentID = models.AutoField(primary_key=True)
        shipmentDateRequested = models.DateTimeField('shipment date created')
        shipmentDateLabelPrinted = models.DateTimeField('shipment date label printed', blank=True, null=True)
        shipmentNote = models.CharField(max_length=120, default='Default Shipment Note')
        warehouseID = models.ForeignKey(Warehouse, on_delete=models.PROTECT, blank=True, null=True)
        shipmentToAddress = models.ForeignKey(Address, related_name='shipmentToAddress', null=True, blank=True, on_delete=models.PROTECT)
        # shipmentToAddress = models.ForeignKey(Address, on_delete=models.PROTECT)
        shipmentLabelIsBought = models.BooleanField(default=False)

        # maybe add shipmentStatus to clarify IsBought
        shipmentStatus = models.CharField(max_length=120, default='in progress', choices=SHIPMENT_STATUS_CHOICES)

        saleID = models.ForeignKey(Sale, on_delete=models.CASCADE)

        shipmentCarrier = models.CharField(max_length=120, choices=CARRIER_OPTIONS)
        shipmentRate = models.CharField(max_length=120, choices=RATE_OPTIONS)
        # easypost providedstuff
        shipmentEasyPostID = models.CharField(max_length=120, blank=True, null=True)
        shipmentCost = models.DecimalField(default=0.00, max_digits=12, decimal_places=2)
        shipmentTrackingNumber = models.CharField(max_length=120, blank=True, null=True)
        shipmentTrackingURL = models.URLField(verbose_name='tracking url', blank=True, null=True)
        shipmentLabelURL = models.URLField(blank=True, null=True)

        shipmentReturnEasyPostID = models.CharField(max_length=120, blank=True, null=True)
        shipmentReturnLabelCost = models.DecimalField(default=0.00, max_digits=12, decimal_places=2)
        shipmentReturnTrackingNumber = models.CharField(max_length=120, blank=True, null=True)
        shipmentReturnLabelURL = models.URLField(blank=True, null=True)
        
    parcel  
        parcelID = models.AutoField(primary_key=True)
        parcelName = models.CharField(max_length=120, choices=PARCEL_NAME_CHOICES)# change: add predefined package names as choices
        parcelWeight = models.DecimalField(default=0.00, max_digits=12, decimal_places=2)
        shipmentID = models.ForeignKey(Shipment, on_delete=models.CASCADE)
        
### shopcart	

    shopcart  
        user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
        shopCartDateCreated = models.DateTimeField(auto_now_add=True)
        shopCartLastModified = models.DateTimeField(auto_now=True)

        shopCartStatus = models.CharField(max_length=40, default=OPEN, choices=STATUS_CHOICES)

        shopCartSubTotal = models.DecimalField(default=0.00, max_digits=12, decimal_places=2)

        shopCartItems = models.ManyToManyField(PurchaseItems, blank=True)
        objects = ShopCartManager()
### tax	 

    jurisdiction  
        jurisdictionID = models.AutoField(primary_key=True)
        jurisdictionLabel = models.CharField(max_length=70)

        # unique for a jurisdiction
        jurisdictionState = models.CharField(max_length=50, blank=True, null=True)
        jurisdictionCity = models.CharField(max_length=50, blank=True, null=True)
        jurisdictionZip = models.CharField(max_length=12, blank=True, null=True)
        
    taxrate  
        taxRateID = models.AutoField(primary_key=True)
        taxRateName = models.CharField(max_length=50)
        taxRateMultiplier = models.DecimalField(max_digits=12, decimal_places=4)
        taxRateDateCreated = models.DateTimeField('date created', auto_now_add=True)
        taxRateValidFrom = models.DateTimeField('start date')
        taxRateValidUntil = models.DateTimeField('end date')
        taxRateNote = models.TextField(max_length=200)
        taxRateIsActive = models.BooleanField(default=False)

        jurisdictionID = models.ForeignKey(Jurisdiction, on_delete=models.CASCADE)
    
### users	

    default django auth (want to override to make emails unique asap)  
    
    guest  
        guestEmail = models.EmailField()
        guestActive = models.BooleanField(default=True)
        guestDateLastUpdated = models.DateTimeField(auto_now=True)
        guestDateCreated = models.DateTimeField(auto_now_add=True)
        guestSendPromos = models.BooleanField(default=False)


## How to manage the site

### Common tasks:

#### Add product for sale  

     -Add product itself  
     -Add product colorset (productcolors in admin site)  
          Colorset is a set of images that correspond to a product color  
               e.g. Test Top - Red  
     -Add product colorset images  
          find colorset in productcolors admin page  
          upload images as desired. First image will be displayed on listing  
  
     -Add product pricing  
     # if you want to be able to add item to cart, add purchase for product
     -Record product stock purchases  
     # product and category level discounts can be added in pricing>pdisctounts/cdiscounts
     -Add product discount  
     -Add product category discount
     # sale level discounts can be added in pricing>sdiscounts. You will have to create salediscountcondition for sale discount. That code is really hacky and will need to be changed in the future probably.
     -Add sale discount  


