from django.shortcuts import render
from drf_spectacular.utils import OpenApiResponse, OpenApiExample, extend_schema, OpenApiParameter, extend_schema_view
from rest_framework import viewsets

from carts_app.models import Cart, Favourites
from carts_app.serializers import CartSerializer, FavouritesSerializer

#SWAGGER-> CartView

@extend_schema_view(
    list=extend_schema(
        summary='Список корзин',
        description='Получение списка корзин с фильтрацией по ID, пользователю и активности.',
        parameters=[
            OpenApiParameter(name='id', description='Фильтрация по ID корзины', required=False, type=int),
            OpenApiParameter(name='user', description='Фильтрация по ID пользователя', required=False, type=int),
            #OpenApiParameter(name='is_active', description='Фильтрация по активности корзины', required=False, type=bool),
        ],
        responses={200: CartSerializer}
    ),
    retrieve=extend_schema(
        summary='Детали корзины',
        description='Получение информации о конкретной корзине по её ID.',
        responses={
            200: CartSerializer,
            404: OpenApiResponse(description='Корзина не найдена', examples=[
                OpenApiExample(
                    'Ошибка',
                    value={'error': 'Корзина с данным ID не найдена'}
                )
            ])
        }
    ),
    create=extend_schema(
        summary='Создание корзины',
        description='Создание новой корзины для пользователя.',
        request=CartSerializer,
        responses={
            201: CartSerializer,
            400: OpenApiResponse(description='Ошибка валидации', examples=[
                OpenApiExample('Ошибка', value={'error': 'Некорректные данные'})
            ])
        }
    ),
    update=extend_schema(
        summary='Обновление корзины',
        description='Полное обновление корзины по ID.',
        request=CartSerializer,
        responses={
            200: CartSerializer,
            400: OpenApiResponse(description='Ошибка обновления')
        }
    ),
    partial_update=extend_schema(
        summary='Частичное обновление корзины',
        description='Изменение отдельных полей корзины (например, активности).',
        request=CartSerializer,
        responses={200: CartSerializer}
    ),
    destroy=extend_schema(
        summary='Удаление корзины',
        description='Удаление корзины по ID.',
        responses={
            204: OpenApiResponse(description='Успешное удаление'),
            404: OpenApiResponse(description='Корзина не найдена', examples=[
                OpenApiExample('Ошибка', value={'error': 'Корзина не найдена'})
            ])
        }
    )
)
class CartView(viewsets.ModelViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    filterset_fields = ['id', 'user']

#SWAGGER->FavouritesView

@extend_schema_view(
    list=extend_schema(
        summary='Список избранного',
        description='Возвращает список всех избранных товаров. Можно фильтровать по ID, пользователю и товару.',
        parameters=[
            OpenApiParameter(name='id', description='Фильтрация по ID избранного', required=False, type=int),
            OpenApiParameter(name='user', description='Фильтрация по ID пользователя', required=False, type=int),
            OpenApiParameter(name='product', description='Фильтрация по ID товара', required=False, type=int),
        ],
        responses={200: FavouritesSerializer}
    ),
    retrieve=extend_schema(
        summary='Детали избранного',
        description='Возвращает конкретную запись избранного по ID.',
        responses={
            200: FavouritesSerializer,
            404: OpenApiResponse(description='Избранное не найдено', examples=[
                OpenApiExample('Ошибка', value={'error': 'Запись избранного не найдена'})
            ])
        }
    ),
    create=extend_schema(
        summary='Добавить в избранное',
        description='Создает новую запись в избранном (связывает товар и пользователя).',
        request=FavouritesSerializer,
        responses={
            201: FavouritesSerializer,
            400: OpenApiResponse(description='Ошибка валидации', examples=[
                OpenApiExample('Ошибка', value={'error': 'Некорректные данные'})
            ])
        }
    ),
    update=extend_schema(
        summary='Обновить избранное',
        description='Полное обновление записи избранного по ID.',
        request=FavouritesSerializer,
        responses={200: FavouritesSerializer}
    ),
    partial_update=extend_schema(
        summary='Частичное обновление избранного',
        description='Частично обновляет запись в избранном.',
        request=FavouritesSerializer,
        responses={200: FavouritesSerializer}
    ),
    destroy=extend_schema(
        summary='Удалить из избранного',
        description='Удаляет запись из избранного по ID.',
        responses={
            204: OpenApiResponse(description='Успешное удаление'),
            404: OpenApiResponse(description='Запись не найдена', examples=[
                OpenApiExample('Ошибка', value={'error': 'Запись избранного с таким ID не найдена'})
            ])
        }
    )
)
class FavouritesView(viewsets.ModelViewSet):
    queryset = Favourites.objects.all()
    serializer_class = FavouritesSerializer
    filterset_fields = ['id', 'user', 'product']

