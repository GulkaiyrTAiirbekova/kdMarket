from http.client import responses
from importlib.metadata import requires

from django.core.cache import cache
from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction
from django.template.context_processors import request
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
from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiParameter, OpenApiExample



@extend_schema_view(
        list = extend_schema(
            summary = "Возвращает список пользователей",
            description = "Возвращает список  всех пользователей с возможностью фильтраций по ID пользователя, по email и по username",
            parameters=[
                OpenApiParameter(name='id', description= "Фильтр по ID пользователя", required=False,type =int),
                OpenApiParameter(name='email', description= "Фильтр по email пользователя", required=False,type =str),
                OpenApiParameter(name='username', description= "Фильтр по Нику пользователя", required=False,type =str),
            ],
            responses = {
                200: UserSerializer,
                400: OpenApiExample(
                    'Ошибка запроса',
                    {'error:' 'Некорректные данные'}
                ),
                404 : OpenApiExample(
                    'Пользователь не найден',
                    {'error:' 'Некорректные данные'}
                ),
            },
        ),
        retrieve = extend_schema(
            summary = 'Получение деталей Пользователя',
            description='Возвращает данные конкретного Пользователя. Результаты кэшируются дл повышения производительности',
            responses={
                200: UserSerializer,
                404: OpenApiExample(
                    'Пользователь не найден',
                    {'error': 'Пользователь с данными ID не найден.'}
                ),
            },
        ),
        create = extend_schema(
            summary ='Отправка кода',
            description=' Создает отправку кода, чтоб в дальнейшем (в API-SMSVerification создать его) Пользователя.В случае ошибки возврашается',
            responses={
                201: UserSerializer,
                404:OpenApiExample(
                    'Ошибка Валидации',
                    {'error': 'Некорректные данные' }
                ),
            },
        ),
        update = extend_schema(
            summary ='Обновление пользователя',
            description=' Обновление Пользователя по его ID.',
            request=UserSerializer,
            responses={
                201: UserSerializer,
                400:OpenApiExample(
                    'Ошибка Валидации',
                    {'error': 'Некорректные данные' },
                ),
                404:OpenApiExample(
                   'Пользователь не найден',
                    {'error': 'Пользователь с данными ID не найден'}
                ),
            },
        ),
        partial_update = extend_schema(
            summary=' Частичное Обновление пользователя',
            description='Частичное Обновляет данные  Пользователя по его ID.',
            request=UserSerializer,
            responses={
                201: UserSerializer,
                400: OpenApiExample(
                    'Ошибка Валидации',
                    {'error': 'Некорректные данные'},
                ),
                404: OpenApiExample(
                    'Пользователь не найден',
                    {'error': 'Пользователь с данными ID не найден'}
                ),
            },
        ),
        destroy = extend_schema(
            summary='Удаление Профиля пользователя',
            description=' Удаляет Профиль пользователя по его ID',
            responses={
                204:OpenApiExample(
                    'Успешное Удаление',
                    {'message':'Профиль пользователя успешно удален'},
                ),
                404: OpenApiExample(
                    'Профиль пользователя не найден',
                    {'error':'Профиль пользователя, которую Вы хотите удалить с данными ID не найден'}
                )
            }
        )
)
class UserApiView(viewsets.ModelViewSet):
    """ Отправка СМС-кода для аутентификации или регисистрации"""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filterset_fields = ['id', 'email', 'username']

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        """ Отправляет СМС_код по номеру телефона. Создание пользователя не происходит на этом
        этапе """
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)  # Автоматически возвращает 404бесли данные невалидны

        email = serializer.validated_data.get('email')

        if is_code_limited(email):
            return Response({'error': 'Превышен лимит кодов.'}, status=status.HTTP_429_TOO_MANY_REQUESTS)
        # Генерация и отпрвка кода
        code = generate_and_save_and_send_code.delay(email)
        if not code:
            logger.error(f'Ошибка при отправке СМС(Ошибка тут)')
            return Response({'error': _('Не удалось отправить код.')}, status.HTTP_500_INTERNAL_SERVER_ERROR)

        cache.set(f'sms_limit_{email}', code, timeout=300)
        print(f"Setting cache: key=sms_limit_{email}, value={code}, timeout=300")
        set_code_limited(email)  # Устанавливаем лимит отправки SMS

        return Response({'message': 'Код отправлен.'}, status=status.HTTP_201_CREATED)
