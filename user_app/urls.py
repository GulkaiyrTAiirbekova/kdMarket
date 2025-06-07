
from rest_framework import routers
from . import views


router = routers.DefaultRouter()

router.register(r'user-sign', views.UserApiView, basename='user_sign')
router.register(r'user-verify', views.SMSVerificationApiView, basename='user_verify')


urlpatterns = router.urls