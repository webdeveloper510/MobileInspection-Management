from rest_framework import serializers
from django.core.exceptions import ValidationError
from django.db.models import Q 
from .models import *
from django.core.exceptions import ValidationError
from uuid import uuid4

class UserRegistrationSerializer(serializers.ModelSerializer):
    password2=serializers.CharField(style={'input_type':'password'},write_only=True)
    class Meta:
        model=User

        fields=['id','email','password','password2','First_name','Last_name','title','mobile','attribute_name']

        extra_kwargs={
        
            'First_name': {'error_messages': {'required': "Firstname is required",'blank':'please provide a firstname'}},
            'Last_name': {'error_messages': {'required': "Lastname is required",'blank':'please provide a lastname'}},
            'email': {'error_messages': {'required': "email is required",'blank':'please provide a email'}},
            'title': {'error_messages': {'required': "title is required",'blank':'please provide a title'}},
            'mobile': {'error_messages': {'required': "mobile Number is required",'blank':'please provide a mobile number'}},
            'attribute_name': {'error_messages': {'required': "attribue_name is required",'blank':'please provide a attribute_name'}},
            'password': {'error_messages': {'required': "password is required",'blank':'please Enter a password'}},
            'password2': {'error_messages': {'required': "confirm password is required",'blank':'Confirm password could not blank'}},
          }

        #validating password and confirm password
    def validate(self, attrs):
      password=attrs.get('password')
      password2=attrs.get('password2')
      if password!=password2:
        raise serializers.ValidationError('password and confirm password doesnot match')

      return attrs

    def create(self, validated_data):
      return User.objects.create_user(** validated_data)

class UserLoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=250)
    class Meta:
     model=User
     fields=['email','password']
     extra_kwargs={
        'email': {'error_messages': {'required': "email is required",'blank':'please provide a email'}},
        'password': {'error_messages': {'required': "password is required",'blank':'please Enter a email'}}
        
    }

 

class LeadSerializer(serializers.ModelSerializer):
     class Meta:
        model= Lead
        fields = ['firstname','lastname','phone','email','comment','date','time']
        extra_kwargs={
            "firstname":{"error_messages":{"required":"firstname is required"}},
            "lastname":{"error_messages":{"required":"lastname is required"}},
            "phone":{"error_messages":{"required":"phone number is required"}},
            "email":{"error_messages":{"required":"email is required"}},
            "comment":{"error_messages":{"required":"comment is required"}},
            "date":{"error_messages":{"required":"date is required"}},
            "time":{"error_messages":{"required":"time is required"}},
        }
           
     def create(self, validate_data):
         return Lead.objects.create(**validate_data)
     
class LeadAddressSerializer(serializers.ModelSerializer):
     class Meta:
        model= LeadAddress
        fields = ['customer_id','street_number','unit_number','addressline1','addressline2','city','state','postal_code','country_name']
        extra_kwargs={
            "customer_id":{"error_messages":{"required":"customer is required"}},
            "street_number":{"error_messages":{"required":"street_number is required"}},
            "unit_number":{"error_messages":{"required":"addressline1 is required"}},
            "addressline2":{"error_messages":{"required":"addressline2 is required"}},
            "city":{"error_messages":{"required":"city is required"}},
            "state":{"error_messages":{"required":"state is required"}},
            "postal_code":{"error_messages":{"required":"postal_code is required"}},
            "country_name":{"error_messages":{"required":"country_name is required"}},
        }
           
     def create(self, validate_data):
         return LeadAddress.objects.create(**validate_data)
     
class ServiceSerializer(serializers.ModelSerializer):
     class Meta:
        model= Service
        fields = '__all__'
           
     def create(self, validate_data):
         return Service.objects.create(**validate_data)

class ServiceAgreementSerializer(serializers.ModelSerializer):
     class Meta:
        model= ServiceAgreement
        fields = '__all__'
           
     def create(self, validate_data):
         return ServiceAgreement.objects.create(**validate_data)
     
class ServiceTypeSerializer(serializers.ModelSerializer):
     class Meta:
        model= ServiceType
        fields = '__all__'
           
     def create(self, validate_data):
         return ServiceType.objects.create(**validate_data)
     
class PromotionCategorySerializer(serializers.ModelSerializer):
     class Meta:
        model= Promotion_Category
        fields = '__all__'
           
     def create(self, validate_data):
         return Promotion_Category.objects.create(**validate_data)
     
class PromotionSerializer(serializers.ModelSerializer):
     class Meta:
        model= Promotion
        fields = '__all__'
           
     def create(self, validate_data):
         return Promotion.objects.create(**validate_data)
     
class OperaterSerializer(serializers.ModelSerializer):
     class Meta:
        model= Operater
        fields = '__all__'
           
     def create(self, validate_data):
         return Operater.objects.create(**validate_data)
     
class AddressSerializer(serializers.ModelSerializer):
     class Meta:
        model= Address
        fields = ['customer_id','street_number','unit_number','addressline1','addressline2','city','state','postal_code','country_name']
        extra_kwargs={
            "customer_id":{"error_messages":{"required":"customer is required"}},
            "street_number":{"error_messages":{"required":"street_number is required"}},
            "unit_number":{"error_messages":{"required":"addressline1 is required"}},
            "addressline2":{"error_messages":{"required":"addressline2 is required"}},
            "city":{"error_messages":{"required":"city is required"}},
            "state":{"error_messages":{"required":"state is required"}},
            "postal_code":{"error_messages":{"required":"postal_code is required"}},
            "country_name":{"error_messages":{"required":"country_name is required"}},
        }
class EstablishmentSerializer(serializers.ModelSerializer):
     class Meta:
        model= Establishment
        fields = '__all__'
           
     def create(self, validate_data):
         return Establishment.objects.create(**validate_data)
     
class ServiceorderSerializer(serializers.ModelSerializer):
     class Meta:
        model= Service_Order
        fields = '__all__'
           
     def create(self, validate_data):
         return Service_Order.objects.create(**validate_data)