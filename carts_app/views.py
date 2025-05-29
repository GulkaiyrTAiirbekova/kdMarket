from django.shortcuts import render
from rest_framework import viewsets

from carts_app.models import Cart, Favourites
from carts_app.serializers import CartSerializer, FavouritesSerializer


class CartView(viewsets.ModelViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer


class FavouritesView(viewsets.ModelViewSet):
    queryset = Favourites.objects.all()
    serializer_class = FavouritesSerializer

