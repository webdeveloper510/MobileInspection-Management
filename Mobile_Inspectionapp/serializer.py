from rest_framework import serializers
from django.core.exceptions import ValidationError
from django.db.models import Q 
from .models import *
from django.core.exceptions import ValidationError
from rest_framework.validators import UniqueValidator
from uuid import uuid4

class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
        )
    First_name = serializers.CharField(max_length=15)
    Last_name = serializers.CharField(max_length=15)
    title = serializers.CharField(max_length=15)
    mobile = serializers.CharField(max_length=15)
    attribute_name = serializers.CharField(max_length=15)
    password = serializers.CharField(max_length=15)
    class Meta:
        model = User
        fields  = ['email', 'First_name','Last_name','title','mobile','attribute_name', 'password']
        
        extra_kwargs={
        'email': {'error_messages': {'required': "email is required",'blank':'please provide a email'}},
        'First_name': {'error_messages': {'required': "firstname is required",'blank':'please Enter a firstname'}},
        'Last_name': {'error_messages': {'required': "lastname is required",'blank':'please Enter a lastname'}},
        'mobile': {'error_messages': {'required': "mobile is required",'blank':'please Enter a mobile'}},
        'password': {'error_messages': {'required': "password is required",'blank':'please Enter a password'}} 
    }
   
    
    def create(self, validate_data):
     return User.objects.create(**validate_data)

class UserLoginSerializer(serializers.ModelSerializer):
    # to accept either username or email
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
            raise ValidationError("User already logged in.")
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
class UserLogoutSerializer(serializers.ModelSerializer):
    token = serializers.CharField()
    status = serializers.CharField(required=False, read_only=True)

    def validate(self, data):
        token = data.get("token", None)
        print(token)
        user = None
        try:
            user = User.objects.get(token=token)
            if not user.ifLogged:
                raise ValidationError("User is not logged in.")
        except Exception as e:
            raise ValidationError(str(e))
        user.ifLogged = False
        user.token = ""
        user.save()
        data['status'] = "User is logged out."
        return data

    class Meta:
        model = User
        fields = (
            'token',
            'status',
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