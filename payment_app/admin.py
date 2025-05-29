from django.contrib import admin

from django.contrib import admin

from .models import (
    Payment, PaymentItem
)

admin.site.register(Payment)
admin.site.register(PaymentItem)
