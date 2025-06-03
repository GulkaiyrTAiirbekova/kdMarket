from django.contrib import admin

from .models import (
    Product, Category, Brand, ProductReview,Attribute,ProductAttribute
)

admin.site.register(Product)
admin.site.register(Category)
admin.site.register(Brand)
admin.site.register(ProductReview)
admin.site.register(Attribute)
admin.site.register(ProductAttribute)