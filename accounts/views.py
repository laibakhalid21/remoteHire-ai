from tokenize import TokenError
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import RegisterSerializer, LoginSerializer, ResendVerificationSerializer, ForgotPasswordSerializer, ResetPasswordSerializer
from rest_framework_simplejwt.tokens import RefreshToken 
from rest_framework.permissions import IsAuthenticated
from .permissions import IsCompany, IsProfessional
from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from .models import CustomUser
from .utils import send_verification_email
from rest_framework.permissions import AllowAny
from django.utils.encoding import force_bytes
from django.core.mail import send_mail 
from rest_framework.throttling import ScopedRateThrottle


# Create your views here.

class RegisterView(APIView):
    def post(self,request):
        serializer=RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user=serializer.save()
            send_verification_email(user,request)
            return Response({
                "message":"Registration successful. Please check your email to verify your account.",
               "user":serializer.data 
            },status=status.HTTP_201_CREATED)
        return Response (serializer.errors,status=status.HTTP_400_BAD_REQUEST)

#generics
# class RegisterViewGeneric(generics.CreateAPIView):
#     serializer_class=RegisterSerializer

class LoginView(APIView):
    throttle_classes=[ScopedRateThrottle]
    throttle_scope="login"
    def post(self,request):
        serializer=LoginSerializer(data=request.data)

        if serializer.is_valid():
            user=serializer.validated_data['user']

            refresh=RefreshToken.for_user(user)
            access_token=str(refresh.access_token)
            return Response({
                "message":"Login successful",
                "refresh_token":str(refresh),
                "access_token":access_token,
                "user":{
                    "email":user.email,
                    "role":user.role,
                    }
                }
                ,status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


class ProtectedView(APIView):
    permission_classes = [IsAuthenticated] #allow only authenticated users to access this view
    def get(self,request):
        return Response({"message":"You are authenticated"},status=status.HTTP_200_OK)


class ProfessionalView(APIView):
    permission_classes = [IsProfessional] #allow only authenticated users to access this view
    def get(self,request):
            return Response({"message":"Welcome professional",
                             "email":request.user.email,
                             },status=status.HTTP_200_OK)


class CompanyView(APIView):
    permission_classes = [IsCompany] #allow only company users to access this view
    def get(self,request):
        return Response({"message":"Welcome company",
                         "email":request.user.email,
                         },status=status.HTTP_200_OK)


class LogoutView(APIView):
    def post(self, request):
        refresh_token=request.data.get("refresh")

        if not refresh_token:
            return Response({
                "error": "Refresh token is required"
            }, status=status.HTTP_400_BAD_REQUEST
            )
        try:
            token=RefreshToken(refresh_token)
            token.blacklist()

            return Response({
                "message": "logout Successful"
            }, status=status.HTTP_205_RESET_CONTENT)
        except TokenError:
            return Response({
                "error": "Invalid refresh token"
            }, status=status.HTTP_400_BAD_REQUEST
            )



class VerifyEmailView(APIView):
    def get(self, request, uid, token):
        try:
            user_id=force_str(urlsafe_base64_decode(uid))
            user=CustomUser.objects.get(pk=user_id)
        except (TypeError , ValueError, OverflowError, CustomUser.DoesNotExist):
            return Response(
                {"error":"Invalid verification link"},
                status=status.HTTP_400_BAD_REQUEST
            )

        if default_token_generator.check_token(user,token):
            user.is_verified=True
            user.save(update_fields=["is_verified"])

            return Response(
                {"message":"Email verified successfully"},
                status=status.HTTP_200_OK
            )

        return Response(
            {"error": "Invalid or expired verification link"},
            status=status.HTTP_400_BAD_REQUEST
        )



class ResendVerificationView(APIView):
    permission_classes=[AllowAny]
    def post(self, request):
        serializer=ResendVerificationSerializer(data=request.data)
        if serializer.is_valid():
            email=serializer.validated_data['email']
            try:
                user=CustomUser.objects.get(email__iexact=email)
            except CustomUser.DoesNotExist:
                return Response(
                    {"error":"No account found with this email"},
                    status=status.HTTP_404_NOT_FOUND
                )
            if user.is_verified:
                return Response(
                    {"message": "Email is already verified."},
                    status=status.HTTP_400_BAD_REQUEST
                )
            send_verification_email(user,request)
            return Response(
                {"message": "Verification email sent successfully."},
                status=status.HTTP_200_OK
            )
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )



class ForgotPasswordView(APIView):
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = "forgot_password"

    def post(self,request):
        serializer=ForgotPasswordSerializer(data=request.data)
        if serializer.is_valid():
            email=serializer.validated_data["email"]

        try:
            user=CustomUser.objects.get(email__iexact=email)
        except CustomUser.DoesNotExist:
            return Response({
                "error": "User with this email does not exist"
            },status=status.HTTP_404_NOT_FOUND)


        if not user.is_verified:
            return Response({
                "error":"Please verify your email before resetting your password"
            }, status=status.HTTP_400_BAD_REQUEST)

        
        uid=urlsafe_base64_encode(force_bytes(user.pk))
        token=default_token_generator.make_token(user)

        reset_link=(
            f"{settings.FRONTEND_URL}/reset-password/{uid}/{token}/"
        )

        send_mail(
            subject="Reset Your Password",
            message=f"Click the link below to reset your password:\n\n{reset_link}",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            fail_silently=False,
        )

        return Response({
            "message": "password reset link sent successfully"
        },status=status.HTTP_200_OK)



class ResetPasswordView(APIView):
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = "resend_verification"

    def post(self,request,uid,token):
        
        try:
            user_id=force_str(urlsafe_base64_decode(uid))
            user=CustomUser.objects.get(pk=user_id)
        except (TypeError,ValueError,OverflowError,CustomUser.DoesNotExist):
            return Response({
                "error":"Invalid reset link"
            }, status=status.HTTP_400_BAD_REQUEST)

        if not default_token_generator.check_token(user,token):
            return Response(
                {"error": "Invalid or expired reset link"},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer= ResetPasswordSerializer(data=request.data,context={"user":user})
        # if not serializer.is_valid():
        #     return Response( serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        serializer.is_valid(raise_exception=True)
        new_password=serializer.validated_data['new_password']
        

        #Everything is valid ->  perform an action
        user.set_password(new_password)
        user.save(update_fields=['password'])

        return Response(
            {"message": "Password reset successfully"},
            status=status.HTTP_200_OK
        )