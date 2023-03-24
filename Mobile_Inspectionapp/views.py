from .models import *
from django.contrib.auth.models import User
from .serializer import *
from rest_framework.response import Response
from rest_framework.views import APIView
from Mobile_Inspectionapp.renderer import UserRenderer
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import action
from .validater import *
from django.http import JsonResponse
from rest_framework_simplejwt.tokens import RefreshToken,AccessToken
from rest_framework.permissions import IsAuthenticated ,AllowAny
from django.http import Http404
from rest_framework.decorators import  permission_classes
from django.conf import settings
from datetime import date 
from django.contrib.auth import authenticate
from django.db.models import Q 
from uuid import uuid4
from django.contrib.auth import login
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from Mobile_Inspection.settings import BASE_URL
from Mobile_Inspectionapp.utils import Util
from django.core.mail import EmailMultiAlternatives, message

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
     position=request.data.get('position')
     if not email:
          return Response({"message":"email is required",'status':"400"})
     if '@' not in email:
         return Response({"message":"please enter valid email",'status':"400"})
     if not First_name:
         return Response({"message":"Firstname is required",'status':"400"})
     if not Last_name:
         return Response({"message":"Lastname is required",'status':"400"})
     if not password:
         return Response({"message":"password is required",'status':"400"})
     if not mobile:
         return Response({"message":"mobile number is required",'status':"400"})
     if User.objects.filter(email=email).exists():

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
     
     serializer = UserRegistrationSerializer(data=request.data)
     if serializer.is_valid(raise_exception=True):
        user = serializer.save()
        id=serializer.data['id']
        dict_data={"id":str(id),"Firstname":First_name,"Lastname":Last_name,"email":email,"title":title,"mobile":mobile,"attribute_name":attribute_name,"position":position}
        return JsonResponse({'message':'Registeration Successfull','status':'200','data':dict_data})


class UserLoginView(APIView): 
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        user = authenticate(email=email, password=password)
        if not email:
             return JsonResponse({"message":"email is required","status":"400","data":{}})
        if not password:
             return JsonResponse({"message":"password is required","status":"400","data":{}})
        
        if not User.objects.filter(email=email).exists(): 
            return JsonResponse({"message":"invalid email address","status":"400"})
        
        if user:
            login(request, user)
            userd=User.objects.filter(email=email).update(ifLogged=True)
            ifLoggedvalue=User.objects.filter(email=email).values('ifLogged')
            value=ifLoggedvalue[0]['ifLogged']
            if value == True:
                token=uuid4()
                user=User.objects.filter(email=email).update(token=token)
                userdetail=User.objects.filter(email=email).values('id','First_name','Last_name','email','mobile','title','attribute_name','position','role')
                data={'id':str(userdetail[0]['id']),'First_name':userdetail[0]['First_name'],'Last_name':userdetail[0]['Last_name'],'email':userdetail[0]['email'],'mobile':userdetail[0]['mobile'],'title':str(userdetail[0]['title']),'attribute_name':userdetail[0]['attribute_name'],'position':userdetail[0]['position'],'role':userdetail[0]['role']}
            return JsonResponse({'message':"Login Successfully","token":token,"data":data})
        else:
            return JsonResponse({"message":"Invalid  credentials","status":"400","data":{}})


class Logout(APIView):
    def post(self, request, format=None):
     token=request.data.get('token')
     if not token:
          return JsonResponse({'message':'logout successfully','status':'200'})
     if not User.objects.filter(token=token).values('token'):
         return JsonResponse({'message':'logout successfully','status':'200'})
     else:
        user = User.objects.filter(token=token).values('token','id')
        User.objects.filter(token=token).update(token=None)
        return JsonResponse({'message':'logout successfully','status':'200'})

class SendPasswordResetLink(APIView):  
     @csrf_exempt 
     def post(self, request, format=None):
        email=request.data.get('email')

        if not email:
            return Response({"message":"email is required","status":"400"})
        
        if not User.objects.filter(email=email).exists():
            return Response({"message":"user with this email does not exists","status":"400"})

        if User.objects.filter(email=email,user_created_by_admin=True).exists():
            user = User.objects.get(email=email)
            link=" http://127.0.0.1:8000/userpasswordreset/"
            subject, from_email, to = 'Reset Your Password', settings.EMAIL_HOST_USER, email
            text_content = 'This is an important message.'
            html_content = '<p>Click Following Link to Reset Your Password</p>' + link
            msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
            msg.attach_alternative(html_content, "text/html")
            msg.send()
            return JsonResponse({'message':'your password reset link successfully send to your email','status':'200'})
        else:
            user = User.objects.get(email=email)
            link = 'http://127.0.0.1:8000/password_set/'
            print(link)
            print('Password Reset Link', link)
            return Response({"message":"success",'status':'200','resetlink':link})

class PasswordSetViewSet(APIView):
    renderer_classes=[UserRenderer]
    def post(self, request, format=None):
     email=request.data.get('email')
     password=request.data.get('password')
     if not email:
            return Response({'message':'email is required','status':'400'})
     if not  User.objects.filter(email=email).exists():
          return Response({'message':'email does not exists','status':'400'})
     if not password:
         return Response({'message':'please enter new password','status':'400'})
     user = User.objects.get(email=email)
     user.set_password(password)
     user.save()
     return Response({'message':'your password is successfully changed','status':'200'})

    
class CustomerProfileView(APIView): 
    @csrf_exempt
    def get(self, request, pk, format=None):
           
            if User.objects.filter(id=pk).exists():
                Csdata = User.objects.filter(id=pk).values('id','First_name','Last_name','email','mobile','title',
                                                                    'attribute_name','position')
                data={"id":str(Csdata[0]['id']),"First_name":Csdata[0]['First_name'],"Last_name":Csdata[0]['Last_name'],
                    "email":Csdata[0]['email'],"mobile":Csdata[0]['mobile'],"title":Csdata[0]['title'],"attribute_name":Csdata[0]['attribute_name'],"position":Csdata[0]['position']}
            
                return JsonResponse({"status":"200","message":"success","data":data})
            else:
                return JsonResponse({"status":"400","message":"user does not Exist"}) 
              
class Profilenotupdate(APIView): 
    @csrf_exempt
    def get(self, request,format=None):
        return JsonResponse({"message":" url not found","status":"400"})
               
class Profileupdate(APIView): 
    @csrf_exempt
    def post(self, request,format=None):
        customer_id=request.data.get('customer_id')
        First_name=request.data.get('First_name')
        Last_name=request.data.get('Last_name')
        email=request.data.get('email')
        mobile=request.data.get('mobile')
        title=request.data.get('title')
        attribute_name=request.data.get('attribute_name')
        position=request.data.get('position')
        if not customer_id:
            return JsonResponse({"message":" Customer id is required","status":"400"})
        if not email:
            return JsonResponse({"message":" email id is required","status":"400"})
        if User.objects.filter(id=customer_id).exists():
            customerdata = User.objects.filter(id=customer_id).values('id','First_name','Last_name','email','mobile','title','position','attribute_name')
            print(customerdata)
            if email:
                email=email
            else:
                email=customerdata[0]['email']
            
            Userdata=User.objects.filter(id=customer_id).update(email=email,First_name=First_name,Last_name=Last_name,mobile=mobile,title=title,attribute_name=attribute_name,position=position)
        else:
            return JsonResponse({"status":"400","message":"user does not exist"})
        return JsonResponse({"status":"200","message":"your data is updated successfully"})
    
    
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
        return JsonResponse({"status":"200","message":"Success","data":array})
          
             
    
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
        return JsonResponse({"status":"200","message":"Success","data":array})  
    
