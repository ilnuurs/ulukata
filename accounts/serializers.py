from django.contrib.auth import authenticate

from .models import User
from rest_framework import serializers
from rest_framework.authtoken.models import Token
from django.contrib.auth.password_validation import validate_password


class LoginSerializers(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    
    def validate(self, attrs):
        print(attrs)
        user = authenticate(email=attrs['email'],password=attrs['password'])
        
        if not user:
            raise serializers.ValidationError('not have email or password')
        
        token, _ = Token.objects.get_or_create(user=user)
        return{'token': token.key, 'email': user.email}
    
    
class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only = True,validators=[validate_password])
    password2 = serializers.CharField(write_only = True)
    
    class Meta:
        model = User
        fields = ('email', 'phone', 'avatar', 'date_on_birth', 'password', 
                  'password2', 'first_name','last_name')
    
    def validate(self,attrs):
        if not attrs.get('password') == attrs.get('password2'):
            raise serializers.ValidationError('парол не совпадает')
        return attrs
    
    def create(self,validated_data):
        validated_data.pop('password2')
        user = User.objects.create(**validated_data)
        Token.objects.create(user=user)
        return validated_data
            
            
class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'avatar', 'phone')
        read_only_fields = ('email',)
        
        
    
class ChangePasswordSerializers(serializers.Serializer):
    old_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True, validators=[validate_password])
    
    def validate(self, attrs: dict):
        user: User = self.context['request'].user
        if not user.check_password(attrs.get('old_password')):
            raise serializers.ValidationError('старый пароль неверен')
        if attrs.get('old_password') == attrs.get('new_password'):
            raise serializers.ValidationError('новый пароль не должен совпадать со старым')
        
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