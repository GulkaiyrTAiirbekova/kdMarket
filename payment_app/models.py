from django.db import models

from goods_app.models import Product
from orders_app.models import Order
from django.contrib.auth import get_user_model

User = get_user_model()


class PAYMENT_METHOD_CHOICES(models.TextChoices):
    CASH_ON_DELIVERY = 'cash_on_delivery', ('Оплата при получении')
    ONLINE_PAYMENT = 'online_payment', ('Онлайн оплата')

class Payment(models.Model):
    transition_id = models.CharField(max_length=100, unique =True,verbose_name="ID транзакции" )
    user = models.ForeignKey(User, on_delete = models.CASCADE,verbose_name ="Кто оплатил")
    order = models.ForeignKey(Order, on_delete=models.CASCADE, verbose_name = "Заказ")
    amount=models.DecimalField(max_digits=6,decimal_places=2, verbose_name = "Сумма платежа")
    payment_method = models.CharField(
        max_length=50, choices=PAYMENT_METHOD_CHOICES.choices,
        default=PAYMENT_METHOD_CHOICES.ONLINE_PAYMENT, verbose_name="Метод оплаты"
    )
    is_paid = models.BooleanField(default=False, verbose_name="Оплачено ли")
    status = models.CharField(default="pending", verbose_name="Статус Продукта")
    transition_error =models.TextField(blank = True,null =True, verbose_name = "ОШибка Транзакции")

    CURRENCY_CHOICES = [
        ('RUB', 'Российский рубль'),
        ('USD', 'Доллар США'),
        ('EUR', 'Евро'),
    ]


    currency = models.CharField(
        max_length=3,
        choices=CURRENCY_CHOICES,
        default = 'USD',
        verbose_name =" Валюта"
    )

    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now=True,verbose_name ="Обновлено")


class PaymentItem(models.Model):
    payment= models.ForeignKey(Payment,on_delete=models.CASCADE,verbose_name ="Платеж")
    product =models.ForeignKey(Product, on_delete=models.CASCADE,verbose_name = "За какой товар оплачено")
    quantity = models.IntegerField(default = 1,verbose_name = "Количество товаров")
    total_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Итоговая сумма"
    )
    created_at = models.DateTimeField(auto_now_add= True,verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True,verbose_name ="Обновлено")
