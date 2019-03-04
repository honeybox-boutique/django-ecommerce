# Clothing Store e-commerce site
Clothing Store e-commerce site

Apps

addresses
assets
billing
coupons	
emails	
homepage	
pricing	
products	
purchases	
sales	
shipping	
shopcart	
speedtest	
tax	
users	

Environment Setup  

Clone it  
Install requirements.txt  
duplicate base_keys.template and rename to base_keys.py  
enter appropriate info into base_keys.py  
run it  

Data models  

addresses  
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

billing  
    billingEmail = email associated with billing profile  
    active = status of billing profile  
    lastUpdated  
    dateCreated  
    profileType - either 'user' billing profile or 'guest'. guest billing profiles get marked inactive after transaction  
    user = user associated with billing profile if any  
    billingToken = stripe customer token  
    
homepage  
    homepageimage  
        homePageImagePath - 
        homePageImageAltText = 
        homePageImageLink =
    bighomepageimage   
        bigHomePageImagePath = 
        bigHomePageImageAltText = 
        bigHomePageImageLink = 
pricing
    pricing
        pricingBasePrice = models.DecimalField(max_digits=12, decimal_places=2)
        pricingDateCreated = models.DateTimeField('date created', auto_now_add=True)
        pricingValidFrom = models.DateTimeField('start date')
        pricingValidUntil = models.DateTimeField('end date')
        pricingNote = models.TextField(max_length=200)
        pricingIsActive = models.BooleanField(default=False)
    
    pdiscount
        pDiscountID = models.AutoField(primary_key=True)  
        pDiscountName = models.CharField(max_length=40)  
        pDiscountDescription = models.TextField(max_length=200)  
        pDiscountType = models.CharField(max_length=30, choices=DISCOUNT_TYPE_CHOICES)  
        pDiscountValue = models.DecimalField(max_digits=12, decimal_places=2)  
        pDiscountDateCreated = models.DateTimeField('date created', auto_now_add=True)  
        pDiscountDateValidFrom = models.DateTimeField('valid from')  
        pDiscountDateValidUntil = models.DateTimeField('valid until')  
        pDiscountCouponCode = models.CharField(max_length=20)  
        pDiscountMaxDiscount = models.DecimalField(max_digits=12, decimal_places=2)  
        pDiscountMinOrderValue = models.DecimalField(max_digits=12, decimal_places=2)  
        pDiscountIsActive = models.BooleanField(default=False)  

        productID = models.ForeignKey(Product, on_delete=models.CASCADE)  
    cdiscount
        cDiscountID = models.AutoField(primary_key=True)
        cDiscountName = models.CharField(max_length=40)
        cDiscountDescription = models.TextField(max_length=200)
        cDiscountType = models.CharField(max_length=30, choices=DISCOUNT_TYPE_CHOICES)
        cDiscountValue = models.DecimalField(max_digits=12, decimal_places=2)
        cDiscountDateCreated = models.DateTimeField('date created', auto_now_add=True)
        cDiscountDateValidFrom = models.DateTimeField('valid from')
        cDiscountDateValidUntil = models.DateTimeField('valid until')
        cDiscountCouponCode = models.CharField(max_length=20)
        cDiscountMaxDiscount = models.DecimalField(max_digits=12, decimal_places=2)
        cDiscountMinOrderValue = models.DecimalField(max_digits=12, decimal_places=2)
        cDiscountIsActive = models.BooleanField(default=False)
        categoryID = models.ForeignKey(Category, on_delete=models.CASCADE)
        sDiscountID = models.AutoField(primary_key=True)
    sdiscount  
        sDiscountName = models.CharField(max_length=40)  
        sDiscountDescription = models.TextField(max_length=200)  
        sDiscountMessage = models.CharField(max_length=150)  
        sDiscountType = models.CharField(max_length=30, choices=DISCOUNT_TYPE_CHOICES)  
        sDiscountValue = models.DecimalField(max_digits=8, decimal_places=3)  
        sDiscountDateCreated = models.DateTimeField('date created')  
        sDiscountDateValidFrom = models.DateTimeField('valid from')  
        sDiscountDateValidUntil = models.DateTimeField('valid until')  
        sDiscountCouponCode = models.CharField('coupon code', max_length=20)  
        sDiscountMaxAmount = models.DecimalField(max_digits=8, decimal_places=3)  
        sDiscountMinSaleValue = models.DecimalField(max_digits=8, decimal_places=3)  
        sDiscountAutomatic = models.BooleanField(default=False)  
        sDiscountIsShippingDiscount = models.BooleanField(default=False)  
        sDiscountIsActive = models.BooleanField(default=False)  
    sdiscountcondition
        sDCID = models.AutoField(primary_key=True)  
        sDCName = models.CharField(max_length=50)  
        sDCFailMessage = models.TextField(max_length=200)  
        sDCType = models.CharField(max_length=50, choices=CONDITION_TYPE_CHOICES)  
        sDCFieldName = models.CharField(max_length=50, choices=FIELD_NAME_CHOICES)  
        sDCCompareOperator = models.CharField(max_length=50, choices=COMPARE_OPERATOR_CHOICES)  
        sDCValue = models.CharField(max_length=70)  
        sDCNumRequired = models.IntegerField(default=1)  

        sDiscountID = models.ForeignKey(SDiscount, on_delete=models.CASCADE)  
    


products
    color  
    category  
    categoryimage  
    size  
    product  
    productcolor  
    productimage  
purchases  
    vendor  
    purchase  
    purchaseitems  
sales	
    customershipmethod  
    sale  
    saleitems  
shipping	
    warehouse  
    shipment  
    parcel  
shopcart	
    shopcart  
speedtest	
tax	 
    jurisdiction  
    taxrate  
    
users	
    default django auth (want to override to make emails unique asap)  
    guest  


How to manage the site

Common tasks:

Add product for sale  
  Add product itself  
  Add product colorset (productcolors in admin site)  
    Colorset is a set of images that correspond to a product color  
    e.g. Test Top - Red  
    Add product colorset images  
      find colorset in productcolors admin page  
      upload images as desired. First image will be displayed on listing  
  
  Add product pricing  
  Record product stock purchases  
  Add product discount  
  Add product category discount  
  Add sale discount  


How to add a product to be displayed for sale on category page  

1. Add product in admin/products  


