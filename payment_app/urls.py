from django.urls import path
from payment_app.views import *
from payment_app import views

urlpatterns = [
     path('order/',OrderView.as_view(),name='order'), 
     path('order_detail/<int:pk>',OrderDetailView.as_view(),name='order_detail'),   
     path('order_id/<int:pk>',OrderByIdView.as_view(),name='order_by_id'),   
     path('stripe/', StripePaymentViewSet.as_view()),
     # path('test/',TestSectionView.as_view()),
     path('paypal/order/', views.PaypalPaymentViewSet.as_view({'post':'create_order'})),
     path('paypal/capture/', views.PaypalPaymentViewSet.as_view({'post':'capture_payment'})),
     path('paymentsuccess/',views.index),
     path('cancelpayment/',views.cancel),
     

]
