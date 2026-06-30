import discord
from discord.ext import commands
import random
import asyncio
import json
import os


class aaalgame(commands.Cog):
    def __init__(self, bot):    
        self.bot = bot
        self.scores_file = "global_points.json" # 🟢 اسم ملف النقاط الموحد والمشترك
        
        # 🟢 التأكد من وجود القفل العام المشترك داخل كائن البوت
        if not hasattr(self.bot, 'global_game_lock'):
            self.bot.global_game_lock = set()

        self.questions = [
            {"image": "صورة_1.png", "answer": "السعودية"},
            {"image": "صورة_2.png", "answer": "الإمارات"},
            {"image": "صورة_3.png", "answer": "الكويت"},
            {"image": "صورة_4.png", "answer": "قطر"},
            {"image": "صورة_5.png", "answer": "البحرين"},
            {"image": "صورة_6.png", "answer": "عمان"},
            {"image": "صورة_7.png", "answer": "اليمن"},
            {"image": "صورة_8.png", "answer": "العراق"},
            {"image": "صورة_9.png", "answer": "سوريا"},
            {"image": "صورة_10.png", "answer": "الأردن"},
            {"image": "صورة_11.png", "answer": "لبنان"},
            {"image": "صورة_12.png", "answer": "فلسطين"},
            {"image": "صورة_13.png", "answer": "مصر"},
            {"image": "صورة_14.png", "answer": "السودان"},
            {"image": "صورة_15.png", "answer": "ليبيا"},
            {"image": "صورة_16.png", "answer": "تونس"},
            {"image": "صورة_17.png", "answer": "الجزائر"},
            {"image": "صورة_18.png", "answer": "المغرب"},
            {"image": "صورة_19.png", "answer": "موريتانيا"},
            {"image": "صورة_20.png", "answer": "الصومال"},
            {"image": "صورة_21.png", "answer": "جيبوتي"},
            {"image": "صورة_22.png", "answer": "جزر القمر"},
            {"image": "صورة_23.png", "answer": "تركيا"},
            {"image": "صورة_24.png", "answer": "إيران"},
            {"image": "صورة_25.png", "answer": "أفغانستان"},
            {"image": "صورة_26.png", "answer": "باكستان"},
            {"image": "صورة_27.png", "answer": "الهند"},
            {"image": "صورة_28.png", "answer": "بنغلاديش"},
            {"image": "صورة_29.png", "answer": "سريلانكا"},
            {"image": "صورة_30.png", "answer": "نيبال"},
            {"image": "صورة_31.png", "answer": "بوتان"},
            {"image": "صورة_32.png", "answer": "المالديف"},
            {"image": "صورة_33.png", "answer": "الصين"},
            {"image": "صورة_34.png", "answer": "اليابان"},
            {"image": "صورة_35.png", "answer": "كوريا الجنوبية"},
            {"image": "صورة_36.png", "answer": "كوريا الشمالية"},
            {"image": "صورة_37.png", "answer": "منغوليا"},
            {"image": "صورة_38.png", "answer": "الفلبين"},
            {"image": "صورة_39.png", "answer": "إندونيسيا"},
            {"image": "صورة_40.png", "answer": "ماليزيا"},
            {"image": "صورة_41.png", "answer": "سنغافورة"},
            {"image": "صورة_42.png", "answer": "تايلاند"},
            {"image": "صورة_43.png", "answer": "فيتنام"},
            {"image": "صورة_44.png", "answer": "ميانمار"},
            {"image": "صورة_45.png", "answer": "كمبوديا"},
            {"image": "صورة_46.png", "answer": "لاوس"},
            {"image": "صورة_47.png", "answer": "بروناي"},
            {"image": "صورة_48.png", "answer": "كازاخستان"},
            {"image": "صورة_49.png", "answer": "أوزبكستان"},
            {"image": "صورة_50.png", "answer": "تركمانستان"},
            {"image": "صورة_51.png", "answer": "طاجيكستان"},
            {"image": "صورة_52.png", "answer": "قيرغيزستان"},
            {"image": "صورة_53.png", "answer": "أذربيجان"},
            {"image": "صورة_54.png", "answer": "جورجيا"},
            {"image": "صورة_55.png", "answer": "أرمينيا"},
            {"image": "صورة_56.png", "answer": "قبرص"},
            {"image": "صورة_57.png", "answer": "روسيا"},
            {"image": "صورة_58.png", "answer": "أوكرانيا"},
            {"image": "صورة_59.png", "answer": "بيلاروسيا"},
            {"image": "صورة_60.png", "answer": "بولندا"},
            {"image": "صورة_61.png", "answer": "التشيك"},
            {"image": "صورة_62.png", "answer": "سلوفاكيا"},
            {"image": "صورة_63.png", "answer": "المجر"},
            {"image": "صورة_64.png", "answer": "رومانيا"},
            {"image": "صورة_65.png", "answer": "بلغاريا"},
            {"image": "صورة_66.png", "answer": "اليونان"},
            {"image": "صورة_67.png", "answer": "ألبانيا"},
            {"image": "صورة_68.png", "answer": "صربيا"},
            {"image": "صورة_69.png", "answer": "كرواتيا"},
            {"image": "صورة_70.png", "answer": "البوسنة والهرسك"},
            {"image": "صورة_71.png", "answer": "سلوفينيا"},
            {"image": "صورة_72.png", "answer": "مقدونيا الشمالية"},
            {"image": "صورة_73.png", "answer": "الجبل الأسود"},
            {"image": "صورة_74.png", "answer": "إيطاليا"},
            {"image": "صورة_75.png", "answer": "إسبانيا"},
            {"image": "صورة_76.png", "answer": "البرتغال"},
            {"image": "صورة_77.png", "answer": "فرنسا"},
            {"image": "صورة_78.png", "answer": "ألمانيا"},
            {"image": "صورة_79.png", "answer": "هولندا"},
            {"image": "صورة_80.png", "answer": "بلجيكا"},
            {"image": "صورة_81.png", "answer": "سويسرا"},
            {"image": "صورة_82.png", "answer": "النمسا"},
            {"image": "صورة_83.png", "answer": "بريطانيا"},
            {"image": "صورة_84.png", "answer": "أيرلندا"},
            {"image": "صورة_85.png", "answer": "السويد"},
            {"image": "صورة_86.png", "answer": "النرويج"},
            {"image": "صورة_87.png", "answer": "الدنمارك"},
            {"image": "صورة_88.png", "answer": "فنلندا"},
            {"image": "صورة_89.png", "answer": "آيسلندا"},
            {"image": "صورة_90.png", "answer": "إستونيا"},
            {"image": "صورة_91.png", "answer": "لاتفيا"},
            {"image": "صورة_92.png", "answer": "ليتوانيا"},
            {"image": "صورة_93.png", "answer": "مالطا"},
            {"image": "صورة_94.png", "answer": "الفاتيكان"},
            {"image": "صورة_95.png", "answer": "سان مارينو"},
            {"image": "صورة_96.png", "answer": "موناكو"},
            {"image": "صورة_97.png", "answer": "أندورا"},
            {"image": "صورة_98.png", "answer": "كندا"},
            {"image": "صورة_99.png", "answer": "أمريكا"},
            {"image": "صورة_100.png", "answer": "المكسيك"},
            {"image": "صورة_101.png", "answer": "كوبا"},
            {"image": "صورة_102.png", "answer": "جامايكا"},
            {"image": "صورة_103.png", "answer": "هايتي"},
            {"image": "صورة_104.png", "answer": "الدومينيكان"},
            {"image": "صورة_105.png", "answer": "غواتيمالا"},
            {"image": "صورة_106.png", "answer": "هندوراس"},
            {"image": "صورة_107.png", "answer": "السلفادور"},
            {"image": "صورة_108.png", "answer": "نيكاراغوا"},
            {"image": "صورة_109.png", "answer": "كوستاريكا"},
            {"image": "صورة_110.png", "answer": "بنما"},
            {"image": "صورة_111.png", "answer": "كولومبيا"},
            {"image": "صورة_112.png", "answer": "فنزويلا"},
            {"image": "صورة_113.png", "answer": "الإكوادور"},
            {"image": "صورة_114.png", "answer": "بيرو"},
            {"image": "صورة_115.png", "answer": "البرازيل"},
            {"image": "صورة_116.png", "answer": "بوليفيا"},
            {"image": "صورة_117.png", "answer": "باراغواي"},
            {"image": "صورة_118.png", "answer": "تشيلي"},
            {"image": "صورة_119.png", "answer": "الأرجنتين"},
            {"image": "صورة_120.png", "answer": "أوروغواي"},
            {"image": "صورة_121.png", "answer": "أستراليا"},
            {"image": "صورة_122.png", "answer": "نيوزيلندا"},
            {"image": "صورة_123.png", "answer": "السنغال"},
            {"image": "صورة_124.png", "answer": "مالي"},
            {"image": "صورة_125.png", "answer": "النيجر"},
            {"image": "صورة_126.png", "answer": "تشاد"},
            {"image": "صورة_127.png", "answer": "الكاميرون"},
            {"image": "صورة_128.png", "answer": "نيجيريا"},
            {"image": "صورة_129.png", "answer": "غانا"},
            {"image": "صورة_130.png", "answer": "ساحل العاج"},
            {"image": "صورة_131.png", "answer": "غينيا"},
            {"image": "صورة_132.png", "answer": "سيراليون"},
            {"image": "صورة_133.png", "answer": "ليبيريا"},
            {"image": "صورة_134.png", "answer": "توغو"},
            {"image": "صورة_135.png", "answer": "بنين"},
            {"image": "صورة_136.png", "answer": "بوركينا فاسو"},
            {"image": "صورة_137.png", "answer": "أنغولا"},
            {"image": "صورة_138.png", "answer": "زامبيا"},
            {"image": "صورة_139.png", "answer": "زيمبابوي"},
            {"image": "صورة_140.png", "answer": "موزمبيق"},
            {"image": "صورة_141.png", "answer": "مدغشقر"},
            {"image": "صورة_142.png", "answer": "جنوب أفريقيا"},
            {"image": "صورة_143.png", "answer": "كينيا"},
            {"image": "صورة_144.png", "answer": "تنزانيا"},
            {"image": "صورة_145.png", "answer": "أوغندا"},
            {"image": "صورة_146.png", "answer": "رواندا"},
            {"image": "صورة_147.png", "answer": "بوروندي"},
            {"image": "صورة_148.png", "answer": "إثيوبيا"},
            {"image": "صورة_149.png", "answer": "إريتريا"},
            {"image": "صورة_150.png", "answer": "الغابون"},
            {"image": "صورة_151.png", "answer": "غامبيا"},
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

    @commands.command(name="-اعلام")
    async def start_game_cmd(self, ctx):
        await self.run_game(ctx.channel)

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return
        if message.content.strip() == "-اعلام":
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
    await bot.add_cog(aaalgame(bot))