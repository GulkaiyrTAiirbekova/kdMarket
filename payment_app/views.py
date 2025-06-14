from django.shortcuts import render
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiResponse, OpenApiExample, extend_schema, extend_schema_view, OpenApiParameter
from rest_framework import viewsets
from payment_app.models import Payment, PaymentItem
from payment_app.serializers import PaymentSerializer, PaymentItemSerializer

#SWAGGER-PaymentView
@extend_schema_view(
    list=extend_schema(
        summary='Список платежей',
        description='Возвращает список всех платежей. Можно фильтровать по id, user, status.',
        parameters=[
            OpenApiParameter(name='id', description='Фильтр по ID платежа', required=False, type=OpenApiTypes.INT),
            OpenApiParameter(name='user', description='Фильтр по ID пользователя', required=False, type=OpenApiTypes.INT),
            OpenApiParameter(name='status', description='Фильтр по статусу (например: paid, failed)', required=False, type=OpenApiTypes.STR),
        ],
        responses={
            200: PaymentSerializer,
            400: OpenApiResponse(description='Ошибка запроса', examples=[
                OpenApiExample('Ошибка', value={'error': 'Неверные параметры фильтрации'})
            ]),
        }
    ),
    retrieve=extend_schema(
        summary='Детали платежа',
        description='Получение информации о конкретном платеже по ID.',
        responses={
            200: PaymentSerializer,
            404: OpenApiResponse(description='Платеж не найден', examples=[
                OpenApiExample('Не найдено', value={'error': 'Платеж с таким ID не найден'})
            ]),
        }
    ),
    create=extend_schema(
        summary='Создание платежа',
        description='Создает новый платеж на основе предоставленных данных.',
        responses={
            201: PaymentSerializer,
            400: OpenApiResponse(description='Ошибка валидации', examples=[
                OpenApiExample('Ошибка', value={'error': 'Неверные данные при создании'})
            ]),
        }
    ),
    update=extend_schema(
        summary='Обновление платежа',
        description='Полное обновление информации о платеже.',
        request=PaymentSerializer,
        responses={
            200: PaymentSerializer,
            400: OpenApiResponse(description='Ошибка валидации', examples=[
                OpenApiExample('Ошибка', value={'error': 'Некорректные данные'})
            ]),
        }
    ),
    partial_update=extend_schema(
        summary='Частичное обновление платежа',
        description='Частично обновляет информацию о платеже.',
        request=PaymentSerializer,
        responses={
            200: PaymentSerializer,
            400: OpenApiResponse(description='Ошибка', examples=[
                OpenApiExample('Ошибка', value={'error': 'Некорректные данные'})
            ]),
        }
    ),
    destroy=extend_schema(
        summary='Удаление платежа',
        description='Удаляет запись о платеже по ID.',
        responses={
            204: OpenApiResponse(description='Успешное удаление', examples=[
                OpenApiExample('Удалено', value={'message': 'Платеж успешно удалён'})
            ]),
            404: OpenApiResponse(description='Не найдено', examples=[
                OpenApiExample('Не найдено', value={'error': 'Платеж не найден'})
            ]),
        }
    )
)
class PaymentView(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    filterset_fields = ['id', 'user', 'status']


#SWAGGER-PaymentItemView

@extend_schema_view(
    list=extend_schema(
        summary='Список элементов платежа',
        description='Возвращает список всех связанных позиций оплаты (товаров, услуг и т.д.). Возможна фильтрация по платежу, товару, сумме.',
        parameters=[
            OpenApiParameter(name='id', description='ID элемента платежа', required=False, type=OpenApiTypes.INT),
            OpenApiParameter(name='payment', description='Фильтр по ID платежа', required=False, type=OpenApiTypes.INT),
            OpenApiParameter(name='product', description='Фильтр по ID товара или услуги', required=False, type=OpenApiTypes.INT),
            OpenApiParameter(name='amount', description='Фильтр по сумме', required=False, type=OpenApiTypes.NUMBER),
        ],
        responses={
            200: PaymentItemSerializer,
            400: OpenApiResponse(description='Ошибка запроса', examples=[
                OpenApiExample('Ошибка', value={'error': 'Некорректные параметры фильтрации'})
            ]),
        }
    ),
    retrieve=extend_schema(
        summary='Детали элемента платежа',
        description='Получает подробности об одном элементе платежа по ID.',
        responses={
            200: PaymentItemSerializer,
            404: OpenApiResponse(description='Не найдено', examples=[
                OpenApiExample('Не найдено', value={'error': 'Элемент платежа с таким ID не найден'})
            ])
        }
    ),
    create=extend_schema(
        summary='Создание элемента платежа',
        description='Создаёт новую позицию платежа (например, конкретный товар или услугу в чеке).',
        responses={
            201: PaymentItemSerializer,
            400: OpenApiResponse(description='Ошибка создания', examples=[
                OpenApiExample('Ошибка', value={'error': 'Неверные данные'})
            ])
        }
    ),
    update=extend_schema(
        summary='Обновление элемента платежа',
        description='Полное обновление существующего элемента платежа.',
        request=PaymentItemSerializer,
        responses={
            200: PaymentItemSerializer,
            400: OpenApiResponse(description='Ошибка обновления', examples=[
                OpenApiExample('Ошибка', value={'error': 'Неверные данные'})
            ])
        }
    ),
    partial_update=extend_schema(
        summary='Частичное обновление элемента платежа',
        description='Обновляет часть полей позиции оплаты.',
        request=PaymentItemSerializer,
        responses={
            200: PaymentItemSerializer,
            400: OpenApiResponse(description='Ошибка', examples=[
                OpenApiExample('Ошибка', value={'error': 'Некорректные данные'})
            ]),
        }
    ),
    destroy=extend_schema(
        summary='Удаление элемента платежа',
        description='Удаляет запись о позиции оплаты.',
        responses={
            204: OpenApiResponse(description='Удалено', examples=[
                OpenApiExample('Успех', value={'message': 'Элемент платежа успешно удалён'})
            ]),
            404: OpenApiResponse(description='Не найдено', examples=[
                OpenApiExample('Ошибка', value={'error': 'Элемент платежа не найден'})
            ])
        }
    )
)
class PaymentItemView(viewsets.ModelViewSet):
    queryset = PaymentItem.objects.all()
    serializer_class = PaymentItemSerializer
    filterset_fields = ['id', 'payment', 'product', 'amount']



