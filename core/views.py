import random
from django.core.mail import send_mail
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Order
from .serializers import OrderSerializer
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from .models import Address, Category, Establishment, Food, Kitchen, Order
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import AddressSerializer,CategorySerializer,EstablishmentSerializer,FoodSerializer,KitchenSerializer,OrderItemSerializer,OrderSerializer



class EstablishmentViewSet(viewsets.ModelViewSet):
    queryset = Establishment.objects.all()
    serializer_class = EstablishmentSerializer

class KitchenViewSet(viewsets.ModelViewSet):
    queryset = Kitchen.objects.all()
    serializer_class = KitchenSerializer

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class FoodViewSet(viewsets.ModelViewSet):
    queryset = Food.objects.all()
    serializer_class = FoodSerializer


class AddressViewSet(viewsets.ModelViewSet):
    queryset = Address.objects.all()
    serializer_class = AddressSerializer




class OrderViewSet(viewsets.ModelViewSet):
  queryset = Order.objects.all()
  serializer_class = OrderSerializer
  permission_classes = [IsAuthenticated]  

  def get_queryset(self):
    user = self.request.user

    if user.is_staff or user.is_superuser:
      return Order.objects.all()
    
    return Order.objects.filter(user=user)

  @action(detail=True, methods=['post'], permission_classes=[IsAdminUser])
  def change_status(self, request, pk=None):
    order = self.get_object()
    new_status = request.data.get('status')
    valid_statuses = [choice[0] for choice in Order.STATUS_CHOICES]

    if new_status not in valid_statuses:
      return Response(
          {
              'error': (
                  f'Неверный статус. Доступные статусы: {valid_statuses}'
              )
          },
          status=status.HTTP_400_BAD_REQUEST,
      )

    order.status = new_status
    order.save()

    return Response(
        {
            'message': f'Статус заказа №{order.id} успешно изменен',
            'status': order.status,
        },
        status=status.HTTP_200_OK,
    )

def send_email_code(email, code):
    send_mail(subject="Код подтверждения для авторизации",message=f"Ваш код подтверждения: {code}",from_email=None,recipient_list=[email],fail_silently=False,)
    return True


# class RequestCodeView(APIView):
#     def get(self, request):
#         return Response({"info": "Отправьте POST-запрос с полями: name, email, birth_year"})

#     def post(self, request):
#         name = request.data.get("name")
#         email = request.data.get("email")
#         birth_year = request.data.get("birth_year")

#         if not email or not name:
#             return Response({"error": "Имя и email обязательны"},status=status.HTTP_400_BAD_REQUEST,)

#         code = str(random.randint(1000, 9999))

#         user, created = User.objects.get_or_create(email=email, defaults={"name": name, "birth_year": birth_year})

#         if not created:
#             user.name = name
#             if birth_year:
#                 user.birth_year = birth_year

#         user.otp_code = code
#         user.save()

#         try:
#             send_email_code(email, code)
#         except Exception as e:
#             return Response({"error": f"Ошибка отправки письма: {str(e)}"},status=status.HTTP_500_INTERNAL_SERVER_ERROR,)

#         return Response({"message": "Код подтверждения отправлен на ваш email", "email": email},status=status.HTTP_200_OK,)


# class VerifyCodeView(APIView):
#     def get(self, request):
#         return Response({"info": "Отправьте POST-запрос с полями: email, code"})

#     def post(self, request):
#         email = request.data.get("email")
#         code = request.data.get("code")

#         if not email or not code:
#             return Response({"error": "Email и код обязательны"}, status=status.HTTP_400_BAD_REQUEST)

#         try:
#             user = User.objects.get(email=email)
#         except User.DoesNotExist:
#             return Response({"error": "Пользователь не найден"}, status=status.HTTP_404_NOT_FOUND)

#         if user.otp_code == code:
#             user.otp_code = None
#             user.save()

          
#             refresh = RefreshToken.for_user(user)

#             return Response(
#                 {
#                     "message": "Успешная авторизация",
#                     "user_id": user.id,
#                     "name": user.name,
#                     "access": str(refresh.access_token), 
#                     "refresh": str(refresh),             
#                 },
#                 status=status.HTTP_200_OK,
#             )

#         return Response({"error": "Неверный код подтверждения"}, status=status.HTTP_400_BAD_REQUEST)
    
    
    
