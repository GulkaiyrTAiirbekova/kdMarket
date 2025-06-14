from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiParameter, OpenApiExample, OpenApiResponse
from rest_framework import viewsets
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend

from .filters import ProductAttributeFilter
from .models import Product, Category, Brand, ProductReview, Attribute, ProductAttribute
from .serializers import ProductSerializer, CategorySerializer, BrandSerializer, ProductReviewSerializer, \
    AttributeSerializer, ProductAttributeSerializer

#SWAGGER-> ProductView

@extend_schema_view(
    list=extend_schema(
        summary="Список товаров",
        description="Возвращает список всех товаров с возможностью фильтрации по категории, бренду,цене  и активности .",
        parameters=[
            OpenApiParameter(name='category', description="Фильтр по ID категории", required=False, type=int),
            OpenApiParameter(name='brand', description="Фильтр по ID бренда", required=False, type=int),
            OpenApiParameter(name='min_price', description="Минимальная цена", required=False, type=float),
            OpenApiParameter(name='max_price', description="Максимальная цена", required=False, type=float),
            OpenApiParameter(name='is_active', description='Активен ли товар', required=False, type=bool),
        ],
        responses={
            200: ProductSerializer(many=True),
            400: OpenApiExample(
                name='Ошибка фильтрации',
                value={'error': 'Некорректные параметры запроса'}
            )
        }
    ),
    retrieve=extend_schema(
        summary="Детали товара",
        description="Возвращает подробную информацию о товаре по его ID.",
        responses={
            200: ProductSerializer,
            404: OpenApiExample(
                name='Товар не найден',
                value={'error': 'Товар с данным ID не найден'}
            )
        }
    ),
    create=extend_schema(
        summary="Создание товара",
        description="Создает новый товар с переданными данными.",
        request=ProductSerializer,
        responses={
            201: ProductSerializer,
            400: OpenApiExample(
                name='Ошибка создания',
                value={'error': 'Некорректные данные'}
            )
        }
    ),
    update=extend_schema(
        summary="Обновление товара",
        description="Полное обновление информации о товаре.",
        request=ProductSerializer,
        responses={
            200: ProductSerializer,
            400: OpenApiExample(
                name='Ошибка валидации',
                value={'error': 'Неверные данные при обновлении'}
            ),
            404: OpenApiExample(
                name='Товар не найден',
                value={'error': 'Товар с данным ID не найден'}
            )
        }
    ),
    partial_update=extend_schema(
        summary="Частичное обновление товара",
        description="Частично обновляет поля товара.",
        request=ProductSerializer,
        responses={
            200: ProductSerializer,
            400: OpenApiExample(
                name='Ошибка валидации',
                value={'error': 'Некорректные данные'}
            ),
            404: OpenApiExample(
                name='Товар не найден',
                value={'error': 'Товар с данным ID не найден'}
            )
        }
    ),
    destroy=extend_schema(
        summary="Удаление товара",
        description="Удаляет товар по его ID.",
        responses={
            204: OpenApiExample(
                name='Успешное удаление',
                value={'message': 'Товар успешно удалён'}
            ),
            404: OpenApiExample(
                name='Товар не найден',
                value={'error': 'Товар с данным ID не найден'}
            )
        }
    )
)