#Get service by id

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
        return JsonResponse({ "status": "200","message": "Success","data":data})
    
# address api 
 
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
        return JsonResponse({"status": "200","message": "Success","data":array})
    
class AddAddressView(APIView):
 renderer_classes=[UserRenderer]
 @csrf_exempt
 def post(self,request,format=None):
    customer_id=request.data.get('customer_id')
    Data=request.data.get('data')
    if not Data:
        return JsonResponse({"message":"address list is empty","status":"400"})
    if not customer_id:
        return JsonResponse({"message":"customer id  is empty","status":"400"})
    if not User.objects.filter(id=customer_id).exists():
            return JsonResponse({"message":" user not found","status":"400"})
    for x in Data:
        unit_number=x['unit_number']
        
        if not unit_number:
            
         return JsonResponse({"message":"unit number is not available","status":"400"})
     
        if Address.objects.filter(unit_number=unit_number).exists():
            return JsonResponse({"message":" Unit number is already available","status":"400"}) 
        
        address=x['address']
        if not  address:
         return JsonResponse({"message":"address is not available ,","status":"400"})
        
        city=x['city']
        if not  city:
         return JsonResponse({"message":"city is not available ,","status":"400"})
     
        state=x['state']
        if not  state:
         return JsonResponse({"message":"state is not available ,","status":"400"})
     
        country=x['country']
        if not  country:
         return JsonResponse({"message":"country is not available ,","status":"400"})
     
        zip_code=x['zip_code']
        if not  zip_code:
         return JsonResponse({"message":"zipcode is not available ,","status":"400"})
        
    for x in Data:
        unit_number=x['unit_number']
        address=x['address']
        city=x['city']
        state=x['state']
        country=x['country']
        zip_code=x['zip_code']
        user = User.objects.get(id= customer_id)
        user.user = user
        addressdata=Address.objects.create(customer_id=user,unit_number=unit_number,addressline1=address,city=city,state=state,postal_code=zip_code,country_name=country)
        serializer2=AddressSerializer(data=addressdata)
        addressdata.save()
        print(addressdata)
    return JsonResponse({"message":"your  adddress is successfully saved","status":"200"})  

class UpdateAddressView(APIView):
  @csrf_exempt
  def post(self, request, pk, format=None):
        address_id=request.data.get('address_id')
        unit_number=request.data.get('unit_number')
        addressline1=request.data.get('addressline1')
        city=request.data.get('city')
        state=request.data.get('state')
        postal_code=request.data.get('postal_code')
        country_name=request.data.get('country_name')

        if not Address.objects.filter(customer_id=pk).exists():
            return JsonResponse({"message":" user with this address is not found","status":"400"})
        
        if not address_id:
            return JsonResponse({"message":" Address  is required","status":"400"})
        
        if not Address.objects.filter(id=address_id).exists():
            return JsonResponse({"message":" address is not found","status":"400"})
       
        else:
            if  unit_number:
                data=Address.objects.filter(id=address_id).update(unit_number=unit_number)
            if  addressline1:
                data=Address.objects.filter(id=address_id).update(addressline1=addressline1)
            if  city:
                data=Address.objects.filter(id=address_id).update(city=city)
            if  state:
                data=Address.objects.filter(id=address_id).update(state=state)
            if  postal_code:
                data=Address.objects.filter(id=address_id).update(postal_code=postal_code)
            if  country_name:
                 data=Address.objects.filter(id=address_id).update(country_name=country_name)

        return Response({"status":"200","message":"your Address is updated successfully"})

class GetAddressById(APIView):
     @csrf_exempt
     def get(self, request,pk,format=None):
         if not Address.objects.filter(customer_id=pk).exists():
                return JsonResponse({"status":"400","message":"Address with this user not found"})
         else:
            array=[]
            address = Address.objects.all().order_by('id')
            serializer2 = AddressSerializer(address, many=True)
            for i in serializer2.data:
                aid=(i['id']) 
                acustomer_id=(i['customer_id']) 
                unit_number=(i['unit_number']) 
                addressline1=(i['addressline1']) 
                city=(i['city']) 
                state=(i['state']) 
                postal_code=(i['postal_code']) 
                country_name=(i['country_name'])
                if acustomer_id == pk:
                    address_data={"id":str(aid),"unit_number":unit_number,"address":addressline1,"city":city,"state":state,"zipcode":postal_code,"country":country_name}
                    array.append(address_data)
                data={"customer_id":str(pk),"address_data":array}                
            return JsonResponse({"status":"200","message":"success","data":data})


# Establishment related api    
class EstablishmenttypeView(APIView):
    @csrf_exempt
    def get(self, request, format=None):
        service = Establishment_type.objects.all().order_by('id')
        serializer = EstablishmentTypeSerializer(service, many=True)
        array=[]
        for x in serializer.data:
          id=(x['id'])
          establishment_type= (x['Establishment_type'])
          data={"id":str(id),"establishment_type":establishment_type}
          array.append(data)
        return JsonResponse({ "status": "200","message": "Success","data":array})

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
        return JsonResponse({ "status": "200","message": "Success","data":array})

class EastablishmentDetailsView(APIView):
    @csrf_exempt
    def get(self, request, pk, format=None):
        if User.objects.filter(id=pk).exists():
            service = Establishment.objects.all().order_by('id')
            serializer = EstablishmentSerializer(service, many=True)
            service = Address.objects.all().order_by('id')
            serializer2 = AddressSerializer(service, many=True)
            array=[]
            data={}
            array2=[]
            establishment_data={}
            address_data={}
            for x in serializer.data:
                id=(x['id'])
                customer_id= (x['customer_id'])
                address_id=(x['address_id'])
                name=(x['name'])
                establishment_type_id=(x['establishment_type_id'])
                if customer_id==pk :
                        Establishment_type_data=Establishment_type.objects.filter(id=establishment_type_id).values('Establishment_type')
                        establishment_type_name=Establishment_type_data[0]['Establishment_type']
                        print(establishment_type_name)
                        establishment_data={"id":str(id),"address_id":str(address_id),"name":name,"establishment_type_id":str(establishment_type_id),"establishment_type_name":establishment_type_name}
                        array.append(establishment_data)
                        
            for i in serializer2.data:
                aid=(i['id']) 
                acustomer_id=(i['customer_id']) 
                unit_number=(i['unit_number']) 
                addressline1=(i['addressline1']) 
                city=(i['city']) 
                state=(i['state']) 
                postal_code=(i['postal_code']) 
                country_name=(i['country_name'])
                if acustomer_id == pk:
                    address_data={"id":str(aid),"unit_number":unit_number,"address":addressline1,"city":city,"state":state,"zipcode":postal_code,"country":country_name}
                    array2.append(address_data)
                data={"customer_id":str(pk),"establishment_data":array,"address_data":array2}
                print(data)                  
            return JsonResponse({"status":"200","message":"success","data":data})
        else:
             return JsonResponse({"message":"user does not exists or do not create any establishsment","status":"400"})      

