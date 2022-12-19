from django.db import models
from django.contrib.auth.models import *
from django.contrib.auth.models import BaseUserManager,AbstractBaseUser
from django.contrib.auth.models import *
from .validater import *

class User(models.Model):
    First_name = models.CharField(max_length=255, null=False,blank= False)
    Last_name = models.CharField(max_length=255, null=False,blank= False)
    email = models.EmailField(max_length=255, null=False,blank= False)
    title=models.CharField(max_length=255, null=False)
    mobile=models.CharField(max_length=255, null=False,blank= False)
    attribute_name=models.CharField(max_length=255, null=False)
    password = models.CharField(max_length=50,blank= False)
    ifLogged = models.BooleanField(default=False)
    token = models.CharField(max_length=500, null=True, default="")

    def __str__(self):
        return "{}".format( self.email) 
    
    def clean(self):
        if self.First_name == None:
            raise ValidationError({
                'website': "Joe must have a website"
            })
  
  
     
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
        return "{} -{}".format(self.customer) 
        
class ServiceAgreement(models.Model):
    service_agreement_form=models.FileField(upload_to="agreement_form/",blank=True,null=True)
    signature=models.FileField(upload_to="signature/",blank=True,null=True)
    customer_id = models.ForeignKey(User, on_delete=models.CASCADE)
    date=models.DateField()
    time=models.TimeField()

    def __str__(self):
        return "{}".format(self.customer_id) 
class ServiceType(models.Model):
    service_agreement_id=models.ForeignKey(ServiceAgreement, on_delete=models.CASCADE)
    service_type_name=models.CharField(max_length=500,null=False)
    price = models.FloatField()
    
    
    # def __str__(self):
    #     return "{} -{}".format(self.service_type_name) 
    
class Service(models.Model):
    service_type_id=models.ForeignKey(ServiceType, on_delete=models.CASCADE)
    name=models.CharField(max_length=500,null=False)
    description=models.TextField(max_length=1000,null=False)
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
    password = models.CharField(max_length=50)
    operater_type=models.CharField(max_length=500,null=False)

class Address(models.Model):
    customer_id = models.ForeignKey(User, on_delete=models.CASCADE)
    street_number=models.CharField(max_length=500,null=False)
    unit_number=models.CharField(max_length=500,null=False)
    addressline1=models.CharField(max_length=500,null=False)
    addressline2=models.CharField(max_length=500,null=False)
    city=models.CharField(max_length=500,null=False)
    state=models.CharField(max_length=500,null=False)
    postal_code=models.CharField(max_length=500,null=False)
    country_name=models.CharField(max_length=500,null=False)
    
class Establishment(models.Model):
    customer_id = models.ForeignKey(User, on_delete=models.CASCADE)
    address_id = models.ForeignKey(Address, on_delete=models.CASCADE)
    name=models.CharField(max_length=250,null=False)
    squarefeet=models.CharField(max_length=250,null=False)
   
    
    def __str__(self):
        return "{} -{}".format(self.customer_id) 

      
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

