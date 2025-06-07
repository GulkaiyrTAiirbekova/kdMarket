from django.urls import path, include
from rest_framework.routers import DefaultRouter

from orders_app.views import OrderView, OrderItemView

router =DefaultRouter()
router.register(r'order', OrderView, basename='order')
router.register(r'orderItem', OrderItemView, basename='orderItem')


urlpatterns = router.urls
