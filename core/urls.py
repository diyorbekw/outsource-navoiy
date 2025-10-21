from django.urls import path, include
from rest_framework import permissions
from rest_framework.routers import DefaultRouter
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from .views import (
    ClientViewSet, FAQViewSet, BlogViewSet, RiskViewSet,
    OneStopShopProgramViewSet, OutSourcingServiceViewSet, ContactViewSet
)

# --- API router ---
router = DefaultRouter()
router.register(r'clients', ClientViewSet)
router.register(r'faqs', FAQViewSet)
router.register(r'blogs', BlogViewSet)
router.register(r'risks', RiskViewSet)
router.register(r'onestopshopprograms', OneStopShopProgramViewSet)
router.register(r'outsourcingservices', OutSourcingServiceViewSet)
router.register(r'contacts', ContactViewSet)

# --- Swagger konfiguratsiyasi ---
schema_view = get_schema_view(
    openapi.Info(
        title="Company API",
        default_version='v1',
        description="Bizning API hujjatlarimiz (Swagger orqali)",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="support@yourcompany.com"),
        license=openapi.License(name="MIT License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('api/', include(router.urls)),

    # Swagger UI
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),

    # Redoc (alternativ interfeys)
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
