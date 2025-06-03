from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views


router =DefaultRouter()
router.register(r'sign', views.UserView, basename='sign')
router.register(r'verify', views.SMSVerificationView, basename='verify')


urlpatterns = router