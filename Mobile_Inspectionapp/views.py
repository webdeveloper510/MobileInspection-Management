from .models import *
from .serializer import *
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from Mobile_Inspectionapp.renderer import UserRenderer
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import action
from django.contrib.auth.hashers import make_password
from .validater import *
from django.http import JsonResponse



# class RegisterView(APIView):
#  renderer_classes=[UserRenderer]
 
#  def post(self,request,format=None):
#     serializer=UserSerializer(data=request.data)
    
#     if serializer.is_valid(raise_exception=True):
#         user=serializer.save()
#         print(serializer.data)
#         data={'First_name':serializer.data['First_name'],'Last_name':serializer.data['Last_name'],'email':serializer.data['email'],'title':str(serializer.data['title']),'mobile':serializer.data['mobile'],'attribute_name':str(serializer.data['attribute_name'])}
#         return JsonResponse({'message':'Registeration Successfull','status':'200','data':data})
#     # return JsonResponse(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
class RegisterView(APIView):
    @csrf_exempt 
    @action(detail=False, methods=['post'])
    def post(self, request, format=None):
     First_name=request.data.get('First_name')
     Last_name=request.data.get('Last_name')
     email=request.data.get('email')
     title=request.data.get('title')
     mobile=request.data.get('mobile')
     attribute_name=request.data.get('attribute_name')
     password=make_password(request.data.get('password'))
     print(password)
     if User.objects.filter(email=email).exists():
         user = User.objects.get(email = email)
         data = {
                'message':'Email is Already Exists',
                'status':"400",
                "data":{}
            }
         return Response(data)
     else:
         registred_data=User.objects.create(First_name=First_name,Last_name=Last_name,email=email,title=title,mobile=mobile,attribute_name=attribute_name,password=password)
         serializer = UserSerializer(data=registred_data)
         registred_data.save()
         dict_data={"Firstname":First_name,"Lastname":Last_name,"email":email,"title":title,"mobile":mobile,"attribute_name":attribute_name}
         return JsonResponse({'message':'Registeration Successfull','status':'200','data':dict_data})

class UserLoginView(APIView):
  renderer_classes = [UserRenderer]
  serializer_class = UserLoginSerializer
  def post(self, request, *args, **kwargs):
        serializer_class = UserLoginSerializer(data=request.data)
        if serializer_class.is_valid(raise_exception=True):
            print('data--',serializer_class.data['token'])
            email=serializer_class.data['email']
            print(email)
            userdetail=User.objects.filter(email=email).values('First_name','Last_name','email','mobile','title','attribute_name')
            print("print--- detail",userdetail[0]['First_name'])
            data={'First_name':userdetail[0]['First_name'],'Last_name':userdetail[0]['Last_name'],'email':userdetail[0]['email'],'mobile':userdetail[0]['mobile'],'title':str(userdetail[0]['title']),'attribute_name':userdetail[0]['attribute_name']}
            return JsonResponse({'message':'Login Successfull','status':'200','data':data})
        return JsonResponse(serializer_class.errors, status=HTTP_400_BAD_REQUEST)
    
# class Logout(APIView):
#     queryset = User.objects.all()
#     serializer_class = UserLogoutSerializer

#     def post(self, request, *args, **kwargs):
#         serializer_class = UserLogoutSerializer(data=request.data)
#         if serializer_class.is_valid(raise_exception=True):
#             return Response(serializer_class.data, status=HTTP_200_OK)
#         return Response(serializer_class.errors, status=HTTP_400_BAD_REQUEST) 
    
class ServiceAgreementView(APIView):
   
    def get(self, request, format=None):
        service = ServiceAgreement.objects.all().order_by('id')
        serializer = ServiceAgreementSerializer(service, many=True)
        print(serializer)
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
            
            
class ContactView(APIView):
 def post(self,request,format=None):
    serializer=ContactSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        user=serializer.save()
        data={'firstname':serializer.data['firstname'],'lastname':serializer.data['lastname'],'email':serializer.data['email'],'phone':serializer.data['phone'],'street_number':serializer.data['street_number'],'address':serializer.data['address'],'city':serializer.data['city'],'state':serializer.data['state'],'country':serializer.data['country'],'zipcode':serializer.data['zipcode']}
        return JsonResponse({'message':'Thanks For Your Query','status':'200','data':data})
    return JsonResponse(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

class CartView(APIView):
 def post(self,request,format=None):
    serializer=CartSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        user=serializer.save()
        return JsonResponse(serializer.data)
    return JsonResponse(serializer.errors,status=status.HTTP_400_BAD_REQUEST)            
            
            
# class LeadView(APIView): 
#    renderer_classes=[UserRenderer]
#    def post(self, request, format=None):
#       serializer=LeadSerializer(data=request.data)
#       if serializer.is_valid(raise_exception=True):
#             serializer.save()
#             return Response({"message":"sucess"})
#       return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) 
  
# class LeadAddressView(APIView): 
#    renderer_classes=[UserRenderer]
#    def post(self, request, format=None):
#       serializer=LeadAddressSerializer(data=request.data)
#       if serializer.is_valid(raise_exception=True):
#             serializer.save()
#             return Response({"message":"sucess"})
#       return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)             

    
# class PromotionCategoryView(APIView):
   
#     def get(self, request, format=None):
#         service = Promotion_Category.objects.all().order_by('id')
#         serializer = PromotionCategorySerializer(service, many=True)
#         return Response(serializer.data)
    
    
#     def post(self, request, format=None):
#         serializer = PromotionCategorySerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response({'message':'Successfully added'})
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
# class PromotionView(APIView):
   
#     def get(self, request, format=None):
#         service = Promotion.objects.all().order_by('id')
#         serializer = PromotionSerializer(service, many=True)
#         return Response(serializer.data)
    
    
#     def post(self, request, format=None):
#         serializer = PromotionSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response({'message':'Successfully added'})
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)