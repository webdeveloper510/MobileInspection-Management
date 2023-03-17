from rest_framework import serializers
from django.core.exceptions import ValidationError
from django.db.models import Q 
from .models import *
from .validater import *
# from django.core.exceptions import ValidationError
# from rest_framework.validators import UniqueValidator
# from uuid import uuid4

# from phonenumber_field.serializerfields import PhoneNumberField


# class UserSerializer(serializers.ModelSerializer):
#     email = serializers.EmailField(
#         validators=[UniqueValidator(queryset=User.objects.all())],required=True
#         )
#     First_name = serializers.CharField(max_length=50,required=True)
#     Last_name = serializers.CharField(max_length=50,required=True)
#     title = serializers.CharField(max_length=50,required=False)
#     mobile =  PhoneNumberField()
#     attribute_name = serializers.CharField(max_length=50,required=False)
#     password = serializers.CharField(max_length=250,required=True)
#     class Meta:
#         model = User
#         fields  = ['id','email', 'First_name','Last_name','title','mobile','attribute_name', 'password']
       
#         # extra_kwargs={
        
#         #     'First_name': {'error_messages': {'required': "Firstname is required",'blank':'please provide a firstname'}},
#         #     'Last_name': {'error_messages': {'required': "Lastname is required",'blank':'please provide a lastname'}},
#         #     'email': {'error_messages': {'required': "email is required",'blank':'please provide a email'}},
#         #     'password': {'error_messages': {'required': "password is required",'blank':'please Enter a password'}},
#         #     'mobile': {'error_messages': {'required': "mobile is required",'blank':'please Enter a mobile'}},
#         #           }
       
#     def create(self, validate_data):
#      return User.objects.create(**validate_data)


class UserRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=['id','email','password','First_name','Last_name','mobile','title','role','position','attribute_name']
        extra_kwargs = {'password': {'write_only': True}}
    def validate(self, attrs):
      password=attrs.get('password')   
      return attrs
    def create(self, validated_data,):
       user=User.objects.create(
       email=validated_data['email'],
       First_name=validated_data['First_name'],
       Last_name=validated_data['Last_name'],
       title=validated_data['title'],
       attribute_name=validated_data['attribute_name'],
       mobile=validated_data['mobile'],
       position=validated_data['position'],)
       user.set_password(validated_data['password']) 
       user.save()
       return user
     
    


class ServiceSerializer(serializers.ModelSerializer):
     class Meta:
        model= Service
        fields = '__all__'
           
     def create(self, validate_data):
         return Service.objects.create(**validate_data)
     
class Service_ImageSerializer(serializers.ModelSerializer):
     class Meta:
        model= Service_Image
        fields = '__all__'
           
     def create(self, validate_data):
         return Service_Image.objects.create(**validate_data)

class ServiceAgreementSerializer(serializers.ModelSerializer):
     class Meta:
        model= ServiceAgreement
        fields = '__all__'
           
     def create(self, validate_data):
         return ServiceAgreement.objects.create(**validate_data)
     
class ServiceTypeSerializer(serializers.ModelSerializer):
    #  servicelist = ServiceSerializer(many=True, read_only=True)
     class Meta:
        model= ServiceType
        fields = '__all__'
           
     def create(self, validate_data):
         return ServiceType.objects.create(**validate_data)

class ContactSerializer(serializers.HyperlinkedModelSerializer):
     class Meta:
        model= Contact
        fields = '__all__'
           
     def create(self, validate_data):
         return Contact.objects.create(**validate_data)
     

     
class AddressSerializer(serializers.ModelSerializer):
     class Meta:
        model= Address
        fields = '__all__'
           
     def create(self, validate_data):
         return Address.objects.create(**validate_data)
     
class EstablishmentTypeSerializer(serializers.ModelSerializer):
     class Meta:
        model= Establishment_type
        fields = '__all__'
           
     def create(self, validate_data):
         return Establishment_type.objects.create(**validate_data)
     
class EstablishmentSerializer(serializers.ModelSerializer):
     class Meta:
        model= Establishment
        fields = '__all__'
           
     def create(self, validate_data):
         return Establishment.objects.create(**validate_data)

class Establishment_ContactSerializer(serializers.ModelSerializer):
     class Meta:
        model= Establishment_Contact
        fields = '__all__'
           
     def create(self, validate_data):
         return Establishment_Contact.objects.create(**validate_data)

     
class Customer_AddressSerializer(serializers.ModelSerializer):
     class Meta:
        model= Customer_Address
        fields = '__all__'
           
     def create(self, validate_data):
         return Customer_Address.objects.create(**validate_data)
     
class UploadpdfSerializer(serializers.ModelSerializer):
     class Meta:
        model= uploadpdf
        fields = '__all__'
           
     def create(self, validate_data):
         return uploadpdf.objects.create(**validate_data)
#new
class OperaterSerializer(serializers.ModelSerializer):
     class Meta:
        model= Operater
        fields = '__all__'
           
     def create(self, validate_data):
         return Operater.objects.create(**validate_data)
     
class ServiceItemSerializer(serializers.ModelSerializer):
     class Meta:
        model= ServiceItem
        fields = '__all__'
           
     def create(self, validate_data):
         return ServiceItem.objects.create(**validate_data)