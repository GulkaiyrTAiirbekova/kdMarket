from django.urls import path, include
from rest_framework.routers import DefaultRouter

from payment_app.views import PaymentView, PaymentItemView

router =DefaultRouter()
router.register(r'payment', PaymentView, basename='payment')
router.register(r'paymentItem', PaymentItemView, basename='paymentItem')


urlpatterns = router.urls