# update eastablishment and address api 
class Update_address_eastablishment(APIView):
    @csrf_exempt
    def post(self, request, pk, format=None):
         eastablishment_data=request.data.get('establishmentdata') 
         address_data=request.data.get('addressdata')
         establishment_id=request.data.get('establishment_id')
         address_id=request.data.get('address_id')
         
         if establishment_id:
                if not Establishment.objects.filter(customer_id=pk).exists():
                        return JsonResponse({"message":"user does not exists","status":"400"})
                if not Establishment.objects.filter(id=establishment_id).exists():
                        return JsonResponse({"message":"establishment not found","status":"400"})
                
         if address_id:
                if not Address.objects.filter(customer_id=pk).exists():
                    return JsonResponse({"message":"user does not exists","status":"400"})
                if not Address.objects.filter(id=address_id).exists():
                    return JsonResponse({"message":"Address not found","status":"400"})
        
         if establishment_id:
             for i in eastablishment_data:
                establishment_type_id=i['establishment_type_id']
                name=i['name'] 
                eastablishment_type_data=i['eastablishment_type_data']
                if name:
                    data = Establishment.objects.filter(id=establishment_id).update(name=name)
                if establishment_type_id: 
                        for mn in eastablishment_type_data:
                           establishment_type_name=mn['establishment_type_name']
                           print(establishment_type_name)
                           data = Establishment_type.objects.filter(id=establishment_type_id).update(Establishment_type=establishment_type_name)
         if address_id: 
            for j in address_data:
                unit_number=j['unit_number']
                addressline1=j['addressline1']
                city=j['city']
                state=j['state']
                country_name=j['country_name']
                postal_code=j['postal_code'] 
                if unit_number:
                    data = Address.objects.filter(id=address_id).update(unit_number=unit_number)
                if addressline1:
                   data = Address.objects.filter(id=address_id).update(addressline1=addressline1)
                if city:
                    data = Address.objects.filter(id=address_id).update(city=city)
                if state:
                    data = Address.objects.filter(id=address_id).update(state=state)
                if postal_code:
                   data = Address.objects.filter(id=address_id).update(postal_code=postal_code)
                if country_name:
                   data = Address.objects.filter(id=address_id).update(country_name=country_name)

         return Response({"status":"200","message":"your data is updated successfully"})

class AddEstablishment(APIView):
    renderer_classes=[UserRenderer] 
    @csrf_exempt
    def post(self,request,format=None):
        customer_id=request.data.get('customer_id')
        establishmentdata=request.data.get('establishmentdata')

        if not customer_id:
            return JsonResponse({"message":"customer id is required","status":"400"})
        
        if not User.objects.filter(id=customer_id).exists():
            return JsonResponse({"message":"user not found","status":"400"})
        
        if not establishmentdata:
            return JsonResponse({"message":" establishment list are empty","status":"400"})
        else:

            for m in establishmentdata:
                    Establishment_type_name=(m['Establishment_type_name'])
                    name=m['name'] 
                    if not name:
                        return JsonResponse({"message":"name field is required","status":"400"})
                    if not Establishment_type_name:
                        return JsonResponse({"message":"Establishment type name is required ","status":"400"})
            
            for l in establishmentdata:
                    name=l['name']
                    Establishment_type_name=l['Establishment_type_name']
                    estypedata=Establishment_type.objects.create(Establishment_type=Establishment_type_name)
                    serializer=EstablishmentTypeSerializer(data=estypedata)
                    estypedata.save()
                    eastablishment_type_id=estypedata.id
                    print(eastablishment_type_id)
                    user = User.objects.get(id= customer_id)
                    user.user = user
                    EstablishmentTypeID = Establishment_type.objects.get(id=eastablishment_type_id)
                    EstablishmentTypeID.EstablishmentID = EstablishmentTypeID
                    esdata=Establishment.objects.create(customer_id=user,name=name,establishment_type_id=EstablishmentTypeID)
                    serializer = EstablishmentSerializer(data=esdata)
                    esdata.save()
            return JsonResponse({"message":"Eastablishment  Added Successfully ","status":"200"})

class UpdateEstablishment(APIView):
 @csrf_exempt
 def post(self, request, pk, format=None):
   establishment_id=request.data.get('establishment_id') 
   establishment_name=request.data.get('establishment_name')     
   establishment_type_id=request.data.get('establishment_type_id')
   establishment_type_name=request.data.get('establishment_type_name')

   if not Establishment.objects.filter(customer_id=pk).exists():
                        return JsonResponse({"message":"user with this eastablishment does not exists","status":"400"})
   
   if not establishment_id:
                        return JsonResponse({"message":"eastablishment id is required","status":"400"})
   
   if not Establishment.objects.filter(id=establishment_id).exists():
                        return JsonResponse({"message":"establishment not found","status":"400"})
   else:
       if establishment_name:
            data = Establishment.objects.filter(id=establishment_id).update(name=establishment_name)

       if establishment_type_name:
           
           if not establishment_type_id:
                return JsonResponse({"message":"establishment type id is required","status":"400"})  
           
           if not Establishment_type.objects.filter(id=establishment_type_id).exists():
                return JsonResponse({"message":"establishment type not found ","status":"400"})  
           else:
               data = Establishment_type.objects.filter(id=establishment_type_id).update(Establishment_type=establishment_type_name)
        
       return Response({"status":"200","message":"eastablishment updated successfully"})    
  
class GetEstablishmentById(APIView):
    @csrf_exempt
    def get(self, request, pk, format=None):

        if not  Establishment.objects.filter(customer_id=pk).exists():
            return JsonResponse({"message":"user with  establishsment does not exist","status":"400"})      
        else:
            establishment = Establishment.objects.all().order_by('id')
            serializer = EstablishmentSerializer(establishment, many=True)
            array=[]
            for x in serializer.data:
                id=(x['id'])
                customer_id= (x['customer_id'])
                address_id=(x['address_id'])
                name=(x['name'])
                establishment_type_id=(x['establishment_type_id'])
                if customer_id==pk :
                        Establishment_type_data=Establishment_type.objects.filter(id=establishment_type_id).values('Establishment_type')
                        establishment_type_name=Establishment_type_data[0]['Establishment_type']
                        print(establishment_type_name)
                        establishment_data={"id":str(id),"address_id":str(address_id),"name":name,"establishment_type_id":str(establishment_type_id),"establishment_type_name":establishment_type_name}
                        array.append(establishment_data)
            return JsonResponse({"status":"200","message":"success","customer_id":str(pk),"data":array})

    
