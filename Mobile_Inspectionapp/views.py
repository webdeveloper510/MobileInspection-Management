from .models import *
from .serializer import *
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from Mobile_Inspectionapp.renderer import UserRenderer
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import action
from .validater import *
from django.http import JsonResponse
import json
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated ,AllowAny
from django.http import Http404
from rest_framework.authtoken.models import Token
from django.contrib import auth
from django.contrib.auth import get_user_model 
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import api_view, permission_classes

from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated

# Generate Token Manually
def get_tokens_for_user(user):
  refresh = RefreshToken.for_user(user)
  return {
      'refresh': str(refresh),
      'access': str(refresh.access_token),
  }
#HELLOO
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
     if User.objects.filter(mobile=mobile).exists():
          data = {
                'message':'mobile number is already exist',
                'status':"400",
                "data":{}
            }
          return Response(data)
     if '@' not in email:
         return Response({"message":"please enter valid email"})
     else:
         registred_data=User.objects.create(First_name=First_name,Last_name=Last_name,email=email,title=title,mobile=mobile,attribute_name=attribute_name,password=password)
         serializer = UserSerializer(data=registred_data)
         registred_data.save()
        #  token = get_tokens_for_user(registred_data)
         id=User.objects.filter(email=email).values('id')
         print(id[0]['id'])
         dict_data={'id':str(id[0]['id']),"Firstname":First_name,"Lastname":Last_name,"email":email,"title":title,"mobile":mobile,"attribute_name":attribute_name}
         return JsonResponse({'message':'Registeration Successfull','status':'200','data':dict_data})


class UserLoginView(APIView): 
    @csrf_exempt 
    @action(detail=False, methods=['post'])
    @permission_classes((AllowAny,))
    def post(self, request, format=None):
        emaild=request.data.get('email')
        password=request.data.get('password')
        user=User.objects.filter(email=emaild).values('ifLogged','email','password','mobile')

        if emaild=='' or password == '':
            return JsonResponse({"message":"Email or PAssword Required","status":"400","data":{}})
            
        if not User.objects.filter(email=emaild , password = password).values('email', 'password') :
            
            return JsonResponse({"message":"wrong Email id or password","status":"400","data":{}})
        
        else:
            user=User.objects.filter(email=emaild).update(ifLogged=True)
            userdetail=User.objects.filter(email=emaild).values('id','First_name','Last_name','email','mobile','title','attribute_name')
            print("print--- detail",userdetail[0]['First_name'])
            data={'id':str(userdetail[0]['id']),'First_name':userdetail[0]['First_name'],'Last_name':userdetail[0]['Last_name'],'email':userdetail[0]['email'],'mobile':userdetail[0]['mobile'],'title':str(userdetail[0]['title']),'attribute_name':userdetail[0]['attribute_name']}
            return JsonResponse({'message':'Login Successfull','status':'200','data':data})
        
class LogoutUser(APIView):
#   permission_classes = [IsAuthenticated]
  authentication_classes = [TokenAuthentication]
  def post(self, request, format=None):
    return Response({'msg':'Logout Successfully'},status=status.HTTP_200_OK)
    
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
          
          
# class ServiceView(APIView):
   
#     def get(self, request, format=None):
#             service_data = Service.objects.all()
#             serializer = ServiceSerializer(service_data, many=True)
#             array = []
#             image_array = []            
#             for x in serializer.data:
#                 id=(x['id'])   
#                 name=(x['name'])
#                 description=(x['description'])
#                 service_type_id=(x['service_type_id'])
#                 service_image = Service_Image.objects.all()
#                 image_serializer = Service_ImageSerializer(service_image, many=True)
#                 for i in image_serializer.data:
#                     service_id = i['service_id']
#                     if id== service_id:
#                         print (id== service_id)
#                         image = i['service_image']
                
#                 dict_data={"id":str(id),"name":name,"description":description,"service_image":image,"service_type_id":str(service_type_id)}
#                 array.append(dict_data)
#             return JsonResponse(array)
        
    
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
        serviceid=serializer.data['id']
        service_type_id=serializer.data['service_type_id']
        service = Service_Image.objects.all().order_by('id')
        serializer2 = Service_ImageSerializer(service, many=True)
        array1=[]
        for x in serializer2.data:
            if serializer.data['id']==x['service_id']:
                service_image1=x['service_image']
                print(service_image1)
                array1.append(service_image1)
        servicetype_detail=ServiceType.objects.filter(id=service_type_id).values('id','price','service_type_name','service_type_description')
        price=servicetype_detail[0]['price']
        service_type_id=servicetype_detail[0]['id']
        service_type_name=servicetype_detail[0]['service_type_name']
        array2=[]
        servicedata={"service_type_id":str(service_type_id),"service_Type_name":service_type_name}
        array2.append(servicedata)
        service_type_description=servicetype_detail[0]['service_type_description']
        
        data={"id":str(serializer.data['id']),"name":serializer.data['name'],"description":serializer.data['description'],"service_image":array1,"price":str(price),"service_type":array2,"service_type_description":service_type_description}
        return JsonResponse({ "code": "200","message": "Success","data":data})
    
