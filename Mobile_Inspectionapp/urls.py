from django.urls import path
from Mobile_Inspectionapp.views import *

urlpatterns = [
    path('login/',UserLoginView.as_view(),name='login'),
    path('register/',RegisterView.as_view(),name='register'),
    path('contact/',ContactView.as_view(),name='contact'),
    path('serviceagreement/',ServiceAgreementView.as_view(),name='service_agreement'),
    path('servicetype/',ServiceTypeView.as_view(),name='servicetype'),
    path('service/',ServiceView.as_view(),name='service'),
    path('service/<int:pk>/',ServiceListView.as_view(),name='serviceid'),
    path('customerinfo/<int:pk>/',CustomerInfo.as_view(),name='customerinfo'),
    path('Address/',AddressView.as_view(),name='address'),
    path('Establishment/',EstablishmentView.as_view(),name='establish'),
    # path('Establishmentregister/',EstablishmentRegisterView.as_view(),name='establishregister'),
    path('logout/',LogoutUser.as_view(),name='logout')
    
    
]