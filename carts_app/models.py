from django.db import models
from goods_app.models import Product
from django.contrib.auth import get_user_model

User = get_user_model()


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE,verbose_name ="Пользователь  карты")
    session_key = models.CharField(max_length=40,verbose_name =" Ключ Сессии",blank =True,null = True)
    product =models.ForeignKey(Product, on_delete=models.CASCADE,verbose_name = "Товар/Продукт")
    quantity = models.IntegerField(default = 1,verbose_name = "Количество")
    created_at = models.DateTimeField(auto_now_add = True)

class Favourites (models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE,verbose_name ="Фаворит Пользователя")
    session_key = models.CharField(max_length=40,verbose_name =" Ключ Сессии",blank =True,null = True)
    product =models.ForeignKey(Product, on_delete=models.CASCADE,verbose_name = "Товар/Продукт")
    created_at = models.DateTimeField(auto_now_add = True)

