from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils import timezone
from datetime import timedelta


class UserManager(BaseUserManager):
    def create_user(self, email=None, password=None):
        if not email:
            raise ValueError('Необходимо указать email!')

        user = self.model(email=email)
        user.set_unusable_password()  # Пароль не обязателен, так как логика через SMS
        user.save(using=self._db)
        return user

    def create_superuser(self, email=None, password=None):
        """
        Создание суперпользователя с обязательным паролем.
        """
        if not email:
            raise ValueError('Необходимо указать email!')
        if not password:
            raise ValueError('Необходимо указать пароль для суперпользователя!')

        # Создаем пользователя без пароля
        user = self.model(email=email)
        # Устанавливаем пароль через метод set_password
        user.set_password(password)
        user.is_staff = True
        user.is_superuser = True
        user.is_active = True  # Обязательно активируем суперпользователя
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True, verbose_name='email')
    username = models.CharField(max_length=50, verbose_name='Имя пользователя')
    image = models.ImageField(upload_to='user_logs/', verbose_name='Профиль пользователя', null=True, blank=True)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)  # Добавлено это поле

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return str(self.email)

    class Meta:
        indexes = [
            models.Index(fields=['email']),
        ]


class SMSVerification(models.Model):
    email = models.EmailField()
    code = models.CharField(max_length=4, verbose_name='Код')
    is_used = models.BooleanField(default=False)
    # created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'email Пользователя: {self.email} Код: {self.code}'

    # def is_code_valid(self):
    #     return (
    #         timezone.now() < self.created_at + timedelta(minutes=3) and not self.is_used
    #     )

    class Meta:
        indexes = [
            models.Index(fields=['email', 'code']),
        ]