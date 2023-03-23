from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.admin import UserAdmin
from .models import *
from django import forms
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField

class UserCreationForm(forms.ModelForm):
   
    password = forms.CharField(label='Password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('email', 'First_name', 'Last_name','title','role','password','mobile','attribute_name','position','token','is_active','user_created_by_admin','dispatcher_user_id')

    def clean_password2(self):
        password = self.cleaned_data.get("password")

    def save(self, commit=True):
       
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user

class UserChangeForm(forms.ModelForm):
   
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ('email','First_name', 'Last_name','title','role','password','mobile','attribute_name','position','token','is_active','user_created_by_admin','dispatcher_user_id')

    def clean_password(self):
        
        return self.initial["password"]


class UserAdmin(BaseUserAdmin):
   
    form = UserChangeForm
    add_form = UserCreationForm

    list_display = ('email', 'First_name', 'Last_name','title','role','password','mobile','attribute_name','position','token','is_active','is_admin','is_superuser','user_created_by_admin','dispatcher_user_id')
    list_filter = ('is_admin',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('First_name','Last_name','mobile','role','title','attribute_name')}),
        ('Permissions', {'fields': ('is_admin',)}),
    )
    # if want to give group permission to stafff user add field groups here
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'First_name', 'Last_name','title','role','password','mobile','attribute_name','position','token','is_active','is_admin','is_superuser','user_created_by_admin','dispatcher_user_id')}
        ),
    )
    readonly_fields =('is_superuser',)
    search_fields = ('email','role')
    ordering = ('email',)
    filter_horizontal = ()
    
    # with help below function staff user can add user and dispatcher but can not see the list
    # def get_queryset(self, request):
    #     qs = super().get_queryset(request)
    #     if request.user.is_superuser:
    #         return qs
    #     return qs.filter(email=request.user)

    # def has_add_permission(self, request, obj=None):
    #     return request.user.is_superuser

    # def has_delete_permission(self, request, obj=None):
    #     return request.user.is_superuser

admin.site.register(User, UserAdmin)

@admin.register(ServiceAgreement)
class ServiceAgreementAdmin(admin.ModelAdmin):
  list_display = ('id','service_agreement_form','signature','customer_id','date','time')
@admin.register(ServiceType)
class ServiceTypeAdmin(admin.ModelAdmin):
  list_display = ('id','service_agreement_id','service_type_description','service_type_name','price')
@admin.register(Service_Image)
class Service_ImageAdmin(admin.ModelAdmin):
  list_display = ('id','service_id','service_image')
@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
  list_display = ('id','service_type_id','name','description')
  
@admin.register(Establishment)
class EstablishmentAdmin(admin.ModelAdmin):
  list_display = ('id','customer_id','address_id','name','establishment_type_id')
@admin.register(Establishment_type)
class Establishment_typeAdmin(admin.ModelAdmin):
  list_display = ('id','Establishment_type')

@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
  list_display = ('id','customer_id','unit_number','addressline1','city','state','postal_code','country_name')

@admin.register(Promotion)
class PromotionAdmin(admin.ModelAdmin):
  list_display = ('id','name','promocode','discount_rate','start_date','end_date')
@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
  list_display = ('id','firstname','lastname','email','phone','address','city','state','country','zipcode','comment')

@admin.register(Customer_Address)
class Customer_AddressAdmin(admin.ModelAdmin):
  list_display = ('id','customer_id','address_id')

@admin.register(uploadpdf)
class uploadpdfAdmin(admin.ModelAdmin):
  list_display = ('id','uploadfile')

@admin.register(Establishment_Contact)
class Establishment_ContactfAdmin(admin.ModelAdmin):
  list_display = ('id','establishment_id','customer_id','firstname','lastname','title','phone')  

@admin.register(Operater)
class OperaterAdmin(admin.ModelAdmin):
  list_display = ('id','firstname','lastname','phone','email','position','operater_type')  

@admin.register(ServiceItem)
class ServiceItemAdmin(admin.ModelAdmin):
  list_display = ('id','establishment_id','service_type_id','operater_id','service_date_time','service_notes')  