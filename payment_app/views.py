from django.shortcuts import render
from payment_app. models import *
from Mobile_Inspectionapp. models import *
from Mobile_Inspectionapp. serializer import *
from payment_app. serializer import *
from rest_framework.views import APIView
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import action
from django.http import JsonResponse
import stripe
from rest_framework.response import Response
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.core.mail import EmailMultiAlternatives, message
from distutils import errors
from django.conf import settings
from Mobile_Inspection.settings import *
from rest_framework import viewsets
from base64 import b64encode
import base64
import requests
import json
from django.http import Http404
from django.http import HttpResponse
from django.template import loader




stripe.api_key=settings.API_SECRET_KEY
class OrderView(APIView):
    @csrf_exempt 
    @action(detail=False, methods=['post'])
    def post(self, request, format=None):
        user_id = request.data.get('user_id')
        service_id = request.data.get('service_id')
        service_type_id = request.data.get('service_type_id')
        quantity = request.data.get('quantity')
        total_price = request.data.get('total_price')
        discount = request.data.get('discount')
        subtotal = request.data.get('subtotal')
        establishment_data = request.data.get('establishment_data')
        address_data = request.data.get('address_data')
        contact_data = request.data.get('contact_data')
        email = request.data.get('email')
        firstname = request.data.get('firstname')
        lastname = request.data.get('lastname')
        phone = request.data.get('phone')
        street_number = request.data.get('street_number')
        unit_number = request.data.get('unit_number')
        address = request.data.get('address')
        address_1 = request.data.get('address_1')
        city = request.data.get('city')
        state = request.data.get('state')
        zip_code = request.data.get('zip_code')
        if not user_id:
             return JsonResponse({"message":"user  is required","status":"400"})
        if not User.objects.filter(id=user_id).exists():
            return JsonResponse({"message":"user does not exist","status":"400"})
        if not service_id:
            return JsonResponse({"message":" service id  is required","status":"400"})
        if not Service.objects.filter(id=service_id).exists():
            return JsonResponse({"message":"service id does not exist","status":"400"})
        if not service_type_id:
            return JsonResponse({"message":" service type  is required","status":"400"})
        if not ServiceType.objects.filter(id=service_type_id).exists():
            return JsonResponse({"message":"service type  does not exist","status":"400"})
        if not quantity:
            return JsonResponse({"message":" quantity is required","status":"400"})
        if not total_price:
            return JsonResponse({"message":" total price is required","status":"400"})
        if not subtotal:
            return JsonResponse({"message":" subtotal is required","status":"400"})
        else:
        
            user = User.objects.get(id=user_id)
            user.user = user
            ServiceId = Service.objects.get(id=service_id)
            ServiceId.ServiceId = ServiceId
            ServiceTypeId = ServiceType.objects.get(id=service_type_id)
            ServiceTypeId.ServiceTypeId = ServiceTypeId
            array1=[]
            array2=[]
            array3=[]
            for i in establishment_data:
              establishment_id =  (i['establishment_id'])
              array1.append(establishment_id)
            print("array",array1)

            for k in address_data:
                address_id = (k['address_id'])
                array2.append(address_id)
            print("array2",array2)

            for m in contact_data:
                contact_id = (m['contact_id'])
                array3.append(contact_id)
            print("array2",array3)
            print(type(array3))
            order_data = Order.objects.create(user_id=user,service_id=ServiceId, service_type_id=ServiceTypeId,quantity=quantity,total_price=total_price,
                        discount=discount,subtotal=subtotal, establishment_data=array1,address_data= array2,
                        contact_data=array3, email=email, First_name=firstname, Last_name=lastname,
                        phone=phone, street_number=street_number, unit_number=unit_number, address=address, address_1=address_1,
                        city=city, state=state, zip_code=zip_code)
            serializer = OrderSerializer(data=order_data)
            order_id = getattr(order_data, 'id')
            print(order_id)
            return JsonResponse({"message":"your details is successfully saved","status":"200","order_id":str(order_id)})

