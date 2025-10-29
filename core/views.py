from rest_framework import viewsets, status, mixins
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework.decorators import action
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from django.utils import timezone
from datetime import timedelta
from django.db.models import Q
from rest_framework.viewsets import ReadOnlyModelViewSet
from .models import (
    Client, FAQ, Blog, Risk,
    OneStopShopProgram, OutSourcingService, Contact,
    SuccessNumber, SpecialCategories, SpecialService,
    Education, InvestorProgram, Statistics, Tax
)
from .serializers import (
    ClientSerializer, FAQSerializer, BlogSerializer,
    RiskSerializer, OneStopShopProgramSerializer,
    OutSourcingServiceSerializer, ContactSerializer,
    SuccessNumberSerializer, SpecialCategoriesSerializer, 
    SpecialServiceSerializer, EducationSerializer,
    InvestorProgramSerializer, StatisticsSerializer, TaxSerializer
)
import requests

# --- Pagination ---
class BlogPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

# --- Blog Filter ---
class BlogFilter:
    @staticmethod
    def filter_queryset(request, queryset):
        period = request.query_params.get('period')
        search = request.query_params.get('search')
        
        # Vaqt bo'yicha filtrlash
        if period:
            now = timezone.now()
            if period == 'weekly':
                start_date = now - timedelta(days=7)
                queryset = queryset.filter(created_at__gte=start_date)
            elif period == 'monthly':
                start_date = now - timedelta(days=30)
                queryset = queryset.filter(created_at__gte=start_date)
            elif period == 'yearly':
                start_date = now - timedelta(days=365)
                queryset = queryset.filter(created_at__gte=start_date)
        
        # Qidiruv
        if search:
            queryset = queryset.filter(
                Q(title__icontains=search) |
                Q(description__icontains=search) |
                Q(content__icontains=search) |
                Q(creator__icontains=search)
            )
        
        return queryset

# --- Base ReadOnly ViewSet ---
class ReadOnlyViewSet(mixins.ListModelMixin, 
                     mixins.RetrieveModelMixin, 
                     viewsets.GenericViewSet):
    """
    Faqat GET so'rovlari (list va retrieve) uchun base ViewSet
    """
    pass

# --- CRUD API-lar ---
class ClientViewSet(ReadOnlyViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context

class FAQViewSet(ReadOnlyViewSet):
    queryset = FAQ.objects.all()
    serializer_class = FAQSerializer

class BlogViewSet(ReadOnlyModelViewSet):
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer
    pagination_class = BlogPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    search_fields = ['title', 'description', 'content', 'creator']
    lookup_field = 'slug'  # <-- Asosiy o‘zgarish shu yerda

    def get_queryset(self):
        queryset = super().get_queryset()
        return BlogFilter.filter_queryset(self.request, queryset)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context

class RiskViewSet(ReadOnlyViewSet):
    queryset = Risk.objects.all()
    serializer_class = RiskSerializer

class OneStopShopProgramViewSet(ReadOnlyViewSet):
    queryset = OneStopShopProgram.objects.all()
    serializer_class = OneStopShopProgramSerializer

class OutSourcingServiceViewSet(ReadOnlyViewSet):
    queryset = OutSourcingService.objects.all()
    serializer_class = OutSourcingServiceSerializer

class ContactViewSet(mixins.CreateModelMixin,
                    mixins.ListModelMixin,
                    mixins.RetrieveModelMixin,
                    viewsets.GenericViewSet):
    """
    Contact uchun GET (list, retrieve) va POST methodlari
    """
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer

    def create(self, request, *args, **kwargs):
        """POST orqali kelgan xabarni saqlash va Telegramga yuborish"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        contact = serializer.save()

        # Telegramga yuborish
        BOT_TOKEN = "7496528180:AAGkAUPuZV3QCsd1svipSL6gcnC0x1sghlA"
        CHAT_ID = "5515940993"

        text = (
            f"📩 *Yangi murojaat!*\n\n"
            f"👤 Ism: {contact.first_name} {contact.last_name}\n"
            f"📧 Email: {contact.email}\n"
            f"📞 Telefon: {contact.phone_number}\n"
            f"🏢 Kompaniya: {contact.company_name}\n\n"
            f"💬 Xabar:\n{contact.text}"
        )

        try:
            requests.post(
                f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
                data={"chat_id": CHAT_ID, "text": text, "parse_mode": "Markdown"},
                timeout=10
            )
        except Exception as e:
            print(f"Telegram xatosi: {e}")

        return Response(serializer.data, status=status.HTTP_201_CREATED)

class SuccessNumberViewSet(ReadOnlyViewSet):
    """
    SuccessNumber uchun faqat GET so'rovi
    """
    queryset = SuccessNumber.objects.all()
    serializer_class = SuccessNumberSerializer

class SpecialCategoriesViewSet(ReadOnlyViewSet):
    """
    SpecialCategories uchun faqat GET so'rovi
    """
    queryset = SpecialCategories.objects.all()
    serializer_class = SpecialCategoriesSerializer

class SpecialServiceViewSet(ReadOnlyViewSet):
    """
    SpecialService uchun faqat GET so'rovi
    """
    queryset = SpecialService.objects.all()
    serializer_class = SpecialServiceSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['category']

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context

class EducationViewSet(ReadOnlyViewSet):
    """
    Education uchun faqat GET so'rovi
    """
    queryset = Education.objects.all()
    serializer_class = EducationSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context

class InvestorProgramViewSet(ReadOnlyViewSet):
    """
    InvestorProgram uchun faqat GET so'rovi
    """
    queryset = InvestorProgram.objects.all()
    serializer_class = InvestorProgramSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context

class StatisticsViewSet(ReadOnlyViewSet):
    """
    Statistics uchun faqat GET so'rovi
    """
    queryset = Statistics.objects.all()
    serializer_class = StatisticsSerializer

class TaxViewSet(ReadOnlyViewSet):
    """
    Tax uchun faqat GET so'rovi
    """
    queryset = Tax.objects.all()
    serializer_class = TaxSerializer