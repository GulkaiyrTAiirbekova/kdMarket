from rest_framework import viewsets
from rest_framework.response import Response

from .models import Product, Category, Brand, ProductReview, Attribute, ProductAttribute
from .serializers import ProductSerializer, CategorySerializer, BrandSerializer, ProductReviewSerializer, \
    AttributeSerializer, ProductAttributeSerializer





class ProductView(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class CategoryView(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class BrandView(viewsets.ModelViewSet):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer

class ProductReviewView(viewsets.ModelViewSet):
    queryset = ProductReview.objects.all()
    serializer_class = ProductReviewSerializer


class AttributeView(viewsets.ModelViewSet):
    queryset = Attribute.objects.all()
    serializer_class = AttributeSerializer

class ProductAttributeView(viewsets.ModelViewSet):
    queryset = ProductAttribute.objects.all()
    serializer_class = ProductAttributeSerializer













    # def create(self, request, *args, **kwargs):
    #     name = Product.objects.get(name=request.name)
    #     if len(name) > 20:
    #         return Response("error")
