
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny,IsAuthenticated
from rest_framework.authtoken.models import Token
from rest_framework import status
from rest_framework.request import Request

from .serializers import LoginSerializers,RegisterSerializer, ProfileSerializer,ChangePasswordSerializers




@api_view(['POST'])
@permission_classes([AllowAny])
def custom_login(request):
    serialiser = LoginSerializers(data=request.data)
    serialiser.is_valid(raise_exception=True)
    
    return Response(serialiser.validated_data)



@api_view(['POST'])
def custom_register(request):
    serializer = RegisterSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data, status=status.HTTP_201_CREATED)

@api_view(['GET','PUT', 'PATCH'])
@permission_classes([IsAuthenticated])
def profile(request):
    user = request.user
    if request.method == 'GET':
        serializer = ProfileSerializer(user)
        return Response(serializer.data)
    
    if request.method in ('PUT','PATCH'):
        serializer = ProfileSerializer(user,request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    
    
@api_view(['POST'])
@permission_classes([IsAuthenticated],)
def Change_password(request: Request):
    serializer = ChangePasswordSerializers(data=request.data, context={'request':request})
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response({'detail':'password chanded succerfuly'})



@api_view(["POST"])
@permission_classes([IsAuthenticated])
def logout(request:Request):
    user = request.user
    Token.objects.filter(user=user).delete()
    return Response({
        'detail': 'Вы успешно вышли из системы'},
        status=status.HTTP_200_OK)
    
    
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def deactivate(request):
    user = request.user
    user.is_active = False
    user.save()

    return Response({"detail": "Аккаунт успешно деактивирован."},status=status.HTTP_200_OK)