class CustomerInfo(APIView):
    
    @csrf_exempt
    def get_object(self, pk):
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            raise Http404
    
    @csrf_exempt
    def get(self, request, pk, format=None):
        user = self.get_object(pk)
        serializer = UserSerializer(user)
        return Response(serializer.data)
            
 
 
class AddressView(APIView):
   
    def get(self, request, format=None):
        service = Address.objects.all().order_by('id')
        serializer = AddressSerializer(service, many=True)
        array=[]
        for x in serializer.data:
            id=(x['id']) 
            unit_number=(x['unit_number']) 
            addressline1=(x['addressline1']) 
            city=(x['city']) 
            state=(x['state']) 
            postal_code=(x['postal_code']) 
            country_name=(x['country_name']) 
            data={"id":str(id),"unit_number":unit_number,"addressline1":addressline1,"city":city,"state":state,"postal_code":postal_code,"country_name":country_name}
            array.append(data)
        return JsonResponse({ "code": "200","message": "Success","data":array})
    
class EstablishmentView(APIView):
    def get(self, request, format=None):
        service = Establishment.objects.all().order_by('id')
        serializer = EstablishmentSerializer(service, many=True)
        array=[]
        for x in serializer.data:
          id=(x['id'])
          customer_id= (x['customer_id'])
          address_id=(x['address_id'])
          name=(x['name'])
          establishment_type_id=(x['establishment_type_id'])
          data={"id":str(id),"customer_id":str(customer_id),"address_id":str(address_id),"name":name,"establishment_type_id":str(establishment_type_id)}
          array.append(data)
        return JsonResponse({ "code": "200","message": "Success","data":array})

class EstablishmentRegisterView(APIView):
 renderer_classes=[UserRenderer]
 def post(self,request,format=None):
    customer_id = request.data.get('customer_id')
    address_id = request.data.get('address_id')
    name = request.data.get('name')
    print('id--',customer_id)
    establishment_type_id = request.data.get('establishment_type_id')
    if customer_id:
        if User.objects.filter(id= customer_id).exists() :
            num = 0
        else:
            return JsonResponse({"message":" Customer id  does not exist","code":"400"})
    else:
            return JsonResponse({"message":" customer id is required ","code":"400"})
    if address_id:
        if Address.objects.filter(id= address_id).exists():
            num = 0
        else:
            return JsonResponse({"message":"address id  does not exist","code":"400"})
    else:
       return JsonResponse({"message":"address id is required ","code":"400"})
    if establishment_type_id:
        if Establishment_type.objects.filter(id= establishment_type_id).exists():
            num = 0
        else:
            return JsonResponse({"message":" address id  does not exist","code":"400"})
    else:
        return JsonResponse({"message":" address id is required  ","code":"400"})
    if name:
        name = name
    else:
        return JsonResponse({"message":"name field can not be empty ","code":"400"})
    #created instance for user ,address id and establishment type id
    user = User.objects.get(id= customer_id)
    user.user = user
    # UserID  = User.objects.filter(id= customer_id).values('id')
    EstablishmentID = Establishment_type.objects.get(id= establishment_type_id)
    EstablishmentID.EstablishmentID =EstablishmentID
    AddressID = Address.objects.get(id= address_id)
    AddressID.AddressID = AddressID
        
    esdata=Establishment.objects.create(customer_id=user  ,  address_id=AddressID,   name=name,   establishment_type_id=EstablishmentID)
    serializer = EstablishmentSerializer(data=esdata)
    esdata.save()
    dict_data={'customer_id':customer_id  , 'address_id':address_id,   'name':name,   'establishment_type_id':establishment_type_id}
    return JsonResponse({"message":"success","code":"200","data":dict_data})

    
    

    
