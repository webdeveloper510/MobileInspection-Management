from rest_framework import serializers
from django.core.exceptions import ValidationError
from django.db.models import Q 
from .models import *
from django.core.exceptions import ValidationError
from rest_framework.validators import UniqueValidator
from uuid import uuid4
from .validater import *
from phonenumber_field.serializerfields import PhoneNumberField




class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        validators=[UniqueValidator(queryset=User.objects.all())],required=True
        )
    First_name = serializers.CharField(max_length=50,required=True)
    Last_name = serializers.CharField(max_length=50,required=True)
    title = serializers.CharField(max_length=50,required=False)
    mobile =  PhoneNumberField()
    attribute_name = serializers.CharField(max_length=50,required=False)
    password = serializers.CharField(max_length=250,required=True)
    class Meta:
        model = User
        fields  = ['id','email', 'First_name','Last_name','title','mobile','attribute_name', 'password']
       
        # extra_kwargs={
        
        #     'First_name': {'error_messages': {'required': "Firstname is required",'blank':'please provide a firstname'}},
        #     'Last_name': {'error_messages': {'required': "Lastname is required",'blank':'please provide a lastname'}},
        #     'email': {'error_messages': {'required': "email is required",'blank':'please provide a email'}},
        #     'password': {'error_messages': {'required': "password is required",'blank':'please Enter a password'}},
        #     'mobile': {'error_messages': {'required': "mobile is required",'blank':'please Enter a mobile'}},
        #           }
        
  
 
    # def validate(self, attrs):
    #     email = attrs.get('email')
    #     print(email)
    #     if User.objects.filter(email=email).exists():
    #         user = User.objects.get(email = email)
    #         data = {
    #             'message':'User Already Exists',
    #             'status':"400",
    #             "data":{}
    #         }
    #     return Response(238923895)
    
    def create(self, validate_data):
     return User.objects.create(**validate_data)
   


class UserLoginSerializer(serializers.ModelSerializer):
    
    email = serializers.EmailField()
    password = serializers.CharField()
    token = serializers.CharField(required=False, read_only=True)

    def validate(self, data):
        # user,email,password validator
        email = data.get("email", None)
        password = data.get("password", None)
        if not email and not password:
            raise ValidationError("Details not entered.")
        user = None
        # if the email has been passed
        if '@' in email:
            user = User.objects.filter(
                Q(email=email) &
                 Q(password=password)
                ).distinct()
            if not user.exists():
                raise ValidationError("User credentials are not correct.")
            user = User.objects.get(email=email)
        if user.ifLogged:
            data={"message":"User already logged in.","status":"400","data":{}}
            raise serializers.ValidationError({"data":data})
        user.ifLogged = True
        data['token'] = uuid4()
        user.token = data['token']
        user.save()
        return data


    class Meta:
        model = User
        fields = (
            'email',
            'password',
            'token',
        )

        read_only_fields = (
            'token',
        )



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
     
# class CartSerializer(serializers.ModelSerializer):
#      class Meta:
#         model= Cart
#         fields = '__all__'
           
#      def create(self, validate_data):
#          return Cart.objects.create(**validate_data)
     
# class PromotionCategorySerializer(serializers.ModelSerializer):
#      class Meta:
#         model= Promotion_Category
#         fields = '__all__'
           
#      def create(self, validate_data):
#          return Promotion_Category.objects.create(**validate_data)  
     
     
     
# class PromotionSerializer(serializers.ModelSerializer):
#      class Meta:
#         model= Promotion
#         fields = '__all__'
           
#      def create(self, validate_data):
#          return Promotion.objects.create(**validate_data)
     
# class OperaterSerializer(serializers.ModelSerializer):
#      class Meta:
#         model= Operater
#         fields = '__all__'
           
#      def create(self, validate_data):
#          return Operater.objects.create(**validate_data)
     
class AddressSerializer(serializers.ModelSerializer):
     class Meta:
        model= Address
        fields = '__all__'
           
     def create(self, validate_data):
         return Address.objects.create(**validate_data)
     
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

class Establishment_ContactSerializer(serializers.ModelSerializer):
     class Meta:
        model= Establishment_Contact
        fields = '__all__'
           
     def create(self, validate_data):
         return Establishment_Contact.objects.create(**validate_data)
