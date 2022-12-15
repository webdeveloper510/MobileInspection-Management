from django.db import models
from django.contrib.auth.models import *
from django.contrib.auth.models import BaseUserManager,AbstractBaseUser
from django.contrib.auth.models import *
     
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
        return "{} -{}".format(self.customer_id)     

class UserManager(BaseUserManager):
    def create_user(self, email, First_name, Last_name,attribute_name,title,mobile, password=None, password2=None):
        """
        Creates and saves a User with the given email, First_name, Last_name, and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            First_name=First_name,
            Last_name=Last_name,
            attribute_name=attribute_name,
            title=title,
            mobile=mobile
            
                         )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, First_name, Last_name, password=None):
        """
        Creates and saves a superuser with the given email,  First_name, Last_name, and password.
        """
        user = self.create_user(
            email,
            password=password,
            First_name=First_name,
            Last_name=Last_name,
           )
        user.is_admin = True
        user.save(using=self._db)
        return user




#  Custom User Model
class User(AbstractBaseUser):
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    First_name = models.CharField(max_length=80)
    Last_name = models.CharField(max_length=80)
    attribute_name=models.CharField(max_length=80)
    title=models.CharField(max_length=80)
    mobile=models.CharField(max_length=80)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    objects = UserManager()

    USERNAME_FIELD = 'email'

    REQUIRED_FIELDS = ['First_name', 'Last_name','attribute_name','title','mobile',]


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
    
    