from django.urls import path
from Mobile_Inspectionapp.views import *


urlpatterns = [
    path('login/',UserLoginView.as_view(),name='login'),
    path('register/',UserRegistrationView.as_view(),name='register'),
    path('lead/',LeadView.as_view(),name='lead'),
    path('address/',LeadAddressView.as_view(),name='leadaddress'),
    path('service/',ServiceView.as_view(),name='service'),
    path('servicetype/',ServiceTypeView.as_view(),name='servicetype'),
    path('promotioncategory/',PromotionCategoryView.as_view(),name='promotion_category'),
    path('promotion/',PromotionView.as_view(),name='promotion'),
    
]