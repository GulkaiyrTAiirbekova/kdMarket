from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils import timezone
from datetime import timedelta
from django.utils.translation import gettext_lazy as _


class UserManager(BaseUserManager):
    def create_user(self, email=None, password=None):
        if not email:
            raise ValueError('Необходимо указать номер телефона!')

        user = self.model(email=email)
        user.set_unusable_password()  # Пароль не обязателен, так как логика через SMS
        user.save(using=self._db)
        return user

    def create_superuser(self, email=None, password=None):
        user = self.create_user(email=email, password=password)
        user.is_staff = True
        user.is_superuser = True
        if password:
            user.set_password(password)
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    # phone_number = PhoneNumberField(unique=True, null=True, blank=True, verbose_name=_('Номер телефона'), default="+0000000000")
    email = models.EmailField(unique=True, verbose_name=_('Email'))
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    image = models.ImageField(upload_to='user_image/', blank=True, null=True)
    username = models.CharField(max_length=210, blank=True, null=True)

    USERNAME_FIELD = 'email'  # Основное поле для входа - phone_number
    REQUIRED_FIELDS = []  # Нет обязательных дополнительных полей

    objects = UserManager()

    def __str__(self):
        return str(self.email)

    class Meta:
        indexes = [
            # models.Index(fields=['phone_number']),
            models.Index(fields=['email']),
        ]


class SMSVerification(models.Model):
    # phone_number = PhoneNumberField(verbose_name=_('Номер телефона'), default='+0000000000')
    email = models.EmailField(verbose_name=_('Email'))
    code = models.CharField(max_length=4)
    is_used = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Пользователь: {self.email}, Код: {self.code}'

    def is_code_valid(self):
        """Проверка, что код действителен и не использован"""
        return (
            timezone.now() < self.created_at + timedelta(minutes=1) and not self.is_used
        )

    class Meta:
        indexes = [
            models.Index(fields=['email', 'code']),
        ]



