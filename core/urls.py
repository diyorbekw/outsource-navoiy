from django.urls import path, include
from rest_framework import permissions
from rest_framework.routers import DefaultRouter
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from .views import (
    ClientViewSet, FAQViewSet, BlogViewSet, RiskViewSet,
    OneStopShopProgramViewSet, OutSourcingServiceViewSet, ContactViewSet,
    SuccessNumberViewSet, SpecialCategoriesViewSet, SpecialServiceViewSet,
    EducationViewSet, InvestorProgramViewSet, StatisticsViewSet, TaxViewSet
)

# --- API router ---
router = DefaultRouter()
router.register(r'clients', ClientViewSet, basename='clients')
router.register(r'faqs', FAQViewSet, basename='faqs')
router.register(r'blogs', BlogViewSet, basename='blogs')
router.register(r'risks', RiskViewSet, basename='risks')
router.register(r'onestopshopprograms', OneStopShopProgramViewSet, basename='onestopshopprograms')
router.register(r'outsourcingservices', OutSourcingServiceViewSet, basename='outsourcingservices')
router.register(r'contacts', ContactViewSet, basename='contacts')
router.register(r'successnumbers', SuccessNumberViewSet, basename='successnumbers')
router.register(r'specialcategories', SpecialCategoriesViewSet, basename='specialcategories')
router.register(r'specialservices', SpecialServiceViewSet, basename='specialservices')
router.register(r'educations', EducationViewSet, basename='educations')
router.register(r'investorprograms', InvestorProgramViewSet, basename='investorprograms')
router.register(r'statistics', StatisticsViewSet, basename='statistics')
router.register(r'taxes', TaxViewSet, basename='taxes')

# --- Swagger konfiguratsiyasi ---
schema_view = get_schema_view(
    openapi.Info(
        title="Company API",
        default_version='v1',
        description="""
        Bizning kompaniya API hujjatlari.
        
        ## Foydalanish:
        - Barcha endpointlar faqat **GET** so'rovlarini qabul qiladi
        - Faqat **Contact** endpointi **POST** so'rovini qabul qiladi
        
        ## Filterlar:
        - **Blogs**: `search`, `period` (weekly, monthly, yearly) parametrlari orqali filtrlash
        - **SpecialServices**: `category` parametri orqali filtrlash
        
        ## Pagination:
        - **Blogs**: Sahifalash mavjud (page_size=10)
        """,
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
    
    # API schema (JSON formatda)
    path('swagger.json', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger.yaml', schema_view.without_ui(cache_timeout=0), name='schema-yaml'),
]