# class ContactView(APIView):
#  def post(self,request,format=None):
#     serializer=ContactSerializer(data=request.data)
#     if serializer.is_valid(raise_exception=True):
#         user=serializer.save()
#         # data={'firstname':serializer.data['firstname'],'lastname':serializer.data['lastname'],'email':serializer.data['email'],'phone':serializer.data['phone'],'street_number':serializer.data['street_number'],'unit_number':serializer.data['unit_number'],'address':serializer.data['address'],'address1':serializer.data['address1'],'city':serializer.data['city'],'state':serializer.data['state'],'country':serializer.data['country'],'zipcode':serializer.data['zipcode']}
#         return JsonResponse({'message':'Thanks for contacting us','status':'200'})
#     # return JsonResponse(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

class CustomerAddressView(APIView):
    @csrf_exempt
    def get_object(self, pk):
        try:
            return Customer_Address.objects.get(pk=pk)
        except Customer_Address.DoesNotExist:
            raise Http404
    
    @csrf_exempt
    def get(self, request, pk, format=None):
        print("fyhgvbjgjbh",pk)
        if Customer_Address.objects.filter(id=pk).exists():
            Csdata = Customer_Address.objects.filter(id=pk).values('customer_id__First_name','customer_id__Last_name','customer_id__email','customer_id__mobile','customer_id__title',
                                                                'customer_id__attribute_name','address_id__unit_number','address_id__addressline1','address_id__city','address_id__state',
                                                                'address_id__postal_code','address_id__country_name')
            print(Csdata[0]['customer_id__First_name'])
            data={"First_name":Csdata[0]['customer_id__First_name'],"Last_name":Csdata[0]['customer_id__Last_name'],
                "email":Csdata[0]['customer_id__email'],"mobile":Csdata[0]['customer_id__mobile'],"title":Csdata[0]['customer_id__title'],"attribute_name":Csdata[0]['customer_id__attribute_name'],
                "unit_number":str(Csdata[0]['address_id__unit_number']),"addressline1":str(Csdata[0]['address_id__addressline1']),"city":str(Csdata[0]['address_id__city']),"state":str(Csdata[0]['address_id__state']),
                "postal_code":str(Csdata[0]['address_id__postal_code']),"country_name":str(Csdata[0]['address_id__country_name'])}
        
            return JsonResponse({"code":"200","message":"success","data":data})
        else:
            return JsonResponse({"code":"400","message":"user does not Exist"})

    
    @csrf_exempt
    def put(self, request, pk, format=None):
        print("",pk)
        if Customer_Address.objects.filter(id = pk).exists():
            customerdata = Customer_Address.objects.filter(id=pk).values("id",'customer_id','address_id','customer_id__First_name','customer_id__Last_name','customer_id__email','customer_id__mobile','customer_id__title',
                                                                'customer_id__attribute_name','address_id__unit_number','address_id__addressline1','address_id__city','address_id__state',
                                                                'address_id__postal_code','address_id__country_name'
                                                                )
            print(customerdata)
            # id=customerdata[0]['id']
            customer_id=customerdata[0]['customer_id']
            address_id=customerdata[0]['address_id']
            First_name=request.data.get('First_name')
            Last_name=request.data.get('Last_name')
            email=request.data.get('email')
            mobile=request.data.get('mobile')
            title=request.data.get('title')
            attribute_name=request.data.get('attribute_name')
            unit_number=request.data.get('unit)_number')
            addressline1=request.data.get('addressline1')
            city=request.data.get('city')
            state=request.data.get('state')
            postal_code=request.data.get('postal_code')
            country_name=request.data.get('country_name')
            dict={'email':email,'First_name':First_name,"Last_name":Last_name,"mobile":mobile,"title":title,"attribute_name":attribute_name,
                "unit_number":str(unit_number),"addressline1":addressline1,"city":city,"state":state,"postal_code":postal_code,
                "country_name":country_name}
            if email:
                email=email
            else:
                email=customerdata[0]['customer_id__email']
            if First_name:
                First_name=First_name
                
            else:
                First_name=customerdata[0]['customer_id__First_name']
            if Last_name:
                Last_name=Last_name
            else:
                Last_name=customerdata[0]['customer_id__Last_name']
            if mobile:
                mobile=mobile
            else:
                mobile=customerdata[0]['customer_id__mobile']
            if title:
                title=title
            else:
                title=customerdata[0]['customer_id__title']
            if attribute_name:
                attribute_name=attribute_name
            else:
                attribute_name=customerdata[0]['customer_id__attribute_name']
            if unit_number:
                unit_number=unit_number
            else:
                unit_number=customerdata[0]['address_id__unit_number']
            if addressline1:
                addressline1=addressline1
            else:
                addressline1=customerdata[0]['address_id__addressline1']
            if city:
                city=city
            else:
                city=customerdata[0]['address_id__city']
            if state:
                state=state
            else:
                state=customerdata[0]['address_id__state']
            if postal_code:
                postal_code=postal_code
            else:
                postal_code=customerdata[0]['address_id__postal_code']
            if country_name:
                country_name=country_name
            else:
                country_name=customerdata[0]['address_id__country_name']
            
            
            Userdata=User.objects.filter(id=customer_id).update(email=email,First_name=First_name,Last_name=Last_name,mobile=mobile,title=title,attribute_name=attribute_name)
            address_data=Address.objects.filter(id=address_id).update(unit_number=unit_number,addressline1=addressline1,city=city,
                                                                    state=state,postal_code=postal_code,country_name=country_name)
        else:
            return JsonResponse({"code":"400","message":"user does not exist"})
        return JsonResponse({"code":"200","message":"you data is updated successfully","data":dict})

    

