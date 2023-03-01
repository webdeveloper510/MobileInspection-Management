from django.db import models
from Mobile_Inspectionapp.models import *

class Order(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    service_id=models.ForeignKey(Service, on_delete=models.CASCADE)
    service_type_id=models.ForeignKey(ServiceType, on_delete=models.CASCADE)
    quantity=models.CharField(max_length = 250)
    total_price=models.FloatField(default=0.0)
    discount=models.CharField(max_length = 250)
    subtotal=models.FloatField(default=0.0)
    payment_type = models.CharField(max_length=90)
    status = models.CharField(max_length=250, default="pending")
    establishment_data = models.CharField(max_length=250)
    address_data = models.CharField(max_length=250)
    contact_data = models.CharField(max_length=250)
    First_name = models.CharField(max_length=250)
    Last_name = models.CharField(max_length=250)
    email = models.EmailField(max_length=250)
    phone = models.CharField(max_length=50)
    street_number = models.CharField(max_length=250)
    unit_number = models.CharField(max_length=250)
    address = models.CharField(max_length=250)
    address_1 = models.CharField(max_length=250)
    city =  models.CharField(max_length=250)
    state =  models.CharField(max_length=250)
    zip_code = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
  
    class Meta:
        verbose_name_plural = "Order"


class capture_paypal_payment(models.Model):
    order_id = models.CharField(max_length=90, null=True, blank=True)
    capture_url = models.CharField(max_length=250)
    status = models.CharField(max_length=150)
    class Meta:
           verbose_name_plural = "Paypal Capture Payments"

class paypal_token(models.Model):
    paypal_access_token = models.CharField(max_length=900)

class stripe_payment(models.Model):
    name = models.CharField(max_length=90)
    receipt_id = models.CharField(max_length=90)
    user_id = models.CharField(max_length=90)
    checkout_id = models.CharField(max_length=90)
    amount_received = models.CharField(max_length=90)
    payment_intent_id = models.CharField(max_length=90)
    billing_details = models.TextField(max_length=350, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    receipt_url = models.CharField(max_length=90, null=True, blank=True)

