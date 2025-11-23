import asyncio
from aiogram import Bot, Dispatcher, types
import sqlite3
import aiohttp
import io
import base64

TOKEN = "8426824622:AAFjedbJoP5AIQQ_9iHj3Tllp-bKbSgEII8"
CHANNEL_ID = -1003470682478
DB_NAME = "posts.db"
API_URL = "http://outsource.sifatdev.uz/api/blogs/"

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
def build_post_dict(message: types.Message):
    text = message.text or message.caption or ""
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
    
    # Content - qolgan barcha qatorlar
    content = "\n".join(non_empty_lines[2:]) if len(non_empty_lines) > 2 else ""

    minutes_to_read = max(1, len(text) // 1000)

    main_image = None
    if message.photo:
        main_image = message.photo[-1]

    result = {
        "title": title,
        "description": description,
        "content": content,
        "minutes_to_read": minutes_to_read,
        "creator": "IT PARK NAVOIY",
        "main_image": main_image,
        "content_image": main_image,
    }
    return result


async def download_image(bot, photo):
    """Rasmni yuklab olish va base64 formatga o'tkazish"""
    try:
        file = await bot.get_file(photo.file_id)
        downloaded = await bot.download_file(file.file_path)
        image_bytes = downloaded.read()
        
        # Base64 ga o'tkazish
        image_base64 = base64.b64encode(image_bytes).decode('utf-8')
        return image_base64
    except Exception as e:
        print(f"Rasm yuklab olishda xato: {e}")
        return None


async def send_to_api(blog_data):
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
            if blog_data.get('main_image_base64'):
                # Base64 ni faylga aylantirish
                image_data = base64.b64decode(blog_data['main_image_base64'])
                
                # Asosiy rasm
                form_data.add_field('main_image', 
                                  io.BytesIO(image_data),
                                  filename='main_image.jpg',
                                  content_type='image/jpeg')
                
                # Kontent rasmi (bir xil rasm)
                form_data.add_field('content_image', 
                                  io.BytesIO(image_data),
                                  filename='content_image.jpg', 
                                  content_type='image/jpeg')
            
            print(f"APIga yuborilayotgan ma'lumotlar:")
            print(f"Title: {blog_data['title']}")
            print(f"Description: {blog_data['description']}")
            print(f"Content uzunligi: {len(blog_data['content'])}")
            print(f"Creator: {blog_data['creator']}")
            print(f"Minutes to read: {blog_data['minutes_to_read']}")
            
            async with session.post(API_URL, data=form_data) as response:
                response_text = await response.text()
                print(f"API javobi: {response.status} - {response_text}")
                
                if response.status == 201:
                    print("✅ Ma'lumot APIga muvaffaqiyatli yuborildi")
                    return True
                else:
                    print(f"❌ APIga yuborishda xato: {response.status}")
                    return False
                    
    except Exception as e:
        print(f"❌ API ulanishida xato: {e}")
        return False


# --- save_post ---
async def save_post(message: types.Message):
    d = build_post_dict(message)

    # Rasmni yuklab olish
    main_image_base64 = None
    if message.photo:
        print("Rasm yuklanmoqda...")
        main_image_base64 = await download_image(message.bot, message.photo[-1])
        if main_image_base64:
            print("Rasm muvaffaqiyatli yuklandi")
            d['main_image_base64'] = main_image_base64
        else:
            print("Rasm yuklash muvaffaqiyatsiz")

    print(f"Title uzunligi: {len(d['title'])}")
    print(f"Description uzunligi: {len(d['description'])}")
    print(f"Content uzunligi: {len(d['content'])}")

    # APIga yuborish
    api_success = await send_to_api(d)
    
    if api_success:
        # Ma'lumotlar bazasiga ham saqlash (ixtiyoriy)
        conn = sqlite3.connect(DB_NAME)
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO posts (message_id, text, image) VALUES (?, ?, ?)",
            (message.message_id, d["title"] + "\n" + d["description"] + "\n" + d["content"], main_image_base64)
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
        await save_post(message)
        print(f"Saved post {message.message_id}")


async def main():
    init_db()
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())