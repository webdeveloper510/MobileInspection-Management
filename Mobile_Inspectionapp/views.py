from .models import *
from .serializer import *
from rest_framework.response import Response
from rest_framework.views import APIView
from Mobile_Inspectionapp.renderer import UserRenderer
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import action
from .validater import *
from django.http import JsonResponse
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated ,AllowAny
from django.http import Http404
from rest_framework.decorators import  permission_classes
from rest_framework_simplejwt.tokens import RefreshToken
from django.conf import settings
from rest_framework.authtoken.models import Token


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
         registred_data=User.objects.create(First_name=First_name,Last_name=Last_name,email=email,title=title,mobile=mobile,attribute_name=attribute_name,password=password)
         serializer = UserSerializer(data=registred_data)
         registred_data.save()
         id=User.objects.filter(email=email).values('id','email')
         user=id[0]['email']
         print(user)
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
                                                                'attribute_name')
            data={"id":str(Csdata[0]['id']),"First_name":Csdata[0]['First_name'],"Last_name":Csdata[0]['Last_name'],
                "email":Csdata[0]['email'],"mobile":Csdata[0]['mobile'],"title":Csdata[0]['title'],"attribute_name":Csdata[0]['attribute_name']}
        
            return JsonResponse({"status":"200","message":"success","data":data})
        else:
            return JsonResponse({"status":"400","message":"user does not Exist"})   
            
# class LogoutUser(APIView):
# #   permission_classes = [IsAuthenticated]
#   authentication_classes = [TokenAuthentication]
#   def post(self, request, format=None):
#     return Response({'msg':'Logout Successfully'},status=status.HTTP_200_OK)
    
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
    Data=request.data.get('data')
    if not Data:
        return JsonResponse({"message":"address list is empty","status":"400"})
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
         return JsonResponse({"message":"zip_code is not available ,","status":"400"})
     
        if not zip_code.isnumeric():
         return JsonResponse({"message":"Zipcode must be integer value,","status":"400"})
     
        if len(zip_code)>8 or len(zip_code)<6:
         return JsonResponse({"message":"Please Enter valid Zipcode ,","status":"400"})
    for x in Data:
        unit_number=x['unit_number']
        address=x['address']
        city=x['city']
        state=x['state']
        country=x['country']
        zip_code=x['zip_code']
        addressdata=Address.objects.create(unit_number=unit_number,addressline1=address,city=city,state=state,postal_code=zip_code,country_name=country)
        serializer2=AddressSerializer(data=addressdata)
        addressdata.save()
        print(addressdata)
    return JsonResponse({"message":"your  adddress is successfully saved","status":"200"})  
    
# Establishment related api    
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
    
    
class EstablishmentRegisterView(APIView):
    @csrf_exempt 
    @action(detail=False, methods=['post'])
    def post(self, request, format=None):  
        customer_id=request.data.get('customer_id') 
        establishment_type_id=request.data.get('establishment_type_id')
        name=request.data.get('name')
        
        if not customer_id:
            return JsonResponse({"message":" Customer id is required ","status":"400"})
        
        if not User.objects.filter(id= customer_id).exists() :
            
           return JsonResponse({"message":" Customer id  does not exist","status":"400"})    
        
        if not  establishment_type_id :
            return JsonResponse({"message":" establishment_type_id is required ","status":"400"})
        
        if not Establishment_type.objects.filter(id= establishment_type_id).exists() :
                   
          return JsonResponse({"message":" establishment_type_id does not exists ","status":"400"})
        
        if name:
            name = name
        else:
            return JsonResponse({"message":"name field can not be empty ","status":"400"})
        
        EstablishmentTypeID = Establishment_type.objects.get(id=establishment_type_id)
        EstablishmentTypeID.EstablishmentID = EstablishmentTypeID
        
        user = User.objects.get(id=customer_id)
        print(user)
        user.user = user
        
        EstablishmentData=Establishment.objects.create(customer_id=user,establishment_type_id=EstablishmentTypeID,name=name)
        serializer = EstablishmentSerializer(data=EstablishmentData)
        EstablishmentData.save()
        return JsonResponse({"message":"your establishment successfully saved ","status":"200"})
    
    
class UpdateEastablishmentAddressView(APIView):
    @csrf_exempt 
    @action(detail=False, methods=['put'])
    def put(self, request, format=None):  
        establishment_id=request.data.get('establishment_id') 
        print(establishment_id)
        address_id=request.data.get('address_id')
        
        if not establishment_id:
            return JsonResponse({"message":" establishment_id is required ","status":"400"})
        
        if not Establishment.objects.filter(id= establishment_id).exists() :
            
         return JsonResponse({"message":" establishment_id is does not exist ","status":"400"})
        
        if not address_id:
            return JsonResponse({"message":"address_id is required ","status":"400"})
        
        if not Address.objects.filter(id=address_id).exists() :
            
         return JsonResponse({"message":"address_id is does not exist ","status":"400"})
        
        updatedata=Establishment.objects.filter(id=establishment_id).update(address_id=address_id)
        
        return JsonResponse({"message":"your address_id successfully updated ","status":"200"})
            
    
