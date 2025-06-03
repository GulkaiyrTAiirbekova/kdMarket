from django.contrib import admin

from django.contrib import admin

from .models import (
    Payment, PaymentItem
)

admin.site.register(Payment)
admin.site.register(PaymentItem)
#from path.to.your.admin_site_class import AdminSite  # замени путь на свой
#custom_admin_site = AdminSite(name="custom_admin")