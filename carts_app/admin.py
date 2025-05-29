from django.contrib import admin

from django.contrib import admin

from .models import (
    Cart, Favourites
)

admin.site.register(Cart)
admin.site.register(Favourites)
