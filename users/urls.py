from django.urls import path
from .views import (
    SignupView, 
    VerifyEmail, 
    LoginView, 
   
)

urlpatterns = [
    path('signup/', SignupView.as_view(), name='signup'),
    path('verify-email/<str:token>/', VerifyEmail.as_view(), name='verify-email'),
    path('login/', LoginView.as_view(), name='login'),

]

