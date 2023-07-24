from django.contrib import admin
from django.urls import path, include

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


urlpatterns = [
    path('', include('restaurant.urls')),
    path('admin/', admin.site.urls),

    path('auth/', include('djoser.urls')),
    path('api/', include('api.urls')),
    path('api/token/login/', TokenObtainPairView.as_view(), name='token-login'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token-refresh'),
]
