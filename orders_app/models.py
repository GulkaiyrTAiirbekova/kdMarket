from django.db import models
from goods_app.models import Product
from django.contrib.auth import get_user_model

User = get_user_model()

class PAYMENT_METHOD_CHOICES(models.TextChoices):
    CASH_ON_DELIVERY = 'cash_on_delivery', ('Оплата при получении')
    ONLINE_PAYMENT = 'online_payment', ('Онлайн оплата')

class Order(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE,verbose_name ="Пользователь")
    created_timestamp = models.DateTimeField(auto_now_add =True,verbose_name = "Когда была создана")
    requires_delivery = models.BooleanField(default = False,verbose_name = "Нужна доставка")
    delivery_address = models.CharField(max_length= 215,null =True,verbose_name ="Адресс доставки")
    pickup_point = models.CharField(max_length =250,blank = True, null= True,verbose_name = "Откукда нужно забрать")
    payment_method = models.CharField(
        max_length=50, choices=PAYMENT_METHOD_CHOICES.choices,
        default=PAYMENT_METHOD_CHOICES.ONLINE_PAYMENT, verbose_name ="Метод оплаты"
    )
    is_paid =models.BooleanField(default = False, verbose_name = "Оплачено ли")
    status = models.CharField(default ="pending",verbose_name = "Статус Продукта" )


    total_price = models.DecimalField(max_digits=10,decimal_places=2,default=0.00)


class OrderItem(models.Model):
    order = models.ForeignKey(Order,on_delete=models.CASCADE,verbose_name = "Заказ")
    product = models.ForeignKey(Product,on_delete= models.CASCADE,verbose_name = "Продукт")
    quantity = models.IntegerField(default = 1,verbose_name = "Количество заказанных товаров")
    price = models.FloatField(default =  0.0, verbose_name ="Цена")
    created_at = models.DateTimeField(auto_now_add = True)
