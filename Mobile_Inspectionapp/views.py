from .models import *
from .serializer import *
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from Mobile_Inspectionapp.renderer import UserRenderer
from django.http import Http404
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
from django.urls import reverse
from distutils import errors
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate




#Creating tokens manually
def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

class UserRegistrationView(APIView):
 renderer_classes=[UserRenderer]
 def post(self,request,format=None):
    serializer=UserRegistrationSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        user=serializer.save()
        return Response({'msg':'Registation successful'},status=status.HTTP_201_CREATED)
    return Response({errors:serializer.errors},status=status.HTTP_400_BAD_REQUEST)

class UserLoginView(APIView):
    renderer_classes=[UserRenderer]
    def post(self,request,format=None):
        serializer=UserLoginSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            email=serializer.data.get('email')
            password=serializer.data.get('password')
            user=authenticate(email=email,password=password)
            if user is not None:
             token= get_tokens_for_user(user)
             return Response({'token':token,'msg':'Login successful','status':'status.HTTP_200_OK'})

            else:
             return Response({'errors':{'non_field_errors':['email or password is not valid']},'status':'status.HTTP_404_NOT_FOUND'})
            
class LeadView(APIView): 
   renderer_classes=[UserRenderer]
   def post(self, request, format=None):
      serializer=LeadSerializer(data=request.data)
      if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({"message":"sucess"})
      return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) 
  
class LeadAddressView(APIView): 
   renderer_classes=[UserRenderer]
   def post(self, request, format=None):
      serializer=LeadAddressSerializer(data=request.data)
      if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({"message":"sucess"})
      return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)             


class ServiceView(APIView):
   
    def get(self, request, format=None):
        service = Service.objects.all().order_by('id')
        serializer = ServiceSerializer(service, many=True)
        return Response(serializer.data)
    
    
    def post(self, request, format=None):
        serializer = ServiceSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message':'Successfully added'})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class ServiceTypeView(APIView):
   
    def get(self, request, format=None):
        service = ServiceType.objects.all().order_by('id')
        serializer = ServiceTypeSerializer(service, many=True)
        return Response(serializer.data)
    
    
    def post(self, request, format=None):
        serializer = ServiceTypeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message':'Successfully added'})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class PromotionCategoryView(APIView):
   
    def get(self, request, format=None):
        service = Promotion_Category.objects.all().order_by('id')
        serializer = PromotionCategorySerializer(service, many=True)
        return Response(serializer.data)
    
    
    def post(self, request, format=None):
        serializer = PromotionCategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message':'Successfully added'})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class PromotionView(APIView):
   
    def get(self, request, format=None):
        service = Promotion.objects.all().order_by('id')
        serializer = PromotionSerializer(service, many=True)
        return Response(serializer.data)
    
    
    def post(self, request, format=None):
        serializer = PromotionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message':'Successfully added'})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)