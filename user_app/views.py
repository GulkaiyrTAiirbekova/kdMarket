from django.core.cache import cache
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from .services.limit_code import set_code_limited, is_code_limited
from .serializers import SMSVerificationSerializer
from .models import User, SMSVerification
from .serializers import UserSerializer
from rest_framework import viewsets
from rest_framework import status

from .services.validation_code import code_valid
from .tasks import generate_and_save_and_send_code


class UserApiView(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data.get('email')

        if is_code_limited(email):
            return Response({'error': 'Превышен лимит кодов.'}, status=status.HTTP_429_TOO_MANY_REQUESTS)

        code = generate_and_save_and_send_code.delay(email)

        cache.set(f'sms_limit_{email}', code, timeout=300)
        print(f"Setting cache: key=sms_limit_{email}, value={code}, timeout=300")
        set_code_limited(email)  # Устанавливаем лимит отправки SMS

        return Response({'message': 'Код отправлен.'}, status=status.HTTP_201_CREATED)


class SMSVerificationApiView(viewsets.ModelViewSet):
    queryset = SMSVerification.objects.all()
    serializer_class = SMSVerificationSerializer

    def create(self, request, *args, **kwargs):
        serializer = SMSVerificationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data.get('email')
        code = serializer.validated_data.get('code')

        if not email:
            return Response({'error': 'email обязателен.'}, status.HTTP_400_BAD_REQUEST)

        if not code:
            return Response({'error': 'Необходимо код подтверждения.'}, status.HTTP_400_BAD_REQUEST)

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









    # def create(self, request, *args, **kwargs):
    #     name = Product.objects.get(name=request.name)
    #     if len(name) > 20:
    #         return Response("error")