class EstablishmentRegisterView(APIView):
    renderer_classes=[UserRenderer] 
    @csrf_exempt
    def post(self,request,format=None):
        customer_id=request.data.get('customer_id')
        establishmentdata=request.data.get('establishmentdata')
        addressdata=request.data.get('addressdata')
        
        if not customer_id:
            return JsonResponse({"message":"customer id is required","status":"400"})
        if not User.objects.filter(id=customer_id).exists():
            return JsonResponse({"message":"customer id is does not exits","status":"400"})
        if not  establishmentdata and not addressdata:
            return JsonResponse({"message":"Fields are empty","status":"400"})
        else:
            if establishmentdata:
                
                for m in establishmentdata:
                    Establishment_type_name=(m['Establishment_type_name'])
                    name=m['name'] 
                    if not name:
                        return JsonResponse({"message":"name field is required","status":"400"})
                    if not Establishment_type_name:
                        return JsonResponse({"message":"Establishment type name is required ","status":"400"})
                    
            if addressdata:
                for j in addressdata:
                    unit_number=j['unit_number']
                    address=j['address']
                    city=j['city']
                    state=j['state']
                    country=j['country']
                    zip_code=j['zip_code']
                    if not  unit_number:
                     return JsonResponse({"message":"unit number is not available ,","status":"400"})
                    if not  address:
                        return JsonResponse({"message":"address is not available ,","status":"400"})
                    if not  city:
                        return JsonResponse({"message":"city is not available ,","status":"400"})
                    if not  state:
                        return JsonResponse({"message":"state is not available ,","status":"400"})
                    if not  country:
                        return JsonResponse({"message":"country is not available ,","status":"400"})
                    if not  zip_code:
                        return JsonResponse({"message":"zipcode is not available ,","status":"400"})
                    
            for l in establishmentdata:
                    name=l['name']
                    Establishment_type_name=l['Establishment_type_name']
                    estypedata=Establishment_type.objects.create(Establishment_type=Establishment_type_name)
                    serializer=EstablishmentTypeSerializer(data=estypedata)
                    estypedata.save()
                    eastablishment_type_id=estypedata.id
                    print(eastablishment_type_id)
                    user = User.objects.get(id= customer_id)
                    user.user = user
                    EstablishmentTypeID = Establishment_type.objects.get(id=eastablishment_type_id)
                    EstablishmentTypeID.EstablishmentID = EstablishmentTypeID
                    esdata=Establishment.objects.create(customer_id=user,name=name,establishment_type_id=EstablishmentTypeID)
                    serializer = EstablishmentSerializer(data=esdata)
                    esdata.save()
                    print(esdata)
                    
            for k in addressdata:
                    unit_number=k['unit_number']
                    address=k['address']
                    city=k['city']
                    state=k['state']
                    country=k['country']
                    zip_code=k['zip_code']
                    user = User.objects.get(id= customer_id)
                    user.user = user
                    addressdat=Address.objects.create(customer_id =user,unit_number=unit_number,addressline1=address,city=city,state=state,postal_code=zip_code,country_name=country)
                    serializer = AddressSerializer(data=addressdat)
                    addressdat.save()
                    print(addressdat)
            
            return JsonResponse({"message":" Details Added Successfully ","status":"200"})
     
    
# connect eastablishment id and address id
class UpdateEastablishmentAddressView(APIView):
    @csrf_exempt 
    @action(detail=False, methods=['put'])
    def put(self, request, format=None):  
        customer_id=request.data.get('customer_id')
        data=request.data.get('data') 
        if not customer_id:

         return JsonResponse({"message":"customer id is required ","status":"400"})

        if not User.objects.filter(id=customer_id).exists():
                return JsonResponse({"message":" customer id is not available","status":"400"}) 

        if not data:
         return JsonResponse({"message":"list is empty","status":"400"})

        for i in data:
            establishment_id = i['establishment_id']
            address_id = i['address_id']
            
            if not establishment_id:
                
             return JsonResponse({"message":"establishment  is required ","status":"400"})
        
            if not Establishment.objects.filter(id=establishment_id).exists():
                return JsonResponse({"message":" establishment  is not available","status":"400"}) 

            if not address_id:
                
             return JsonResponse({"message":"address  is required ","status":"400"})  

            if not Address.objects.filter(id=address_id).exists():
                return JsonResponse({"message":" address  is not available","status":"400"}) 
             
        for j in data:
            establishment_id = j['establishment_id']
            address_id = j['address_id']
            updatedata=Establishment.objects.filter(id=establishment_id).update(address_id=address_id)
        return JsonResponse({"message":"Your address is successfully connected with eastablishment","status":"200"})    
            
    
class ContactEstablishmentView(APIView):
    @csrf_exempt 
    @action(detail=False, methods=['post'])
    def post(self, request, format=None):
        customer_id=request.data.get('customer_id')
        data=request.data.get('data')
        if not customer_id: 
            return JsonResponse({"message":" Customer id is required ","status":"400"})    
        if not User.objects.filter(id= customer_id).exists() :
            return JsonResponse({"message":" Customer id  does not exist","status":"400"})     
        if not data:
            return JsonResponse({"message":"contact list  is empty","status":"400"}) 
        for x in data:
            establishment_id = int(x['establishment_id'])
            firstname=x['firstname'] 
            lastname=x['lastname']
            title=x['title']
            phone=x['phone']
            if not establishment_id:
                return JsonResponse({"message":" establishment id is required ","status":"400"})

            if not Establishment.objects.filter(id= establishment_id).exists():
                return JsonResponse({"message":" establishment id  does not exist","status":"400"})
            if establishment_id:
                EstablishmentID = Establishment.objects.get(id=establishment_id)
                EstablishmentID.EstablishmentID = EstablishmentID
            
                Establishment_Contact_data = Establishment_Contact.objects.create(customer_id=customer_id, establishment_id=EstablishmentID,firstname=firstname,lastname=lastname,title=title,phone=phone)
                serializer = Establishment_ContactSerializer(data=Establishment_Contact_data)
                Establishment_Contact_data.save()
        return JsonResponse({"message":"Your Contact is successfully saved","status":"200"})    

class Update_Establishment_Contact(APIView):

    def post(self, request, pk, format=None):
        establishment_contact_id=request.data.get('establishment_contact_id')
        establishment_id=request.data.get('establishment_id')
        firstname=request.data.get('firstname')
        lastname=request.data.get('lastname')
        title=request.data.get('title')
        phone=request.data.get('phone')

        if not Establishment_Contact.objects.filter(customer_id=pk).exists():
             return JsonResponse({"message":" user not found","status":"400"})
        if not establishment_contact_id:
            return JsonResponse({"message":" establishment conatct is  not found","status":"400"})
        if not Establishment_Contact.objects.filter(id=establishment_contact_id).exists():
             return JsonResponse({"message":" eastablishment not found","status":"400"})
        else:
            if establishment_id:
                data = Establishment_Contact.objects.filter(id=establishment_contact_id).update(establishment_id=establishment_id)
            if firstname:
                data = Establishment_Contact.objects.filter(id=establishment_contact_id).update(firstname=firstname)
            if lastname:
                data = Establishment_Contact.objects.filter(id=establishment_contact_id).update(lastname=lastname)
            if title:
                data = Establishment_Contact.objects.filter(id=establishment_contact_id).update(title=title)
            if phone:
                data = Establishment_Contact.objects.filter(id=establishment_contact_id).update(phone=phone)

        return Response({"status":"200","message":"your contact is updated successfully"})

class CustomerAddressView(APIView):
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
        
            return JsonResponse({"status":"200","message":"success","data":data})
        else:
            return JsonResponse({"status":"400","message":"user does not Exist"})

    
    @csrf_exempt
    def put(self, request, pk, format=None):
        print("",pk)
        if Customer_Address.objects.filter(id = pk).exists():
            customerdata = Customer_Address.objects.filter(id=pk).values("id",'customer_id','address_id','customer_id__First_name','customer_id__Last_name','customer_id__email','customer_id__mobile','customer_id__title',
                                                                'customer_id__password')
            print(customerdata)
            # id=customerdata[0]['id']
            customer_id=customerdata[0]['customer_id']
            First_name=request.data.get('First_name')
            Last_name=request.data.get('Last_name')
            email=request.data.get('email')
            mobile=request.data.get('mobile')
            title=request.data.get('title')
            password=request.data.get('password')
            
            dict={'email':email,'First_name':First_name,"Last_name":Last_name,"mobile":mobile,"title":title,"password":password}
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
            if password:
                password=password
            else:
                password=customerdata[0]['customer_id__password']
            
            Userdata=User.objects.filter(id=customer_id).update(email=email,First_name=First_name,Last_name=Last_name,mobile=mobile,title=title,password=password)
        else:
            return JsonResponse({"status":"400","message":"user does not exist"})
        return JsonResponse({"status":"200","message":"you data is updated successfully","data":dict})

