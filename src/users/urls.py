from django.urls import re_path
from drfpasswordless.settings import api_settings
from drfpasswordless.views import ObtainMobileCallbackToken
from .utils import OptionalSlashRouter
from rest_framework_simplejwt.views import TokenVerifyView

from .views import CustomObtainAuthTokenFromCallbackToken, UserProfileView, UserAddressView

app_name = 'users'


urlpatterns = [
    re_path(api_settings.PASSWORDLESS_AUTH_PREFIX + r'mobile/?$', ObtainMobileCallbackToken.as_view(), name='auth_mobile'),
    # re_path(api_settings.PASSWORDLESS_AUTH_PREFIX + r'email/?$', ObtainEmailCallbackToken.as_view(), name='auth_email'),
    re_path(api_settings.PASSWORDLESS_AUTH_PREFIX + r'customtoken/?$', CustomObtainAuthTokenFromCallbackToken.as_view(), name='auth_token'),
    re_path(r'token/verify/?$', TokenVerifyView.as_view(), name='token_verify'),
]


router = OptionalSlashRouter()
router.register(r'address/?', UserAddressView)
router.register(r'profile/?', UserProfileView)
urlpatterns += router.urls
