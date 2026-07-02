import discord
from discord.ext import commands
import random
import asyncio
import json
import os


class khmngame(commands.Cog):
    def __init__(self, bot):    
        self.bot = bot
        self.scores_file = "global_points.json" # 🟢 اسم ملف النقاط الموحد والمشترك
        
        # 🟢 التأكد من وجود القفل العام المشترك داخل كائن البوت
        if not hasattr(self.bot, 'global_game_lock'):
            self.bot.global_game_lock = set()

        self.questions = [
            {"image": "خمن_1.png", "answer": "القلم"},
            {"image": "خمن_2.png", "answer": "الإبرة"},
            {"image": "خمن_3.png", "answer": "العمر"},
            {"image": "خمن_4.png", "answer": "الجوع"},
            {"image": "خمن_5.png", "answer": "الكرسي"},
            {"image": "خمن_6.png", "answer": "الإبرة"},
            {"image": "خمن_7.png", "answer": "الظل"},
            {"image": "خمن_8.png", "answer": "السحاب"},
            {"image": "خمن_9.png", "answer": "بيت الشعر"},
            {"image": "خمن_10.png", "answer": "المشط"},
            {"image": "خمن_11.png", "answer": "الحذاء"},
            {"image": "خمن_12.png", "answer": "الدبوس"},
            {"image": "خمن_13.png", "answer": "الشجرة"},
            {"image": "خمن_14.png", "answer": "البصل"},
            {"image": "خمن_15.png", "answer": "السمسم"},
            {"image": "خمن_16.png", "answer": "الزمن"},
            {"image": "خمن_17.png", "answer": "الفلفل"},
            {"image": "خمن_18.png", "answer": "الإسفنج"},
            {"image": "خمن_19.png", "answer": "صدى الصوت"},
            {"image": "خمن_20.png", "answer": "المرآة"},
            {"image": "خمن_21.png", "answer": "العمر"},
            {"image": "خمن_22.png", "answer": "النار"},
            {"image": "خمن_23.png", "answer": "الراديو"},
            {"image": "خمن_24.png", "answer": "الماء"},
            {"image": "خمن_25.png", "answer": "الإعصار"},
            {"image": "خمن_26.png", "answer": "النهر"},
            {"image": "خمن_27.png", "answer": "السور"},
            {"image": "خمن_28.png", "answer": "الحفرة"},
            {"image": "خمن_29.png", "answer": "المسمار"},
            {"image": "خمن_30.png", "answer": "الطائرة الورقية"},
            {"image": "خمن_31.png", "answer": "الريح"},
            {"image": "خمن_32.png", "answer": "الظل"},
            {"image": "خمن_33.png", "answer": "الفقاعة"},
            {"image": "خمن_34.png", "answer": "الشجرة"},
            {"image": "خمن_35.png", "answer": "الحصان"},
            {"image": "خمن_36.png", "answer": "البيض"},
            {"image": "خمن_37.png", "answer": "القفاز"},
            {"image": "خمن_38.png", "answer": "الثلج"},
            {"image": "خمن_39.png", "answer": "الصدى"},
            {"image": "خمن_40.png", "answer": "الضوء"},
            {"image": "خمن_41.png", "answer": "الهاتف"},
            {"image": "خمن_42.png", "answer": "الصمت"},
            {"image": "خمن_43.png", "answer": "النهر"},
            {"image": "خمن_44.png", "answer": "الطريق"},
            {"image": "خمن_45.png", "answer": "الباب"},
            {"image": "خمن_46.png", "answer": "المسمار"},
            {"image": "خمن_47.png", "answer": "الدائرة"},
            {"image": "خمن_48.png", "answer": "الحلوى"},
            {"image": "خمن_49.png", "answer": "الفطر"},
            {"image": "خمن_50.png", "answer": "البرد"},
            {"image": "خمن_51.png", "answer": "الطريق"},
            {"image": "خمن_52.png", "answer": "البيض"},
            {"image": "خمن_53.png", "answer": "القميص"},
            {"image": "خمن_54.png", "answer": "الخريطة"},
            {"image": "خمن_55.png", "answer": "الدخان"},
            {"image": "خمن_56.png", "answer": "الخريطة"},
            {"image": "خمن_57.png", "answer": "الحفرة"},
            {"image": "خمن_58.png", "answer": "الجليد"},
            {"image": "خمن_59.png", "answer": "النهر"},
            {"image": "خمن_60.png", "answer": "الضوء"},
            {"image": "خمن_61.png", "answer": "العمر"},
            {"image": "خمن_62.png", "answer": "البيانو"},
            {"image": "خمن_63.png", "answer": "الإبريق"},
            {"image": "خمن_64.png", "answer": "الساعة"},
            {"image": "خمن_65.png", "answer": "الساعة"},
            {"image": "خمن_66.png", "answer": "السرير"},
            {"image": "خمن_67.png", "answer": "العمر"},
            {"image": "خمن_68.png", "answer": "اسمك"},
            {"image": "خمن_69.png", "answer": "الدائرة"},
            {"image": "خمن_70.png", "answer": "الساعة"},
            {"image": "خمن_71.png", "answer": "الغد"},
            {"image": "خمن_72.png", "answer": "الضوء"},
            {"image": "خمن_73.png", "answer": "الظل"},
            {"image": "خمن_74.png", "answer": "البيض"},
            {"image": "خمن_75.png", "answer": "الليل"},
            {"image": "خمن_76.png", "answer": "الساعة"},
            {"image": "خمن_77.png", "answer": "حرف القاف"},
            {"image": "خمن_78.png", "answer": "السمك"},
            {"image": "خمن_79.png", "answer": "الخبرة"},
            {"image": "خمن_80.png", "answer": "الطاولة"},
            {"image": "خمن_81.png", "answer": "الرسالة"},
            {"image": "خمن_82.png", "answer": "الهواء"},
            {"image": "خمن_83.png", "answer": "السيارة"},
            {"image": "خمن_84.png", "answer": "الصدأ"},
            {"image": "خمن_85.png", "answer": "الضوء"},
            {"image": "خمن_86.png", "answer": "الطبل"},
            {"image": "خمن_87.png", "answer": "المسمار"},
            {"image": "خمن_88.png", "answer": "السر"},
            {"image": "خمن_89.png", "answer": "النجوم"},
            {"image": "خمن_90.png", "answer": "النهر"},
            {"image": "خمن_91.png", "answer": "الساعة"},
            {"image": "خمن_92.png", "answer": "الوسادة"},
            {"image": "خمن_93.png", "answer": "الكتاب"},
            {"image": "خمن_94.png", "answer": "العلم"},
            {"image": "خمن_95.png", "answer": "الكرسي"},
            {"image": "خمن_96.png", "answer": "الصمت"},
            {"image": "خمن_97.png", "answer": "النار"},
            {"image": "خمن_98.png", "answer": "المرآة"}
            
            
         ]


    # 🟢 دالة قراءة النقاط وتحديثها في الملف الموحد مباشرة
    def add_score(self, user_id):
        if os.path.exists(self.scores_file):
            with open(self.scores_file, "r", encoding="utf-8") as f:
                try:
                    scores = json.load(f)
                except json.JSONDecodeError:
                    scores = {}
        else:
            scores = {}
        
        user_id_str = str(user_id)
        scores[user_id_str] = scores.get(user_id_str, 0) + 1
        
        with open(self.scores_file, "w", encoding="utf-8") as f:
            json.dump(scores, f, ensure_ascii=False, indent=4)
            
        return scores[user_id_str]

    @commands.command(name="-خمن")
    async def start_game_cmd(self, ctx):
        await self.run_game(ctx.channel)

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return
        if message.content.strip() == "-خمن":
            await self.run_game(message.channel)

    async def run_game(self, channel):
        # 🟢 الفحص باستخدام القفل العام لمنع تشغيل اللعبة إذا كانت هناك لعبة أخرى نشطة
        if channel.id in self.bot.global_game_lock:
            return await channel.send("⚠️ هناك لعبة جارية بالفعل في هذا الروم! انتظر حتى تنتهي.")

        q = random.choice(self.questions)
        # 🟢 قفل الروم في البوت كاملاً
        self.bot.global_game_lock.add(channel.id)
        
        # 📂 تحديد مسار المجلد الذي يحتوي على الصور
        image_path = os.path.join("images", q["image"])

        # ⚙️ التحقق من أن ملف الصورة موجود فعلياً في المجلد
        if os.path.exists(image_path):
            file = discord.File(image_path, filename=q["image"])
            await channel.send(file=file)
        else:
            await channel.send(f"⚠️ خطأ: لم يتم العثور على ملف الصورة في المسار: `{image_path}`")
            self.bot.global_game_lock.discard(channel.id) # إلغاء القفل عند الخطأ
            return

        def check(m):
            return m.channel == channel and not m.author.bot

        try:
            while True:
                msg = await self.bot.wait_for("message", check=check, timeout=20.0)

                if msg.content.strip() == q["answer"]:
                    # 🟢 تحديث وحفظ النقاط في ملف الجيسون الموحد
                    new_score = self.add_score(msg.author.id)

                    embed = discord.Embed(
                        title="",
                        description=f" {msg.author.mention} فاز في اللعبة!",
                        color=discord.Color.green(),
                    )

                    view = discord.ui.View()
                    
                    # زر النقاط (شفاف/رمادي مع نجمة)
                    score_button = discord.ui.Button(
                        label=f" 𐙚        {new_score}",
                        style=discord.ButtonStyle.secondary,
                        disabled=True,
                    )

                    # الزر السحري (للدعم)
                    magic_button = discord.ui.Button(
                        label="⋆. 𐙚 ˚",
                        style=discord.ButtonStyle.secondary  
                    )

                    # الدالة اللي تتنفذ لما ينضغط الزر السحري
                    async def magic_callback(interaction: discord.Interaction):
                        await interaction.response.send_message(
                            "👋 أهلاً بك! هذا سيرفر الدعم الفني الخاص بنا. حياك الله:\nhttps://discord.gg/zkJpxjk2rN", 
                            ephemeral=True # هذي تخلي الرسالة تطلع للي ضغط الزر بس
                        )
                    
                    # ربط الدالة بالزر
                    magic_button.callback = magic_callback

                    # إضافة الأزرار للرسالة
                    view.add_item(score_button)
                    view.add_item(magic_button)

                    await channel.send(embed=embed, view=view)
                    break 
                else:
                    await msg.add_reaction("❌") 

        except asyncio.TimeoutError:
            await channel.send("⌛ انتهى الوقت! لم يقم أحد بالإجابة الصحيحة.")

        finally:
            # 🟢 فتح القفل العام المشترك فور انتهاء اللعبة
            self.bot.global_game_lock.discard(channel.id)


async def setup(bot):
    await bot.add_cog(khmngame(bot))