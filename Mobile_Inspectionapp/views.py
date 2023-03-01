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
from rest_framework_simplejwt.tokens import RefreshToken
from django.conf import settings
from rest_framework.authtoken.models import Token
from datetime import date 
from django.contrib.auth import authenticate






# Generate Token Manually
def get_tokens_for_user(user):
  refresh = RefreshToken.for_user(user)
  return {
      'refresh': str(refresh),
      'access': str(refresh.access_token),
  }
# User Register class

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
         return Response({"message":"please enter valid email",'status':"400"})
     if not First_name:
         return Response({"message":"Firstname is required",'status':"400"})
     if not Last_name:
         return Response({"message":"Lastname is required",'status':"400"})
     if not password:
         return Response({"message":"password is required",'status':"400"})
     if not mobile:
         return Response({"message":"mobile number is required",'status':"400"})
     else:
         registred_data=User.objects.create(First_name=First_name,Last_name=Last_name,email=email,title=title,mobile=mobile,attribute_name=attribute_name,password=password,position=position)
         serializer = UserSerializer(data=registred_data)
         registred_data.save()
         id=User.objects.filter(email=email).values('id','email')
         user=id[0]['email']
         print(user)
         print(id[0]['id'])
         dict_data={'id':str(id[0]['id']),"Firstname":First_name,"Lastname":Last_name,"email":email,"title":title,"mobile":mobile,"attribute_name":attribute_name,"position":position}
         return JsonResponse({'message':'Registeration Successfull','status':'200','data':dict_data})


class UserLoginView(APIView): 
    @csrf_exempt 
    @action(detail=False, methods=['post'])
    @permission_classes((AllowAny,))
    def post(self, request, format=None):
        username=request.data.get('email')
        password=request.data.get('password')
        if username=='' or password == '':
            return JsonResponse({"message":"Email or PAssword Required","status":"400","data":{}})
            
        if not User.objects.filter(email=username , password = password).values('email', 'password') :
            
            return JsonResponse({"message":"wrong Email id or password","status":"400","data":{}})
        
        else:
            # user=User.objects.filter(email=emaild).update(ifLogged=True)
            user = User.objects.get(email=username)
            userdetail=User.objects.filter(email=username).values('id','First_name','Last_name','email','mobile','title','attribute_name','position')
            print("print--- detail",userdetail[0]['First_name'])
            # token=get_tokens_for_user(user)
            # print(token)
            data={'id':str(userdetail[0]['id']),'First_name':userdetail[0]['First_name'],'Last_name':userdetail[0]['Last_name'],'email':userdetail[0]['email'],'mobile':userdetail[0]['mobile'],'title':str(userdetail[0]['title']),'attribute_name':userdetail[0]['attribute_name'],'position':userdetail[0]['position']}
            return JsonResponse({'message':'Login Successfull','status':'200','data':data})
        
class SendPasswordResetLink(APIView):  
    @csrf_exempt 
    @action(detail=False, methods=['post'])
    def post(self, request, format=None):
        email=request.data.get('email')
        if User.objects.filter(email=email).exists():
            user = User.objects.get(email = email)
            link = 'http://127.0.0.1:8000/password_set/'
            print(link)
            print('Password Reset Link', link)
            return Response({"message":"success",'status':'200','resetlink':link})
        else:
            return Response({"message":"user does not exist ","status":"400"})
    
class PasswordSetViewSet(APIView):
    @csrf_exempt 
    @action(detail=False, methods=['post'])
    def post(self, request, format=None):
        email=request.data.get('email')
        print(email)
        newpassword=request.data.get('password')
        print(newpassword)
        if email:
            if User.objects.filter(email=email).exists():
                print(User.objects.filter(email=email).exists())
                User.objects.filter(email=email).update(password=newpassword)
                user_data=User.objects.filter(email=email).values('id')
                user_id=user_data[0]['id']
                print(user_id)
                data={"id":str(user_id),"email":email}
                return JsonResponse({"message":"you password is successfully changed","status":"200","data":data})
            else:
                return JsonResponse({"message":"you are entring a wrong email id","status":"400"})
        else:
            return JsonResponse({"message":"please enter valid email id","status":"400"})

    
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
    
from rest_framework import generics  
         
class LogoutUser(generics.GenericAPIView):
  permission_classes = [IsAuthenticated]
  def post(self, request, format=None):
    return Response({'msg':'Logout Successfully'})
    
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
                        establishment_data={"id":str(id),"address_id":str(address_id),"name":name,"establishment_type_id":str(establishment_type_id)}
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
             

     
        
          
        
      
   
    




