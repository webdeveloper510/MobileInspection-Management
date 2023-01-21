from django.db import models
from django.contrib.auth.models import *
from .validater import *
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth.hashers import make_password
from django.core.validators import MinValueValidator,MaxValueValidator
# from django_cryptography.fields import encrypt


class User(models.Model):
    First_name = models.CharField(max_length=50, null=False,default="")
    Last_name = models.CharField(max_length=50, null=False,default="")
    email = models.EmailField(max_length=50, null=False,default="")
    title=models.CharField(max_length=50, null=False,default="")
    mobile=PhoneNumberField(null=False)
    attribute_name=models.CharField(max_length=50, null=False,default="")
    password = models.CharField(max_length=250,null=False)
    ifLogged  = models.BooleanField(default=False)
    token = models.CharField(max_length=500, null=True, default="")
    
    

    def __str__(self):
        return "{}".format( self.email) 
    
    # def save(self, *args, **kwargs):
         
    #     self.password = make_password(self.password)
    #     super(User,self).save(*args, **kwargs)
    
    
     
class Lead(models.Model):
    firstname=models.CharField(max_length=500,null=False)
    lastname=models.CharField(max_length=500,null=False)
    phone=models.CharField(max_length=500,null=False)
    email=models.EmailField()
    comment=models.TextField(max_length=500,null=False)
    date=models.DateField()
    time=models.TimeField()
    
    def __str__(self):
        return "{} -{}".format(self.firstname)   
    
class LeadAddress(models.Model):
    customer_id = models.ForeignKey(Lead, on_delete=models.CASCADE)
    street_number=models.CharField(max_length=500,null=False)
    unit_number=models.CharField(max_length=500,null=False)
    addressline1=models.CharField(max_length=500,null=False)
    addressline2=models.CharField(max_length=500,null=False)
    city=models.CharField(max_length=500,null=False)
    state=models.CharField(max_length=500,null=False)
    postal_code=models.CharField(max_length=500,null=False)
    country_name=models.CharField(max_length=500,null=False)
    
    def __str__(self):
        return "{} -{}".format(self.customer_id) 
        
class ServiceAgreement(models.Model):
    customer_id = models.ForeignKey(User, on_delete=models.CASCADE)
    service_agreement_form=models.FileField(upload_to="agreement_form/",blank=True,null=True)
    signature=models.FileField(upload_to="signature/",blank=True,null=True)
    date=models.DateField(null= True)
    time=models.TimeField(null= True)

    def __str__(self):
        return "{}".format(self.customer_id) 
    
SERVICE_TYPE_CHOICES = (
           ("ONETIME", "OneTime"),
           ("MEMBERSHIP", "Membership"),
)
    
class ServiceType(models.Model):
    service_agreement_id=models.ForeignKey(ServiceAgreement, on_delete=models.CASCADE)
    service_type_name=models.CharField(max_length=500,choices=SERVICE_TYPE_CHOICES,default = 'ONETIME',null=False)
    service_type_description=models.TextField(max_length=1000,null=True)
    price = models.FloatField(null=True)
    
    
    # def __str__(self):
    #     return "{} -{}".format(self.service_type_name) 

    
class Service(models.Model):
    service_type_id=models.ForeignKey(ServiceType, on_delete=models.CASCADE)
    name=models.CharField(max_length=500,null=True)
    description=models.TextField(max_length=1000,null=True,blank=True)
    
class Service_Image(models.Model):
    service_id=models.ForeignKey(Service, on_delete=models.CASCADE)
    service_image=models.ImageField(upload_to="products_images/",blank=True,null=True)
      
    # def __str__(self):
    #     return "{} ".format(self.service_type_id) 
    
class Promotion(models.Model):
    name=models.CharField(max_length=500,null=False)
    description=models.TextField(max_length=1000,null=False)
    discount_rate = models.FloatField()
    start_date=models.DateField()
    end_date=models.DateField()
    
    # def __str__(self):
    #     return "{} -{}".format(self.name)     

