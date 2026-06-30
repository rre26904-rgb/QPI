import discord
from discord.ext import commands
import random
import asyncio
import json
import os


class ssagame(commands.Cog):
    def __init__(self, bot):    
        self.bot = bot
        self.scores_file = "global_points.json" # 🟢 اسم ملف النقاط الموحد والمشترك
        
        # 🟢 التأكد من وجود القفل العام المشترك داخل كائن البوت
        if not hasattr(self.bot, 'global_game_lock'):
            self.bot.global_game_lock = set()

        self.questions = [
            {"image": "صحح_1.png", "answer": "سيارة"},
            {"image": "صحح_2.png", "answer": "طاولة"},
            {"image": "صحح_3.png", "answer": "شاشة"},
            {"image": "صحح_4.png", "answer": "لوحة"},
            {"image": "صحح_5.png", "answer": "مدرسته"},
            {"image": "صحح_6.png", "answer": "كتابته"},
            {"image": "صحح_7.png", "answer": "غرفته"},
            {"image": "صحح_8.png", "answer": "حديقة"},
            {"image": "صحح_9.png", "answer": "شجرة"},
            {"image": "صحح_10.png", "answer": "وردة"},
            {"image": "صحح_11.png", "answer": "قصة"},
            {"image": "صحح_12.png", "answer": "لعبة"},
            {"image": "صحح_13.png", "answer": "كرة"},
            {"image": "صحح_14.png", "answer": "نظارة"},
            {"image": "صحح_15.png", "answer": "حقيبة"},
            {"image": "صحح_16.png", "answer": "ساعة"},
            {"image": "صحح_17.png", "answer": "صورة"},
            {"image": "صحح_18.png", "answer": "ورقة"},
            {"image": "صحح_19.png", "answer": "قطة"},
            {"image": "صحح_20.png", "answer": "غابة"},
            {"image": "صحح_21.png", "answer": "سيارته"},
            {"image": "صحح_22.png", "answer": "كتابها"},
            {"image": "صحح_23.png", "answer": "استعمال"},
            {"image": "صحح_24.png", "answer": "اختبار"},
            {"image": "صحح_25.png", "answer": "استغفار"},
            {"image": "صحح_26.png", "answer": "اسم"},
            {"image": "صحح_27.png", "answer": "ابن"},
            {"image": "صحح_28.png", "answer": "اثنين"},
            {"image": "صحح_29.png", "answer": "امرأة"},
            {"image": "صحح_30.png", "answer": "ماءً"},
            {"image": "صحح_31.png", "answer": "سماءً"},
            {"image": "صحح_32.png", "answer": "شاطئ"},
            {"image": "صحح_33.png", "answer": "قرأ"},
            {"image": "صحح_34.png", "answer": "مسؤول"},
            {"image": "صحح_35.png", "answer": "شؤون"},
            {"image": "صحح_36.png", "answer": "رئيسي"},
            {"image": "صحح_37.png", "answer": "دائم"},
            {"image": "صحح_38.png", "answer": "فجأة"},
            {"image": "صحح_39.png", "answer": "شيء"},
            {"image": "صحح_40.png", "answer": "دفء"},
            {"image": "صحح_41.png", "answer": "جزءًا"},
            {"image": "صحح_42.png", "answer": "قراءة"},
            {"image": "صحح_43.png", "answer": "براءة"},
            {"image": "صحح_44.png", "answer": "تساءل"},
            {"image": "صحح_45.png", "answer": "تفاءل"},
            {"image": "صحح_46.png", "answer": "تشاءم"},
            {"image": "صحح_47.png", "answer": "ملجأ"},
            {"image": "صحح_48.png", "answer": "مبدأ"},
            {"image": "صحح_49.png", "answer": "يقرأ"},
            {"image": "صحح_50.png", "answer": "أكلته"},
            {"image": "صحح_51.png", "answer": "شربته"},
            {"image": "صحح_52.png", "answer": "ضابط"},
            {"image": "صحح_53.png", "answer": "ظرف"},
            {"image": "صحح_54.png", "answer": "نظارة"},
            {"image": "صحح_55.png", "answer": "منظار"},
            {"image": "صحح_56.png", "answer": "حفظ"},
            {"image": "صحح_57.png", "answer": "حظ"},
            {"image": "صحح_58.png", "answer": "ظلام"},
            {"image": "صحح_59.png", "answer": "مظلات"},
            {"image": "صحح_60.png", "answer": "ظهر"},
            {"image": "صحح_61.png", "answer": "نظافة"},
            {"image": "صحح_62.png", "answer": "ظبي"},
            {"image": "صحح_63.png", "answer": "ظلم"},
            {"image": "صحح_64.png", "answer": "لحظة"},
            {"image": "صحح_65.png", "answer": "ملاحظة"},
            {"image": "صحح_66.png", "answer": "استيقظ"},
            {"image": "صحح_67.png", "answer": "محافظة"},
            {"image": "صحح_68.png", "answer": "عظم"},
            {"image": "صحح_69.png", "answer": "نظر"},
            {"image": "صحح_70.png", "answer": "انتظار"},
            {"image": "صحح_71.png", "answer": "منظر"},
            {"image": "صحح_72.png", "answer": "ظل"},
            {"image": "صحح_73.png", "answer": "ظفر"},
            {"image": "صحح_74.png", "answer": "فظيع"},
            {"image": "صحح_75.png", "answer": "يحفظ"},
            {"image": "صحح_76.png", "answer": "محفوظ"},
            {"image": "صحح_77.png", "answer": "عظيم"},
            {"image": "صحح_78.png", "answer": "كظم"},
            {"image": "صحح_79.png", "answer": "غليظ"},
            {"image": "صحح_80.png", "answer": "ضرس"},
            {"image": "صحح_81.png", "answer": "ضفدع"},
            {"image": "صحح_82.png", "answer": "بيضة"},
            {"image": "صحح_83.png", "answer": "حافظ"},
            {"image": "صحح_84.png", "answer": "نظام"},
            {"image": "صحح_85.png", "answer": "مظلوم"},
            {"image": "صحح_86.png", "answer": "ظاهرة"},
            {"image": "صحح_87.png", "answer": "وظيفة"},
            {"image": "صحح_88.png", "answer": "ملهى"},
            {"image": "صحح_89.png", "answer": "مبنى"},
            {"image": "صحح_90.png", "answer": "حتى"},
            {"image": "صحح_91.png", "answer": "مستشفى"},
            {"image": "صحح_92.png", "answer": "ذكرى"},
            {"image": "صحح_93.png", "answer": "فتوى"},
            {"image": "صحح_94.png", "answer": "دعوى"},
            {"image": "صحح_95.png", "answer": "حلوى"},
            {"image": "صحح_96.png", "answer": "كبرى"},
            {"image": "صحح_97.png", "answer": "صغرى"},
            {"image": "صحح_98.png", "answer": "رمى"},
            {"image": "صحح_99.png", "answer": "بنى"},
            {"image": "صحح_100.png", "answer": "مشى"},
            {"image": "صحح_101.png", "answer": "بكى"},
            {"image": "صحح_102.png", "answer": "جرى"},
            {"image": "صحح_103.png", "answer": "شفى"},
            {"image": "صحح_104.png", "answer": "قضى"},
            {"image": "صحح_105.png", "answer": "هدى"},
            {"image": "صحح_106.png", "answer": "طهى"},
            {"image": "صحح_107.png", "answer": "دعا"},
            {"image": "صحح_108.png", "answer": "رجا"},
            {"image": "صحح_109.png", "answer": "شكا"},
            {"image": "صحح_110.png", "answer": "نما"},
            {"image": "صحح_111.png", "answer": "هذا"},
            {"image": "صحح_112.png", "answer": "هذه"},
            {"image": "صحح_113.png", "answer": "لكن"},
            {"image": "صحح_114.png", "answer": "هؤلاء"},
            {"image": "صحح_115.png", "answer": "ذلك"},
            {"image": "صحح_116.png", "answer": "الرحمن"},
            {"image": "صحح_117.png", "answer": "شكراً"},
            {"image": "صحح_118.png", "answer": "عفواً"},
            {"image": "صحح_119.png", "answer": "طبعاً"},
            {"image": "صحح_120.png", "answer": "قريباً"},
            {"image": "صحح_121.png", "answer": "جداً"},
            {"image": "صحح_122.png", "answer": "أهلاً"},
            {"image": "صحح_123.png", "answer": "صباحاً"},
            {"image": "صحح_124.png", "answer": "مساءً"},
            {"image": "صحح_125.png", "answer": "كتاباً"},
            {"image": "صحح_126.png", "answer": "قلماً"},
            {"image": "صحح_127.png", "answer": "باباً"},
            {"image": "صحح_128.png", "answer": "بيتاً"},
            {"image": "صحح_129.png", "answer": "مباراة"},
            {"image": "صحح_130.png", "answer": "سياراته"},
            {"image": "صحح_131.png", "answer": "أوقات"},
            {"image": "صحح_132.png", "answer": "أصوات"},
            {"image": "صحح_133.png", "answer": "أموات"},
            {"image": "صحح_134.png", "answer": "أبيات"},
            {"image": "صحح_135.png", "answer": "أنتِ"},
            {"image": "صحح_136.png", "answer": "ذهبتِ"},
            {"image": "صحح_137.png", "answer": "كتبتِ"},
            {"image": "صحح_138.png", "answer": "لكِ"},
            {"image": "صحح_139.png", "answer": "منكِ"},
            {"image": "صحح_140.png", "answer": "عنكِ"},
            {"image": "صحح_141.png", "answer": "إليكِ"},
            {"image": "صحح_142.png", "answer": "عليكِ"},
            {"image": "صحح_143.png", "answer": "فيكِ"},
            {"image": "صحح_144.png", "answer": "يعطيكِ"},
            {"image": "صحح_145.png", "answer": "صلِّ"},
            {"image": "صحح_146.png", "answer": "أدعو"},
            {"image": "صحح_147.png", "answer": "مياه"},
            {"image": "صحح_148.png", "answer": "وجه"},
            {"image": "صحح_149.png", "answer": "فواكه"},
            {"image": "صحح_150.png", "answer": "آلة"}
           
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

    @commands.command(name="-صحح")
    async def start_game_cmd(self, ctx):
        await self.run_game(ctx.channel)

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return
        if message.content.strip() == "-صحح":
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
    await bot.add_cog(ssagame(bot))