#Документация (SWAGGER -DRF-SPECTECULAR) API->SMSVerificationApiView
@from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiParameter, OpenApiExample, OpenApiResponse

@extend_schema_view(
    list=extend_schema(
        summary='Получение списка Верификаций и создание Профиля',
        description='Возвращает список всех верификаций и созданий пользователя с возможностью фильтрации по ID, email и номеру телефона',
        parameters=[
            OpenApiParameter(name='id', description='Фильтр по ID Верификации', required=False, type=int),
            OpenApiParameter(name='email', description='Фильтр по email верификации', required=False, type=str),
            OpenApiParameter(name='code', description='Фильтр по коду верификации', required=False, type=str),
        ],
        responses={
            200: SMSVerificationSerializer,
            400: OpenApiResponse(description='Ошибка запроса', examples=[
                OpenApiExample(
                    'Ошибка запроса',
                    value={'error': 'Некорректные данные'}
                )
            ]),
            404: OpenApiResponse(description='Верификация не найдена', examples=[
                OpenApiExample(
                    'Верификация не найдена',
                    value={'error': 'Некорректные данные'}
                )
            ])
        }
    ),
    retrieve=extend_schema(
        summary='Получение деталей Верификаций Профиля',
        description='Возвращает данные корректных верификаций пользователя. Результаты кэшируются.',
        responses={
            200: SMSVerificationSerializer,
            400: OpenApiResponse(description='Ошибка', examples=[
                OpenApiExample(
                    'Ошибка',
                    value={'error': 'Верификация Пользователя с данным ID не найдена'}
                )
            ])
        }
    ),
    create=extend_schema(
        summary='Создание Верификации Профиля',
        description='Создает новую верификацию пользователя. В случае ошибки возвращает сообщение об ошибке',
        responses={
            200: SMSVerificationSerializer,
            400: OpenApiResponse(description='Ошибка', examples=[
                OpenApiExample(
                    'Ошибка валидации',
                    value={'error': 'Некорректные данные'}
                )
            ])
        }
    ),
    update=extend_schema(
        summary='Обновление Верификации пользователя',
        description='Обновляет данные верификации пользователя по его ID.',
        request=SMSVerificationSerializer,
        responses={
            200: SMSVerificationSerializer,
            400: OpenApiResponse(description='Ошибка', examples=[
                OpenApiExample(
                    'Ошибка валидации',
                    value={'error': 'Верификация пользователя с данными ID не найдена'}
                )
            ])
        }
    ),
    partial_update=extend_schema(
        summary='Частичное обновление Верификации пользователя',
        description='Частично обновляет данные верификации пользователя по его ID.',
        request=SMSVerificationSerializer,
        responses={
            200: SMSVerificationSerializer,
            400: OpenApiResponse(description='Ошибка', examples=[
                OpenApiExample(
                    'Ошибка валидации',
                    value={'error': 'Некорректные данные'}
                )
            ]),
            404: OpenApiResponse(description='Не найдено', examples=[
                OpenApiExample(
                    'Верификация не найдена',
                    value={'error': 'Верификация пользователя с данным ID не найдена'}
                )
            ])
        }
    )
)

    destroy = extend_schema(
        summary='Удаление Верификаций пользователя',
        description='Удаляет Верификацию польщователя по его ID',
        responses={
            204:OpenApiExample(
                'Успешное Удаление',
                {'message':'Верификация пользователя успешно удалена'},
            ),
            404:OpenApiExample(
                'Верификация пользователя не найдена',
                {'error':'Верификация пользователя, которую Вы хотите удалить с данными ID не найдена'}
            )
        }
    )


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
            OpenApiParameter(name ='id',decription ='Фильтр по ID верификации',required =False,type=int),
            OpenApiParameter(name ='email',decription ='Фильтр по email верификации',required =False,type=str),
            OpenApiParameter(name ='username',decription ='Фильтр по коду верификации',required =False,type=str),
        ],
        responses = {
            200: UserSerializer,
            400: OpenApiExample(
                'Ошибка запроса',
                {'error':'Некорректные данные'}
            ),
            404: OpenApiExample(
                'Профиль польщователя не найден',
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
