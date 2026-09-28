from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from .serializers import LoginSerializers,RegisterSerializer


class LoginView(GenericAPIView):
    serializer_class = LoginSerializers
    permission_classes = [AllowAny]
    
    def post(self,request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.validated_data)
    
    
    
class CustomRegister(GenericAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]
    
    def register(self,request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.validated.data) 