# class TestSectionView(APIView):
#  renderer_classes=[UserRenderer]
#  def post(self,request,format=None):
#     customer_id = request.data.get('customer_id')
#     address_id = request.data.get('address_id')
#     name = request.data.get('name')
#     unit_number=request.data.get('unit_number')
#     address=request.data.get('address')
#     city=request.data.get('city')
#     state=request.data.get('state')
#     country=request.data.get('country')
#     zip_code=request.data.get('zip_code')
#     print(len(zip_code))
#     establishment_type_id = request.data.get('establishment_type_id')
#     if address_id:
#         if not Address.objects.filter(id=address_id).exists():
#             return JsonResponse({"message":"address_id is not available ","status":"400"})
#         if not customer_id:
#             return JsonResponse({"message":"customer_id is not available ","status":"400"})
       
#         if not User.objects.filter(id=customer_id).exists():
#             return JsonResponse({"message":"customer_id  does not exits","status":"400"})
#         if not name:
#             return JsonResponse({"message":"name field is required","status":"400"})
#         if not Establishment.objects.filter(id=establishment_type_id).exists():
#             return JsonResponse({"message":"Establishment_id  does not exits","status":"400"})
#         if unit_number:
#            unit_number=unit_number
#            return JsonResponse({"message":"address_id is available,other address field is not required","status":"400"})
#         if address:
#            address=address
#            return JsonResponse({"message":"address_id is available ,other address field is not required","status":"400"})
#         if city:
#            city=city
#            return JsonResponse({"message":"address_id is available ,other address field is not required","status":"400"})
#         if state:
#            state=state
#            return JsonResponse({"message":"address_id is available ,other address field is not required","status":"400"})
#         if country:
#            country=country
#            return JsonResponse({"message":"address_id is available ,other address field is not required","status":"400"})
#         if zip_code:
#            zip_code=zip_code
#            return JsonResponse({"message":"address_id is available ,other address field is not required","status":"400"})
       
#         user = User.objects.get(id= customer_id)
#         user.user = user
        
#         EstablishmentID = Establishment_type.objects.get(id= establishment_type_id)
#         EstablishmentID.EstablishmentID =EstablishmentID
        
#         AddressID = Address.objects.get(id= address_id)
#         AddressID.AddressID = AddressID
            
#         esdata=Establishment.objects.create(customer_id=user ,address_id=AddressID, name=name,establishment_type_id=EstablishmentID)
#         serializer = EstablishmentSerializer(data=esdata)
#         esdata.save()
#         dict_data={'customer_id':customer_id,'address_id':address_id,'name':name,'establishment_type_id':establishment_type_id }
#         return JsonResponse({"message":"success","status":"200","data":dict_data})
        
#     else:
#         if not customer_id:
#             return JsonResponse({"message":"customer_id is not available ","status":"400"})
       
#         if not User.objects.filter(id=customer_id).exists():
#             return JsonResponse({"message":"customer_id is does not exits","status":"400"})
        
#         if not establishment_type_id:
#             return JsonResponse({"message":"establishment_type_id is not available ","status":"400"})
        
#         if not Establishment_type.objects.filter(id=establishment_type_id).exists():
#             return JsonResponse({"message":"establishment_type_id is does not exits","status":"400"})
#         if not name:
#            return JsonResponse({"message":"name field can not be empty","status":"400"})
        
#         if not  unit_number:
#             return JsonResponse({"message":"unit number is not available ,","status":"400"})
#         if not  address:
#             return JsonResponse({"message":"address is not available ,","status":"400"})
#         if not  city:
#             return JsonResponse({"message":"city is not available ,","status":"400"})
#         if not  state:
#             return JsonResponse({"message":"state is not available ,","status":"400"})
#         if not  country:
#             return JsonResponse({"message":"country is not available ,","status":"400"})
#         if not  zip_code:
#             return JsonResponse({"message":"zip_code is not available ,","status":"400"})
#         if not zip_code.isnumeric():
#             return JsonResponse({"message":"Zipcode must be integer value,","status":"400"})
#         if len(zip_code)>8 or len(zip_code)<6:
#             return JsonResponse({"message":"Please Enter valid Zipcode ,","status":"400"})
#         addressdata=Address.objects.create(unit_number=unit_number,addressline1=address,city=city,state=state,postal_code=zip_code,country_name=country)
#         serializer2=AddressSerializer(data=addressdata)
#         addressdata.save()
#         print(addressdata)
#         addressid=addressdata.id
        
#         user = User.objects.get(id= customer_id)
#         user.user = user
#         EstablishmentID = Establishment_type.objects.get(id= establishment_type_id)
#         EstablishmentID.EstablishmentID =EstablishmentID
#         AddressID = Address.objects.get(id= addressid)
#         AddressID.AddressID = AddressID
        
#         esdata=Establishment.objects.create(customer_id=user,name=name,establishment_type_id=EstablishmentID,address_id=AddressID)
#         dict_data={'customer_id':customer_id,'address_id':str(addressid),'name':name,'establishment_type_id':establishment_type_id }
#         return JsonResponse({"message":"success","status":"200","data":dict_data})    
    
    
    
    

    
 