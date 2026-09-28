from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import AddressViewSet,CategoryViewSet,EstablishmentViewSet,FoodViewSet,KitchenViewSet,OrderViewSet



router = DefaultRouter()
router.register("establishments", EstablishmentViewSet)
router.register("kitchens", KitchenViewSet)
router.register("categories", CategoryViewSet)
router.register("foods", FoodViewSet)
router.register("addresses", AddressViewSet)
router.register('orders', OrderViewSet)


urlpatterns = [
    path("", include(router.urls)),

]