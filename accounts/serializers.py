from rest_framework import serializers
from .models import CustomUser
from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError as DjangoValidationError
from django.db import transaction
from profiles.models import ProfessionalProfile


# Reusable password validation for registration and password reset
def validate_password_rules(password, user):
    if not any(char.isdigit() for char in password):
        raise serializers.ValidationError(
            "Password must contain at least one digit"
        )
    if not any(char.isupper() for char in password):
        raise serializers.ValidationError(
            "Password must contain at least one uppercase letter"
        )
    if not any(char.islower() for char in password):
        raise serializers.ValidationError(
            "Password must contain at least one lowercase letter"
        )
    if not any(char in '!@#$%^&*()_+-=[]{}|;:,.<>?/' for char in password):
        raise serializers.ValidationError(
            "Password must contain at least one special character"
        )
# Apply Django's built-in password validators
    try:
        validate_password(password, user=user)
    except DjangoValidationError as e:
        raise serializers.ValidationError(e.messages)

    return password     



class RegisterSerializer(serializers.ModelSerializer):
    password2=serializers.CharField(style={'input_type':'password'},write_only=True)
    class Meta:
        model= CustomUser
        fields=['email','password','password2','role']
        extra_kwargs={
            'password': {"write_only":True}
        }

    #field-level validation
    # Check email uniqueness before creating the user
    def validate_email(self,value):
        value=value.lower()
        if CustomUser.objects.filter(email__iexact=value).exists():
            raise serializers.ValidationError("Email already exists")
        # if(not value.endswith('@gmail.com')):
        #     raise serializers.ValidationError("Email must be a Gmail address")
        return value

    
    #object-level validation
    # Validate password confirmation and password strength
    def validate(self, attrs):
        password=attrs.get('password')
        password2=attrs.get('password2')
        email=attrs.get('email').lower()
        if password != password2:
            raise serializers.ValidationError("Password and Confirm Password doesn't match")

        #check passwrd confirmation
        # Temporary user is needed for Django's password validators
        user=CustomUser(email=email)
        validate_password_rules(password,user=user)
        return attrs

    
    
    # Create the actual user after all validation passes

    def create(self, validated_data):
        validated_data.pop('password2')
        return CustomUser.objects.create_user(**validated_data)
       
    
    # @transaction.atomic
    # def create(self, validated_data):
    #     validated_data.pop('password2')
    #     user=CustomUser.objects.create_user(**validated_data)
    #     if user.role=='professional':
    #         ProfessionalProfile.objects.create(user=user)

    #     return user



class LoginSerializer(serializers.Serializer):
    email=serializers.EmailField()
    password=serializers.CharField(write_only=True)

    #object-level validation
    # Validate credentials and email verification status
    def validate(self,attrs):
        email=attrs.get('email').lower()
        password=attrs.get('password')
    #authenticate is a function that takes email and password and returns user object if valid else None
        user=authenticate(username=email,password=password)

        if user is None:
            raise serializers.ValidationError("Invalid email or password")

        if not user.is_verified:
            raise serializers.ValidationError(
                "Please verify your email before logging in."
            )
        
        attrs['user']=user
        return attrs 
    #validated data will be passed to the view as serializer.validated_data

class ResendVerificationSerializer(serializers.Serializer):
    email=serializers.EmailField()

    def validate_email(self, value):
        return value.lower()

class ForgotPasswordSerializer(serializers.Serializer):
    email=serializers.EmailField()

    def validate_email(self, value):
        return value.lower()

class ResetPasswordSerializer(serializers.Serializer):

    new_password=serializers.CharField(write_only=True)
    def validate_new_password(self, value):
        # User is passed from the view through serializer context
        user=self.context.get("user")
        validate_password_rules(value,user=user)
        return value
         
