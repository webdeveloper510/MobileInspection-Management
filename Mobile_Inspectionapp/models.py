from django.db import models
from django.contrib.auth.models import *
from django.contrib.auth.models import BaseUserManager,AbstractBaseUser

class User(models.Model):
    username = models.CharField(max_length=255, null=False)
    email = models.EmailField(max_length=255, null=False)
    password = models.CharField(max_length=50)
    ifLogged = models.BooleanField(default=False)
    token = models.CharField(max_length=500, null=True, default="")

    def __str__(self):
        return "{} -{}".format(self.username, self.email)

    

class Inspection(models.Model):
    pha_name=models.CharField(max_length=500,null=False)
    pha_code=models.CharField(max_length=500,null=False)
    property_id=models.CharField(max_length=500,null=False)
    inspector_id=models.CharField(max_length=500,null=False)
    owner_id=models.CharField(max_length=500,null=False)
    owner_name=models.CharField(max_length=500,null=False)
    inspection_date=models.DateField()
    inspection_time=models.DateTimeField()
    unit=models.CharField(max_length=500,null=False)
    unit_addressline1=models.CharField(max_length=500,null=False)
    unit_addressline2=models.CharField(max_length=500,null=False)
    city=models.CharField(max_length=500,null=False)
    state=models.CharField(max_length=500,null=False)
    zip_code=models.CharField(max_length=500,null=False)
    zip_plus=models.CharField(max_length=500,null=False)
    
    def __str__(self):
        return "{} -{}-{}-{}-{}-{}-{}-{}-{}-{}-{}-{}-{} ".format(self.pha_code,self.pha_name,
                                                       self.property_id, self.inspector_id,self.owner_id,
                                                       self.owner_name ,self.inspection_date,
                                                       self.inspection_time,self.unit,self.unit_addressline1,
                                                       self.unit_addressline2,self.city,self.state,self.zip_code,self.zip_plus)
    
class Unit(models.Model):
    add_unit=models.CharField(max_length=500)
    
    def __str__(self):
        return "{} -{}".format(self.add_unit)
    
class Services(models.Model):
    services=models.CharField(max_length=500)
    
    def __str__(self):
        return "{} -{}".format(self. add_decision)
    
class ElectricalInspectableItem(models.Model):
    item=models.CharField(max_length=500)
    
    def __str__(self):
        return "{} -{}".format(self. add_decision)    
    
