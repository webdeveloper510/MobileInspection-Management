from .models import *
from .serializer import *
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from Mobile_Inspectionapp.renderer import UserRenderer
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import action
from django.contrib.auth.hashers import check_password
from .validater import *
from django.http import JsonResponse
import json
from rest_framework.authtoken.models import Token
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import login
from django.contrib.auth import authenticate
from django.contrib.auth import authenticate, login, logout
from django.utils import timezone
from rest_framework.permissions import IsAuthenticated
from django.http import Http404

def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

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
     password=request.data.get('password')
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
        #  token = get_tokens_for_user(registred_data)
         dict_data={"Firstname":First_name,"Lastname":Last_name,"email":email,"title":title,"mobile":mobile,"attribute_name":attribute_name}
         return JsonResponse({'message':'Registeration Successfull','status':'200','data':dict_data})

# class UserLoginView(APIView):
#   renderer_classes = [UserRenderer]
#   serializer_class = UserLoginSerializer
#   def post(self, request, *args, **kwargs):
#         serializer_class = UserLoginSerializer(data=request.data)
        
#         if serializer_class.is_valid(raise_exception=True):
#             print('data--',serializer_class.data['token'])
#             email=serializer_class.data['email']
#             print(email)
#             userdetail=User.objects.filter(email=email).values('First_name','Last_name','email','mobile','title','attribute_name')
#             print("print--- detail",userdetail[0]['First_name'])
#             data={'First_name':userdetail[0]['First_name'],'Last_name':userdetail[0]['Last_name'],'email':userdetail[0]['email'],'mobile':userdetail[0]['mobile'],'title':str(userdetail[0]['title']),'attribute_name':userdetail[0]['attribute_name']}
#             return JsonResponse({'message':'Login Successfull','status':'200','data':data})
#         return JsonResponse(serializer_class.errors, status=status.HTTP_200_OK)

class UserLoginView(APIView): 
    @csrf_exempt 
    @action(detail=False, methods=['post'])
    def post(self, request, format=None):
     emaild=request.data.get('email')
     password=request.data.get('password')
     user=User.objects.filter(email=emaild).values('ifLogged','email','password')
     if not User.objects.filter(email=emaild).values('email'):
         
        return Response({"message":"user does not exist"})
     print(user[0]['ifLogged'])
     print(user[0]['email'])
     print(user[0]['password'])
     emaildb=user[0]['email']
     print(emaildb)
     passworddb=user[0]['password']
     ifLogged=(user[0]['ifLogged'])
     print('if logged---',ifLogged)
    #  data={"message":"User already logged in.","status":"400","data":{}}
    
     if ifLogged==True:
         print(123)
         return JsonResponse({"message":"User already logged in.","status":"400","data":{}})
    #  if User.objects.get(email = emaildb):
    #       print("hre")
    #     #   user = User.objects.get(email != esssmail)
    #       return Response({"message":"user does not exist"})
     else:
         user=User.objects.filter(email=emaild).update(ifLogged=True)
         userdetail=User.objects.filter(email=emaild).values('First_name','Last_name','email','mobile','title','attribute_name')
         print("print--- detail",userdetail[0]['First_name'])
         data={'First_name':userdetail[0]['First_name'],'Last_name':userdetail[0]['Last_name'],'email':userdetail[0]['email'],'mobile':userdetail[0]['mobile'],'title':str(userdetail[0]['title']),'attribute_name':userdetail[0]['attribute_name']}
         return JsonResponse({'message':'Login Successfull','status':'200','data':data})
            
            
        
        
        
    


    
class ServiceAgreementView(APIView):
   
    def get(self, request, format=None):
        service = ServiceAgreement.objects.all().order_by('id')
        serializer = ServiceAgreementSerializer(service, many=True)
        array=[]
        for x in serializer.data:
            id=(x['id'])
            service_agreement_form=(x['service_agreement_form'])
            signature=(x['signature'])
            date=(x['date'])
            time=(x['time'])
            customer_id=(x['customer_id'])
            dict_data={"id":str(id),"service_agreement_form":service_agreement_form,"signature":signature,"date":date,"time":time,"customer_id":str(customer_id)}
            array.append(dict_data)
            print(array)
        return JsonResponse({"code":"200","message":"Success","data":array})
          
          
class ServiceView(APIView):
   
    def get(self, request, format=None):
        service = Service.objects.all().order_by('id')
        serializer = ServiceSerializer(service, many=True)
        array=[]
        for x in serializer.data:
            id=(x['id'])   
            name=(x['name'])
            description=(x['description'])
            service_image=(x['service_image'])
            service_type_id=(x['service_type_id'])
            dict_data={"id":str(id),"name":name,"description":description,"service_image":service_image,"service_type_id":str(service_type_id)}
            array.append(dict_data)
            print(array)
        return JsonResponse({"code":"200","message":"Success","data":array})   
        
    
class ServiceTypeView(APIView):
   
    def get(self, request, format=None):
        service = ServiceType.objects.all().order_by('id')
        serializer = ServiceTypeSerializer(service, many=True)
        array=[]
        array1=[]
        for x in serializer.data:
            id=(x['id'])   
            service_type_name=(x['service_type_name'])
            price=(x['price'])
            service_type_description=(x['service_type_description'])
            dict_data={"id":str(id),"service_type_name":service_type_name,"price":str(price),"service_type_description":service_type_description,"service_agreement_id":""}
            
            array.append(dict_data)
            # print(array)
        return JsonResponse({"code":"200","message":"Success","data":array})  
    

class ServiceListView(APIView):
    
    @csrf_exempt
    def get_object(self, pk):
        try:
            return Service.objects.get(pk=pk)
        except Service.DoesNotExist:
            raise Http404  
        
    def get(self, request, pk, format=None):
        snippet = self.get_object(pk)
        serializer = ServiceSerializer(snippet)
        print(serializer.data['id'])
        service_type_id=serializer.data['service_type_id']
        servicetype_detail=ServiceType.objects.filter(id=service_type_id).values('price','service_type_name','service_type_description')
        price=servicetype_detail[0]['price']
        service_type_name=servicetype_detail[0]['service_type_name']
        service_type_description=servicetype_detail[0]['service_type_description']
        
        data={"id":str(serializer.data['id']),"name":serializer.data['name'],"description":serializer.data['description'],"service_image":serializer.data['service_image'],"service_type_id":str(serializer.data['service_type_id']),"price":str(price),"service_type_name":service_type_name,"service_type_description":service_type_description}
        return JsonResponse({ "code": "200","message": "Success","data":data})
            
            
class ContactView(APIView):
 def post(self,request,format=None):
    serializer=ContactSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        user=serializer.save()
        # data={'firstname':serializer.data['firstname'],'lastname':serializer.data['lastname'],'email':serializer.data['email'],'phone':serializer.data['phone'],'street_number':serializer.data['street_number'],'unit_number':serializer.data['unit_number'],'address':serializer.data['address'],'address1':serializer.data['address1'],'city':serializer.data['city'],'state':serializer.data['state'],'country':serializer.data['country'],'zipcode':serializer.data['zipcode']}
        return JsonResponse({'message':'Thanks for contacting us','status':'200'})
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