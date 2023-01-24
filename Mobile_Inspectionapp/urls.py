from django.urls import path
from Mobile_Inspectionapp.views import *
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.authtoken import views

urlpatterns = [
    path('login/',UserLoginView.as_view(),name='login'),
    path('password_set/',PasswordSetViewSet.as_view()),
    path('register/',RegisterView.as_view(),name='register'),
    path('resetpasswordlink/',SendPasswordResetLink.as_view(), name='send-reset-password link'),
    path('contact/',ContactView.as_view(),name='contact'),
    path('serviceagreement/',ServiceAgreementView.as_view(),name='service_agreement'),
    path('servicetype/',ServiceTypeView.as_view(),name='servicetype'),
    path('service/',Serviceview.as_view(),name='service'),
    path('service/<int:pk>/',ServiceListView.as_view(),name='serviceid'),
    path('Address/',AddressView.as_view(),name='address'),
    path('addaddress/',AddAddressView.as_view(),name='addaddress'),
    path('Establishment/',EstablishmentView.as_view(),name='establish'),
    path('Establishmentregister/',EstablishmentRegisterView.as_view(),name='eastablishment-Register'),
    path('update_eastablishment_address/',UpdateEastablishmentAddressView.as_view(),name='eastablishment-Register'),
    path('contact_establishment/',ContactEstablishmentView.as_view(),name='establish-contact'),
    path('customeraddress/<int:pk>/',CustomerAddressView.as_view(),name='customer_address'),
    path('pdf/',pdfview.as_view(),name="pdf"),
    path('profile/<int:pk>',CustomerProfileView.as_view(),name="profile"),
    # path('test/',TestView.as_view(),name="test"),

    
    
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)