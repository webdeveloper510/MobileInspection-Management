from django.urls import path
from Mobile_Inspectionapp.views import *

urlpatterns = [
    path('login/',UserLoginView.as_view(),name='login'),
    path('register/',RegisterView.as_view(),name='register'),
    path('contact/',ContactView.as_view(),name='contact'),
    path('serviceagreement/',ServiceAgreementView.as_view(),name='service_agreement'),
    path('servicetype/',ServiceTypeView.as_view(),name='servicetype'),
    path('service/',ServiceView.as_view(),name='service'),
    path('cart/',CartView.as_view(),name='cart'),
    path('logout/',LogoutUser.as_view(),name='logout'),
    
]