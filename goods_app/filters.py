import django_filters
from goods_app.models import ProductAttribute

class ProductAttributeFilter(django_filters.FilterSet):
    product = django_filters.NumberFilter(field_name='product__id')
    attribute = django_filters.NumberFilter(field_name='attribute__id')
    product_name = django_filters.CharFilter(field_name='product__name', lookup_expr='icontains')
    is_value_empty = django_filters.BooleanFilter(method='filter_is_value_empty')

    class Meta:
        model = ProductAttribute
        fields = ['product', 'attribute', 'product_name']

    def filter_is_value_empty(self, queryset, name, value):
        if value:
            return queryset.filter(value__isnull=True)
        return queryset.exclude(value__isnull=True)
