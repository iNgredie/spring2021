from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView


urlpatterns = [
    path('admin/', admin.site.urls),
    # My apps
    path('api/v1/', include('src.users.urls')),
    path('api/v1/', include('src.send_values.urls')),
    path('api/v1/', include('src.tasks.urls')),
    path('api/v1/', include('src.articles.urls')),
    path('api/v1/', include('src.dynamic_settings.urls')),
    path('api/v1/', include('src.services.urls')),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    # Optional UI:
    path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
