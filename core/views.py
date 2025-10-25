from rest_framework import viewsets, status
from rest_framework.response import Response
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
    queryset = Blog.objects.all().order_by('-created_at')
    serializer_class = BlogSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context

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