class OrderDetailView(APIView):
    @csrf_exempt
    def get(self, request, pk, format=None):
        array=[]
        if not Order.objects.filter(user_id=pk).exists():
                return JsonResponse({"status":"400","message":"no order found"})
        else:
            # order = Order.objects.all()
            # serializer = OrderSerializer(order, many=True)
            dict=Order.objects.filter(user_id=pk)
            serializer = OrderSerializer(dict, many=True)
         
            for x in serializer.data:
                order_id=x['id']
                user_id=x['user_id']
                order_id=x['id']
                service_id=x['service_id']
                service_type_id=x['service_type_id']
                quantity=x['quantity']
                total_price=x['total_price']
                discount=x['discount']
                subtotal=x['subtotal']
                payment_type=x['payment_type']
                status=x['status']
                establishment_data=x['establishment_data']
                es_data = eval(establishment_data)
                
                establishsment_data_array=[]
                for e in es_data:
                   
                    e_data = Establishment.objects.filter(id=e).values('id','name','address_id','customer_id','establishment_type_id')
                    data_easdatblishment={'id':str(e_data[0]['id']),'name':e_data[0]['name'],'address_id':str(e_data[0]['address_id']),'establishment_type_id':str(e_data[0]['establishment_type_id'])}

                    establishsment_data_array.append(data_easdatblishment)
                address_data=x['address_data']
                add_data = eval(address_data)
                address_data_array=[]
                for k in add_data:
                    adata=Address.objects.filter(id=k).values('id','unit_number','addressline1','city','state','postal_code','country_name')
                    data_address={"id":str(adata[0]['id']),'unit_number':adata[0]['unit_number'],'address':adata[0]['addressline1'],'city':adata[0]['city'],'state':adata[0]['state'],'country':adata[0]['country_name']}
                    address_data_array.append(data_address)
                
                contact_data=x['contact_data']
                con_data = eval(contact_data)
                contact_data_array=[]
                for j in con_data:
                    cdata=Establishment_Contact.objects.filter(id=j).values('id','firstname','lastname','title','establishment_id','customer_id')
                    data_contact={"id":str(cdata[0]['id']),'firstname':cdata[0]['firstname'],'lastname':cdata[0]['lastname'],'title':cdata[0]['title'],'establishment_id':str(cdata[0]['establishment_id']),'customer_id':str(cdata[0]['customer_id'])}
                    contact_data_array.append(data_contact)
                
                First_name=x['First_name']
                Last_name=x['Last_name']
                email=x['email']
                phone=x['phone']
                street_number=x['street_number']
                unit_number=x['unit_number']
                address=x['address']
                address_1=x['address_1']
                city=x['city']
                state=x['state']
                zip_code=x['zip_code']
                created_at=x['created_at']
                updated_at=x['updated_at']
                data={"id":str(order_id),"user_id":str(user_id),"service_id ":str(service_id),
                "service_type_id":str(service_type_id),
                "quantity":quantity, "total_price":str(total_price),"discount":discount,"subtotal":str(subtotal),
                "payment_type":payment_type,"status":status,"establishment_data":establishsment_data_array,
                "address_data":address_data_array,"contact_data":contact_data_array,
                "First_name":First_name,"Last_name":Last_name,
                    "email":email,"phone":phone,"street_number":street_number,"unit_number":unit_number,"address":address,"address_1":address_1,
                    "city":city,"state":state,"zip_code":str(zip_code),"created_at":created_at,"updated_at":updated_at}
                
                array.append(data)
              

            return JsonResponse({"status":"200","message":"success","data":array})
