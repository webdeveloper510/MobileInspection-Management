from .models import *
from .serializer import *
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from Mobile_Inspectionapp.renderer import UserRenderer


#Creating tokens manually
class RegisterView(APIView):
  renderer_classes = [UserRenderer]
  def post(self, request, format=None):
    serializer = UserSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = serializer.save()
    user.is_active = False
    user.save()
    return Response({"success":"you have registred successfully "},status=status.HTTP_201_CREATED)

class UserLoginView(APIView):
  renderer_classes = [UserRenderer]
  queryset = User.objects.all()
  serializer_class = UserLoginSerializer
  def post(self, request, *args, **kwargs):
        serializer_class = UserLoginSerializer(data=request.data)
        if serializer_class.is_valid(raise_exception=True):
            return Response({"Status":"200 ok"})
        return Response(serializer_class.errors, status=HTTP_400_BAD_REQUEST)
    
class Logout(APIView):
    queryset = User.objects.all()
    serializer_class = UserLogoutSerializer

    def post(self, request, *args, **kwargs):
        serializer_class = UserLogoutSerializer(data=request.data)
        if serializer_class.is_valid(raise_exception=True):
            return Response(serializer_class.data, status=HTTP_200_OK)
        return Response(serializer_class.errors, status=HTTP_400_BAD_REQUEST) 
    
class ServiceAgreementView(APIView):
   
    def get(self, request, format=None):
        service = ServiceAgreement.objects.all().order_by('id')
        serializer = ServiceAgreementSerializer(service, many=True)
        return Response(serializer.data)
          
class ServiceView(APIView):
   
    def get(self, request, format=None):
        service = Service.objects.all().order_by('id')
        serializer = ServiceSerializer(service, many=True)
        return Response(serializer.data)
    
class ServiceTypeView(APIView):
   
    def get(self, request, format=None):
        service = ServiceType.objects.all().order_by('id')
        serializer = ServiceTypeSerializer(service, many=True)
        return Response(serializer.data)
            
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