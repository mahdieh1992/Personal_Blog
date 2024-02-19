from rest_framework import serializers
from ...models import CustomUser
from django.core.exceptions import ValidationError
from django.contrib.auth import password_validation as passvalidate
from django.contrib.auth import authenticate
from django.shortcuts import get_object_or_404


class RegisterSerializer(serializers.Serializer):
    """
        serializer for register user 
    """
    email=serializers.CharField()
    password=serializers.CharField(style={'input_type':'password'})
    ConfirmPassword=serializers.CharField(style={'input_type':'password'})


    def validate(self, data):
        """
            Validate for :
                 Match password and confirmPassword,
                 Complex password,
                 The email has not been registered before.
        """
        password=data.get('password')
        ConfirmPassword=data.get('ConfirmPassword')
        email=data.get('email')
        if password != ConfirmPassword:
            raise ValidationError('Password and ConfirmPassword is not match',code='password_is_not_match')
        if CustomUser.objects.filter(email=email).exists():
            raise ValidationError({'user':'Email already exists'},code='user exists')
        try:
            passvalidate.validate_password(password=password)
        except ValidationError as err:  
            raise ValidationError({'detail':tuple(err.messages)},code='not_complex_password')
        return data
    
    def create(self, validated_data):
        try:
            user=CustomUser.objects.create(email=validated_data['email'])
            user.set_password(validated_data['password'])
            user.save()
            return user
        except ValidationError as err:
            raise ({'detail':err.message})

class ResendVerifyEmailSerializer(serializers.Serializer):
    email=serializers.CharField()

    def validate(self, data):
        """
            checking email has been exist and not expired
        """
        email=data.get('email')
        user=get_object_or_404(CustomUser,email=email)  
        if not user.is_confirm:
            data['user']=user   
            return data
        raise ValidationError('Dear user: you verified already',code='user_verified')
