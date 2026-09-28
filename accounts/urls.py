from accounts.otp_send import RegisterView,ResetPasswordView,SendOTPView,VerifyOTPView
from django.urls import include, path

from . import views

urlpatterns = [

    path('login/', views.custom_login, name='login'),
    path('profile/', views.profile, name='profile'),
    path('change-password/', views.Change_password, name='change-password'),
    path('logout/', views.logout, name='logout'),  
    path('deactivate/', views.deactivate, name='deactivate'),
    path('otp-email/', SendOTPView.as_view(), name='SendOTP'),
    path('otp-verify/', VerifyOTPView.as_view(), name='verifyOTP'),
    path('reset-password/', ResetPasswordView.as_view(), name='resetpassword'),
    path('register/', RegisterView.as_view(), name='register'   ), 
]