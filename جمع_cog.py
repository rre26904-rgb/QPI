import discord
from discord.ext import commands
import random
import asyncio
import json
import os


class gmgame(commands.Cog):
    def __init__(self, bot):    
        self.bot = bot
        self.scores_file = "global_points.json" # 🟢 اسم ملف النقاط الموحد والمشترك
        
        # 🟢 التأكد من وجود القفل العام المشترك داخل كائن البوت
        if not hasattr(self.bot, 'global_game_lock'):
            self.bot.global_game_lock = set()

        self.questions = [
            {"image": "جمع_1.png", "answer": "أقلام"},
            {"image": "جمع_2.png", "answer": "كتب"},
            {"image": "جمع_3.png", "answer": "أبواب"},
            {"image": "جمع_4.png", "answer": "نوافذ"},
            {"image": "جمع_5.png", "answer": "أشجار"},
            {"image": "جمع_6.png", "answer": "أزهار"},
            {"image": "جمع_7.png", "answer": "سيارات"},
            {"image": "جمع_8.png", "answer": "طاولات"},
            {"image": "جمع_9.png", "answer": "كراسي"},
            {"image": "جمع_10.png", "answer": "طلاب"},
            {"image": "جمع_11.png", "answer": "معلمون"},
            {"image": "جمع_12.png", "answer": "مهندسون"},
            {"image": "جمع_13.png", "answer": "أطباء"},
            {"image": "جمع_14.png", "answer": "مستشفيات"},
            {"image": "جمع_15.png", "answer": "مدارس"},
            {"image": "جمع_16.png", "answer": "جامعات"},
            {"image": "جمع_17.png", "answer": "شركات"},
            {"image": "جمع_18.png", "answer": "مصانع"},
            {"image": "جمع_19.png", "answer": "مساجد"},
            {"image": "جمع_20.png", "answer": "بيوت"},
            {"image": "جمع_21.png", "answer": "منازل"},
            {"image": "جمع_22.png", "answer": "غرف"},
            {"image": "جمع_23.png", "answer": "صالات"},
            {"image": "جمع_24.png", "answer": "مطابخ"},
            {"image": "جمع_25.png", "answer": "حمامات"},
            {"image": "جمع_26.png", "answer": "أسرة"},
            {"image": "جمع_27.png", "answer": "دواليب"},
            {"image": "جمع_28.png", "answer": "سجادات"},
            {"image": "جمع_29.png", "answer": "لوحات"},
            {"image": "جمع_30.png", "answer": "مصابيح"},
            {"image": "جمع_31.png", "answer": "شبابيك"},
            {"image": "جمع_32.png", "answer": "جدران"},
            {"image": "جمع_33.png", "answer": "بلاطات"},
            {"image": "جمع_34.png", "answer": "ستائر"},
            {"image": "جمع_35.png", "answer": "قمصان"},
            {"image": "جمع_36.png", "answer": "بناطيل"},
            {"image": "جمع_37.png", "answer": "فساتين"},
            {"image": "جمع_38.png", "answer": "تنانير"},
            {"image": "جمع_39.png", "answer": "أحذية"},
            {"image": "جمع_40.png", "answer": "جوارب"},
            {"image": "جمع_41.png", "answer": "قبعات"},
            {"image": "جمع_42.png", "answer": "أوشحة"},
            {"image": "جمع_43.png", "answer": "معاطف"},
            {"image": "جمع_44.png", "answer": "أحزمة"},
            {"image": "جمع_45.png", "answer": "خواتم"},
            {"image": "جمع_46.png", "answer": "عقود"},
            {"image": "جمع_47.png", "answer": "ساعات"},
            {"image": "جمع_48.png", "answer": "نظارات"},
            {"image": "جمع_49.png", "answer": "حقائب"},
            {"image": "جمع_50.png", "answer": "طيارون"},
            {"image": "جمع_51.png", "answer": "نجارون"},
            {"image": "جمع_52.png", "answer": "حدادون"},
            {"image": "جمع_53.png", "answer": "خبازون"},
            {"image": "جمع_54.png", "answer": "صيادون"},
            {"image": "جمع_55.png", "answer": "جزارون"},
            {"image": "جمع_56.png", "answer": "خياطون"},
            {"image": "جمع_57.png", "answer": "محامون"},
            {"image": "جمع_58.png", "answer": "قضاة"},
            {"image": "جمع_59.png", "answer": "ضباط"},
            {"image": "جمع_60.png", "answer": "جنود"},
            {"image": "جمع_61.png", "answer": "شرطيون"},
            {"image": "جمع_62.png", "answer": "قطارات"},
            {"image": "جمع_63.png", "answer": "طائرات"},
            {"image": "جمع_64.png", "answer": "سفن"},
            {"image": "جمع_65.png", "answer": "قوارب"},
            {"image": "جمع_66.png", "answer": "حافلات"},
            {"image": "جمع_67.png", "answer": "دراجات"},
            {"image": "جمع_68.png", "answer": "صواريخ"},
            {"image": "جمع_69.png", "answer": "دبابات"},
            {"image": "جمع_70.png", "answer": "غواصات"},
            {"image": "جمع_71.png", "answer": "شاحنات"},
            {"image": "جمع_72.png", "answer": "مكتبات"},
            {"image": "جمع_73.png", "answer": "عيادات"},
            {"image": "جمع_74.png", "answer": "صيدليات"},
            {"image": "جمع_75.png", "answer": "مخابز"},
            {"image": "جمع_76.png", "answer": "بقالات"},
            {"image": "جمع_77.png", "answer": "أسواق"},
            {"image": "جمع_78.png", "answer": "متاجر"},
            {"image": "جمع_79.png", "answer": "ملاعب"},
            {"image": "جمع_80.png", "answer": "حدائق"},
            {"image": "جمع_81.png", "answer": "متاحف"},
            {"image": "جمع_82.png", "answer": "سينمات"},
            {"image": "جمع_83.png", "answer": "مسارح"},
            {"image": "جمع_84.png", "answer": "فنادق"},
            {"image": "جمع_85.png", "answer": "مطاعم"},
            {"image": "جمع_86.png", "answer": "أجبان"},
            {"image": "جمع_87.png", "answer": "لحوم"},
            {"image": "جمع_88.png", "answer": "بيض"},
            {"image": "جمع_89.png", "answer": "عسل"},
            {"image": "جمع_90.png", "answer": "مربيات"},
            {"image": "جمع_91.png", "answer": "حليبات"},
            {"image": "جمع_92.png", "answer": "قهوات"},
            {"image": "جمع_93.png", "answer": "شايات"},
            {"image": "جمع_94.png", "answer": "عصائر"},
            {"image": "جمع_95.png", "answer": "سكريات"},
            {"image": "جمع_96.png", "answer": "أملاح"},
            {"image": "جمع_97.png", "answer": "فيزياء"},
            {"image": "جمع_98.png", "answer": "كيمياء"},
            {"image": "جمع_99.png", "answer": "أحياء"},
            {"image": "جمع_100.png", "answer": "هندسات"},
            {"image": "جمع_101.png", "answer": "جغرافيات"},
            {"image": "جمع_102.png", "answer": "تواريخ"},
            {"image": "جمع_103.png", "answer": "حواسيب"},
            {"image": "جمع_104.png", "answer": "شبكات"},
            {"image": "جمع_105.png", "answer": "رؤوس"},
            {"image": "جمع_106.png", "answer": "شعور"},
            {"image": "جمع_107.png", "answer": "وجوه"},
            {"image": "جمع_108.png", "answer": "أعين"},
            {"image": "جمع_109.png", "answer": "حواجب"},
            {"image": "جمع_110.png", "answer": "أنوف"},
            {"image": "جمع_111.png", "answer": "أفواه"},
            {"image": "جمع_112.png", "answer": "شفاه"},
            {"image": "جمع_113.png", "answer": "أسنان"},
            {"image": "جمع_114.png", "answer": "ألسنة"},
            {"image": "جمع_115.png", "answer": "آذان"},
            {"image": "جمع_116.png", "answer": "خدود"},
            {"image": "جمع_117.png", "answer": "رقبات"},
            {"image": "جمع_118.png", "answer": "أكتاف"},
            {"image": "جمع_119.png", "answer": "أذرع"},
            {"image": "جمع_120.png", "answer": "أيدي"},
            {"image": "جمع_121.png", "answer": "أصابع"},
            {"image": "جمع_122.png", "answer": "أظافر"},
            {"image": "جمع_123.png", "answer": "صدور"},
            {"image": "جمع_124.png", "answer": "بطون"},
            {"image": "جمع_125.png", "answer": "ظهور"},
            {"image": "جمع_126.png", "answer": "أقدام"},
            {"image": "جمع_127.png", "answer": "كعوب"},
            {"image": "جمع_128.png", "answer": "ركب"},
            {"image": "جمع_129.png", "answer": "أكباد"},
            {"image": "جمع_130.png", "answer": "قلوب"},
            {"image": "جمع_131.png", "answer": "رئات"},
            {"image": "جمع_132.png", "answer": "كلى"},
            {"image": "جمع_133.png", "answer": "معدات"},
            {"image": "جمع_134.png", "answer": "دماء"},
            {"image": "جمع_135.png", "answer": "ألوان"},
            {"image": "جمع_136.png", "answer": "أقمار"},
            {"image": "جمع_137.png", "answer": "شموس"},
            {"image": "جمع_138.png", "answer": "نجوم"},
            {"image": "جمع_139.png", "answer": "كواكب"},
            {"image": "جمع_140.png", "answer": "نيازك"},
            {"image": "جمع_141.png", "answer": "مجرات"},
            {"image": "جمع_142.png", "answer": "فضاءات"},
            {"image": "جمع_143.png", "answer": "أكوان"},
            {"image": "جمع_144.png", "answer": "ربيعات"},
            {"image": "جمع_145.png", "answer": "صيفيات"},
            {"image": "جمع_146.png", "answer": "خريفات"},
            {"image": "جمع_147.png", "answer": "شتاءات"},
            {"image": "جمع_148.png", "answer": "صباحات"},
            {"image": "جمع_149.png", "answer": "مساءات"},
            {"image": "جمع_150.png", "answer": "ليالي"},
            {"image": "جمع_151.png", "answer": "نهارات"},
            {"image": "جمع_152.png", "answer": "سنوات"},
            {"image": "جمع_153.png", "answer": "شهور"},
            {"image": "جمع_154.png", "answer": "أسابيع"},
            {"image": "جمع_155.png", "answer": "أيام"},
            {"image": "جمع_156.png", "answer": "دقائق"},
            {"image": "جمع_157.png", "answer": "ثواني"},
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

    @commands.command(name="-جمع")
    async def start_game_cmd(self, ctx):
        await self.run_game(ctx.channel)

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return
        if message.content.strip() == "-جمع":
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
    await bot.add_cog(gmgame(bot))