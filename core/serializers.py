from rest_framework import serializers
from .models import Address, Category, Establishment, Food, Kitchen, Order, OrderItem


class FoodSerializer(serializers.ModelSerializer):

    class Meta:
        model = Food
        fields = "__all__"


class CategorySerializer(serializers.ModelSerializer):
    foods = FoodSerializer(many=True, read_only=True)

    class Meta:
        model = Category
        fields = "__all__"


class KitchenSerializer(serializers.ModelSerializer):
    categories = CategorySerializer(many=True, read_only=True)

    class Meta:
        model = Kitchen
        fields = "__all__"


class EstablishmentSerializer(serializers.ModelSerializer):
    kitchens = KitchenSerializer(many=True, read_only=True)

    class Meta:
        model = Establishment
        fields = "__all__"


class AddressSerializer(serializers.ModelSerializer):

    class Meta:
        model = Address
        fields = "__all__"




class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['id', 'food', 'quantity', 'price']
        extra_kwargs = {'price': {'required': False}}

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = ['id', 'user', 'address', 'status', 'created_at', 'total_price', 'items']
        read_only_fields = ['total_price', 'created_at', 'status']

    def create(self, validated_data):
        items_data = validated_data.pop('items')
        order = Order.objects.create(**validated_data)
        total = 0
        for item_data in items_data:
            food = item_data['food']
            quantity = item_data.get('quantity', 1)
            price = food.price * quantity
            total += price
            OrderItem.objects.create(order=order, food=food, quantity=quantity, price=food.price)
        
        order.total_price = total
        order.save()
        return order