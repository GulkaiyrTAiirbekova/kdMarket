from http.client import responses
from importlib.metadata import requires

from django.core.cache import cache
from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction
from django.template.context_processors import request
from drf_spectacular.types import OpenApiTypes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.utils.representation import serializer_repr
from rest_framework_simplejwt.tokens import RefreshToken
from yaml import serialize

from .services.limit_code import set_code_limited, is_code_limited
from .serializers import SMSVerificationSerializer
from .models import User, SMSVerification
from .serializers import UserSerializer
from rest_framework import viewsets
from rest_framework import status
from .services.validation_code import code_valid
from .tasks import generate_and_save_and_send_code
from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiParameter, OpenApiExample, OpenApiResponse


@extend_schema_view(
    list=extend_schema(
        summary="Возвращает список пользователей",
        description="Возвращает список всех пользователей с фильтрацией по id, email и username",
        parameters=[
            OpenApiParameter(name='id', description="Фильтр по ID пользователя", required=False, type=OpenApiTypes.INT),
            OpenApiParameter(name='email', description="Фильтр по email пользователя", required=False, type=OpenApiTypes.STR),
            OpenApiParameter(name='username', description="Фильтр по username пользователя", required=False, type=OpenApiTypes.STR),
        ],
        responses={
            200: UserSerializer,
            400: OpenApiExample('Ошибка запроса', value={'error': 'Некорректные данные'}),
            404: OpenApiExample('Пользователь не найден', value={'error': 'Пользователь с таким ID не найден'}),
        }
    ),
    retrieve=extend_schema(
        summary='Получение деталей пользователя',
        description='Возвращает данные конкретного пользователя',
        responses={
            200: UserSerializer,
            404: OpenApiExample('Пользователь не найден', value={'error': 'Пользователь с таким ID не найден'}),
        }
    ),
    create=extend_schema(
        summary='Отправка кода',
        description='Создает отправку кода для дальнейшей верификации пользователя',
        responses={
            201: OpenApiExample('Код отправлен', value={'message': 'Код отправлен'}),
            400: OpenApiExample('Ошибка валидации', value={'error': 'Некорректные данные'}),
        }
    ),
    update=extend_schema(
        summary='Обновление пользователя',
        description='Обновление пользователя по его ID',
        request=UserSerializer,
        responses={
            200: UserSerializer,
            400: OpenApiExample('Ошибка валидации', value={'error': 'Некорректные данные'}),
            404: OpenApiExample('Пользователь не найден', value={'error': 'Пользователь с таким ID не найден'}),
        }
    ),
    partial_update=extend_schema(
        summary='Частичное обновление пользователя',
        description='Частичное обновление пользователя по его ID',
        request=UserSerializer,
        responses={
            200: UserSerializer,
            400: OpenApiExample('Ошибка валидации', value={'error': 'Некорректные данные'}),
            404: OpenApiExample('Пользователь не найден', value={'error': 'Пользователь с таким ID не найден'}),
        }
    ),
    destroy=extend_schema(
        summary='Удаление профиля пользователя',
        description='Удаляет профиль пользователя по его ID',
        responses={
            204: OpenApiExample('Успешное удаление', value={'message': 'Профиль пользователя успешно удален'}),
            404: OpenApiExample('Профиль пользователя не найден', value={'error': 'Профиль пользователя с таким ID не найден'}),
        }
    )
)
class UserApiView(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filterset_fields = ['id', 'email', 'username']

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data.get('email')

        if is_code_limited(email):
            return Response({'error': 'Превышен лимит отправки кодов.'}, status=status.HTTP_429_TOO_MANY_REQUESTS)

        generate_and_save_and_send_code.delay(email)
        set_code_limited(email)

        return Response({'message': 'Код отправлен.'}, status=status.HTTP_201_CREATED)

#Документация (SWAGGER -DRF-SPECTECULAR) API->SMSVerificationApiView

@extend_schema_view(
    list=extend_schema(
        summary='Получение списка верификаций',
        description='Возвращает список всех верификаций с фильтрацией по ID, email и коду',
        parameters=[
            OpenApiParameter(name='id', description='Фильтр по ID верификации', required=False, type=OpenApiTypes.INT),
            OpenApiParameter(name='email', description='Фильтр по email', required=False, type=OpenApiTypes.STR),
            OpenApiParameter(name='code', description='Фильтр по коду верификации', required=False, type=OpenApiTypes.STR),
        ],
        responses={
            200: SMSVerificationSerializer,
            400: OpenApiResponse(description='Ошибка запроса', examples=[
                OpenApiExample('Ошибка запроса', value={'error': 'Некорректные данные'})
            ]),
            404: OpenApiResponse(description='Верификация не найдена', examples=[
                OpenApiExample('Верификация не найдена', value={'error': 'Запись не найдена'})
            ]),
        }
    ),
    retrieve=extend_schema(
        summary='Детали верификации',
        description='Возвращает детали конкретной верификации пользователя',
        responses={
            200: SMSVerificationSerializer,
            404: OpenApiResponse(description='Не найдено', examples=[
                OpenApiExample('Не найдено', value={'error': 'Верификация не найдена'})
            ]),
        }
    ),
    create=extend_schema(
        summary='Создание верификации',
        description='Создает новую верификацию пользователя по email и коду',
        responses={
            200: SMSVerificationSerializer,
            400: OpenApiResponse(description='Ошибка валидации', examples=[
                OpenApiExample('Ошибка', value={'error': 'Некорректные данные'})
            ]),
        }
    ),
    update=extend_schema(
        summary='Обновление верификации',
        description='Обновляет данные верификации пользователя по ID',
        request=SMSVerificationSerializer,
        responses={
            200: SMSVerificationSerializer,
            400: OpenApiResponse(description='Ошибка валидации', examples=[
                OpenApiExample('Ошибка', value={'error': 'Некорректные данные'})
            ]),
            404: OpenApiResponse(description='Не найдено', examples=[
                OpenApiExample('Не найдено', value={'error': 'Верификация не найдена'})
            ]),
        }
    ),
    partial_update=extend_schema(
        summary='Частичное обновление верификации',
        description='Частично обновляет данные верификации по ID',
        request=SMSVerificationSerializer,
        responses={
            200: SMSVerificationSerializer,
            400: OpenApiResponse(description='Ошибка валидации', examples=[
                OpenApiExample('Ошибка', value={'error': 'Некорректные данные'})
            ]),
            404: OpenApiResponse(description='Не найдено', examples=[
                OpenApiExample('Не найдено', value={'error': 'Верификация не найдена'})
            ]),
        }
    ),
    destroy=extend_schema(
        summary='Удаление верификации',
        description='Удаляет верификацию пользователя по ID',
        responses={
            204: OpenApiResponse(description='Успешное удаление', examples=[
                OpenApiExample('Удалено', value={'message': 'Верификация успешно удалена'})
            ]),
            404: OpenApiResponse(description='Не найдено', examples=[
                OpenApiExample('Не найдено', value={'error': 'Верификация не найдена'})
            ]),
        }
    )
)
#class SMSVerificationApiView(viewsets.ModelViewSet):
#    queryset = SMSVerification.objects.all()
#    serializer_class = SMSVerificationSerializer
#    filterset_fields = ['id', 'email', 'code']

class SMSVerificationApiView(viewsets.ModelViewSet):
    """
    Верификация SMS-кода и создание пользователя
    """
    queryset = SMSVerification.objects.all()
    serializer_class = SMSVerificationSerializer
    filterset_fields = ['id', 'email', 'code']

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        serializer = SMSVerificationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data.get('email')
        code = serializer.validated_data.get('code')

        if not email:
            return Response({'error': 'email обязателен.'}, status.HTTP_400_BAD_REQUEST)

        if not code:
            return Response({'error': 'Необходим код подтверждения.'}, status.HTTP_400_BAD_REQUEST)

        # Проверяем код из кэша
        if not code_valid(email, code):
            return Response({'error': 'Код не валиден или истек.'}, status.HTTP_400_BAD_REQUEST)

        try:
            # Проверяем запись SMS
            verification = SMSVerification.objects.get(email=email, code=code, is_used=False)
            verification.is_used = True
            verification.save()

            # Проверяем или создаем пользователя
            user, created = User.objects.get_or_create(email=email)

            cache.delete(f'sms_code_{email}')

            refresh = RefreshToken.for_user(user)

            # Генерация токенов
            if created:
                return Response({
                    'message': 'Успешный вход!, хотите дополнить профиль?',
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                }, status.HTTP_201_CREATED)

            return Response({
                'message': 'Успешный вход!',
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }, status.HTTP_200_OK)

        except ObjectDoesNotExist:
            return Response({'error': 'Код не найден или уже использован.'}, status.HTTP_400_BAD_REQUEST)

#Документация (swagger-drd-spectecular)API->UserProfileApiView(0:18)
@extend_schema_view(
    list = extend_schema(
        summary ='Получение списка Профиля пользователей',
        description = 'Возвращает список всез Пользователей с возможностью фильтрации по ID пользователя,по email,по username',
        parameters=[
            OpenApiParameter(name ='id',description ='Фильтр по ID верификации',required =False,type=int),
            OpenApiParameter(name ='email',description ='Фильтр по email верификации',required =False,type=str),
            OpenApiParameter(name ='username',description ='Фильтр по коду верификации',required =False,type=str),
        ],
        responses = {
            200: UserSerializer,
            400: OpenApiExample(
                'Ошибка запроса',
                {'error':'Некорректные данные'}
            ),
            404: OpenApiExample(
                'Профиль пользователя не найден',
                {'error':'Некорректные данные'}
            ),
        },
    ),
    retrive= extend_schema(
        summary='Получение деталей Профиля пользователя',
        description='Возвращает  данные конкретного профиля Пользователя .Результаты кэшируются для повышения производительности',
        responses = {
            200: UserSerializer,
            404: OpenApiExample(
                'Профиль польщователя не найден',
                {'error': 'Профиль польщователя с данными ID не найден '}
            ),
        },
    ),
    update = extend_schema(
        summary='Обновление  Профиля пользователя',
        description='Обновляет данные профиля Пользователя  по ID.',
        request= UserSerializer,
        responses={
            200: UserSerializer,
            400: OpenApiExample(
                'Ошибка запроса',
                {'error': 'Некорректные данные'}
            ),
            404: OpenApiExample(
                'Профиль пользователя не найден',
                {'error': 'Профиль польщователя с данными ID не найден '}
            ),
        },
    ),
    partial_update= extend_schema(
        summary=' Частичное Обновление  Профиля пользователя',
        description='Частично Обновляет данные профиля Пользователя  по ID.',
        request=UserSerializer,
        responses={
            200: UserSerializer,
            400: OpenApiExample(
                'Ошибка Валидации',
                {'error': 'Некорректные данные'}
            ),
            404: OpenApiExample(
                'Профиль пользователя не найден',
                {'error': 'Профиль польщователя с данными ID не найден '}
            ),
        },
    ),
    destroy=extend_schema(
        summary='Удаление Профиля пользователя',
        description='Удаление Профиля пользователя по его ID. ',
        responses={
            204: OpenApiExample(
                'Успешное Удаление',
                {'message':'Профиль пользователя успешно удален'},
            ),
            404: OpenApiExample(
                'Профиль пользователя не найден',
                {'error': 'Профиль пользователя, которого хотите удалить с данными ID не найден '}
            )
        }
    )
)


class UserProfileApiView(viewsets.ModelViewSet):
    """
    Профиль пользователя (только для аутентифийированных пользователей)
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    filterset_fields =['id','email','username']

    def retrieve(self, request, *args, **kwargs):
        """ Получение данных профиля"""
        serializer = UserSerializer(request.user)
        return Response(serializer.data)
    def update(self, request, *args, **kwargs):
        """Обновление данных профиля"""
        serializer = UserSerializer(request.user,data=request.data,partial=False)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data,status.HTTP_200_OK)

    def patch(self,request):
        """ Частичное обновление данных"""
        serializer =UserSerializer(request.user)


















    # def create(self, request, *args, **kwargs):
    #     name = Product.objects.get(name=request.name)
    #     if len(name) > 20:
    #         return Response("error")
