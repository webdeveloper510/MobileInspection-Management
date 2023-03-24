from django.db import models
from django.contrib.auth.models import *
from .validater import *
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager
from django.contrib.auth.models import UserManager
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.utils.translation import gettext_lazy as _


USER_TYPE_CHOICES = (
           ("dispatcher", "dispatcher"),
           ("customer", "customer"),
          
)
#custom User Manager
class UserManager(BaseUserManager):
    def create_user(self, email, First_name, Last_name, title,role,mobile,attribute_name,position,password=None):
        
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            First_name=First_name,
            Last_name=Last_name,
            title=title,
            role=role,
            mobile=mobile,
            attribute_name=attribute_name,
            position=position
                         )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None):
        """
        Creates and saves a superuser with the given email and password.
        """
        user = self.create_user(
            email,
            First_name="None",
            Last_name="None",
            title="None",
            role="None",
            mobile="None",
            attribute_name="None",
            position="None",
            password=password,
           )
        user.is_admin = True
    
        user.save(using=self._db)
        return user

class User(AbstractBaseUser,PermissionsMixin):
  
    First_name = models.CharField(max_length=50, null=False,default="")
    Last_name = models.CharField(max_length=50, null=False,default="")
    email = models.EmailField(max_length=50, null=False,default="",unique=True)
    title=models.CharField(max_length=50, null=True,blank=True,default="")
    role=models.CharField(max_length=50, null=True,blank=True,default="customer",choices=USER_TYPE_CHOICES)
    mobile=models.CharField(max_length=50, null=False,default="")
    attribute_name=models.CharField(max_length=50, null=True,blank=True,default="")
    password = models.CharField(max_length=250,null=False)
    position=models.CharField(max_length=250, null=True,blank=True,default="")
    ifLogged  = models.BooleanField(default=True)
    token = models.CharField(max_length=500, null=True, default="",blank=True)
    is_staff  = models.BooleanField(default=False)
    is_active   = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True,null=True)
    updated_at =  models.DateTimeField(auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_superuser=models.BooleanField(default=False)
    user_created_by_admin=models.BooleanField(default=False)
    dispatcher_user_id=models.CharField(max_length=500, null=True, default="",blank=True)
    objects = UserManager()
    USERNAME_FIELD = "email"
    # REQUIRED_FIELDS = []
    
    def ___str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return self.is_admin
        #return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin
    class Meta:
        verbose_name="User"


        
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
    name=models.CharField(max_length=500,null=True,blank=True)
    promocode=models.CharField(max_length=500,null=True,blank=True)
    discount_rate=models.CharField(max_length=500)
    start_date=models.DateField()
    end_date=models.DateField()
    


class Address(models.Model):
    customer_id = models.ForeignKey(User, on_delete=models.CASCADE,blank=True,null=True)
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
    Establishment_type=models.CharField(max_length=250,null=True, blank= True)
   
    
class Establishment(models.Model):
    customer_id = models.ForeignKey(User, on_delete=models.CASCADE ,blank=True,null=True)
    address_id = models.ForeignKey(Address, on_delete=models.CASCADE,blank=True,null=True)
    name=models.CharField(max_length=250,null=True)
    establishment_type_id=models.ForeignKey(Establishment_type, on_delete=models.CASCADE,blank=True,null=True)
    
class Establishment_Contact(models.Model):
    establishment_id= models.ForeignKey(Establishment, on_delete=models.CASCADE ,null=True)
    customer_id=models.CharField(max_length=50,null=False)
    firstname=models.CharField(max_length=250,null=True)
    lastname=models.CharField(max_length=250,null=True)
    title=models.CharField(max_length=250,null=True)
    phone=PhoneNumberField(max_length=250,null=True)


class Contact(models.Model):
    firstname=models.CharField(max_length=500,null=True,blank=True)
    lastname=models.CharField(max_length=500,null=True,blank=True)
    email=models.EmailField(blank=True)
    phone=PhoneNumberField(null=True,blank=True)
    address=models.CharField(max_length=500,null=True,blank=True)
    unit_number=models.CharField(max_length=500,null=True,blank=True)
    city=models.CharField(max_length=500,null=True,blank=True)
    state=models.CharField(max_length=500,null=True,blank=True)
    country=models.CharField(max_length=500,null=True,blank=True)
    zipcode=models.IntegerField(null=True,blank=True)
    comment=models.TextField(max_length=500,null=True,blank=True)


class uploadpdf(models.Model):
    uploadfile=models.FileField(upload_to="products_images/",blank=True,null=True)

#new
class Operater(models.Model):
    firstname=models.CharField(max_length=500,null=False)
    lastname=models.CharField(max_length=500,null=False)
    phone=models.CharField(max_length=500,null=False)
    email=models.EmailField()
    position=models.CharField(max_length=500,null=False)
    operater_type=models.CharField(max_length=500,null=False,default="None")
    dispatcher_id=models.ForeignKey(User, on_delete=models.CASCADE ,null=True)
#new
class ServiceItem(models.Model):
    establishment_id= models.ForeignKey(Establishment, on_delete=models.CASCADE ,null=True,blank=True,default='None')
    service_type_id= models.ForeignKey(ServiceType, on_delete=models.CASCADE ,null=True,blank=True)
    operater_id=models.ForeignKey(Operater, on_delete=models.CASCADE ,null=True,blank=True)
    service_date_time=models.DateTimeField()
    service_notes=models.TextField(max_length=1000,null=True,blank=True)
    dispatcher_id=models.ForeignKey(User, on_delete=models.CASCADE ,null=True)
    