class OrderByIdView(APIView): 
    @csrf_exempt
    def get(self, request, pk, format=None):
        establishsment_data_array=[] 
        address_data_array=[]
        contact_data_array=[]

        if not Order.objects.filter(id=pk).exists():
            return JsonResponse({"status":"400","message":"no order found"})
        else:
            order_data =Order.objects.filter(id=pk).values('id','user_id','service_id','service_type_id','quantity','total_price',
                                                                    'discount','subtotal','payment_type','status','establishment_data','address_data','contact_data','First_name','Last_name','email','phone',
                                                                'street_number','unit_number','address','address_1','city','state','zip_code','created_at','updated_at')
            esdata=order_data[0]['establishment_data']
            es_data = eval(esdata)
            addata=order_data[0]['address_data']
            add_data = eval(addata)
            condata=order_data[0]['contact_data']
            Con_data = eval(condata)
            for i in es_data:
                if not Establishment.objects.filter(id=i).exists():
                    return JsonResponse({"message":" Eastablishment is not exist","status":"400"})
            for k in add_data:
                if not Address.objects.filter(id=k).exists():
                    return JsonResponse({"message":" Address is not exist","status":"400"})
            for j in Con_data:
                if not Establishment_Contact.objects.filter(id=j).exists():
                    return JsonResponse({"message":" contact is not exist","status":"400"})
                
            e_data = Establishment.objects.filter(id=i).values('id','name','address_id','customer_id','establishment_type_id')
            data_easdatblishment={'id':str(e_data[0]['id']),'name':e_data[0]['name'],'address_id':str(e_data[0]['address_id']),'establishment_type_id':str(e_data[0]['establishment_type_id'])}
            establishsment_data_array.append(data_easdatblishment)
        
            adata=Address.objects.filter(id=k).values('id','unit_number','addressline1','city','state','postal_code','country_name')
            data_address={"id":str(adata[0]['id']),'unit_number':adata[0]['unit_number'],'address':adata[0]['addressline1'],'city':adata[0]['city'],'state':adata[0]['state'],'country':adata[0]['country_name']}
            address_data_array.append(data_address)

            cdata=Establishment_Contact.objects.filter(id=j).values('id','firstname','lastname','title','establishment_id','customer_id')
            data_contact={"id":str(cdata[0]['id']),'firstname':cdata[0]['firstname'],'lastname':cdata[0]['lastname'],'title':cdata[0]['title'],'establishment_id':str(cdata[0]['establishment_id']),'customer_id':str(cdata[0]['customer_id'])}
            contact_data_array.append(data_contact)

            data={"id":str(order_data[0]['id']),"user_id":str(order_data[0]['user_id']),"service_id":str(order_data[0]['service_id']),
            "service_type_id":str(order_data[0]['service_type_id']),
            "quantity":order_data[0]['quantity'], "total_price":str(order_data[0]['total_price']),"discount":order_data[0]['discount'],"subtotal":str(order_data[0]['subtotal']),
            "payment_type":order_data[0]['payment_type'],"status":order_data[0]['status'],"establishment_data":establishsment_data_array,
            "address_data":address_data_array,"contact_data":contact_data_array,
            "First_name":order_data[0]['First_name'],"Last_name":order_data[0]['Last_name'],
                "email":order_data[0]['email'],"phone":order_data[0]['phone'],"street_number":order_data[0]['street_number'],"unit_number":order_data[0]['unit_number'],"address":order_data[0]['address'],"address_1":order_data[0]['address_1'],
                "city":order_data[0]['city'],"state":order_data[0]['state'],"zip_code":str(order_data[0]['zip_code']),"created_at":order_data[0]['created_at'],"updated_at":order_data[0]['updated_at']}
            return JsonResponse({"status":"200","message":"success","data":data})
        

