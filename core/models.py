from django.core.validators import MinValueValidator
from django.db import models
from django_resized import ResizedImageField


class Establishment(models.Model):
    name = models.CharField(max_length=255, verbose_name="Название заведения")
    description = models.TextField(max_length=500, verbose_name='описание')
    image = ResizedImageField(upload_to='establishments/')
    delivery_time = models.PositiveIntegerField(verbose_name='Время доставки (мин)') 
    delivery_price_from = models.IntegerField(verbose_name='цена от:')
    address = models.CharField(max_length=200, verbose_name="адрес")

    def __str__(self):
        return self.name
    
    


class Kitchen(models.Model):
    establishment = models.ForeignKey(Establishment, on_delete=models.CASCADE, related_name="kitchens", verbose_name="Заведение")
    name = models.CharField(max_length=255, verbose_name="Название кухни")
    
    def __str__(self):
        return f"{self.name} ({self.establishment.name})"


class Category(models.Model):
    kitchen = models.ForeignKey(Kitchen, on_delete=models.CASCADE, related_name="categories", verbose_name="Кухня")
    name = models.CharField(max_length=255, verbose_name="Название категории")

    def __str__(self):
        return f"{self.name} -> {self.kitchen.name}"


class Food(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="foods", verbose_name="Категория")
    name = models.CharField(max_length=255, verbose_name="Название блюда")
    price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)], verbose_name="Цена")
    description = models.TextField(blank=True, null=True, verbose_name="Описание")
    minutes = models.PositiveIntegerField(verbose_name='время готовки (мин)') # Recommended change
    image = ResizedImageField(upload_to='foods/', verbose_name='фотка')

    def __str__(self):
        return f"{self.name} — {self.price} сом"


class Address(models.Model):  
    user = models.ForeignKey('accounts.User', on_delete=models.CASCADE, related_name="addresses", verbose_name="Пользователь")
    name = models.CharField(max_length=100, verbose_name='название') # Added max_length
    address = models.CharField(max_length=500, verbose_name="адрес")
    is_default = models.BooleanField(default=False, verbose_name='адрес по умолчанию')

    def __str__(self):
        return f"{self.user.email}: {self.address}"


class Order(models.Model):
    STATUS_CHOICES = (
        ('pending', 'В обработке'),
        ('cooking', 'Готовится'),
        ('delivering', 'Доставляется'),
        ('completed', 'Завершен'),
        ('cancelled', 'Отменен'),
    )
    
    user = models.ForeignKey('accounts.User', on_delete=models.CASCADE, related_name='orders', verbose_name='Пользователь') # Fixed lowercase user
    address = models.ForeignKey(Address, on_delete=models.SET_NULL, null=True, verbose_name='Адрес доставки')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name='Статус заказа')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name='Общая сумма')

    def __str__(self):
        return f"Заказ №{self.id} — {self.user.name}" # Fixed extra parenthesis


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items', verbose_name='Заказ')
    food = models.ForeignKey(Food, on_delete=models.CASCADE, verbose_name='Блюдо')
    quantity = models.PositiveIntegerField(default=1, verbose_name='Количество')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена на момент заказа')

    def __str__(self):
        return f"{self.food.name} x {self.quantity}"