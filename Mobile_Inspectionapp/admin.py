from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import *

class UserModelAdmin(BaseUserAdmin):
   
    list_display = ('id','email','username','is_admin')
    list_filter = ('is_admin',)
    fieldsets = (
      ('User Credentials', {'fields': ('email', 'password')}),
      ('Personal info', {'fields': ('username', )}),
      ('Permissions', {'fields': ('is_admin',)}),
  )
    add_fieldsets = (
      (None, {
          'classes': ('wide',),
          'fields': ('email', 'username',  'password'),
      }),
  )
    search_fields = ('email',)
    ordering = ('email', 'id')
    filter_horizontal = ()

admin.site.register(User)
# admin.site.register(UserManager)
admin.site.register(Service)
admin.site.register(ServiceAgreement)
admin.site.register(ServiceType)
admin.site.register(Operater)
admin.site.register(Lead)
admin.site.register(LeadAddress)
admin.site.register(Establishment)
admin.site.register(Service_Order)
admin.site.register(Address)
admin.site.register(Promotion_Category)
admin.site.register(Promotion)

