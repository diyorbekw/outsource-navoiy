from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import (
    Client, FAQ, Blog, Risk,
    OneStopShopProgram, OutSourcingService, Contact
)
from .serializers import (
    ClientSerializer, FAQSerializer, BlogSerializer,
    RiskSerializer, OneStopShopProgramSerializer,
    OutSourcingServiceSerializer, ContactSerializer
)
import requests


# --- CRUD API-lar ---
class ClientViewSet(viewsets.ModelViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer


class FAQViewSet(viewsets.ModelViewSet):
    queryset = FAQ.objects.all()
    serializer_class = FAQSerializer


class BlogViewSet(viewsets.ModelViewSet):
    queryset = Blog.objects.all().order_by('-created_at')
    serializer_class = BlogSerializer


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
