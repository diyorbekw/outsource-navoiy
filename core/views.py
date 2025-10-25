from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from django.utils import timezone
from datetime import timedelta
from django.db.models import Q
from .models import (
    Client, FAQ, Blog, Risk,
    OneStopShopProgram, OutSourcingService, Contact,
    SuccessNumber, SpecialCategories, SpecialService
)
from .serializers import (
    ClientSerializer, FAQSerializer, BlogSerializer,
    RiskSerializer, OneStopShopProgramSerializer,
    OutSourcingServiceSerializer, ContactSerializer,
    SuccessNumberSerializer, SpecialCategoriesSerializer, SpecialServiceSerializer
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

# --- CRUD API-lar ---
class ClientViewSet(viewsets.ModelViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context

class FAQViewSet(viewsets.ModelViewSet):
    queryset = FAQ.objects.all()
    serializer_class = FAQSerializer

class BlogViewSet(viewsets.ModelViewSet):
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer
    pagination_class = BlogPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    search_fields = ['title', 'description', 'content', 'creator']

    def get_queryset(self):
        queryset = super().get_queryset()
        return BlogFilter.filter_queryset(self.request, queryset)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context

    def list(self, request, *args, **kwargs):
        """Blog listini qaytarish filtrlash va paginatsiya bilan"""
        queryset = self.filter_queryset(self.get_queryset())
        
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

class RiskViewSet(viewsets.ModelViewSet):
    queryset = Risk.objects.all()
    serializer_class = RiskSerializer

class OneStopShopProgramViewSet(viewsets.ModelViewSet):
    queryset = OneStopShopProgram.objects.all()
    serializer_class = OneStopShopProgramSerializer

class OutSourcingServiceViewSet(viewsets.ModelViewSet):
    queryset = OutSourcingService.objects.all()
    serializer_class = OutSourcingServiceSerializer

class ContactViewSet(viewsets.ModelViewSet):
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

# --- Maxsus GET API-lar ---
class SuccessNumberViewSet(viewsets.ViewSet):
    """
    SuccessNumber uchun faqat GET so'rovi (birinchi yozuvni qaytaradi)
    """
    def list(self, request):
        success_number = SuccessNumber.objects.first()
        if success_number:
            serializer = SuccessNumberSerializer(success_number)
            return Response(serializer.data)
        return Response({"detail": "Ma'lumot topilmadi"}, status=status.HTTP_404_NOT_FOUND)

class SpecialCategoriesViewSet(viewsets.ViewSet):
    """
    SpecialCategories uchun faqat GET so'rovi (barcha kategoriyalarni qaytaradi)
    """
    def list(self, request):
        categories = SpecialCategories.objects.all()
        serializer = SpecialCategoriesSerializer(categories, many=True)
        return Response(serializer.data)

class SpecialServiceViewSet(viewsets.ViewSet):
    """
    SpecialService uchun faqat GET so'rovi
    - Barcha servislarni yoki kategoriya bo'yicha filtrlash
    """
    def list(self, request):
        category_id = request.query_params.get('category_id')
        
        if category_id:
            services = SpecialService.objects.filter(category_id=category_id)
        else:
            services = SpecialService.objects.all()
            
        serializer = SpecialServiceSerializer(services, many=True, context={'request': request})
        return Response(serializer.data)