class Promotion_Category(models.Model):
    promotion_id= models.ForeignKey(Promotion, on_delete=models.CASCADE)
    service_type_id= models.ForeignKey(ServiceType, on_delete=models.CASCADE)
    
    # def __str__(self):
    #     return "{} -{}".format(self.service_type_id) 
    

    
class Operater(models.Model):
    firstname=models.CharField(max_length=500,null=False)
    lastname=models.CharField(max_length=500,null=False)
    phone=models.CharField(max_length=500,null=False)
    email=models.EmailField()
    title=models.CharField(max_length=500,null=False)
    password =models.CharField(max_length=50)
    operater_type=models.CharField(max_length=500,null=False)

class Address(models.Model):
    unit_number=models.CharField(max_length=500,null=False)
    addressline1=models.CharField(max_length=500,null=False)
    city=models.CharField(max_length=500,null=False)
    state=models.CharField(max_length=500,null=False)
    postal_code=models.CharField(max_length=500,null=False)
    country_name=models.CharField(max_length=500,null=False)

class Customer_Address(models.Model):
    customer_id= models.ForeignKey(User, on_delete=models.CASCADE)
    address_id=models.ForeignKey(Address, on_delete=models.CASCADE,blank=True,null=True)

class Establishment_type(models.Model):
    Establishment_type=models.CharField(max_length=250,null=False)
    title=models.CharField(max_length=250,null=False)
    
class Establishment(models.Model):
    customer_id = models.ForeignKey(User, on_delete=models.CASCADE ,null=True)
    address_id = models.ForeignKey(Address, on_delete=models.CASCADE,blank=True,null=True)
    name=models.CharField(max_length=250,null=True)
    establishment_type_id=models.ForeignKey(Establishment_type, on_delete=models.CASCADE,null=True)
    
class Establishment_Contact(models.Model):
    establishment_id= models.ForeignKey(Establishment, on_delete=models.CASCADE ,null=True)
    firstname=models.CharField(max_length=250,null=True)
    lastname=models.CharField(max_length=250,null=True)
    title=models.CharField(max_length=250,null=True)
    phone=PhoneNumberField(max_length=250,null=True)
    
    
class Service_Order(models.Model):
    User_id = models.ForeignKey(User, on_delete=models.CASCADE)
    service_id = models.ForeignKey(Service, on_delete=models.CASCADE)
    order_status=models.CharField(max_length=250,null=False)
    operater_id = models.ForeignKey(Operater, on_delete=models.CASCADE)
    service_datetime=models.DateTimeField()
    service_fee = models.FloatField()
    total_amount = models.FloatField()
    requested_service_datetime=models.DateTimeField()
    Establishment_id = models.ForeignKey(Establishment, on_delete=models.CASCADE)
   
    
    def __str__(self):
        return "{} -{}".format(self.User_id)     

class Contact(models.Model):
    firstname=models.CharField(max_length=500,null=True,blank=True)
    lastname=models.CharField(max_length=500,null=True,blank=True)
    email=models.EmailField(blank=True)
    phone=PhoneNumberField(null=True,blank=True)
    street_number=models.CharField(max_length=500,null=True,blank=True)
    unit_number=models.CharField(max_length=500,null=True,blank=True)
    address=models.CharField(max_length=500,null=True,blank=True)
    address1=models.CharField(max_length=500,null=True,blank=True)
    city=models.CharField(max_length=500,null=True,blank=True)
    state=models.CharField(max_length=500,null=True,blank=True)
    country=models.CharField(max_length=500,null=True,blank=True)
    zipcode=models.IntegerField(null=True,blank=True)
    comment=models.TextField(max_length=500,null=True,blank=True)
    
class Cart(models.Model):
    service_id = models.ForeignKey(Service, on_delete=models.CASCADE, null=False, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class uploadpdf(models.Model):
    uploadfile=models.FileField(upload_to="products_images/",blank=True,null=True)
    