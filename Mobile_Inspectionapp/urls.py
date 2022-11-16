from django.urls import path
from Mobile_Inspectionapp.views import *


urlpatterns = [
    path('inspection/',InspectionView.as_view(),name='inspection'),
    path('login/',Login.as_view(),name='login'),
    path('logout/',Logout.as_view(),name='logout'),
    path('unitlist/', UnitListView.as_view(),name='unitlist'),
    path('addunit/', UnitListView.as_view(),name='addunit'),
    path('deleteunit/<int:pk>', DeleteUnit.as_view(),name='deleteunit'),
    path('serviceslist/', ServicesListView.as_view(),name='serviceslist'),
    path('add_services/', ServicesListView.as_view(),name='addservices'),
    path('deleteservice/<int:pk>', DeleteService.as_view(),name='deleteservice'),
    path('add_electricalitem/', ElectricalInspectableItemView.as_view(),name='additem'),
    path('electricalitemlist/', ElectricalInspectableItemView.as_view(),name='itemlist'),
    path('delete_electricalInspectable/<int:pk>', DeleteElectricalInspectableItem.as_view(),name='delete_electricalInspectable')
    
]