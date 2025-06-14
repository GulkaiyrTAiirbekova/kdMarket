from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.types import OpenApiTypes
from rest_framework import viewsets
from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiParameter, OpenApiExample, OpenApiResponse
from rest_framework.response import Response

from orders_app.models import Order, OrderItem
from orders_app.serializers import OrderSerializer, OrderItemSerializer, OrderUpdateSerializer

#SWAGGER-OrderView
@extend_schema_view(
    list=extend_schema(
        summary="Получение списка заказов",
        description="Возвращает список всех заказов с возможностью фильтрации по ID заказа и по статусу.",
        parameters=[
            OpenApiParameter(name='id', description="Фильтр по ID заказа", required=False, type=int),
            OpenApiParameter(name='status', description="Фильтр по статусу заказа", required=False, type=str),
        ],
        responses={
            200: OrderSerializer(many=True),
            400: OpenApiExample(
                'Ошибка запроса',
                value={'error': 'Некорректные данные'}
            )
        }
    ),
    retrieve=extend_schema(
        summary="Получение деталей заказа",
        description="Возвращает подробную информацию о заказе по ID.",
        responses={
            200: OrderSerializer,
            404: OpenApiExample(
                'Заказ не найден',
                value={'error': 'Заказ с данным ID не найден'}
            )
        }
    ),
    create=extend_schema(
        summary="Создание нового заказа",
        description="Создает новый заказ.",
        request=OrderSerializer,
        responses={
            201: OrderSerializer,
            400: OpenApiExample(
                'Ошибка валидации',
                value={'error': 'Некорректные данные'}
            )
        }
    ),
    update=extend_schema(
        summary="Обновление заказа",
        description="Полное обновление информации заказа по ID.",
        request=OrderSerializer,
        responses={
            200: OrderSerializer,
            400: OpenApiExample(
                'Ошибка валидации',
                value={'error': 'Некорректные данные'}
            ),
            404: OpenApiExample(
                'Заказ не найден',
                value={'error': 'Заказ с данным ID не найден'}
            )
        }
    ),
    partial_update=extend_schema(
        summary="Частичное обновление заказа",
        description="Обновляет часть данных заказа по ID.",
        request=OrderSerializer,
        responses={
            200: OrderSerializer,
            400: OpenApiExample(
                'Ошибка валидации',
                value={'error': 'Некорректные данные'}
            ),
            404: OpenApiExample(
                'Заказ не найден',
                value={'error': 'Заказ с данным ID не найден'}
            )
        }
    ),
    destroy=extend_schema(
        summary="Удаление заказа",
        description="Удаляет заказ по ID.",
        responses={
            204: OpenApiExample(
                'Успешное удаление',
                value={'message': 'Заказ успешно удален'}
            ),
            404: OpenApiExample(
                'Заказ не найден',
                value={'error': 'Заказ с данным ID не найден'}
            )
        }
    )
)


