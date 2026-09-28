from django.contrib import admin
from .models import Establishment, Kitchen, Category, Food, Address, Order
from accounts.models import User

admin.site.register(Establishment)
admin.site.register(Kitchen)
admin.site.register(Category)
admin.site.register(Food)
admin.site.register(User)
admin.site.register(Address)
admin.site.register(Order)