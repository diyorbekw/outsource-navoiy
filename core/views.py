from django.shortcuts import render
from .models import Blog, FAQ, Risk, OneStopShopProgram, Client, Contact
from django.http import JsonResponse
import requests

# Create your views here.
def home(request):
    blogs = Blog.objects.all().order_by('-created_at')[:3]
    faqs = FAQ.objects.all()
    clients = Client.objects.all()
    return render(request, 'index.html', {'blogs': blogs, 'faqs': faqs, 'clients': clients})

def bpo(request):
    return render(request, 'bpo.html')

def explore(request):
    risks = Risk.objects.all()
    onestopshopprograms = OneStopShopProgram.objects.all()
    return render(request, 'explore.html', {'risks': risks, 'onestopshopprograms': onestopshopprograms})

def market(request):
    return render(request, 'market.html')

def why(request):
    return render(request, 'why.html')

def it_visa(request):
    return render(request, 'it.html')


def contact_view(request):
    if request.method == "POST":
        # qabul qilish: hozirgi HTML nomlarini ham, eski CamelCase'ni ham qabul qiladi
        first_name = request.POST.get('first_name') or request.POST.get('firstName')
        last_name  = request.POST.get('last_name')  or request.POST.get('lastName')
        email      = request.POST.get('email')
        phone      = request.POST.get('phone')      or request.POST.get('phone_number')
        company    = request.POST.get('company')    or request.POST.get('company_name')
        message    = request.POST.get('message')    or request.POST.get('text')

        # DEBUG: server konsolga POST ichini ko'rsat (keyin olib tashla)
        print("CONTACT POST:", request.POST)

        # minimal validatsiya
        if not first_name or not last_name or not email or not message:
            return JsonResponse({
                "success": False,
                "error": "Required fields missing",
                "received": dict(request.POST)
            }, status=400)

        contact = Contact.objects.create(
            first_name=first_name,
            last_name=last_name,
            email=email,
            phone_number=phone,
            company_name=company,
            text=message
        )

        # Telegram yuborish (TOKENni environment dan oling — xavfsizlik uchun)
        BOT_TOKEN = "7496528180:AAGkAUPuZV3QCsd1svipSL6gcnC0x1sghlA"
        CHAT_ID = "5515940993"
        text = (
            f"📩 *Yangi murojaat keldi!*\n\n"
            f"👤 Ism: {first_name} {last_name}\n"
            f"📧 Email: {email}\n"
            f"📞 Telefon: {phone}\n"
            f"🏢 Kompaniya: {company}\n\n"
            f"💬 Xabar:\n{message}"
        )

        try:
            requests.post(
                f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
                data={"chat_id": CHAT_ID, "text": text, "parse_mode": "Markdown"}
            )
        except Exception as e:
            print("Telegram error:", e)

    blogs = Blog.objects.all().order_by('-created_at')[:3]
    faqs = FAQ.objects.all()
    clients = Client.objects.all()
    return render(request, 'index.html', {'blogs': blogs, 'faqs': faqs, 'clients': clients})