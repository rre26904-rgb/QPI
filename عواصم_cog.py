import discord
from discord.ext import commands
import random
import asyncio
import json
import os


class asssgame(commands.Cog):
    def __init__(self, bot):    
        self.bot = bot
        self.scores_file = "global_points.json" # 🟢 اسم ملف النقاط الموحد والمشترك
        
        # 🟢 التأكد من وجود القفل العام المشترك داخل كائن البوت
        if not hasattr(self.bot, 'global_game_lock'):
            self.bot.global_game_lock = set()

        self.questions = [
            {"image": "عواصم_1.png", "answer": "الرياض"},
            {"image": "عواصم_2.png", "answer": "أبو ظبي"},
            {"image": "عواصم_3.png", "answer": "الكويت"},
            {"image": "عواصم_4.png", "answer": "الدوحة"},
            {"image": "عواصم_5.png", "answer": "المنامة"},
            {"image": "عواصم_6.png", "answer": "مسقط"},
            {"image": "عواصم_7.png", "answer": "صنعاء"},
            {"image": "عواصم_8.png", "answer": "بغداد"},
            {"image": "عواصم_9.png", "answer": "دمشق"},
            {"image": "عواصم_10.png", "answer": "عمان"},
            {"image": "عواصم_11.png", "answer": "بيروت"},
            {"image": "عواصم_12.png", "answer": "القدس"},
            {"image": "عواصم_13.png", "answer": "القاهرة"},
            {"image": "عواصم_14.png", "answer": "الخرطوم"},
            {"image": "عواصم_15.png", "answer": "طرابلس"},
            {"image": "عواصم_16.png", "answer": "تونس"},
            {"image": "عواصم_17.png", "answer": "الجزائر"},
            {"image": "عواصم_18.png", "answer": "الرباط"},
            {"image": "عواصم_19.png", "answer": "نواكشوط"},
            {"image": "عواصم_20.png", "answer": "مقديشو"},
            {"image": "عواصم_21.png", "answer": "جيبوتي"},
            {"image": "عواصم_22.png", "answer": "موروني"},
            {"image": "عواصم_23.png", "answer": "أنقرة"},
            {"image": "عواصم_24.png", "answer": "طهران"},
            {"image": "عواصم_25.png", "answer": "كابل"},
            {"image": "عواصم_26.png", "answer": "إسلام آباد"},
            {"image": "عواصم_27.png", "answer": "نيودلهي"},
            {"image": "عواصم_28.png", "answer": "دكا"},
            {"image": "عواصم_29.png", "answer": "كولومبو"},
            {"image": "عواصم_30.png", "answer": "كاتماندو"},
            {"image": "عواصم_31.png", "answer": "تيمفو"},
            {"image": "عواصم_32.png", "answer": "ماليه"},
            {"image": "عواصم_33.png", "answer": "بكين"},
            {"image": "عواصم_34.png", "answer": "طوكيو"},
            {"image": "عواصم_35.png", "answer": "سيول"},
            {"image": "عواصم_36.png", "answer": "بيونغ يانغ"},
            {"image": "عواصم_37.png", "answer": "أولان باتور"},
            {"image": "عواصم_38.png", "answer": "مانيلا"},
            {"image": "عواصم_39.png", "answer": "جاكرتا"},
            {"image": "عواصم_40.png", "answer": "كوالالمبور"},
            {"image": "عواصم_41.png", "answer": "سنغافورة"},
            {"image": "عواصم_42.png", "answer": "بانكوك"},
            {"image": "عواصم_43.png", "answer": "هانوي"},
            {"image": "عواصم_44.png", "answer": "نايبيداو"},
            {"image": "عواصم_45.png", "answer": "بنوم بنه"},
            {"image": "عواصم_46.png", "answer": "فيينتيان"},
            {"image": "عواصم_47.png", "answer": "بندر سري بكاوان"},
            {"image": "عواصم_48.png", "answer": "أستانا"},
            {"image": "عواصم_49.png", "answer": "طشقند"},
            {"image": "عواصم_50.png", "answer": "عشق آباد"},
            {"image": "عواصم_51.png", "answer": "دوشنبه"},
            {"image": "عواصم_52.png", "answer": "بيشكيك"},
            {"image": "عواصم_53.png", "answer": "باكو"},
            {"image": "عواصم_54.png", "answer": "تبليسي"},
            {"image": "عواصم_55.png", "answer": "يريفان"},
            {"image": "عواصم_56.png", "answer": "نيقوسيا"},
            {"image": "عواصم_57.png", "answer": "موسكو"},
            {"image": "عواصم_58.png", "answer": "كييف"},
            {"image": "عواصم_59.png", "answer": "مينسك"},
            {"image": "عواصم_60.png", "answer": "وارسو"},
            {"image": "عواصم_61.png", "answer": "براغ"},
            {"image": "عواصم_62.png", "answer": "براتيسلافا"},
            {"image": "عواصم_63.png", "answer": "بودابست"},
            {"image": "عواصم_64.png", "answer": "بوخارست"},
            {"image": "عواصم_65.png", "answer": "صوفيا"},
            {"image": "عواصم_66.png", "answer": "أثينا"},
            {"image": "عواصم_67.png", "answer": "تيرانا"},
            {"image": "عواصم_68.png", "answer": "بلغراد"},
            {"image": "عواصم_69.png", "answer": "زغرب"},
            {"image": "عواصم_70.png", "answer": "سراييفو"},
            {"image": "عواصم_71.png", "answer": "ليوبليانا"},
            {"image": "عواصم_72.png", "answer": "سكوبيه"},
            {"image": "عواصم_73.png", "answer": "بودغوريتسا"},
            {"image": "عواصم_74.png", "answer": "روما"},
            {"image": "عواصم_75.png", "answer": "مدريد"},
            {"image": "عواصم_76.png", "answer": "لشبونة"},
            {"image": "عواصم_77.png", "answer": "باريس"},
            {"image": "عواصم_78.png", "answer": "برلين"},
            {"image": "عواصم_79.png", "answer": "أمستردام"},
            {"image": "عواصم_80.png", "answer": "بروكسل"},
            {"image": "عواصم_81.png", "answer": "بيرن"},
            {"image": "عواصم_82.png", "answer": "فيينا"},
            {"image": "عواصم_83.png", "answer": "لندن"},
            {"image": "عواصم_84.png", "answer": "دبلن"},
            {"image": "عواصم_85.png", "answer": "ستوكهولم"},
            {"image": "عواصم_86.png", "answer": "أوسلو"},
            {"image": "عواصم_87.png", "answer": "كوبنهاغن"},
            {"image": "عواصم_88.png", "answer": "هلسنكي"},
            {"image": "عواصم_89.png", "answer": "ريكيافيك"},
            {"image": "عواصم_90.png", "answer": "تالين"},
            {"image": "عواصم_91.png", "answer": "ريغا"},
            {"image": "عواصم_92.png", "answer": "فيلنيوس"},
            {"image": "عواصم_93.png", "answer": "فاليتا"},
            {"image": "عواصم_94.png", "answer": "الفاتيكان"},
            {"image": "عواصم_95.png", "answer": "سان مارينو"},
            {"image": "عواصم_96.png", "answer": "موناكو"},
            {"image": "عواصم_97.png", "answer": "أندورا لا فيلا"},
            {"image": "عواصم_98.png", "answer": "أوتاوا"},
            {"image": "عواصم_99.png", "answer": "واشنطن"},
            {"image": "عواصم_100.png", "answer": "مكسيكو"},
            {"image": "عواصم_101.png", "answer": "هافانا"},
            {"image": "عواصم_102.png", "answer": "كينغستون"},
            {"image": "عواصم_103.png", "answer": "بورت أو برانس"},
            {"image": "عواصم_104.png", "answer": "سانتو دومينغو"},
            {"image": "عواصم_105.png", "answer": "غواتيمالا"},
            {"image": "عواصم_106.png", "answer": "تيغوسيغالبا"},
            {"image": "عواصم_107.png", "answer": "سان سلفادور"},
            {"image": "عواصم_108.png", "answer": "ماناغوا"},
            {"image": "عواصم_109.png", "answer": "سان خوسيه"},
            {"image": "عواصم_110.png", "answer": "بنما"},
            {"image": "عواصم_111.png", "answer": "بوغوتا"},
            {"image": "عواصم_112.png", "answer": "كاراكاس"},
            {"image": "عواصم_113.png", "answer": "كيتو"},
            {"image": "عواصم_114.png", "answer": "ليما"},
            {"image": "عواصم_115.png", "answer": "برازيليا"},
            {"image": "عواصم_116.png", "answer": "لاباز"},
            {"image": "عواصم_117.png", "answer": "أسونسيون"},
            {"image": "عواصم_118.png", "answer": "سانتياغو"},
            {"image": "عواصم_119.png", "answer": "بوينس آيرس"},
            {"image": "عواصم_120.png", "answer": "مونتيفيديو"},
            {"image": "عواصم_121.png", "answer": "كانبرا"},
            {"image": "عواصم_122.png", "answer": "ويلينغتون"},
            {"image": "عواصم_123.png", "answer": "داكار"},
            {"image": "عواصم_124.png", "answer": "باماكو"},
            {"image": "عواصم_125.png", "answer": "نيامي"},
            {"image": "عواصم_126.png", "answer": "انجمينا"},
            {"image": "عواصم_127.png", "answer": "ياوندي"},
            {"image": "عواصم_128.png", "answer": "أبوجا"},
            {"image": "عواصم_129.png", "answer": "أكرا"},
            {"image": "عواصم_130.png", "answer": "ياموسوكرو"},
            {"image": "عواصم_131.png", "answer": "كوناكري"},
            {"image": "عواصم_132.png", "answer": "فريتاون"},
            {"image": "عواصم_133.png", "answer": "مونروفيا"},
            {"image": "عواصم_134.png", "answer": "لومي"},
            {"image": "عواصم_135.png", "answer": "بورتو نوفو"},
            {"image": "عواصم_136.png", "answer": "واغادوغو"},
            {"image": "عواصم_137.png", "answer": "لواندا"},
            {"image": "عواصم_138.png", "answer": "لوساكا"},
            {"image": "عواصم_139.png", "answer": "هراري"},
            {"image": "عواصم_140.png", "answer": "مابوتو"},
            {"image": "عواصم_141.png", "answer": "أنتاناناريفو"},
            {"image": "عواصم_142.png", "answer": "بريتوريا"},
            {"image": "عواصم_143.png", "answer": "نيروبي"},
            {"image": "عواصم_144.png", "answer": "دودوما"},
            {"image": "عواصم_145.png", "answer": "كمبالا"},
            {"image": "عواصم_146.png", "answer": "كيغالي"},
            {"image": "عواصم_147.png", "answer": "جيتيزا"},
            {"image": "عواصم_148.png", "answer": "أديس أبابا"},
            {"image": "عواصم_149.png", "answer": "أسمرة"},
            {"image": "عواصم_150.png", "answer": "ليبرفيل"}
           
            
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

    @commands.command(name="-عواصم")
    async def start_game_cmd(self, ctx):
        await self.run_game(ctx.channel)

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return
        if message.content.strip() == "-عواصم":
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
    await bot.add_cog(asssgame(bot))