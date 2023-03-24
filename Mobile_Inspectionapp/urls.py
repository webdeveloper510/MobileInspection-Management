from django.urls import path
from Mobile_Inspectionapp.views import *
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.authtoken import views
from django.contrib import admin


urlpatterns = [
    path('login/',UserLoginView.as_view(),name='login'),
    path('logout/',Logout.as_view(),name='logout'),
    path('register/',RegisterView.as_view(),name='register'),
    path('create_multiple_customer/',CreateMultipleCustomerView.as_view(),name='CreateMultipleCustomer'),
    path('update_multiple_customer/',UpdateMultipleCustomerView.as_view(),name='UpdateMultipleCustomer'),
    path('create_multiple_dispatcher/',CreateMultipleDispatcherView.as_view(),name='CreateMultipleDispatcher'),
    path('update_multiple_dispatcher/',UpdateMultipleDispatcherView.as_view(),name='UpdateMultipleDispatcher'),
    path('resetpasswordlink/',SendPasswordResetLink.as_view(), name='send-reset-password link'),
    path('password_set/',PasswordSetViewSet.as_view()),
    path('contact/',ContactView.as_view(),name='contact'),
    path('serviceagreement/',ServiceAgreementView.as_view(),name='service_agreement'),
    path('servicetype/',ServiceTypeView.as_view(),name='servicetype'),
    path('service/',Serviceview.as_view(),name='service'),
    path('service/<int:pk>/',ServiceListView.as_view(),name='serviceid'),
    path('Address/',AddressView.as_view(),name='address'),
    path('update_address_eastablishment/<int:pk>',Update_address_eastablishment.as_view(),name='update_address'),# update address and eastablishment api 
    path('addaddress/',AddAddressView.as_view(),name='addaddress'),
    path('updateaddress/<int:pk>',UpdateAddressView.as_view(),name='updateaddressbyid'),
    path('getaddress/<int:pk>',GetAddressById.as_view(),name='getaddressbyid'),
    path('Establishment/',EstablishmentView.as_view(),name='establish'),
    path('get_eastablishment_address/<int:pk>',EastablishmentDetailsView.as_view(),name='establish-by-id'),
    path('establishmenttype/',EstablishmenttypeView.as_view(),name='establishtype'),
    path('Establishmentregister/',EstablishmentRegisterView.as_view(),name='eastablishment-Register'),
    path('add_establishment/',AddEstablishment.as_view(),name='add-eastablishment'),
    path('update_establishment/<int:pk>',UpdateEstablishment.as_view(),name='update_establishment'),
    path('get_establishment/<int:pk>',GetEstablishmentById.as_view(),name='get_establishment'),
    path('update_eastablishment_address/',UpdateEastablishmentAddressView.as_view(),name='eastablishment-update-address'),# connect eastablishment and addess api
    path('contact_establishment/',ContactEstablishmentView.as_view(),name='establish-contact'),
    path('update_eastablishment_contact/<int:pk>',Update_Establishment_Contact.as_view(),name='establish-contact'),
    path('customeraddress/<int:pk>/',CustomerAddressView.as_view(),name='customer_address'),
    path('pdf/',pdfview.as_view(),name="pdf"),
    path('profile/',Profilenotupdate.as_view(),name="notupdate"),
    path('profile/<int:pk>',CustomerProfileView.as_view(),name="profile"),
    path('profileupdate/',Profileupdate.as_view(),name="update"),
    path('promocode_discount/',PromocodeDiscountView.as_view(),name="promo"),
    path('establishment_contact_list/<int:pk>',Establishment_contact_listView.as_view()),
    path('create_operater/',CreateOperaterView.as_view(),name="create_operater"),# create operater new
    path('update_operater/<int:pk>',UpdateOperaterView.as_view(),name="update_operater"),# update operater new
    path('get_operater_by_id/<int:pk>',GetOperaterById.as_view(),name="getoperater_byid"),# get operater by id new
    path('get_operater/',GetOperaterDetail.as_view(),name="getoperater"),# get all operater detail new
    path('create_service_item/',CreateServiceItemView.as_view(),name="create_service_item"),# create service item new
    path('update_service_item/<int:pk>',UpdateServiceItemView.as_view(),name="update_service_item"),# create service item new
    path('get_serviceitem_by_id/<int:pk>',GetServiceItemById.as_view(),name="GetServiceItemById"),# get service item by id
    path('get_service_item/',GetServiceItemDetail.as_view(),name="GetServiceItemDetail"),# get all service item detail new
    path('user_details_by_dispatcher_id/', UserDetailByDispatcherIdView.as_view(),name="GetDispatcherDetailByDispatcherId"),#brand new
    path('test/',TestSectionView.as_view(),name="test"),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)

admin.site.site_header = 'Inspection Squad'