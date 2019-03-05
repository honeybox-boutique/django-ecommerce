# Django/Ptyon e-commerce site

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
        colorID = primary key
        colorName = models.CharField(max_length=50)
        colorDescription = models.TextField(max_length=200)
    
    category  
        categoryName = models.CharField(max_length=200)
        categoryDescription = models.CharField(max_length=200)
    
    categoryimage  
        categoryImageID = primary key
        categoryImagePath = models.ImageField(upload_to='categories')
        categoryID = models.ForeignKey(Category, on_delete=models.CASCADE)
    
    size  
        sizeID = primary key
        sizeName = models.CharField(max_length=200)
        sizeDescription = models.TextField(max_length=200)
        sizeNotes = models.TextField(max_length=255)
    
    product  
        productID = primary key
        productName = product name
        productDescription = product description
        productSlug = product slug. currently not using unique slug generator
        productCategories = categories product gets displayed in / discounts applied
        productSizes = size options for product
        #Calculated fields - calculated on pricing, pdiscount, and cdiscount signals I think
        productDiscountAmount = current discount amount based on active pricing and active product and category discounts
        productSalePrice = current final product sale price inclusive of highest between pdiscount/cdiscount
        productBasePrice = current active product base price
        productDiscountType = dollar amount or percentage. type of applied discount if any
        productDiscountValue = discount value
        
        # colorID - relationship to many to many intermediary table productcolor. This is used to load image sets for every productcolor instance. This way each color will have unique image set. Should probably be renamed to productcolorimageset or something.
        colorID = models.ManyToManyField(Color, through='ProductColor')
        
    productcolor  
        productColorID = primary key
        productColorName = name of productcolor imageset. Have been using the following names: PRODUCT NAME - COLOR

        productID = product associated with color imageset
        colorID = color associated with color imageset
    productimage  
        productImageID = primary key
        productImagePath = path to image
        # will Add alt text field here - productImageAltText = models.CharField(max_length=40)
        
        productColorID = color imageset image is associated with
### purchases  

    vendor
        vendorID = primary key
        vendorName = models.CharField(max_length=40)
        vendorDescription = models.TextField(max_length=200)
        vendorNotes = models.TextField(max_length=200)
        vendorWebsite = models.URLField(max_length=200)
    purchase - inventory purchase from vendor
        purchaseID = primary key
        purchaseDate = models.DateTimeField('date purchased')
        purchaseNote = purchase note. currently what is displayed in admin listview
        purchaseStatus = status of purchase.
        
        # This related table represent one item in inventory. Whether or not someone can add something to cart depends on if there is a purchaseitem that is available
        productID = models.ManyToManyField(Product, through='PurchaseItems')
        # User that logged purchase. probably need to make this require administrative user somehow
        userID = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    purchaseitems  
        prodStockID = primary key
        piPrice = price inventory item was purchased for
        piCondition = current condition. not used for anything right now
        piNotes = notes. not used for anything right now
        piBarcode = not used right now. may eventually implement barcodes here or on product model
        # size of purch item
        piSize = models.ForeignKey(Size, on_delete=models.CASCADE)
        # color of purch item
        piColor = models.ForeignKey(Color, on_delete=models.CASCADE)
        # purchase associated with purchitem
        purchaseID = models.ForeignKey(Purchase, on_delete=models.CASCADE)
        # product that purchitem is
        productID = models.ForeignKey(Product, on_delete=models.CASCADE)
        # vendor of purchitem
        vendorID = models.ForeignKey(Vendor, on_delete=models.CASCADE) 
        piIsAvailable = field to determine if item is available for sale. marked unavailable if included in sale
### sales	

    customershipmethod  - shipping method options for customers on site
        cSMID = primary key
        cSMName = ship method name
        cSMDescription = ship method description. This will probably be used to display ship method options in checkout
        cSMChargeAmount = amount to charge for this ship method
        
    sale  
        saleID = primary key
        saleStringID = ID generated from util that is more readable/usable to lookup stuff
        saleDate = models.DateTimeField('sale date', auto_now_add=True)
        saleNote = currently not used. may add something here
        saleStatus = status of sale. defuault is created. anything created can be modified, else changes won't  be applied (i think) choices=SALE_STATUS_CHOICES)
        
        #calculated fields
        saleSubTotal = sum of sale item sale prices (inclusive of p/cdiscounts), sum(saleitemprice - p-cDiscount). this is retrieved from cart subtotal I think on sale save
        saleDiscountAmount = discount amount for sale level discounts applied. calculated on sale save
        saleTaxAmount = tax amount charged. calculated on sale save. Based on shipping state, city, and zip.        
        # customer ship method selection
        customerShipMethodID = models.ForeignKey(CustomerShipMethod, on_delete=models.PROTECT, null=True, blank=True)
        # customer shipping and total
        saleShipCostAmountCharged = shipping cost charged to customer. retrieved from shipmethod selection

        saleTotal = actual total for sale
        # might include saleTotalShippingCost - total shipping cost including portion we are paying
        # shipping address associated with sale
        saleShippingAddress = models.ForeignKey(Address, related_name='saleShippingAddress', null=True, blank=True, on_delete=models.PROTECT)
        # billing address associated with sale
        saleBillingAddress = models.ForeignKey(Address, related_name='saleBillingAddress', null=True, blank=True, on_delete=models.PROTECT)
        # applied discounts for sale
        saleDiscounts = models.ManyToManyField(SDiscount, blank=True)
        # sale items included in sale
        saleItems = models.ManyToManyField(PurchaseItems, through='SaleItems')
        # billing profile associated with sale
        saleBillingProfile = models.ForeignKey(BillingProfile, on_delete=models.CASCADE)
        # payment card associated with sale
        salePaymentCard = models.ForeignKey(Card, on_delete=models.CASCADE, blank=True, null=True)
        
    saleitems  - items in sale
        saleItemID = primary key
        siBasePrice = sale item base price
        siDiscountAmount = amount discounted
        siSalePrice = sale item sale price
        siNote = not used currently. might add something here
        # sale saleitem is associated with
        saleID = models.ForeignKey(Sale, on_delete=models.CASCADE)
        # inventory item associated with sale
        prodStockID = models.ForeignKey(PurchaseItems, on_delete=models.PROTECT)
