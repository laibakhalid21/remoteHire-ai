from django.urls import path
from .views import LoginView, LogoutView, ProfessionalView,CompanyView, ResendVerificationView,VerifyEmailView , ProtectedView, RegisterView, ForgotPasswordView, ResetPasswordView
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    #    path('login/', TokenObtainPairView.as_view(), name='login'),
    path('protected/', ProtectedView.as_view(), name='protected'),
    path('token/refresh/',
         TokenRefreshView.as_view(),
         name='token_refresh'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('professional/', ProfessionalView.as_view(), name='professional'),
    path('company/', CompanyView.as_view(), name='company'),
    path('verify-email/<uid>/<token>/', VerifyEmailView.as_view(), name='verify-email'),
    path('resend-verification/',ResendVerificationView.as_view(), name='resend-verification'),
    path('forgot-password/', ForgotPasswordView.as_view(),name='forgot-password'),
    path('reset-password/<uid>/<token>/', ResetPasswordView.as_view(), name='reset-password'),
]