# contact us Api
   
class ContactView(APIView):   
    @csrf_exempt 
    @action(detail=False, methods=['post'])
    def post(self, request, format=None):
        firstname=request.data.get('firstname')
        Lastname=request.data.get('lastname')
        email=request.data.get('email')
        phone=request.data.get('phone')
        unit_number=request.data.get('unit_number')
        address=request.data.get('address')
        city=request.data.get('city')
        state=request.data.get('state')
        country=request.data.get('country')
        zipcode=request.data.get('zipcode')
        comment=request.data.get('comment')
        
        if not email:
            return JsonResponse({"message":"email is required","status":"400"})
        if not phone:
            return JsonResponse({"message":"phone number is required","status":"400"})
        if not zipcode:
            return JsonResponse({"message":"zipcode is required","status":"400"})
        else:
            contact_data=Contact.objects.create(firstname=firstname,lastname=Lastname,email=email,phone=phone,
                                            unit_number=unit_number,address=address,city=city,
                                            state=state,country=country,zipcode=zipcode,comment=comment)
            
            serializer =ContactSerializer(data=contact_data)
            contact_data.save()
            print(contact_data)
            return JsonResponse({"message":"Thanks for contacting us","status":"200"})


            
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
            return JsonResponse({"status":"200","message":"success","data":array})
        


     
from django.conf import settings

class pdfview(APIView):
    def get(self, request, format=None):
        service_data = uploadpdf.objects.all()
        serializer = UploadpdfSerializer(service_data, many=True)
        print(serializer.data[0])
        url = settings.BASE_URL+serializer.data[0]['uploadfile']
        return Response(url)
    
class PromocodeDiscountView(APIView):   
    renderer_classes=[UserRenderer] 
    def post(self,request,format=None):
        promocode=request.data.get('promocode')
        print(promocode)
        if not promocode:
            return JsonResponse({"message":"Please enter promocode","status":"400",})
        if not Promotion.objects.filter(promocode=promocode).exists():
            return JsonResponse({"message":"Please enter a valid promocode","status":"400",})
        promodates = Promotion.objects.filter(promocode=promocode).values('start_date','end_date')
        startdate=promodates[0]['start_date']
        enddate=promodates[0]['end_date']
        current_date = date.today()
        # print(current_date)
        if current_date > enddate:
            return JsonResponse({"message":"offer is expired","status":"400"})
        else:
            Promotion.objects.filter(promocode=promocode).exists()  
            discountdata=Promotion.objects.filter(promocode=promocode).values('discount_rate')
            discountrate=discountdata[0]['discount_rate']
            data={"discount":discountrate}
            return JsonResponse({"message":"success","status":"200",'data':data})
     
class TestSectionView(APIView):
    @csrf_exempt 
    def post(self, request, format=None):
        email=request.data.get('email')

        if not email:
            return Response({"message":"email is required","status":"400"})
        
        if not User.objects.filter(email=email).exists():
            return Response({"message":"user with this email does not exists","status":"400"})

        if User.objects.filter(email=email,user_created_by_admin=True).exists():
            user = User.objects.get(email=email)
            link=" http://127.0.0.1:8000/userpasswordreset/"
            subject, from_email, to = 'Reset Your Password', settings.EMAIL_HOST_USER, email
            text_content = 'This is an important message.'
            html_content = '<p>Click Following Link to Reset Your Password</p>' + link
            msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
            msg.attach_alternative(html_content, "text/html")
            msg.send()
            return JsonResponse({'message':'your password reset link successfully send to your email','status':'200'})
        else:
            user = User.objects.get(email = email)
            link = 'http://127.0.0.1:8000/password_set/'
            print(link)
            print('Password Reset Link', link)
            return Response({"message":"success",'status':'200','resetlink':link})
           
        


        
class Establishment_contact_listView(APIView):
    def get(self, request, pk, format=None):   
        customer_id = int(pk)
        print(customer_id)
        array = []
        dict= {}
        if not customer_id: 
            return JsonResponse({"status":"400","message":" Customer id is required ","data":array})    
        if not User.objects.filter(id= customer_id).exists() :
            return JsonResponse({"status":"400","message":" Customer id  does not exist","data":array})  
        if not Establishment_Contact.objects.filter(customer_id= customer_id).exists() :
            return JsonResponse({"status":"400","message":"User Establishment contact does not exist.","data":array})  
        else:
            list_data = Establishment_Contact.objects.filter(customer_id=customer_id)
            serializers = Establishment_ContactSerializer(list_data, many=True)
            for x in serializers.data:
                id = str(x['id'])
                establishment_id = str(x['establishment_id'])
                firstname = x['firstname']
                lastname = x['lastname']
                title = x['title']
                phone = str(x['phone'])
                dict = {"id":id,"establishment_id":establishment_id,"firstname":firstname,"lastname":lastname,"title":title,"phone":phone}
                array.append(dict)
        return JsonResponse({"status":"200","msg":"success","data":array})
             
 #new   

# operater api
class  CreateOperaterView(APIView):# new
     @csrf_exempt
     def post(self, request,format=None): 
         
         dispatcher_id=request.data.get('dispatcher_id')
         operater_data=request.data.get('operater_data')

         if not dispatcher_id:
              return Response({"message":"dispatcher detail required","status":"400"})
         
         if not User.objects.filter(id=dispatcher_id,role="dispatcher").exists():
              return Response({"message":"invalid dispatcher detail","status":"400"})
         
         if not operater_data:
             return Response({"message":"you can not send empty detail","status":"400"})
         
         else:
             for i in operater_data:
                 
                 firstname=i['firstname']
                 lastname=i['lastname']
                 phone=i['phone']
                 email=i['email']
                 position=i['position']

                 if not firstname:
                     return Response({"message":"firstname is required","status":"400"})
                 
                 if not lastname:
                     return Response({"message":"lastname is required","status":"400"})
                 
                 if not phone:
                     return Response({"message":"mobile number  is required","status":"400"})
                 
                 if not email:
                     return Response({"message":"email is required","status":"400"})
                 
                 if not position:
                     return Response({"message":"position is required","status":"400"})
                 
             
             for j in operater_data:
                 
                 firstname=j['firstname']
                 lastname=j['lastname']
                 phone=j['phone']
                 email=j['email']
                 position=j['position']    
                 Dispatcher_Id = User.objects.get(id=dispatcher_id)
                 Dispatcher_Id.Dispatcher_Id = Dispatcher_Id
                 operater_data=Operater.objects.create(firstname=firstname,lastname=lastname,phone=phone,email=email,position=position,dispatcher_id=Dispatcher_Id)
                 serializer=OperaterSerializer(data=operater_data)
                 operater_data.save()
                 
         return Response({"message":"Detail successfully saved","status":"200"})

