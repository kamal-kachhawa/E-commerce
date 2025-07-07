from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from api.views import EmailTokenObtainPairView


urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/user/", include("api.urls")),
    path("api/", include("myapp.urls")),
    path("api/token/", EmailTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    # path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    # path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    # path("api/excel/", include("myapp.urls")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
