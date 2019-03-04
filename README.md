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


