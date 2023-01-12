from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import *

class UserModelAdmin(BaseUserAdmin):
   
    list_display = ('id','email','First_name','Last_name','is_admin')
    list_filter = ('is_admin',)
    fieldsets = (
      ('User Credentials', {'fields': ('email', 'password')}),
      ('Personal info', {'fields': ('First_name','Last_name', )}),
      ('Permissions', {'fields': ('is_admin',)}),
  )
    add_fieldsets = (
      (None, {
          'classes': ('wide',),
          'fields': ('email', 'First_name', 'Last_name' 'password'),
      }),
  )
    search_fields = ('email',)
    ordering = ('email', 'id')
    filter_horizontal = ()

admin.site.register(User)
@admin.register(ServiceAgreement)
class ServiceAgreementAdmin(admin.ModelAdmin):
  list_display = ('id','service_agreement_form','signature','customer_id','date','time')
@admin.register(ServiceType)
class ServiceTypeAdmin(admin.ModelAdmin):
  list_display = ('id','service_agreement_id','service_type_name','price')
@admin.register(Service_Image)
class Service_ImageAdmin(admin.ModelAdmin):
  list_display = ('id','service_id','service_image')
@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
  list_display = ('id','service_type_id','name','description')
@admin.register(Operater)
class OperaterAdmin(admin.ModelAdmin):
  list_display = ('id','firstname','lastname','phone','email','title','password','operater_type')
@admin.register(Lead)
class LeadAdmin(admin.ModelAdmin):
  list_display = ('id','firstname','lastname','phone','email','comment','date','time')
@admin.register(LeadAddress)
class LeadAddressAdmin(admin.ModelAdmin):
  list_display = ('id','customer_id','street_number','unit_number','addressline1','addressline2','city','state','postal_code','country_name')
@admin.register(Establishment)
class EstablishmentAdmin(admin.ModelAdmin):
  list_display = ('id','customer_id','address_id','name','establishment_type_id')
@admin.register(Establishment_type)
class Establishment_typeAdmin(admin.ModelAdmin):
  list_display = ('id','Establishment_type','title')
@admin.register(Service_Order)
class Service_OrderAdmin(admin.ModelAdmin):
  list_display = ('id','User_id','service_id','order_status','operater_id','service_datetime','service_fee','total_amount','requested_service_datetime','Establishment_id')
@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
  list_display = ('id','unit_number','addressline1','city','state','postal_code','country_name')
@admin.register(Promotion_Category)
class Promotion_CategoryAdmin(admin.ModelAdmin):
  list_display = ('id','promotion_id','service_type_id')
@admin.register(Promotion)
class PromotionAdmin(admin.ModelAdmin):
  list_display = ('id','name','description','discount_rate','start_date','end_date')

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
  list_display = ('id','firstname','lastname','email','phone','street_number','address','city','state','country','zipcode')

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
  list_display = ('id','service_id','created_at','updated_at')