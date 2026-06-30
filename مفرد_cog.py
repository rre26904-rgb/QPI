import discord
from discord.ext import commands
import random
import asyncio
import json
import os


class mfrdgame(commands.Cog):
    def __init__(self, bot):    
        self.bot = bot
        self.scores_file = "global_points.json" # 🟢 اسم ملف النقاط الموحد والمشترك
        
        # 🟢 التأكد من وجود القفل العام المشترك داخل كائن البوت
        if not hasattr(self.bot, 'global_game_lock'):
            self.bot.global_game_lock = set()

        self.questions = [
            {"image": "مفرد_1.png", "answer": "قلم"}
            {"image": "مفرد_2.png", "answer": "كتاب"}
            {"image": "مفرد_3.png", "answer": "باب"}
            {"image": "مفرد_4.png", "answer": "نافذة"}
            {"image": "مفرد_5.png", "answer": "شجرة"}
            {"image": "مفرد_6.png", "answer": "زهرة"}
            {"image": "مفرد_7.png", "answer": "سيارة"}
            {"image": "مفرد_8.png", "answer": "طاولة"}
            {"image": "مفرد_9.png", "answer": "كرسي"}
            {"image": "مفرد_10.png", "answer": "طالب"}
            {"image": "مفرد_11.png", "answer": "معلم"}
            {"image": "مفرد_12.png", "answer": "مهندس"}
            {"image": "مفرد_13.png", "answer": "طبيب"}
            {"image": "مفرد_14.png", "answer": "مستشفى"}
            {"image": "مفرد_15.png", "answer": "مدرسة"}
            {"image": "مفرد_16.png", "answer": "جامعة"}
            {"image": "مفرد_17.png", "answer": "شركة"}
            {"image": "مفرد_18.png", "answer": "مصنع"}
            {"image": "مفرد_19.png", "answer": "مسجد"}
            {"image": "مفرد_20.png", "answer": "بيت"}
            {"image": "مفرد_21.png", "answer": "منزل"}
            {"image": "مفرد_22.png", "answer": "غرفة"}
            {"image": "مفرد_23.png", "answer": "صالة"}
            {"image": "مفرد_24.png", "answer": "مطبخ"}
            {"image": "مفرد_25.png", "answer": "حمام"}
            {"image": "مفرد_26.png", "answer": "سرير"}
            {"image": "مفرد_27.png", "answer": "دولاب"}
            {"image": "مفرد_28.png", "answer": "سجادة"}
            {"image": "مفرد_29.png", "answer": "لوحة"}
            {"image": "مفرد_30.png", "answer": "مصباح"}
            {"image": "مفرد_31.png", "answer": "شباك"}
            {"image": "مفرد_32.png", "answer": "جدار"}
            {"image": "مفرد_33.png", "answer": "بلاطة"}
            {"image": "مفرد_34.png", "answer": "ستارة"}
            {"image": "مفرد_35.png", "answer": "قميص"}
            {"image": "مفرد_36.png", "answer": "بنطال"}
            {"image": "مفرد_37.png", "answer": "فستان"}
            {"image": "مفرد_38.png", "answer": "تنورة"}
            {"image": "مفرد_39.png", "answer": "حذاء"}
            {"image": "مفرد_40.png", "answer": "جورب"}
            {"image": "مفرد_41.png", "answer": "قبعة"}
            {"image": "مفرد_42.png", "answer": "وشاح"}
            {"image": "مفرد_43.png", "answer": "معطف"}
            {"image": "مفرد_44.png", "answer": "حزام"}
            {"image": "مفرد_45.png", "answer": "خاتم"}
            {"image": "مفرد_46.png", "answer": "عقد"}
            {"image": "مفرد_47.png", "answer": "ساعة"}
            {"image": "مفرد_48.png", "answer": "نظارة"}
            {"image": "مفرد_49.png", "answer": "حقيبة"}
            {"image": "مفرد_50.png", "answer": "طيار"}
            {"image": "مفرد_51.png", "answer": "نجار"}
            {"image": "مفرد_52.png", "answer": "حداد"}
            {"image": "مفرد_53.png", "answer": "خباز"}
            {"image": "مفرد_54.png", "answer": "صياد"}
            {"image": "مفرد_55.png", "answer": "جزار"}
            {"image": "مفرد_56.png", "answer": "خياط"}
            {"image": "مفرد_57.png", "answer": "محامي"}
            {"image": "مفرد_58.png", "answer": "قاضي"}
            {"image": "مفرد_59.png", "answer": "ضابط"}
            {"image": "مفرد_60.png", "answer": "جندي"}
            {"image": "مفرد_61.png", "answer": "شرطي"}
            {"image": "مفرد_62.png", "answer": "قطار"}
            {"image": "مفرد_63.png", "answer": "طائرة"}
            {"image": "مفرد_64.png", "answer": "سفينة"}
            {"image": "مفرد_65.png", "answer": "قارب"}
            {"image": "مفرد_66.png", "answer": "حافلة"}
            {"image": "مفرد_67.png", "answer": "دراجة"}
            {"image": "مفرد_68.png", "answer": "صاروخ"}
            {"image": "مفرد_69.png", "answer": "دبابة"}
            {"image": "مفرد_70.png", "answer": "غواصة"}
            {"image": "مفرد_71.png", "answer": "شاحنة"}
            {"image": "مفرد_72.png", "answer": "مكتبة"}
            {"image": "مفرد_73.png", "answer": "عيادة"}
            {"image": "مفرد_74.png", "answer": "صيدلية"}
            {"image": "مفرد_75.png", "answer": "مخبز"}
            {"image": "مفرد_76.png", "answer": "بقالة"}
            {"image": "مفرد_77.png", "answer": "سوق"}
            {"image": "مفرد_78.png", "answer": "متجر"}
            {"image": "مفرد_79.png", "answer": "ملعب"}
            {"image": "مفرد_80.png", "answer": "حديقة"}
            {"image": "مفرد_81.png", "answer": "متحف"}
            {"image": "مفرد_82.png", "answer": "سينما"}
            {"image": "مفرد_83.png", "answer": "مسرح"}
            {"image": "مفرد_84.png", "answer": "فندق"}
            {"image": "مفرد_85.png", "answer": "مطعم"}
            {"image": "مفرد_86.png", "answer": "جبن"}
            {"image": "مفرد_87.png", "answer": "لحم"}
            {"image": "مفرد_88.png", "answer": "بيضة"}
            {"image": "مفرد_89.png", "answer": "عسل"}
            {"image": "مفرد_90.png", "answer": "مربى"}
            {"image": "مفرد_91.png", "answer": "حليب"}
            {"image": "مفرد_92.png", "answer": "قهوة"}
            {"image": "مفرد_93.png", "answer": "شاي"}
            {"image": "مفرد_94.png", "answer": "عصير"}
            {"image": "مفرد_95.png", "answer": "سكر"}
            {"image": "مفرد_96.png", "answer": "ملح"}
            {"image": "مفرد_97.png", "answer": "فيزياء"}
            {"image": "مفرد_98.png", "answer": "كيمياء"}
            {"image": "مفرد_99.png", "answer": "حي"}
            {"image": "مفرد_100.png", "answer": "هندسة"}
            {"image": "مفرد_101.png", "answer": "جغرافيا"}
            {"image": "مفرد_102.png", "answer": "تاريخ"}
            {"image": "مفرد_103.png", "answer": "حاسوب"}
            {"image": "مفرد_104.png", "answer": "شبكة"}
            {"image": "مفرد_105.png", "answer": "رأس"}
            {"image": "مفرد_106.png", "answer": "شعرة"}
            {"image": "مفرد_107.png", "answer": "وجه"}
            {"image": "مفرد_108.png", "answer": "عين"}
            {"image": "مفرد_109.png", "answer": "حاجب"}
            {"image": "مفرد_110.png", "answer": "أنف"}
            {"image": "مفرد_111.png", "answer": "فم"}
            {"image": "مفرد_112.png", "answer": "شفة"}
            {"image": "مفرد_113.png", "answer": "سن"}
            {"image": "مفرد_114.png", "answer": "لسان"}
            {"image": "مفرد_115.png", "answer": "أذن"}
            {"image": "مفرد_116.png", "answer": "خد"}
            {"image": "مفرد_117.png", "answer": "رقبة"}
            {"image": "مفرد_118.png", "answer": "كتف"}
            {"image": "مفرد_119.png", "answer": "ذراع"}
            {"image": "مفرد_120.png", "answer": "يد"}
            {"image": "مفرد_121.png", "answer": "إصبع"}
            {"image": "مفرد_122.png", "answer": "ظفر"}
            {"image": "مفرد_123.png", "answer": "صدر"}
            {"image": "مفرد_124.png", "answer": "بطن"}
            {"image": "مفرد_125.png", "answer": "ظهر"}
            {"image": "مفرد_126.png", "answer": "قدم"}
            {"image": "مفرد_127.png", "answer": "كعب"}
            {"image": "مفرد_128.png", "answer": "ركبة"}
            {"image": "مفرد_129.png", "answer": "كبد"}
            {"image": "مفرد_130.png", "answer": "قلب"}
            {"image": "مفرد_131.png", "answer": "رئة"}
            {"image": "مفرد_132.png", "answer": "كلية"}
            {"image": "مفرد_133.png", "answer": "معدة"}
            {"image": "مفرد_134.png", "answer": "دم"}
            {"image": "مفرد_135.png", "answer": "لون"}
            {"image": "مفرد_136.png", "answer": "قمر"}
            {"image": "مفرد_137.png", "answer": "شمس"}
            {"image": "مفرد_138.png", "answer": "نجم"}
            {"image": "مفرد_139.png", "answer": "كوكب"}
            {"image": "مفرد_140.png", "answer": "نيزك"}
            {"image": "مفرد_141.png", "answer": "مجرة"}
            {"image": "مفرد_142.png", "answer": "فضاء"}
            {"image": "مفرد_143.png", "answer": "كون"}
            {"image": "مفرد_144.png", "answer": "ربيع"}
            {"image": "مفرد_145.png", "answer": "صيف"}
            {"image": "مفرد_146.png", "answer": "خريف"}
            {"image": "مفرد_147.png", "answer": "شتاء"}
            {"image": "مفرد_148.png", "answer": "صباح"}
            {"image": "مفرد_149.png", "answer": "مساء"}
            {"image": "مفرد_150.png", "answer": "ليلة"}
            {"image": "مفرد_151.png", "answer": "نهار"}
            {"image": "مفرد_152.png", "answer": "سنة"}
            {"image": "مفرد_153.png", "answer": "شهر"}
            {"image": "مفرد_154.png", "answer": "أسبوع"}
            {"image": "مفرد_155.png", "answer": "يوم"}
            {"image": "مفرد_156.png", "answer": "دقيقة"}
            {"image": "مفرد_157.png", "answer": "ثانية"}
            

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

    @commands.command(name="-مفرد")
    async def start_game_cmd(self, ctx):
        await self.run_game(ctx.channel)

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return
        if message.content.strip() == "-مفرد":
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
    await bot.add_cog(mfrdgame(bot))