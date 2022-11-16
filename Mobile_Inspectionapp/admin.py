from django.contrib import admin
from Mobile_Inspectionapp.models import Inspection ,User,Unit,Services,ElectricalInspectableItem
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

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
admin.site.register(Inspection)
admin.site.register(Unit)
admin.site.register(Services)
admin.site.register(ElectricalInspectableItem)