class UpdateOperaterView(APIView):# new
  @csrf_exempt
  def post(self, request, pk, format=None):
      
      operater_update_data=request.data.get('operater_update_data')

      if not Operater.objects.filter(dispatcher_id=pk).exists():
          return JsonResponse({"message":"invalid dispatcher detail","status":"400"})
      else:
      
        for j in operater_update_data:
        
            operater_id=j['operater_id']
            firstname=j['firstname']
            lastname=j['lastname']
            phone=j['phone']
            email=j['email']
            position=j['position']    
            
            if not operater_id:
             return JsonResponse({"message":"operater detail required","status":"400"})
            
            if not Operater.objects.filter(id=operater_id).exists():
             return JsonResponse({"message":" operater does not exist with this dispatcher detail","status":"400"})
        
        for k in operater_update_data:
        
            operater_id=k['operater_id']
            firstname=k['firstname']
            lastname=k['lastname']
            phone=k['phone']
            email=k['email']
            position=k['position']  
       
            
            if firstname:
                data=Operater.objects.filter(id=operater_id).update(firstname=firstname)

            if lastname:
                    data=Operater.objects.filter(id=operater_id).update(lastname=lastname)   

            if phone:
                    data=Operater.objects.filter(id=operater_id).update(phone=phone)

            if email:
                data=Operater.objects.filter(id=operater_id).update(email=email)

            if position:
                data=Operater.objects.filter(id=operater_id).update(position=position)
                

        return JsonResponse({"message":"details successfully updated","status":"200"})
      
#get by dispatcher id
class GetOperaterById(APIView):
     @csrf_exempt
     def get(self, request,pk,format=None):
         if not Operater.objects.filter(dispatcher_id=pk).exists():
                return JsonResponse({"status":"400","message":"dispatcher not found"})
         else:
            array=[]
            operater = Operater.objects.all().order_by('id')
            serializer2 =  OperaterSerializer(operater, many=True)
            for i in serializer2.data:
                oid=(i['id']) 
                firstname=(i['firstname']) 
                lastname=(i['lastname']) 
                phone=(i['phone']) 
                email=(i['email']) 
                position=(i['position']) 
                dispatcher_id=(i['dispatcher_id']) 
                
                if dispatcher_id == pk:
                    operater_data={"id":str(oid),"firstname":firstname,"lastname":lastname,"phone":phone,"email":email,"position":position}
                    array.append(operater_data)             
            return JsonResponse({"status":"200","message":"success","dispatcher_id":str(pk),"data":array}) 
         



   # get all operater detail   

# get all operater detail
class GetOperaterDetail(APIView):
    @csrf_exempt
    def get(self, request, format=None):
        operater = Operater.objects.all().order_by('id')
        serializer = OperaterSerializer(operater, many=True)
        array=[]
        for i in serializer.data:
            oid=(i['id']) 
            firstname=(i['firstname']) 
            lastname=(i['lastname']) 
            phone=(i['phone']) 
            email=(i['email']) 
            position=(i['position']) 
            operater_data={"id":str(oid),"firstname":firstname,"lastname":lastname,"phone":phone,"email":email,"position":position}
            array.append(operater_data)
        return JsonResponse({"status": "200","message": "Success","data":array})   
    

# create service item api
class CreateServiceItemView(APIView):
    renderer_classes=[UserRenderer] 
    @csrf_exempt
    def post(self,request,format=None):
        dispatcher_id=request.data.get('dispatcher_id')
        service_item_data=request.data.get('service_item_data')

        if not dispatcher_id:
              return Response({"message":"dispatcher detail required","status":"400"})
         
        if not User.objects.filter(id=dispatcher_id,role="dispatcher").exists():
              return Response({"message":"invalid dispatcher detail","status":"400"})

        if not service_item_data:
            return JsonResponse({"message":"you can not send empty details",'status':'400'})
        
        else:
           for i in service_item_data:
                 
                 establishment_id=i['establishment_id']
                 service_type_id=i['service_type_id']
                 operater_id=i['operater_id']
                 service_date_time=i['service_date_time']
                 service_notes=i['service_notes']

                 if not establishment_id:
                     return JsonResponse({"message":"eastablishment is required",'status':'400'})
                 
                 if not Establishment.objects.filter(id=establishment_id).exists():
                     return JsonResponse({"message":"eastablishment detail not found","status":"400"})
                 
                 if not service_type_id:
                     return JsonResponse({"message":"service type  is required",'status':'400'})
                 
                 if not ServiceType.objects.filter(id=service_type_id).exists():
                     return JsonResponse({"message":"service type detail not found","status":"400"})
                 
                 if not operater_id:
                     return JsonResponse({"message":"operater  is required",'status':'400'})
                 
                 if not Operater.objects.filter(id=operater_id).exists():
                     return JsonResponse({"message":"operater detail not found","status":"400"})
                 
                 if not service_date_time:
                     return JsonResponse({"message":"Service date and time is required",'status':'400'})
                 
                 if not service_notes:
                     return JsonResponse({"message":"Service notes is required",'status':'400'})
                 
           for k in service_item_data:
            
                 establishment_id=k['establishment_id']
                 service_type_id=k['service_type_id']
                 operater_id=k['operater_id']
                 service_date_time=k['service_date_time']
                 service_notes=k['service_notes']

                 Eastablishment_Id = Establishment.objects.get(id=establishment_id)
                 Eastablishment_Id.Eastablishment_Id = Eastablishment_Id

                 Service_Type_Id = ServiceType.objects.get(id=service_type_id)
                 Service_Type_Id.Service_Type_Id = Service_Type_Id

                 Operater_Id = Operater.objects.get(id=operater_id)
                 Operater_Id.Operater_Id = Operater_Id

                 Dispatcher_Id = User.objects.get(id=dispatcher_id)
                 Dispatcher_Id.Dispatcher_Id = Dispatcher_Id
                
                 service_item_data=ServiceItem.objects.create(establishment_id=Eastablishment_Id,service_type_id=Service_Type_Id,operater_id=Operater_Id,service_date_time=service_date_time,service_notes=service_notes,dispatcher_id=Dispatcher_Id)
                 serializer=ServiceItemSerializer(data=service_item_data)
                 service_item_data.save()
           return JsonResponse({"message":"service item successfully created",'status':'200'})

# get service item by id
class GetServiceItemById(APIView):
     @csrf_exempt
     def get(self, request,pk,format=None):
         if not ServiceItem.objects.filter(dispatcher_id=pk).exists():
                return JsonResponse({"status":"400","message":"invalid dispatcher detail"})
         else:
            array=[]
            service_item = ServiceItem.objects.all().order_by('id')
            serializer2 =  ServiceItemSerializer(service_item, many=True)
            for i in serializer2.data:
                sid=(i['id']) 
                establishment_id=i['establishment_id']
                service_type_id=i['service_type_id']
                operater_id=i['operater_id']
                service_date_time=i['service_date_time']
                service_notes=i['service_notes']
                dispatcher_id=(i['dispatcher_id']) 
                
                if dispatcher_id == pk:
                    service_item_data={"id":str(sid),"establishment_id":str(establishment_id),"service_type_id":str(service_type_id),"operater_id":str(operater_id),"service_date_time":service_date_time,"service_notes":service_notes}
                    array.append(service_item_data)             
            return JsonResponse({"status":"200","message":"success","dispatcher_id":str(pk),"data":array}) 

