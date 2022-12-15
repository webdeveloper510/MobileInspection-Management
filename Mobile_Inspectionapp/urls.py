from django.urls import path
from Mobile_Inspectionapp.views import *

urlpatterns = [
    path('login/',UserLoginView.as_view(),name='login'),
    path('register/',UserRegistrationView.as_view(),name='register'),
    path('serviceagreement/',ServiceAgreementView.as_view(),name='service_agreement'),
    path('servicetype/',ServiceTypeView.as_view(),name='servicetype'),
    path('service/',ServiceView.as_view(),name='service'),
    
]