class OrderView(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['user', 'status']


#swagger->OrderItemView
@extend_schema_view(
    list=extend_schema(
        summary="Список позиций заказа",
        description="Возвращает список всех позиций заказов. Можно фильтровать по ID заказа и продукту.",
        parameters=[
            OpenApiParameter(name='order', description="Фильтр по ID заказа", required=False, type=int),
            OpenApiParameter(name='product', description="Фильтр по ID продукта", required=False, type=int),
        ],
        responses={
            200: OrderItemSerializer(many=True),
            400: OpenApiExample(
                name='Ошибка запроса',
                value={'error': 'Некорректные данные'}
            )
        }
    ),
    retrieve=extend_schema(
        summary="Детали позиции заказа",
        description="Возвращает детальную информацию о позиции заказа по её ID.",
        responses={
            200: OrderItemSerializer,
            404: OpenApiExample(
                name='Позиция не найдена',
                value={'error': 'Позиция заказа с данным ID не найдена'}
            )
        }
    ),
    create=extend_schema(
        summary="Создание позиции заказа",
        description="Создает новую позицию заказа.",
        request=OrderItemSerializer,
        responses={
            201: OrderItemSerializer,
            400: OpenApiExample(
                name='Ошибка валидации',
                value={'error': 'Некорректные данные'}
            )
        }
    ),
    update=extend_schema(
        summary="Обновление позиции заказа",
        description="Полное обновление позиции заказа по её ID.",
        request=OrderItemSerializer,
        responses={
            200: OrderItemSerializer,
            400: OpenApiExample(
                name='Ошибка валидации',
                value={'error': 'Некорректные данные'}
            ),
            404: OpenApiExample(
                name='Позиция не найдена',
                value={'error': 'Позиция заказа с данным ID не найдена'}
            )
        }
    ),
    partial_update=extend_schema(
        summary="Частичное обновление позиции заказа",
        description="Обновляет часть информации позиции заказа по её ID.",
        request=OrderItemSerializer,
        responses={
            200: OrderItemSerializer,
            400: OpenApiExample(
                name='Ошибка валидации',
                value={'error': 'Некорректные данные'}
            ),
            404: OpenApiExample(
                name='Позиция не найдена',
                value={'error': 'Позиция заказа с данным ID не найдена'}
            )
        }
    ),
    destroy=extend_schema(
        summary="Удаление позиции заказа",
        description="Удаляет позицию заказа по её ID.",
        responses={
            204: OpenApiExample(
                name='Успешное удаление',
                value={'message': 'Позиция заказа успешно удалена'}
            ),
            404: OpenApiExample(
                name='Позиция не найдена',
                value={'error': 'Позиция заказа с данным ID не найдена'}
            )
        }
    )
)
class OrderItemView(viewsets.ModelViewSet):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['order', 'product']

#swagger->OrderItemView
@extend_schema_view(
    list=extend_schema(
        summary="Список позиций заказа",
        description="Возвращает список всех позиций заказов с возможностью фильтрации по заказу и товару.",
        parameters=[
            OpenApiParameter(name='order', description="Фильтр по ID заказа", required=False, type=int),
            OpenApiParameter(name='product', description="Фильтр по ID продукта", required=False, type=int),
        ],
        responses={
            200: OrderItemSerializer(many=True),
            400: OpenApiExample(
                name='Ошибка запроса',
                value={'error': 'Некорректные параметры запроса'}
            )
        }
    ),
    retrieve=extend_schema(
        summary="Получение позиции заказа",
        description="Возвращает подробную информацию о конкретной позиции заказа по её ID.",
        responses={
            200: OrderItemSerializer,
            404: OpenApiExample(
                name='Позиция заказа не найдена',
                value={'error': 'Позиция заказа с данным ID не найдена'}
            )
        }
    ),
    create=extend_schema(
        summary="Создание позиции заказа",
        description="Создает новую позицию заказа (товар внутри заказа).",
        request=OrderItemSerializer,
        responses={
            201: OrderItemSerializer,
            400: OpenApiExample(
                name='Ошибка создания',
                value={'error': 'Некорректные данные для создания позиции заказа'}
            )
        }
    ),
    update=extend_schema(
        summary="Полное обновление позиции заказа",
        description="Полностью обновляет данные позиции заказа по её ID.",
        request=OrderItemSerializer,
        responses={
            200: OrderItemSerializer,
            400: OpenApiExample(
                name='Ошибка валидации',
                value={'error': 'Некорректные данные при обновлении'}
            ),
            404: OpenApiExample(
                name='Позиция не найдена',
                value={'error': 'Позиция заказа с данным ID не найдена'}
            )
        }
    ),
    partial_update=extend_schema(
        summary="Частичное обновление позиции заказа",
        description="Обновляет только переданные поля позиции заказа.",
        request=OrderItemSerializer,
        responses={
            200: OrderItemSerializer,
            400: OpenApiExample(
                name='Ошибка валидации',
                value={'error': 'Некорректные данные'}
            ),
            404: OpenApiExample(
                name='Позиция не найдена',
                value={'error': 'Позиция заказа с данным ID не найдена'}
            )
        }
    ),
    destroy=extend_schema(
        summary="Удаление позиции заказа",
        description="Удаляет позицию заказа по её ID.",
        responses={
            204: OpenApiExample(
                name='Успешное удаление',
                value={'message': 'Позиция заказа успешно удалена'}
            ),
            404: OpenApiExample(
                name='Позиция не найдена',
                value={'error': 'Позиция заказа с данным ID не найдена'}
            )
        }
    )
)

class OrderItemView(viewsets.ModelViewSet):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer




class OrderCreateSerializer:
    pass

#swagger->OrderView

@extend_schema_view(
    list=extend_schema(
        summary="Список заказов",
        description="Возвращает список заказов с возможностью фильтрации по статусу или пользователю",
        parameters=[
            OpenApiParameter(name='user', description='ID пользователя', required=False, type=int),
            OpenApiParameter(name='status', description='Статус заказа', required=False, type=str),
        ],
        responses={200: OrderSerializer}
    ),
    retrieve=extend_schema(
        summary="Детали заказа",
        responses={200: OrderSerializer, 404: OpenApiResponse(description="Не найден")}
    ),
    create=extend_schema(
        summary="Создание заказа",
        request=OrderCreateSerializer,
        responses={201: OrderSerializer, 400: OpenApiResponse(description="Ошибка валидации")}
    ),
    update=extend_schema(
        summary="Обновление заказа",
        request=OrderUpdateSerializer,
        responses={200: OrderSerializer}
    ),
    partial_update=extend_schema(
        summary="Частичное обновление заказа",
        request=OrderUpdateSerializer,
        responses={200: OrderSerializer}
    ),
    destroy=extend_schema(
        summary="Удаление заказа",
        responses={204: OpenApiResponse(description="Удалено")}
    )
)
class OrderView(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    filterset_fields = ['user', 'status']

    def get_serializer_class(self):
        if self.action == 'create':
            return OrderCreateSerializer
        elif self.action in ['update', 'partial_update']:
            return OrderUpdateSerializer
        return OrderSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        order = serializer.save()

        # Пример логики: отправить уведомление или списать со склада
        # notify_user(order.user)
        # update_stock(order)

        return Response(OrderSerializer(order).data, status=201)


#swagger->OrderItemView

@extend_schema_view(
    list=extend_schema(
        summary="Список элементов заказа",
        description="Возвращает список всех элементов заказа с возможностью фильтрации по ID заказа и ID продукта.",
        parameters=[
            OpenApiParameter(name='order', description='ID заказа', required=False, type=int),
            OpenApiParameter(name='product', description='ID товара', required=False, type=int),
        ],
        responses={
            200: OrderItemSerializer(many=True),
            400: OpenApiResponse(description="Некорректные параметры запроса")
        }
    ),
    retrieve=extend_schema(
        summary="Получение элемента заказа",
        description="Возвращает информацию об элементе заказа по его ID.",
        responses={
            200: OrderItemSerializer,
            404: OpenApiResponse(description="Элемент заказа не найден")
        }
    ),
    create=extend_schema(
        summary="Создание элемента заказа",
        description="Создает новый элемент в заказе.",
        request=OrderItemSerializer,
        responses={
            201: OrderItemSerializer,
            400: OpenApiResponse(description="Некорректные данные при создании")
        }
    ),
    update=extend_schema(
        summary="Обновление элемента заказа",
        description="Полное обновление информации об элементе заказа.",
        request=OrderItemSerializer,
        responses={
            200: OrderItemSerializer,
            400: OpenApiResponse(description="Некорректные данные при обновлении"),
            404: OpenApiResponse(description="Элемент заказа не найден")
        }
    ),
    partial_update=extend_schema(
        summary="Частичное обновление элемента заказа",
        description="Частично обновляет элемент заказа.",
        request=OrderItemSerializer,
        responses={
            200: OrderItemSerializer,
            400: OpenApiResponse(description="Некорректные данные"),
            404: OpenApiResponse(description="Элемент заказа не найден")
        }
    ),
    destroy=extend_schema(
        summary="Удаление элемента заказа",
        description="Удаляет элемент заказа по его ID.",
        responses={
            204: OpenApiResponse(description="Элемент заказа успешно удалён"),
            404: OpenApiResponse(description="Элемент заказа не найден")
        }
    )
)
class OrderItemView(viewsets.ModelViewSet):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['order', 'product']
#?????????????????????????????????????
#class Order(models.Model):
#    user = models.ForeignKey(User, on_delete=models.CASCADE)
#    status = models.CharField(max_length=100)