class ProductView(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['category', 'brand','min_price','max_price', 'is_active']


# SWAGGER-> ProductReviewView
@extend_schema_view(
    list=extend_schema(
        summary="Список отзывов",
        description="Возвращает список всех отзывов на товары.Фильтрация по товару, пользователю и ",
        parameters=[
            OpenApiParameter(name='product', description='ID товара', required=False, type=int),
            OpenApiParameter(name='user', description='ID пользователя', required=False, type=int),
            OpenApiParameter(name='rating', description='Оценка отзыва', required=False, type=int),
        ],
        responses={
            200: ProductReviewSerializer(many=True),
            400: OpenApiExample(
                name='Ошибка запроса',
                value={'error': 'Некорректные параметры запроса'}
            )
        }
    ),
    retrieve=extend_schema(
        summary="Детали отзыва",
        description="Возвращает подробности об отзыве по его ID.",
        responses={
            200: ProductReviewSerializer,
            404: OpenApiExample(
                name='Отзыв не найден',
                value={'error': 'Отзыв с данным ID не найден'}
            )
        }
    ),
    create=extend_schema(
        summary="Создание отзыва",
        description="Создает отзыв на товар. Пользователь должен быть авторизован.",
        request=ProductReviewSerializer,
        responses={
            201: ProductReviewSerializer,
            400: OpenApiExample(
                name='Ошибка создания',
                value={'error': 'Ошибка в данных отзыва'}
            )
        }
    ),
    update=extend_schema(
        summary="Обновление отзыва",
        description="Полное обновление отзыва по его ID.",
        request=ProductReviewSerializer,
        responses={
            200: ProductReviewSerializer,
            400: OpenApiExample(
                name='Ошибка обновления',
                value={'error': 'Ошибка при обновлении отзыва'}
            ),
            404: OpenApiExample(
                name='Отзыв не найден',
                value={'error': 'Отзыв с данным ID не найден'}
            )
        }
    ),
    partial_update=extend_schema(
        summary="Частичное обновление отзыва",
        description="Обновляет отдельные поля отзыва.",
        request=ProductReviewSerializer,
        responses={
            200: ProductReviewSerializer,
            400: OpenApiExample(
                name='Ошибка валидации',
                value={'error': 'Некорректные данные'}
            ),
            404: OpenApiExample(
                name='Отзыв не найден',
                value={'error': 'Отзыв с данным ID не найден'}
            )
        }
    ),
    destroy=extend_schema(
        summary="Удаление отзыва",
        description="Удаляет отзыв по его ID.",
        responses={
            204: OpenApiExample(
                name='Успешное удаление',
                value={'message': 'Отзыв успешно удалён'}
            ),
            404: OpenApiExample(
                name='Отзыв не найден',
                value={'error': 'Отзыв с данным ID не найден'}
            )
        }
    )
)

class ProductReviewView(viewsets.ModelViewSet):
    queryset = ProductReview.objects.all()
    serializer_class = ProductReviewSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['product', 'user', 'rating']


#SWAGGER-> CategoryView
@extend_schema_view(
    list=extend_schema(
        summary="Список категорий",
        description="Возвращает список всех категорий товаров",
        parameters=[
            OpenApiParameter(name='parent', description='Родительская категория', required=False, type=int),
],
        responses={
            200: CategorySerializer(many=True),
            400: OpenApiExample(
                name='Ошибка запроса',
                value={'error': ' Ошибка при получении списка категорий'}
            )
        }
    ),
    retrieve=extend_schema(
        summary="Детали категории",
        description="Возвращает  информацию о конкретной категории по его ID.",
        responses={
            200: CategorySerializer,
            404: OpenApiExample(
                name='Категория не найден',
                value={'error': 'Категория с данным ID не найден'}
            )
        }
    ),
    create=extend_schema(
        summary="Создание категории",
        description="Создает новую категорию товаров.",
        request=CategorySerializer,
        responses={
            201: CategorySerializer,
            400: OpenApiExample(
                name='Ошибка валидации',
                value={'error': 'Переданы Некорректные данные'}
            )
        }
    ),
    update=extend_schema(
        summary="Обновление категории",
        description="Полное обновление информации о категории.",
        request=CategorySerializer,
        responses={
            200: CategorySerializer,
            400: OpenApiExample(
                name='Ошибка Обновления',
                value={'error': 'Некорректные  данные при обновлении'}
            ),
            404: OpenApiExample(
                name='Категория не найдена',
                value={'error': 'Категория с данным ID не найден'}
            )
        }
    ),
    partial_update=extend_schema(
        summary="Частичное обновление Категории",
        description="Частично обновляет поля Категории.",
        request=CategorySerializer,
        responses={
            200: CategorySerializer,
            400: OpenApiExample(
                name='Ошибка валидации',
                value={'error': 'Ошибка в переданных данных'}
            ),
            404: OpenApiExample(
                name='Товар не найден',
                value={'error': 'Категория с данным ID не найден'}
            )
        }
    ),
    destroy=extend_schema(
        summary="Удаление Категории",
        description="Удаляет категорию по её ID.",
        responses={
            204: OpenApiExample(
                name='Успешное удаление',
                value={'message': 'Категория успешно удалёна'}
            ),
            404: OpenApiExample(
                name='Категория не найдена',
                value={'error': 'Категория с данным ID не найдена'}
            )
        }
    )
)

class CategoryView(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = [DjangoFilterBackend]

#SWAGGER-> BrandView
@extend_schema_view(
    list=extend_schema(
        summary="Список брендов",
        description="Возвращает список всех брендов.",
        responses={
            200: BrandSerializer(many=True),
            400: OpenApiExample(
                name='Ошибка запроса',
                value={'error': ' Ошибка при получении списка брендов'}
            )
        }
    ),
    retrieve=extend_schema(
        summary="Детали бренда",
        description="Возвращает информацию о конкретном бренде по ID.",
        responses={
            200: BrandSerializer,
            404: OpenApiExample(
                name='Бренд  не найден',
                value={'error': 'Бренд  с данным ID не найден'}
            )
        }
    ),
    create=extend_schema(
        summary="Создание Бренда",
        description="Создает новый бренд товаров.",
        request=BrandSerializer,
        responses={
            201: BrandSerializer,
            400: OpenApiExample(
                name='Ошибка валидации',
                value={'error': 'Переданы Некорректные данные'}
            )
        }
    ),
    update=extend_schema(
        summary="Обновление бренда",
        description="Полное обновление информации о бренде.",
        request=BrandSerializer,
        responses={
            200: BrandSerializer,
            400: OpenApiExample(
                name='Ошибка Обновления',
                value={'error': 'Некорректные  данные при обновлении'}
            ),
            404: OpenApiExample(
                name='Бренд  не найдена',
                value={'error': 'Бренд  с данным ID не найден'}
            )
        }
    ),
    partial_update=extend_schema(
        summary="Частичное обновление бренда ",
        description="Частично обновляет поля бренда.",
        request=BrandSerializer,
        responses={
            200: BrandSerializer,
            400: OpenApiExample(
                name='Ошибка валидации',
                value={'error': 'Ошибка в переданных данных'}
            ),
            404: OpenApiExample(
                name='Бренд  не найден',
                value={'error': 'Бренд  с данным ID не найден'}
            )
        }
    ),
    destroy=extend_schema(
        summary="Удаление бренда",
        description="Удаляет бренд по её ID.",
        responses={
            204: OpenApiExample(
                name='Успешное удаление',
                value={'message': 'Бренд успешно удалён'}
            ),
            404: OpenApiExample(
                name='Бренд  не найдена',
                value={'error': 'Бренд  с данным ID не найдена'}
            )
        }
    )
)

class BrandView(viewsets.ModelViewSet):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer




# SWAGGER-> AttributeView
@extend_schema_view(
    list=extend_schema(
        summary="Список атрибутов",
        description="Возвращает список всех атрибутов товаров.",
        responses={
            200: AttributeSerializer(many=True),
            400: OpenApiExample(
                name="Ошибка запроса",
                value={"error": "Некорректные параметры запроса"}
            ),
        },
    ),
    retrieve=extend_schema(
        summary="Детали атрибута",
        description="Возвращает данные конкретного атрибута по его ID.",
        responses={
            200: AttributeSerializer,
            404: OpenApiExample(
                name="Атрибут не найден",
                value={"error": "Атрибут с данным ID не найден"},
            ),
        },
    ),
    create=extend_schema(
        summary="Создание атрибута",
        description="Создает новый атрибут для товаров.",
        request=AttributeSerializer,
        responses={
            201: AttributeSerializer,
            400: OpenApiExample(
                name="Ошибка валидации",
                value={"error": "Некорректные данные для создания атрибута"},
            ),
        },
    ),
    update=extend_schema(
        summary="Обновление атрибута",
        description="Полное обновление атрибута по ID.",
        request=AttributeSerializer,
        responses={
            200: AttributeSerializer,
            400: OpenApiExample(
                name="Ошибка обновления",
                value={"error": "Некорректные данные при обновлении"},
            ),
            404: OpenApiExample(
                name="Атрибут не найден",
                value={"error": "Атрибут с данным ID не найден"},
            ),
        },
    ),
    partial_update=extend_schema(
        summary="Частичное обновление атрибута",
        description="Обновляет отдельные поля атрибута по ID.",
        request=AttributeSerializer,
        responses={
            200: AttributeSerializer,
            400: OpenApiExample(
                name="Ошибка валидации",
                value={"error": "Некорректные данные при частичном обновлении"},
            ),
            404: OpenApiExample(
                name="Атрибут не найден",
                value={"error": "Атрибут с данным ID не найден"},
            ),
        },
    ),
    destroy=extend_schema(
        summary="Удаление атрибута",
        description="Удаляет атрибут по его ID.",
        responses={
            204: OpenApiExample(
                name="Успешное удаление",
                value={"message": "Атрибут успешно удалён"},
            ),
            404: OpenApiExample(
                name="Атрибут не найден",
                value={"error": "Атрибут с данным ID не найден"},
            ),
        },
    ),
)
class AttributeView(viewsets.ModelViewSet):
    queryset = Attribute.objects.all()
    serializer_class = AttributeSerializer


# SWAGGER-> ProductAttributeView
@extend_schema_view(
    list=extend_schema(
        summary="Список атрибутов",
        description="Возвращает список всех атрибутов товаров. Возможна Фильтрация по продукту, атрибуту, имени продукта и пустому значению",
        parameters=[
            OpenApiParameter(name='product', description='ID товара', required=False, type=int),
            OpenApiParameter(name='attribute', description='ID атрибута', required=False, type=int),
            OpenApiParameter(name='product_name', description='Название товара (поиск)', required=False, type=str),
            OpenApiParameter(name='is_value_empty', description='Пустое значение', required=False, type=bool),
        ],
        responses={
            200: AttributeSerializer(many=True),
            400: OpenApiResponse(
                description="Ошибка запроса",
                examples=[
                    OpenApiExample(
                        name="Ошибка запроса",
                        value={"error": "Некорректные параметры запроса"}
                    )
                ]
            ),
        },
    ),
    retrieve=extend_schema(
        summary="Детали связи продукт-атрибут",
        description="Возвращает конкретную связь между продуктом и атрибутом по ID.",
        responses={
            200: ProductAttributeSerializer,
            404: OpenApiResponse(
                description="Связь не найдена",
                examples=[
                    OpenApiExample(
                        name="Связь не найдена",
                        value={"error": "Связь продукт-атрибут с данным ID не найдена"}
                    )
                ]
            ),
        }
    ),
    create=extend_schema(
        summary="Создание связи продукт-атрибут",
        description="Создает новую связь между продуктом и его атрибутом.",
        request=ProductAttributeSerializer,
        responses={
            201: ProductAttributeSerializer,
            400: OpenApiResponse(
                description="Ошибка создания",
                examples=[
                    OpenApiExample(
                        name="Ошибка создания",
                        value={"error": "Ошибка в данных связи"}
                    )
                ]
            ),
        }
    ),
    update=extend_schema(
        summary="Обновление связи продукт-атрибут",
        description="Полное обновление существующей связи между продуктом и атрибутом.",
        request=ProductAttributeSerializer,
        responses={
            200: ProductAttributeSerializer,
            400: OpenApiResponse(
                description="Ошибка обновления",
                examples=[
                    OpenApiExample(
                        name="Ошибка обновления",
                        value={"error": "Ошибка при обновлении связи"}
                    )
                ]
            ),
            404: OpenApiResponse(
                description="Связь не найдена",
                examples=[
                    OpenApiExample(
                        name="Связь не найдена",
                        value={"error": "Связь с данным ID не найдена"}
                    )
                ]
            ),
        }
    ),
    partial_update=extend_schema(
        summary="Частичное обновление связи продукт-атрибут",
        description="Обновляет только указанные поля связи между продуктом и атрибутом.",
        request=ProductAttributeSerializer,
        responses={
            200: ProductAttributeSerializer,
            400: OpenApiResponse(
                description="Ошибка валидации",
                examples=[
                    OpenApiExample(
                        name="Ошибка валидации",
                        value={"error": "Некорректные данные"}
                    )
                ]
            ),
            404: OpenApiResponse(
                description="Связь не найдена",
                examples=[
                    OpenApiExample(
                        name="Связь не найдена",
                        value={"error": "Связь с данным ID не найдена"}
                    )
                ]
            ),
        }
    ),
    destroy=extend_schema(
        summary="Удаление связи продукт-атрибут",
        description="Удаляет связь между продуктом и атрибутом по ID.",
        responses={
            204: OpenApiResponse(
                description="Успешное удаление",
                examples=[
                    OpenApiExample(
                        name="Успешное удаление",
                        value={"message": "Связь успешно удалена"}
                    )
                ]
            ),
            404: OpenApiResponse(
                description="Связь не найдена",
                examples=[
                    OpenApiExample(
                        name="Связь не найдена",
                        value={"error": "Связь с данным ID не найдена"}
                    )
                ]
            ),
        }
    )
)
class ProductAttributeView(viewsets.ModelViewSet):
    queryset = ProductAttribute.objects.all()
    serializer_class = ProductAttributeSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = ProductAttributeFilter