# update service item view  pending 
class UpdateServiceItemView(APIView):# new
  @csrf_exempt
  def put(self, request, pk, format=None):
      
      update_service_item=request.data.get('update_service_item')

      if not ServiceItem.objects.filter(dispatcher_id=pk).exists():
          return JsonResponse({"message":"invalid dispatcher detail","status":"400"})
      else:
      
        for i in update_service_item:
            service_item_id=(i['service_item_id']) 
            establishment_id=i['establishment_id']
            service_type_id=i['service_type_id']
            operater_id=i['operater_id']
            service_date_time=i['service_date_time']
            service_notes=i['service_notes']
          
    
            if not service_item_id:
             return JsonResponse({"message":"service_item_id is required","status":"400"})
            
            if not ServiceItem.objects.filter(id=service_item_id).exists():
             return JsonResponse({"message":" service item does not exist with this dispatcher detail","status":"400"})
            
            if not establishment_id:
                return JsonResponse({"message":"please select eastablishment ","status":"400"})

            if not Establishment.objects.filter(id=establishment_id).exists():
             return JsonResponse({"message":" eastablishment does not exists","status":"400"})
            
            if not service_type_id:
                 return JsonResponse({"message":"please select service type ","status":"400"})

            if not ServiceType.objects.filter(id=service_type_id).exists():
             return JsonResponse({"message":" service type does not exists","status":"400"})
            
            if not operater_id:
                 return JsonResponse({"message":"please select operater ","status":"400"})


            if not Operater.objects.filter(id=operater_id).exists():
             return JsonResponse({"message":" operater does not exists","status":"400"})
            
        
        for k in update_service_item:
        
            service_item_id=(k['service_item_id']) 
            establishment_id=k['establishment_id']
            service_type_id=k['service_type_id']
            operater_id=k['operater_id']
            service_date_time=k['service_date_time']
            service_notes=k['service_notes'] 
            Csdata = ServiceItem.objects.filter(id=service_item_id).values('establishment_id','service_type_id','operater_id','service_date_time','service_notes')
            
            
            if establishment_id:
                establishment_id=establishment_id
            else:
                establishment_id=Csdata[0]['establishment_id']
            
            if service_type_id:
                service_type_id=establishment_id
            else:
                service_type_id=Csdata[0]['service_type_id']
            
            if operater_id:
                operater_id=operater_id
            else:
                operater_id=Csdata[0]['operater_id']

            if service_date_time:
                service_date_time=service_date_time
            else:
                service_date_time=Csdata[0]['service_date_time']
            
            if service_notes:
                service_notes=service_notes
            else:
                service_notes=Csdata[0]['service_notes']
                
            if establishment_id:
                data=ServiceItem.objects.filter(id=service_item_id).update(establishment_id=establishment_id)

            if service_type_id:
                    data=ServiceItem.objects.filter(id=service_item_id).update(service_type_id=service_type_id)  

            if operater_id:
                data=ServiceItem.objects.filter(id=service_item_id).update(operater_id=operater_id)

            if service_date_time:
                data=ServiceItem.objects.filter(id=service_item_id).update(service_date_time=service_date_time)
            
            if service_notes:
                data=ServiceItem.objects.filter(id=service_item_id).update(service_notes=service_notes)
                

        return JsonResponse({"message":"details successfully updated","status":"200"})



# get all service item detail    
class GetServiceItemDetail(APIView):
    @csrf_exempt
    def get(self, request, format=None):
        operater = ServiceItem.objects.all().order_by('id')
        serializer = ServiceItemSerializer(operater, many=True)
        array=[]
        for i in serializer.data:
            sid=(i['id']) 
            establishment_id=i['establishment_id']
            service_type_id=i['service_type_id']
            operater_id=i['operater_id']
            service_date_time=i['service_date_time']
            service_notes=i['service_notes']
            service_item_data={"id":str(sid),"establishment_id":str(establishment_id),"service_type_id":str(service_type_id),"operater_id":str(operater_id),"service_date_time":service_date_time,"service_notes":service_notes}
            array.append(service_item_data)     
        return JsonResponse({"status": "200","message": "Success","data":array})   

# create multiple customer Api

class CreateMultipleCustomerView(APIView):
    @csrf_exempt 
    @action(detail=False, methods=['post'])
    def post(self, request, format=None):
        customer_data=request.data.get('customer_data')
        dispatcher_id=request.data.get('dispatcher_id')
      
        if not customer_data:
            return Response({"message":"you can not send empty data", "status":"400"})
        
        if not dispatcher_id:
            return Response({"message":"dispatcher detail is required", "status":"400"})
       
        if not  User.objects.filter(id=dispatcher_id,role="dispatcher").exists():
            return Response({"message":"dispatcher details does not exist ", "status":"400"})
        
        else:

            for i in customer_data:
                First_name=i['First_name']
                Last_name=i['Last_name']
                email=i['email']
                title=i['title']
                mobile=i['mobile']
                attribute_name=i['attribute_name']
                password=i['password']
                position=i['position']
                role=i['role']

                if not First_name:
                    return Response({"message":"firstname is required",'status':"400"})
                
                if not Last_name:
                    return Response({"message":"lastname is required",'status':"400"})
                
                if not email:
                    return Response({"message":"email is required",'status':"400"})
                
                if '@' not in email:
                    return Response({"message":"please enter valid email",'status':"400"})
                
                if User.objects.filter(email=email).exists():

                    data = {
                            'message':'Email is Already Exists',
                            'status':"400",
                        }
                    return Response(data)
                
                if not mobile:
                    return Response({"message":"mobile number is required",'status':"400"})
                
                if User.objects.filter(mobile=mobile).exists():
                    data = {
                            'message':'mobile number is already exist',
                            'status':"400",
                        }
                    return Response(data)
                
                if not password:
                    
                    return Response({"message":"password is required",'status':"400"})
                
                if not role:
                    return Response({"message":"role is required",'status':"400"})
                
                if not role:
                    return Response({"message":"role is required",'status':"400"})
                
                if role !='customer':
                    return Response({"message":"please enter valid role"})
            
            for j in customer_data:
                    First_name=j['First_name']
                    Last_name=j['Last_name']
                    email=j['email']
                    title=j['title']
                    mobile=j['mobile']
                    attribute_name=j['attribute_name']
                    password=j['password']
                    position=j['position']
                    role=j['role']
                    user_data=User.objects.create(First_name=First_name,Last_name=Last_name,email=email,
                                                title=title,mobile=mobile,
                                                attribute_name=attribute_name,position=position,role=role,dispatcher_user_id=dispatcher_id)
                    user = User.objects.get(email=email)
                    user.set_password(password)
                    user.save()
            return JsonResponse({'message':'Registeration Successfull','status':'200'})

# update multiple customer
class UpdateMultipleCustomerView(APIView):
    def post(self, request,format=None):
      dispatcher_id=request.data.get('dispatcher_id')
      update_customer_data=request.data.get('update_customer_data')
     
      if not update_customer_data:
            return Response({"message":"you can not send empty data", "status":"400"})

      if not dispatcher_id:
        return Response({"message":"dispatcher detail is required", "status":"400"})
      
      if not  User.objects.filter(dispatcher_user_id=dispatcher_id).exists():
            return Response({"message":"dispatcher does not exist ", "status":"400"})
     
      else:
          for i in update_customer_data:
                customer_id=i['customer_id']
                First_name=i['First_name']
                Last_name=i['Last_name']
                email=i['email']
                title=i['title']
                mobile=i['mobile']
                attribute_name=i['attribute_name']
                position=i['position']
               

                if not customer_id:
                    return Response({"message":"customer id is required", "status":"400"})
                
                if not User.objects.filter(id=customer_id,dispatcher_user_id=dispatcher_id).exists():
                    return Response({"message":"user with this dispatcher does not exists", "status":"400"})
                
          for j in update_customer_data:
                customer_id=j['customer_id']
                First_name=j['First_name']
                Last_name=j['Last_name']
                email=j['email']
                title=j['title']
                mobile=j['mobile']
                attribute_name=j['attribute_name']
                position=j['position']
               

                if First_name:
                     data=User.objects.filter(id=customer_id).update(First_name=First_name)

                if Last_name:
                     data=User.objects.filter(id=customer_id).update(Last_name=Last_name)

                if email:
                     data=User.objects.filter(id=customer_id).update(email=email)
                
                if title:
                     data=User.objects.filter(id=customer_id).update(title=title)

                if mobile:
                     data=User.objects.filter(id=customer_id).update(mobile=mobile)

                if attribute_name:
                     data=User.objects.filter(id=customer_id).update(attribute_name=attribute_name)
               
                if position:
                     data=User.objects.filter(id=customer_id).update(position=position)

      return JsonResponse({'message':'customer data updated successfully','status':'200'})         

