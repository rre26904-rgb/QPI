import discord
from discord.ext import commands
import asyncio
import sys
import os

# حل مشكلة الـ Event Loop لنظام ويندوز
if sys.platform == 'win32':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

# 🔒 تعديل التوكن: جلب التوكن بشكل آمن من متغيرات السيرفر (Railway)
TOKEN = os.getenv("DISCORD_TOKEN") 

intents = discord.Intents.default()
intents.message_content = True 
intents.guilds = True
intents.voice_states = True   # 👈 أضفناها عشان لو البوت فيه كوجات صوت يشتغل بدون مشاكل
intents.members = True        # 👈 أضفناها عشان الكوجات والألعاب تتعرف على الأعضاء

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f'======================================')
    print(f'تم تسجيل الدخول: {bot.user.name}')
    print(f'البوت جاهز والألعاب محملة تلقائياً!')
    print(f'======================================')

async def main():
    async with bot:
        # البحث التلقائي عن الملفات التي تنتهي بـ _cog.py في نفس المجلد
        current_dir = os.path.dirname(os.path.abspath(__file__))
        
        for filename in os.listdir(current_dir):
            if filename.endswith("_cog.py"):
                cog_name = filename[:-3] # حذف .py من الاسم
                try:
                    await bot.load_extension(cog_name)
                    print(f"✅ تم تحميل: {cog_name}")
                except Exception as e:
                    print(f"❌ فشل تحميل {cog_name}: {e}")
        
        # حماية إضافية: التأكد من أن التوكن تم تعريفه في السيرفر قبل التشغيل
        if not TOKEN:
            print("❌ خطأ: لم يتم العثور على متغير DISCORD_TOKEN في إعدادات Railway!")
            return
            
        await bot.start(TOKEN)

if __name__ == "__main__":
    asyncio.run(main())