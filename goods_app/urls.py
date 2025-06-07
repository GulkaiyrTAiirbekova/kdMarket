from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProductView, CategoryView, BrandView, ProductReviewView, AttributeView, ProductAttributeView

router =DefaultRouter()
router.register(r'products', ProductView, basename='products')
router.register(r'category',CategoryView,basename='category')
router.register(r'brand',BrandView,basename='brand')
router.register(r'productReview',ProductReviewView,basename='productReview')
router.register(r'attribute',AttributeView,basename='attribute')
router.register(r'productAttribute',ProductAttributeView,basename='productAttribute')


urlpatterns = router.urls


