import asyncio
from aiogram import Bot, Dispatcher, types
import sqlite3
import aiohttp
import io
import base64
import json
from html import escape
from collections import defaultdict

TOKEN = "8426824622:AAFjedbJoP5AIQQ_9iHj3Tllp-bKbSgEII8"
CHANNEL_ID = -1003470682478
DB_NAME = "posts.db"
API_URL = "https://outsource.sifatdev.uz/api/blogs/"

# Media grouplarni saqlash uchun
media_groups = defaultdict(list)
media_group_tasks = {}  # Har bir media group uchun vazifa

# --- SQLite ---
def init_db():
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS posts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            message_id INTEGER,
            text TEXT,
            image BLOB
        )
    """)
    conn.commit()
    conn.close()


# --- Utils for parsing post into dict ---
def build_post_dict(text, images_count=0):
    """Matn va rasmlar soniga asoslanib post ma'lumotlarini yaratish"""
    
    lines = text.strip().split("\n")
    
    # Bo'sh qatorlarni olib tashlash
    non_empty_lines = [line.strip() for line in lines if line.strip()]
    
    title = non_empty_lines[0] if len(non_empty_lines) > 0 else ""
    
    # Description - faqat 2-abzas va 120 belgidan oshmasligi kerak
    description = ""
    if len(non_empty_lines) > 1:
        description = non_empty_lines[1]
        # Description ni 120 belgiga cheklash
        if len(description) > 120:
            description = description[:117] + "..."

    # Content - qolgan barcha qatorlar (HTML formatda)
    content_lines = non_empty_lines[2:] if len(non_empty_lines) > 2 else []
    content = "<br>".join(content_lines)

    minutes_to_read = max(1, len(text) // 1000)

    result = {
        "title": title,
        "description": description,
        "content": content,
        "minutes_to_read": minutes_to_read,
        "creator": "IT PARK NAVOIY",
    }
    return result


async def download_image(bot, photo):
    """Rasmni yuklab olish"""
    try:
        file = await bot.get_file(photo.file_id)
        downloaded = await bot.download_file(file.file_path)
        image_bytes = downloaded.read()
        return image_bytes
    except Exception as e:
        print(f"Rasm yuklab olishda xato: {e}")
        return None


async def build_rich_content(text, images):
    """Rich text content yaratish - barcha qo'shimcha rasmlarni contentga qo'shish"""
    # Asosiy matnni HTML formatga o'tkazish
    html_content = escape(text).replace('\n', '<br>')
    
    # Agar ko'p rasm bo'lsa, ularni content boshiga qo'shish
    if len(images) > 1:
        image_tags = []
        for i, image_bytes in enumerate(images[1:], 1):
            # Rasmlarni base64 formatda contentga qo'shish
            image_base64 = base64.b64encode(image_bytes).decode('utf-8')
            image_tag = f'<img src="data:image/jpeg;base64,{image_base64}" alt="Image {i}" style="max-width: 100%; margin: 10px 0;">'
            image_tags.append(image_tag)
        
        # Rasmlarni content boshiga qo'shish
        html_content = "<br>".join(image_tags) + "<br><br>" + html_content
    
    return html_content


async def send_to_api(blog_data, main_image_bytes=None, content_image_bytes=None):
    """Ma'lumotlarni Django APIga yuborish"""
    try:
        async with aiohttp.ClientSession() as session:
            # FormData yaratish
            form_data = aiohttp.FormData()
            
            # Matn ma'lumotlari
            form_data.add_field('title', blog_data['title'])
            form_data.add_field('description', blog_data['description'])
            form_data.add_field('content', blog_data['content'])
            form_data.add_field('creator', blog_data['creator'])
            form_data.add_field('minutes_to_read', str(blog_data['minutes_to_read']))
            
            # Rasmlarni qo'shish
            if main_image_bytes:
                # Asosiy rasm
                form_data.add_field('main_image', 
                                  io.BytesIO(main_image_bytes),
                                  filename='main_image.jpg',
                                  content_type='image/jpeg')
            
            if content_image_bytes:
                # Kontent rasmi (main image bilan bir xil)
                form_data.add_field('content_image', 
                                  io.BytesIO(content_image_bytes),
                                  filename='content_image.jpg', 
                                  content_type='image/jpeg')
            elif main_image_bytes:
                # Agar alohida content image berilmagan bo'lsa, main_imageni ishlat
                form_data.add_field('content_image', 
                                  io.BytesIO(main_image_bytes),
                                  filename='content_image.jpg', 
                                  content_type='image/jpeg')
            
            print(f"APIga yuborilayotgan ma'lumotlar:")
            print(f"Title: {blog_data['title']}")
            print(f"Description: {blog_data['description']}")
            print(f"Content uzunligi: {len(blog_data['content'])}")
            print(f"Creator: {blog_data['creator']}")
            print(f"Minutes to read: {blog_data['minutes_to_read']}")
            print(f"Asosiy rasm mavjud: {'Ha' if main_image_bytes else 'Yoq'}")
            print(f"Kontent rasmi mavjud: {'Ha' if content_image_bytes else 'Yoq'}")
            
            headers = {
                'User-Agent': 'TelegramBot/1.0',
                'Accept': 'application/json',
            }
            
            async with session.post(API_URL, data=form_data, headers=headers) as response:
                response_text = await response.text()
                print(f"API javobi: {response.status} - {response_text}")
                
                try:
                    response_data = json.loads(response_text)
                    if response.status == 201:
                        print("✅ Ma'lumot APIga muvaffaqiyatli yuborildi")
                        return True
                    else:
                        print(f"❌ APIga yuborishda xato: {response.status}")
                        print(f"Xato tafsilotlari: {response_data}")
                        return False
                except json.JSONDecodeError:
                    print(f"❌ JSON javobini o'qib bo'lmadi: {response_text}")
                    return False
                    
    except Exception as e:
        print(f"❌ API ulanishida xato: {e}")
        return False


async def process_media_group(media_group_id, bot):
    """Media groupni qayta ishlash - FAQAT BIR MARTA CHAQIRILADI"""
    if media_group_id not in media_groups:
        print(f"Media group {media_group_id} topilmadi")
        return
    
    messages_data = media_groups[media_group_id]
    
    print(f"🎯 Media groupni qayta ishlash: {media_group_id}, {len(messages_data)} ta xabar")
    
    # Birinchi xabardan matn olish (odatda birinchi xabarda matn bor)
    text = ""
    main_message_id = None
    
    for msg_data in messages_data:
        if msg_data.get('text') or msg_data.get('caption'):
            text = msg_data.get('text') or msg_data.get('caption') or ""
            main_message_id = msg_data.get('message_id')
            print(f"📝 Matn topildi: {text[:100]}...")
            break
    
    if not text.strip():
        print("❌ Media groupda matn topilmadi")
        # Media groupni tozalash
        if media_group_id in media_groups:
            del media_groups[media_group_id]
        if media_group_id in media_group_tasks:
            del media_group_tasks[media_group_id]
        return
    
    # Barcha rasmlarni yuklab olish
    all_images = []
    for i, msg_data in enumerate(messages_data):
        if msg_data.get('photo'):
            print(f"🖼️ {i+1}-rasm yuklanmoqda...")
            image_bytes = await download_image(bot, msg_data['photo'])
            if image_bytes:
                all_images.append(image_bytes)
                print(f"✅ {i+1}-rasm yuklandi, hajmi: {len(image_bytes)} bayt")
    
    print(f"📊 Jami {len(all_images)} ta rasm yuklandi")
    
    # Post ma'lumotlarini yaratish
    d = build_post_dict(text, len(all_images))
    
    # Rich content yaratish (qo'shimcha rasmlarni contentga qo'shish)
    rich_content = await build_rich_content(text, all_images)
    d['content'] = rich_content

    print(f"📄 Media group post:")
    print(f"   Title: {d['title']}")
    print(f"   Description: {d['description']}")
    print(f"   Content uzunligi: {len(d['content'])}")
    print(f"   Rasmlar soni: {len(all_images)}")

    # Rasmlarni taqsimlash
    main_image_bytes = None
    content_image_bytes = None
    
    if len(all_images) >= 1:
        main_image_bytes = all_images[0]  # Birinchi rasm
        content_image_bytes = all_images[0]  # Content image ham birinchi rasm
        print(f"🎯 Asosiy rasm tanlandi")

    # FAQAT BIR MARTA APIga yuborish
    print("🚀 APIga BIR MARTA yuborilmoqda...")
    api_success = await send_to_api(d, main_image_bytes, content_image_bytes)
    
    if api_success:
        print("✅ Media group post APIga muvaffaqiyatli yuborildi")
        
        # Ma'lumotlar bazasiga saqlash (faqat bitta post)
        conn = sqlite3.connect(DB_NAME)
        cur = conn.cursor()
        
        image_base64 = base64.b64encode(main_image_bytes).decode('utf-8') if main_image_bytes else None
        
        cur.execute(
            "INSERT INTO posts (message_id, text, image) VALUES (?, ?, ?)",
            (main_message_id, text, image_base64)
        )
        conn.commit()
        conn.close()
        
        print("💾 Ma'lumotlar saqlandi")
    else:
        print("❌ Media group post APIga yuborish muvaffaqiyatsiz")
    
    # Media groupni tozalash
    if media_group_id in media_groups:
        del media_groups[media_group_id]
    if media_group_id in media_group_tasks:
        del media_group_tasks[media_group_id]


async def schedule_media_group_processing(media_group_id, bot):
    """Media groupni qayta ishlashni rejalashtirish"""
    # Agar allaqachon vazifa boshlasa, yangisini yaratmaslik
    if media_group_id in media_group_tasks:
        return
    
    # Yangi vazifa yaratish
    media_group_tasks[media_group_id] = asyncio.create_task(
        process_media_group_delayed(media_group_id, bot)
    )


async def process_media_group_delayed(media_group_id, bot):
    """Media groupni kechiktirib qayta ishlash"""
    # 2 soniya kutish (barcha xabarlar kelishi uchun)
    await asyncio.sleep(2)
    
    # Media groupni qayta ishlash
    await process_media_group(media_group_id, bot)


async def save_single_post(message: types.Message):
    """Yakka postni saqlash"""
    text = message.text or message.caption or ""
    
    # Post ma'lumotlarini yaratish
    d = build_post_dict(text)

    # Rasmlarni yuklab olish
    main_image_bytes = None
    content_image_bytes = None

    if message.photo:
        print("🖼️ Rasm yuklanmoqda...")
        main_image_bytes = await download_image(message.bot, message.photo[-1])
        if main_image_bytes:
            print(f"✅ Rasm muvaffaqiyatli yuklandi, hajmi: {len(main_image_bytes)} bayt")
            content_image_bytes = main_image_bytes

    # Rich content yaratish
    rich_content = await build_rich_content(text, [main_image_bytes] if main_image_bytes else [])
    d['content'] = rich_content

    print(f"📄 Yakka post:")
    print(f"   Title: {d['title']}")
    print(f"   Description: {d['description']}")
    print(f"   Content uzunligi: {len(d['content'])}")

    # APIga yuborish
    api_success = await send_to_api(d, main_image_bytes, content_image_bytes)
    
    if api_success:
        # Ma'lumotlar bazasiga saqlash
        conn = sqlite3.connect(DB_NAME)
        cur = conn.cursor()
        
        image_base64 = base64.b64encode(main_image_bytes).decode('utf-8') if main_image_bytes else None
        
        cur.execute(
            "INSERT INTO posts (message_id, text, image) VALUES (?, ?, ?)",
            (message.message_id, text, image_base64)
        )
        conn.commit()
        conn.close()
        
        print("✅ Ma'lumotlar saqlandi va APIga yuborildi")
    else:
        print("❌ APIga yuborish muvaffaqiyatsiz, ma'lumotlar saqlanmadi")


# --- Bot ---
bot = Bot(token=TOKEN)
dp = Dispatcher()


@dp.channel_post()
async def channel_listener(message: types.Message):
    if message.chat.id == CHANNEL_ID:
        # Media groupni tekshirish
        if message.media_group_id:
            media_group_id = message.media_group_id
            print(f"📦 Media group aniqlandi: {media_group_id}")
            
            # Xabarni media groupga qo'shish
            media_data = {
                'message_id': message.message_id,
                'text': message.text or message.caption or "",
                'photo': message.photo[-1] if message.photo else None
            }
            media_groups[media_group_id].append(media_data)
            
            print(f"➕ Media group {media_group_id} ga xabar qo'shildi. Jami: {len(media_groups[media_group_id])} ta")
            
            # Media groupni qayta ishlashni rejalashtirish
            await schedule_media_group_processing(media_group_id, message.bot)
            
        else:
            # Yakka post
            print(f"📄 Yakka post qayta ishlanmoqda: {message.message_id}")
            await save_single_post(message)
        
        print(f"💾 Saved post {message.message_id}")


async def main():
    init_db()
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())