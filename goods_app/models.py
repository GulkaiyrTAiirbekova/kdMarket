from django.core.cache import cache
from django.db import models
from django.utils.functional import cached_property
from django.utils.text import slugify

from django.contrib.auth import get_user_model

User = get_user_model()


class Category(models.Model):
    slug = models.SlugField(max_length = 25, verbose_name = "url")
    name = models.CharField(max_length= 25, verbose_name = "Название")
    image = models.ImageField(upload_to = "Category_images/", verbose_name ="Изображение категории")


class Brand(models.Model):
    slug = models.SlugField(max_length = 25, verbose_name = "url")
    name = models.CharField(max_length= 25, verbose_name = "Название")
    logo = models.ImageField(upload_to = "Brand_logo/", verbose_name ="Лого Бренда")
    description = models.TextField(verbose_name= "Описание")

class Product (models.Model):
    slug = models.SlugField(max_length=25, verbose_name="url")
    name = models.CharField(max_length=25, verbose_name="Название")
    description = models.TextField(verbose_name="Описание")
    is_on_sale = models.BooleanField(default = True, verbose_name =" На продаже")
    quantity = models.IntegerField(default = 1,verbose_name = "Количество товаров")
    discount_price = models.BooleanField(default = False, verbose_name =" Скидка на Продукт")
    price = models.FloatField(default =  0.0, verbose_name ="Цена")
    category =models.ForeignKey(Category, on_delete=models.CASCADE)
    brand =models.ForeignKey(Brand, on_delete=models.CASCADE)
    image = models.ImageField(upload_to = "Product_images/", verbose_name ="Изображение категории")

    def final_price(self):
        cache_k = f'product_{self.id}_final_price'
        price = cache.get(cache_k) # use reddis

        if price is None:
            discount = self.discount_price / 100
            price  = round(self.price * (1- discount), 2) if self.is_on_sale else self.price

            cache.set(cache_k,price,60*60)

        return price



    def save(self,*args,**kwargs):
        if not self.slug:
            self.slug = slugify(self.name)

        super().save(*args,**kwargs)



class ProductReview(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    product = models.ForeignKey(Product , on_delete=models.CASCADE)
    comment = models.CharField(max_length =150,verbose_name = "Комментарии")
    image = models.ImageField(upload_to  = "Product_Review_images/", verbose_name = "Изобаржение продукта")

class Attribute(models.Model):
    name =models.CharField(max_length=80, verbose_name = "Имя Атрибута")
    type_attribute = models. CharField(max_length=100,verbose_name =" Тип Атрибута")

class ProductAttribute(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    attribute = models.ForeignKey(Attribute, on_delete=models.CASCADE)
    value = models.CharField(max_length=100,verbose_name ="Значение продукта")









