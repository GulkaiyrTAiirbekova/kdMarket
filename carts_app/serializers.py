from rest_framework import serializers
from .models import Cart
from .models import Favourites

class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        field = '__all__'


class FavouritesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favourites
        field = '__all__'