class StripePaymentViewSet(APIView):
    @csrf_exempt 
    @action(detail=False, methods=['POST'])        
    def post(self, request, format=None):
        user_id = request.data.get('user_id')
        order_id = request.data.get('order_id')
        number = request.data.get('number')
        exp_month = request.data.get('exp_month')
        exp_year = request.data.get('exp_year')
        cvc = request.data.get('cvc')
        if not user_id:
            return Response({"message":"User id is null", "status": "401 Unauthorized"})
        if not order_id:
            return Response({"message":"order id is null", "status": "401 Unauthorized"})
        if not number:
            return Response({"message":"Please enter your card number", "status": "401 Unauthorized"})
        if not exp_month:
            return Response({"message":"Please enter expiry month", "status": "401 Unauthorized"})
        if not exp_year:
            return Response({"message":"Please enter expiry year", "status": "401 Unauthorized"})
        if not cvc:
            return Response({"message":"Please enter cvc", "status": "401 Unauthorized"})
        if not User.objects.filter(id=user_id).exists():
            return Response({"message":"User id does not exist", "status": "401 Unauthorized"})
        if not Order.objects.filter(id=order_id).exists():
            return Response({"message":"order id does not exist", "status": "401 Unauthorized"})
        else:
            user_data = User.objects.get(id=user_id)
            print( user_data.email)
            order_data = Order.objects.get(id=order_id)
            try:
                token_data = stripe.Token.create(
                card={
                    "name":user_data.First_name,
                    "number": number,
                    "exp_month": exp_month,
                    "exp_year": exp_year,
                    "cvc": cvc,
                }, )
                card_token = token_data['id']
                card_id = token_data['card']['id']
                pass
            except stripe.error.CardError as error:
                return Response(error.user_message)
            if card_token == card_token:
                customer_data = stripe.Customer.create( name =user_data.First_name,email=user_data.email)
                customer_id = customer_data['id']

            if customer_id == customer_id:
                source_data = stripe.Customer.create_source(customer_id,source=card_token)

            if source_data == source_data:
                payment_intent = stripe.PaymentIntent.create(
                customer = customer_id,
                amount= int(order_data.subtotal),
                currency="usd",
                payment_method_types=["card"],
                payment_method = card_id,
                confirmation_method = 'automatic',
                confirm=True,
                
                metadata= {'order_id': order_id,'user_id': user_id},
                )
                payment_intent_id = payment_intent['id']
                status = payment_intent['status']
                if status == "succeeded":
                    order_data = Order.objects.filter(id=order_id).update(status="succeeded", payment_type="stripe")
                    send_mail(
                    'Payment Success',
                    'we have successfully received your payment with stripe',
                    settings.EMAIL_HOST_USER,
                    [user_data.email],
                    fail_silently=False,
                    )

                    return Response({"message":"Payment Completed", "status":"200_Created"})
                else:
                    send_mail(
                    'Payment pending',
                    'your payment is pending ',
                    settings.EMAIL_HOST_USER,
                    [user_data.email],
                    fail_silently=False,
                    )
                    return Response({"message":"Payment pending","status":"400"})
            return Response("ok")

class TestSectionView(APIView):
  pass
      