### shipping	

    warehouse - used in shipping label 'from' address
        warehouseID = primary key
        warehouseName = warehouse name
        # currently associated with address model. forces address to be associated with user. might change this since it really doesn't  make sense
        warehouseAddress = models.ForeignKey(Address, on_delete=models.PROTECT)
        
    shipment  - shipment associated with sale. currently created automatically when sale is marked payed
        shipmentID = primary key
        shipmentDateRequested = date shipment was automatically generated from sale payment
        shipmentDateLabelPrinted = date shipment label was printed
        shipmentNote = currently not used. might use in future
        # warehouse product will come from. used as from address in shipping label
        warehouseID = models.ForeignKey(Warehouse, on_delete=models.PROTECT, blank=True, null=True)
        # to address in shipping label. address is pulled from sale
        shipmentToAddress = models.ForeignKey(Address, related_name='shipmentToAddress', null=True, blank=True, on_delete=models.PROTECT)
        shipmentLabelIsBought = used to determine whether the shipping label should be bought. If checked, label is bought and shipment status is changed to 'printed'. 

        shipmentStatus = used to send email to customer. if marked 'printed' an email will be sent out. Could pose problems with multi-shipment orders. may need to add bool field to allow create shipment without sending email.
        #sale associated with shipment
        saleID = models.ForeignKey(Sale, on_delete=models.CASCADE)

        shipmentCarrier = shipping carrier. have hardcoded these options.
        shipmentRate = shipping rate. hardcoded these options.
        
        # easypost providedstuff
        shipmentEasyPostID = models.CharField(max_length=120, blank=True, null=True)
        shipmentCost = cost if label is used
        shipmentTrackingNumber = tracking number
        shipmentTrackingURL = tracking url
        shipmentLabelURL = label url for printing
        
        # currently return labels are being bought for every sale. might change this so customers will have to enter a saleid on returns page and will then get a link to the label via email or something.
        shipmentReturnEasyPostID = return label id
        shipmentReturnLabelCost = return label cost if used
        shipmentReturnTrackingNumber = return label tracking number
        shipmentReturnLabelURL = return label url for printing
        
    parcel - package included in shipment. currently shipment can have multiple parcels per model definition. USPS doesn't allow this so only one parcel can be added per shipment. might change relationship accordingly depending on what other carriers do and whether they allow multi-parcel shipments.
        parcelID = primary key
        parcelName = name of package selection. options hardcoded from USPS options
        parcelWeight = weight in ounces of package
        
        #shipment parcel is associated with
        shipmentID = models.ForeignKey(Shipment, on_delete=models.CASCADE)
        
### shopcart	

    shopcart  - user/guest shopping cart
        user = user associated with shop cart. onetoone relation.
        shopCartDateCreated = models.DateTimeField(auto_now_add=True)
        shopCartLastModified = models.DateTimeField(auto_now=True)
        shopCartStatus = not currently doing anything. may be useful to check if cart was changed.
        shopCartSubTotal = subtotal of items in cart inclusive of discounts
        
        # items in shopping cart
        shopCartItems = models.ManyToManyField(PurchaseItems, blank=True)
        
### tax	 

    jurisdiction  -  shipping locations for which to charge applicable tax
        jurisdictionID = primary key
        jurisdictionLabel = label shown in admin site

        # should unique for a jurisdiction
        jurisdictionState = state. need to change so choices are same as other state fields in models
        jurisdictionCity = city
        jurisdictionZip = postal code
        
    taxrate  -  tax rates associated with jurisdiction
        taxRateID = primary key
        taxRateName = name
        # multiplier for tax rate
        taxRateMultiplier = models.DecimalField(max_digits=12, decimal_places=4)
        taxRateDateCreated = models.DateTimeField('date created', auto_now_add=True)
        taxRateValidFrom = models.DateTimeField('start date')
        taxRateValidUntil = models.DateTimeField('end date')
        taxRateNote = not currently used other than basic note taking
        taxRateIsActive = calculated field based on dates. calced in pre_save signal for taxrate
        
        # jurisdiction tax rate is associated with
        jurisdictionID = models.ForeignKey(Jurisdiction, on_delete=models.CASCADE)
    
### users	

    users - default django auth 
        want to override to make emails unique asap
        will add send promos field to mark if promotional emails should be sent to user email.
    
    guest - created if checking out as guest
        guestEmail = email
        guestActive = is guest active? not sure if being used currently
        guestDateLastUpdated = models.DateTimeField(auto_now=True)
        guestDateCreated = models.DateTimeField(auto_now_add=True)
        # not used currently. will be used to determine if promotional emails can be sent
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