# create multiple dispatcher 
class CreateMultipleDispatcherView(APIView): 
    @csrf_exempt 
    @action(detail=False, methods=['post'])
    def post(self, request, format=None):
        dispatcher_data=request.data.get('dispatcher_data')
        dispatcher_id=request.data.get('dispatcher_id')
        

        if not dispatcher_data:
            return Response({"message":"you can not send empty data", "status":"400"})
        if not dispatcher_id:
            return Response({"message":"dispatcher id is required", "status":"400"})
       
        if not  User.objects.filter(id=dispatcher_id,role="dispatcher").exists():
            return Response({"message":"dispatcher id  does not exist ", "status":"400"})
        else:

            for i in dispatcher_data:
                First_name=i['First_name']
                Last_name=i['Last_name']
                email=i['email']
                title=i['title']
                mobile=i['mobile']
                attribute_name=i['attribute_name']
                password=i['password']
                position=i['position']
                role=i['role']

                if not First_name:
                    return Response({"message":"firstname is required",'status':"400"})
                
                if not Last_name:
                    return Response({"message":"lastname is required",'status':"400"})
                
                if not email:
                    return Response({"message":"email is required",'status':"400"})
                
                if '@' not in email:
                    return Response({"message":"please enter valid email",'status':"400"})
                
                if User.objects.filter(email=email).exists():

                    data = {
                            'message':'Email is Already Exists',
                            'status':"400",
                            "data":{}
                        }
                    return Response(data)
                
                if not mobile:
                    return Response({"message":"mobile number is required",'status':"400"})
                
                if User.objects.filter(mobile=mobile).exists():
                    data = {
                            'message':'mobile number is already exist',
                            'status':"400",
                            "data":{}
                        }
                    return Response(data)
                
                if not password:
                    
                    return Response({"message":"password is required",'status':"400"})
                
                if not role:
                    return Response({"message":"role is required",'status':"400"})
                
                if not role:
                    return Response({"message":"role is required",'status':"400"})
                
                if role !='dispatcher':
                    return Response({"message":"please enter valid role"})
            
            for j in dispatcher_data:
                    First_name=j['First_name']
                    Last_name=j['Last_name']
                    email=j['email']
                    title=j['title']
                    mobile=j['mobile']
                    attribute_name=j['attribute_name']
                    password=j['password']
                    position=j['position']
                    role=j['role']
                    user_data=User.objects.create(First_name=First_name,Last_name=Last_name,email=email,
                                                title=title,mobile=mobile,
                                                attribute_name=attribute_name,position=position,role=role,dispatcher_user_id=dispatcher_id)
                    user = User.objects.get(email=email)
                    user.set_password(password)
                    user.save()
            return JsonResponse({'message':'Registeration Successfull','status':'200'})
            
# update multiple dispatcher
class UpdateMultipleDispatcherView(APIView):
    def post(self, request,format=None):
      dispatcher_id=request.data.get('dispatcher_id')
      update_dispatcher_data=request.data.get('update_dispatcher_data')
      
      if not update_dispatcher_data:
            return Response({"message":"you can not send empty data", "status":"400"})

      if not dispatcher_id:
        return Response({"message":"dispatcher id is required", "status":"400"})
      
      if not  User.objects.filter(dispatcher_user_id=dispatcher_id).exists():
            return Response({"message":"dispatcher does not exist ", "status":"400"})
     
      else:
          for i in update_dispatcher_data:
                dispatcherid=i['dispatcherid']
                First_name=i['First_name']
                Last_name=i['Last_name']
                email=i['email']
                title=i['title']
                mobile=i['mobile']
                attribute_name=i['attribute_name']
                position=i['position']
               

                if not dispatcherid:
                    return Response({"message":"customer id is required", "status":"400"})
                
                if not User.objects.filter(id=dispatcherid,dispatcher_user_id=dispatcher_id).exists():
                    return Response({"message":"user with this dispatcher does not exists", "status":"400"})
                
                if  User.objects.filter(email=email).exists():
                     return Response({"message":"user with this email id is already exists", "status":"400"})
                
          for j in update_dispatcher_data:
                dispatcherid=j['dispatcherid']
                First_name=j['First_name']
                Last_name=j['Last_name']
                email=j['email']
                title=j['title']
                mobile=j['mobile']
                attribute_name=j['attribute_name']
                position=j['position']
               

                if First_name:
                     data=User.objects.filter(id=dispatcherid).update(First_name=First_name)

                if Last_name:
                     data=User.objects.filter(id=dispatcherid).update(Last_name=Last_name)

                if email:
                     data=User.objects.filter(id=dispatcherid).update(email=email)
                
                if title:
                     data=User.objects.filter(id=dispatcherid).update(title=title)

                if mobile:
                     data=User.objects.filter(id=dispatcherid).update(mobile=mobile)

                if attribute_name:
                     data=User.objects.filter(id=dispatcherid).update(attribute_name=attribute_name)
               
                if position:
                     data=User.objects.filter(id=dispatcherid).update(position=position)

      return JsonResponse({'message':'dispatcher data updated successfully','status':'200'})   

class UserDetailByDispatcherIdView(APIView):
        def post(self,request,format=None): 
            dispatcher_id=request.data.get('dispatcher_id')
            roles=request.data.get('role')

            if not dispatcher_id:
                return Response({"message":" dispatcher detail required", "status":"400"})
            
            if not roles:
                 return Response({"message":" role required", "status":"400"})
            
            if not User.objects.filter(dispatcher_user_id=dispatcher_id).exists():
             return Response({"message":"invalid dispatcher detail", "status":"400"})
            
            else:
                array=[]
                user_detail = User.objects.all().order_by('id')
                serializer2 =  UserRegistrationSerializer(user_detail, many=True)
                for i in serializer2.data:
                    user_id=i['id']
                    First_name=i['First_name']
                    Last_name=i['Last_name']
                    email=i['email']
                    title=i['title']
                    mobile=i['mobile']
                    attribute_name=i['attribute_name']
                    position=i['position']
                    role=i['role']
                    dispatcherid=i['dispatcher_user_id']
                    
                    if dispatcher_id == dispatcherid and roles==role:
                        dispatcher_data={"user_id":str(user_id),"First_name":First_name,"Last_name":Last_name,"mobile":mobile,"email":email,"position":position,"title":title,"attribute_name":attribute_name,"role":role}
                        array.append(dispatcher_data) 
                return JsonResponse({'message':'success','status':'200','dispatcher_id':str(dispatcher_id),'data':array}) 
