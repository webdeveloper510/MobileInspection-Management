from django.contrib import admin
from payment_app .models import *

# @admin.register(Checkout)
# class CheckoutAdmin(admin.ModelAdmin):
#   list_display = ('id','user_id','service_id','service_type_id','quantity','total_price','discount','subtotal')

@admin.register(Order)
class CheckoutAdmin(admin.ModelAdmin):
  list_display = ('id','user_id','service_id','service_type_id','quantity','total_price','discount','subtotal',
  'payment_type','status','establishment_data','address_data','contact_data','First_name','Last_name','email','phone','street_number','unit_number',
  'address','address_1','city','state','zip_code','created_at','updated_at')

@admin.register(capture_paypal_payment)
class capture_paypal_paymentModelAdmin(admin.ModelAdmin):
    list_display = ('id','order_id','capture_url','status')
    list_filter = ('order_id','status')
    search_fields = ('order_id','status')
    ordering = ('status','order_id')
    filter_horizontal = ()

    def has_add_permission(self, request):
        return False

    # def has_delete_permission(self, request, obj=None):
    #     return False