class ContactEstablishmentView(APIView):
    @csrf_exempt 
    @action(detail=False, methods=['post'])
    def post(self, request, format=None):
        data=request.data.get('data')
        if not data:
         return JsonResponse({"message":"contact list  is empty","status":"400"})
        for x in data:
            
            customer_id=x['customer_id']
            
            if not customer_id: 
                return JsonResponse({"message":" Customer id is required ","status":"400"})
            
            if not User.objects.filter(id= customer_id).exists() :
               return JsonResponse({"message":" Customer id  does not exist","status":"400"})
        
            establishment_id=x['establishment_id']
            
            if not establishment_id:
                return JsonResponse({"message":" establishment id is required ","status":"400"})
                
            if not Establishment.objects.filter(id= establishment_id).exists():
             return JsonResponse({"message":" establishment id  does not exist","status":"400"})
             
            firstname=x['firstname'] 
            lastname=x['lastname']
            title=x['title']
            phone=x['phone']
            
        for i in data:
          customer_id=i['customer_id']
          establishment_id=i['establishment_id']
          firstname=i['firstname']
          lastname=i['lastname']
          title=i['title']
          phone=i['phone']
       
          EstablishmentID = Establishment.objects.get(id=establishment_id)
          EstablishmentID.EstablishmentID = EstablishmentID
        
          user = User.objects.get(id= customer_id)
          user.user = user
       
          Cedata=Establishment_Contact.objects.create(customer_id=user,establishment_id=EstablishmentID,firstname=firstname,lastname=lastname,title=title,phone=phone)
          serializer = Establishment_ContactSerializer(data=Cedata)
          Cedata.save()
          print(Cedata)
        #   dict_data={"customer_id":customer_id,"establishment_id":establishment_id,"firstname":firstname,"lastname":lastname,"title":title,"phone":phone}
        return JsonResponse({"message":"Your Contact is successfully saved","status":"200"})    


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
        street_number=request.data.get('street_number')
        unit_number=request.data.get('unit_number')
        address=request.data.get('address')
        address1=request.data.get('address1')
        city=request.data.get('city')
        state=request.data.get('state')
        country=request.data.get('country')
        zipcode=request.data.get('zipcode')
        comment=request.data.get('comment')
        if not firstname:
            return JsonResponse({"message":"Firstname is required","status":"400"})
        if not Lastname:
            return JsonResponse({"message":"lastname is required","status":"400"})
        if not email:
            return JsonResponse({"message":"email is required","status":"400"})
        if not phone:
            return JsonResponse({"message":"phone number is required","status":"400"})
        if not street_number:
            return JsonResponse({"message":"street_number is required","status":"400"})
        if not unit_number:
            return JsonResponse({"message":"unit_number is required","status":"400"})
        if not address:
            return JsonResponse({"message":"address is required","status":"400"})
        if not address1:
            return JsonResponse({"message":"address1 is required","status":"400"})
        if not city:
            return JsonResponse({"message":"city is required","status":"400"})
        if not state:
            return JsonResponse({"message":"state is required","status":"400"})
        if not country:
            return JsonResponse({"message":"country is required","status":"400"})
        if not zipcode:
            return JsonResponse({"message":"zipcode is required","status":"400"})
        if not zipcode.isnumeric():
            return JsonResponse({"message":"Zipcode must be integer value,","status":"400"})
        if len(zipcode)>8 or len(zipcode)<6:
            return JsonResponse({"message":"Please Enter valid Zipcode ,","status":"400"})
        else:
            contact_data=Contact.objects.create(firstname=firstname,lastname=Lastname,email=email,phone=phone,
                                            street_number=street_number,unit_number=unit_number,address=address,address1=address1,city=city,
                                            state=state,country=country,zipcode=zipcode,comment=comment)
            
            serializer =ContactSerializer(data=contact_data)
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
            return JsonResponse({"status":"200","message":"success","Data":array})
        


     
from django.conf import settings

class pdfview(APIView):
    def get(self, request, format=None):
        service_data = uploadpdf.objects.all()
        serializer = UploadpdfSerializer(service_data, many=True)
        print(serializer.data[0])
        url = settings.BASE_URL+serializer.data[0]['uploadfile']
        return Response(url)
    


    
    
    




# class EstablishmentRegisterView(APIView):
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
    
    
    
    
    
    
    
 