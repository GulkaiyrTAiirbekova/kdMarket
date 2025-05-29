from django.urls import path, include
from rest_framework.routers import DefaultRouter

from carts_app.views import CartView, FavouritesView

router =DefaultRouter()
router.register(r'cart', CartView, basename='cart')
router.register(r'favourites', FavouritesView, basename='favourites')

urlpatterns = router

