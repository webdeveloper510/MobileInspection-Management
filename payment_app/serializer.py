from rest_framework import serializers
from payment_app. models import *

# class CheckoutSerializer(serializers.ModelSerializer):
#      class Meta:
#         model= Checkout
#         fields = '__all__'
           
#      def create(self, validate_data):
#          return Checkout.objects.create(**validate_data)

class OrderSerializer(serializers.ModelSerializer):
     class Meta:
        model= Order
        fields = '__all__'
           
     def create(self, validate_data):
         return Order.objects.create(**validate_data)
     

class capture_paypal_paymentSerializer(serializers.ModelSerializer):
     class Meta:
        model= capture_paypal_payment
        fields = '__all__'
           
     def create(self, validate_data):
         return Order.objects.create(**validate_data)