class PaypalPaymentViewSet(viewsets.ViewSet):
    @csrf_exempt 
    @action(detail=False, methods=['POST'])
    def create_order(self, request, *args, **kwargs):
        global paypal_access_token
        user_id = request.data.get('user_id')
        order_id = request.data.get('order_id')
        if not user_id:
            return Response({"msg":"User id is null", "status": "401 Unauthorized"})
        if not order_id:
            return Response({"msg":"Checkout id is null", "status": "401 Unauthorized"})
        if not User.objects.filter(id=user_id).exists():
            return Response({"msg":"User id does not exist", "status": "401 Unauthorized"})
        if not Order.objects.filter(id=order_id).exists():
            return Response({"msg":"Checkout id does not exist", "status": "401 Unauthorized"})
        else:
           
            user_data = User.objects.get(id=user_id)
            checkout_data = Order.objects.get(id=order_id)
            encoded_auth = base64.b64encode((settings.CLIENT_ID + ':' + settings.CLIENT_SECRET).encode())
            headers ={ 'Authorization': f'Basic {encoded_auth.decode()}', 'Content-Type': 'application/json'  }
            paypal_access_token = requests.request("POST", "https://api.sandbox.paypal.com/v1/oauth2/token", headers=headers, data='grant_type=client_credentials')
            paypal_access_token = paypal_access_token.json()
            paypal_access_token = paypal_access_token['access_token']
            k=paypal_token.objects.all().count()
            # print(k)
            if k ==0:
                paypal_token.objects.create(paypal_access_token=paypal_access_token)
            else:
               m= paypal_token.objects.all().first()
               token_id = getattr(m,'id')
               paypal_token.objects.filter(id=token_id).update(paypal_access_token=paypal_access_token)
            if not paypal_access_token:
                return Response("Invalid paypal access token")
            else:
                payload = json.dumps({
                "intent": "CAPTURE",
                "purchase_units": [ {
                    "amount": {
                        "currency_code": "USD",
                        "value": checkout_data.subtotal,
                        # "order_id": checkout_id
                    } } ],
                "application_context": {
                    "return_url": "http://127.0.0.1:8000/paymentsuccess/",
                    "cancel_url": "http://127.0.0.1:8000/cancelpayment/"
                } })
                headers = {"Content-Type": "application/json", "Authorization": 'Bearer '+paypal_access_token}
                create_order_response = requests.request("POST", "https://api-m.sandbox.paypal.com/v2/checkout/orders", headers=headers, data=payload)
                create_order_response = create_order_response.json()
                approval_link = create_order_response['links'][1]['href']
                paypal_order_id = create_order_response['id']
                capture = create_order_response['links'][3]['href']
                if not Order.objects.filter(id=order_id).exists():
                    order_data = Order.objects.create(order_id=order_id, payment_type="paypal",amount=checkout_data.subtotal,status="pending")
                    
                else:
                    order_id = Order.objects.filter(id=order_id).values('id')
                    order_id = order_id[0]['id']
                    if not capture_paypal_payment.objects.filter(order_id=order_id).exists():
                        capture_paypal_payment.objects.create(order_id=order_id,capture_url=capture, status="pending")
                    else:
                        capture_paypal_payment.objects.filter(order_id=order_id).update(capture_url=capture)
                    return Response({"message":"order created","approval_link":approval_link,"paypal_access_token":paypal_access_token,"status":"200"})
        return Response(approval_link)
    
    @csrf_exempt 
    @action(detail=False, methods=['POST'])
    def capture_payment(self, request, *args, **kwargs):
        paypal_access_token = paypal_token.objects.all().first()
        paypal_access_token = getattr(paypal_access_token, 'paypal_access_token')
        order_id = request.data.get('order_id')
        # user_id = request.data.get('user_id')
        # user_data = User.objects.get(id=user_id)
        if not capture_paypal_payment.objects.filter(order_id=order_id).exists():
            return Response({"message":"order id does not exist","status":"400"})
        else:
            obj = capture_paypal_payment.objects.filter(status="pending",order_id=order_id).values('id','capture_url','order_id')
            # capture_url = getattr(obj, 'capture_url')
            capture_url=obj[0]['capture_url']
            # order_id = int(getattr(obj, 'order_id'))
            order_id=obj[0]['order_id']
            # capture_paypal_payment_id = int(getattr(obj, 'id'))
            capture_paypal_payment_id=obj[0]['id']
            headers = {'Content-Type': 'application/json','Authorization': 'Bearer '+paypal_access_token}
            response = requests.request("POST", capture_url, headers=headers)
            response = response.json()
            if 'status' in response: 
                paypal_order_id = response['id']
                payer_id = response['payer']['payer_id']     
                country = response['payer']['address']['country_code']     
                currency = response['purchase_units'][0]['payments']['captures'][0]['amount']['currency_code']
                amount = response['purchase_units'][0]['payments']['captures'][0]['amount']['value']
                capture_payment_id = response['purchase_units'][0]['payments']['captures'][0]['id']
                create_time = response['purchase_units'][0]['payments']['captures'][0]['create_time']
                update_time = response['purchase_units'][0]['payments']['captures'][0]['update_time']
                
                if str(response['status']) == "COMPLETED":
                    order_data = Order.objects.filter(id=order_id).update(status='succeeded',payment_type="paypal")
                    capture_paypal_payment_data = capture_paypal_payment.objects.filter(id=capture_paypal_payment_id).update(status="completed")
                return Response({"message":"payment success","status":"200"})
        return Response({"message":"payment is not captured as payment is not approved by user.","status":"400"})
    
    
def index(request):
  template = loader.get_template('thankyou.html')
  return HttpResponse(template.render())  

def cancel(request):
  template = loader.get_template('cancel.html')
  return HttpResponse(template.render())  


 
