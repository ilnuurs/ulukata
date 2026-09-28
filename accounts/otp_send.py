from datetime import timedelta
import random
from django.core.mail import send_mail
from django.utils import timezone
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import OTPcode, User
from .serializers import (
    ResetPasswordSerializer,
    SendOTPSerializer,
    VerifyOTPSerializer,
)


class SendOTPView(APIView):
    def post(self, request):
        serializer = SendOTPSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Используем 'mail', как в сериализаторе
        email = serializer.validated_data['mail']

        OTPcode.objects.filter(email=email).delete()

        code = str(random.randint(100000, 999999))

        OTPcode.objects.create(
            email=email,
            code=code,
            expire_at=timezone.now() + timedelta(minutes=5),
        )

        send_mail(
            subject='Ваш код подтверждения APARTAMENT',
            message=f'Ваш код: {code}',
            from_email='ilnurkerimov9@gmail.com',
            recipient_list=[email],
        )

        return Response({'message': 'Код отправлен'})


class VerifyOTPView(APIView):
    def post(self, request):
        serializer = VerifyOTPSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data['mail']
        code = serializer.validated_data['code']

        otp = OTPcode.objects.filter(email=email, code=code).first()

        if otp is None:
            return Response(
                {'error': 'Код не найден или неверный'},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        if otp.is_expired:
            otp.delete()
            return Response(
                {'error': 'Код истек, запросите новый'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        return Response(
            {'message': 'Код подтвержден успешно!'}, status=status.HTTP_200_OK
        )


class ResetPasswordView(APIView):
    def post(self, request):
        serializer = ResetPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data['mail']
        code = serializer.validated_data['code']
        new_password = serializer.validated_data['new_password']

        otp = OTPcode.objects.filter(email=email, code=code).first()

        if otp is None:
            return Response(
                {'error': 'Код не совпадает или его нет'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if otp.is_expired:
            otp.delete()
            return Response(
                {'error': 'Код истек, запросите новый'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response(
                {'error': 'Пользователь не найден'},
                status=status.HTTP_404_NOT_FOUND,
            )

        user.set_password(new_password)
        user.save()

        otp.delete()

        return Response(
            {'message': 'Пароль успешно изменен'}, status=status.HTTP_200_OK
        )


class RegisterView(APIView):
    def post(self, request):
        email = request.data.get('email')
        username = request.data.get('username')
        password = request.data.get('password')
        code = request.data.get('otp')

        if not all([email, username, password, code]):
            return Response(
                {'error': 'Заполните все поля'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if User.objects.filter(email=email).exists():
            return Response(
                {'error': 'Пользователь уже существует'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            otp = OTPcode.objects.get(email=email)
        except OTPcode.DoesNotExist:
            return Response(
                {'error': 'OTP не найден'}, status=status.HTTP_404_NOT_FOUND
            )

        if otp.code != code:
            return Response(
                {'error': 'Неверный код'}, status=status.HTTP_400_BAD_REQUEST
            )

        if otp.is_expired:
            otp.delete()
            return Response(
                {'error': 'Код истек'}, status=status.HTTP_400_BAD_REQUEST
            )

        user = User.objects.create_user(
            username=username, email=email, password=password
        )

        otp.delete()
        return Response(
            {
                'message': 'Регистрация успешна',
                'user_id': user.id,
            },
            status=status.HTTP_201_CREATED,
        )