class ContactView(APIView):   
    @csrf_exempt 
    @action(detail=False, methods=['post'])
    def post(self, request, format=None):
        firstname=request.data.get('firstname')
        Lastname=request.data.get('lastname')
        email=request.data.get('email')
        phone=request.data.get('phone')
        street_number=request.data.get('street_number')
        unit_number=request.data.get('unit_number')
        address=request.data.get('address')
        address1=request.data.get('address1')
        city=request.data.get('city')
        state=request.data.get('state')
        country=request.data.get('country')
        zipcode=request.data.get('zipcode')
        comment=request.data.get('comment')
        
        if firstname=="":
            return JsonResponse({"message":"Firstname is required","status":"400"})
        if Lastname=="":
            return JsonResponse({"message":"lastname is required","status":"400"})
        if email=="":
            return JsonResponse({"message":"email is required","status":"400"})
        if phone=="":
            return JsonResponse({"message":"phone number is required","status":"400"})
        else:
            contact_data=Contact.objects.create(firstname=firstname,lastname=Lastname,email=email,phone=phone,
                                            street_number=street_number,unit_number=unit_number,address=address,address1=address1,city=city,
                                            state=state,country=country,zipcode=zipcode,comment=comment)
            
            serializer = UserSerializer(data=contact_data)
            contact_data.save()
            return JsonResponse({"message":"thanks for contacting us","status":"200"})

         
            
class Serviceview(APIView):   

    def get(self, request, format=None):
            service_data = Service.objects.all()
            serializer = ServiceSerializer(service_data, many=True)
            array = []
            image_array = []            
            for x in serializer.data:
                id=(x['id'])   
                name=(x['name'])
                description=(x['description'])
                service_type_id=(x['service_type_id'])
                service_image = Service_Image.objects.all()
                image_serializer = Service_ImageSerializer(service_image, many=True)
                for i in image_serializer.data:
                    service_id = i['service_id']
                    if id== service_id:
                        print (id== service_id)
                        image = i['service_image']
                
                dict_data={"id":str(id),"name":name,"description":description,"service_image":image,"service_type_id":str(service_type_id)}
                array.append(dict_data)
            return JsonResponse({"code":"200","message":"success","Data":array})
        
class TestLoginView(APIView):  
    # get method handler
    permission_classes = (IsAuthenticated, )
    queryset = User.objects.all()
    serializer_class = UserLoginSerializer

    def post(self, request, *args, **kwargs):
        serializer_class = UserLoginSerializer(data=request.data)
        if serializer_class.is_valid(raise_exception=True):
            return Response(serializer_class.data, status=HTTP_200_OK)
        return Response(serializer_class.errors, status=HTTP_400_BAD_REQUEST)     

# class Test(APIView):  
#     @csrf_exempt 
#     @action(detail=False, methods=['post'])
#     def post(self, request, format=None):
#         customer_id=request.data.get('customer_id')
#         address_id=request.data.get('address_id')
#         name=request.data.get('name')
#         establishment_type_id=request.data.get('establishment_type_id')
#         c_id=User.objects.filter(id=customer_id).values('id')
#         a_id=Address.objects.filter(id=address_id).values('id')
#         e_id=Establishment_type.objects.filter(id=establishment_type_id).values('id')
#         print("customer id---",c_id[0]['id'])
#         print("address id---",a_id[0]['id'])
#         print("Establishmenttype id ---",e_id[0]['id'])
        
#         if customer_id==None:
#             return JsonResponse({"error":"Customer_id is required ","code":"400"})
#         else:
#          return Response(123)
from django.conf import settings

class pdfview(APIView):
    def get(self, request, format=None):
        service_data = uploadpdf.objects.all()
        serializer = UploadpdfSerializer(service_data, many=True)
        print(serializer.data[0])
        url = settings.BASE_URL+serializer.data[0]['uploadfile']
        return Response(url)