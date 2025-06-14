from django.contrib import admin
from django.urls import path,include
from rest_framework import routers
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView
from goods_app.urls import router as goods_router
from carts_app.urls import router as carts_router
from orders_app.urls import router as orders_router
from payment_app.urls import router as payment_router
from user_app.urls import router as user_router



router = routers.DefaultRouter()

router.registry.extend(goods_router.registry)
router.registry.extend(carts_router.registry)
router.registry.extend(orders_router.registry)
router.registry.extend(payment_router.registry)
router.registry.extend(user_router.registry)




urlpatterns = [
    path('admin/', admin.site.urls),
    path("api/", include(router.urls)),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    # Optional UI:
    path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    #path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]
