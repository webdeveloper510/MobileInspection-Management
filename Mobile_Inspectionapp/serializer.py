from rest_framework import serializers
from Mobile_Inspectionapp.models import User, Inspection,Unit,Services,ElectricalInspectableItem
from django.core.exceptions import ValidationError
from django.db.models import Q 
from django.core.exceptions import ValidationError
from uuid import uuid4


class UserLoginSerializer(serializers.ModelSerializer):
    # to accept either username or email
    user_id = serializers.CharField()
    password = serializers.CharField()
    token = serializers.CharField(required=False, read_only=True)

    def validate(self, data):
        # user,email,password validator
        user_id = data.get("user_id", None)
        password = data.get("password", None)
        if not user_id and not password:
            raise ValidationError("Details not entered.")
        user = None
        # if the email has been passed
        if '@' in user_id:
            user = User.objects.filter(
                Q(email=user_id) &
                Q(password=password)
                ).distinct()
            if not user.exists():
                raise ValidationError("User credentials are not correct.")
            user = User.objects.get(email=user_id)
        else:
            user = User.objects.filter(
                Q(username=user_id) &
                Q(password=password)
            ).distinct()
            if not user.exists():
                raise ValidationError("User credentials are not correct.")
            user = User.objects.get(username=user_id)
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
            'user_id',
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
 
class InspectionSerializer(serializers.ModelSerializer):
    class Meta:
        model=Inspection
        fields = ['pha_name','pha_code','property_id','inspector_id','owner_id','owner_name','inspection_date','inspection_time','unit','unit_addressline1','unit_addressline2','city','state','zip_code','zip_plus']
        extra_kwargs={
                    "pha_name":{"error_messages":{"required":"pha_name is required"}},
                    "pha_code":{"error_messages":{"required":"pha_code is required"}},
                    "property_id":{"error_messages":{"required":"property_id is required"}},
                    "inspector_id":{"error_messages":{"required":"inspector_id is required"}},
                    "owner_id":{"error_messages":{"required":"owner_id is required"}},
                    "owner_name":{"error_messages":{"required":"owner_name is required"}},
                    "inspection_date":{"error_messages":{"required":"inspection_date is required"}},
                    "inspection_time":{"error_messages":{"required":"inspection_time is required"}},
                    "unit":{"error_messages":{"required":"unit is required"}},
                    "unit_addressline1":{"error_messages":{"required":"unit_addressline1 is required"}},
                    "unit_addressline2":{"error_messages":{"required":"unit_addressline2 is required"}},
                    "city":{"error_messages":{"required":"city is required"}},
                    "state":{"error_messages":{"required":"state is required"}},
                    "zip_code":{"error_messages":{"required":"zip_code is required"}},
                    "zip_plus":{"error_messages":{"required":"zip_plus is required"}},
                    
                      }
        
    def create(self, validate_data):
     return Inspection.objects.create(**validate_data)
 

class UnitSerializer(serializers.ModelSerializer):
     class Meta:
        model= Unit
        fields = '__all__'
           
     def create(self, validate_data):
         return Unit.objects.create(**validate_data)

class ServicesSerializer(serializers.ModelSerializer):
     class Meta:
        model= Services
        fields = '__all__'
           
     def create(self, validate_data):
         return Services.objects.create(**validate_data)

class ElectricalInspectableItemSerializer(serializers.ModelSerializer):
     class Meta:
        model= ElectricalInspectableItem
        fields = '__all__'
           
     def create(self, validate_data):
         return ElectricalInspectableItem.objects.create(**validate_data)