from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.authtoken.models import Token
from .models import User


class LoginSerializers(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    
    def validate(self, attrs):
        user = authenticate(email=attrs['email'], password=attrs['password'])
        if not user:
            raise serializers.ValidationError('Неверный email или пароль')
        
        token, _ = Token.objects.get_or_create(user=user)
        return {'token': token.key, 'email': user.email}


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        fields = ('email', 'phone', 'avatar', 'date_of_birth', 'password', 'password2', 'first_name', 'last_name')
    
    def validate(self, attrs):
        if attrs.get('password') != attrs.get('password2'):
            raise serializers.ValidationError('Пароли не совпадают')
        return attrs
    
    def create(self, validated_data):
        validated_data.pop('password2')
        password = validated_data.pop('password')
        user = User.objects.create_user(password=password, **validated_data)
        Token.objects.create(user=user)
        return user


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'avatar', 'phone', 'date_of_birth', 'gender')
        read_only_fields = ('email',)


class ChangePasswordSerializers(serializers.Serializer):
    old_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True, validators=[validate_password])
    
    def validate(self, attrs: dict):
        user: User = self.context['request'].user
        if not user.check_password(attrs.get('old_password')):
            raise serializers.ValidationError('Старый пароль неверен')
        if attrs.get('old_password') == attrs.get('new_password'):
            raise serializers.ValidationError('Новый пароль не должен совпадать со старым')
        return attrs
    
    def save(self, **kwargs):
        user: User = self.context['request'].user
        user.set_password(self.validated_data['new_password'])
        user.save()
        return user


class SendOTPSerializer(serializers.Serializer):
    mail = serializers.EmailField()


class VerifyOTPSerializer(serializers.Serializer):
    mail = serializers.EmailField()
    code = serializers.CharField(min_length=6, max_length=6)


class ResetPasswordSerializer(serializers.Serializer):
    mail = serializers.EmailField()
    code = serializers.CharField(min_length=6, max_length=6)
    new_password = serializers.CharField(min_length=8)