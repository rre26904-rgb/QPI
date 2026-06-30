import discord
from discord.ext import commands
import random
import asyncio
import json
import os


class trtrgame(commands.Cog):
    def __init__(self, bot):    
        self.bot = bot
        self.scores_file = "global_points.json" # 🟢 اسم ملف النقاط الموحد والمشترك
        
        # 🟢 التأكد من وجود القفل العام المشترك داخل كائن البوت
        if not hasattr(self.bot, 'global_game_lock'):
            self.bot.global_game_lock = set()

        self.questions = [
            {"image": "ترتيب_1.png", "answer": "34789"},
            {"image": "ترتيب_2.png", "answer": "012489"},
            {"image": "ترتيب_3.png", "answer": "34567"},
            {"image": "ترتيب_4.png", "answer": "012389"},
            {"image": "ترتيب_5.png", "answer": "12456"},
            {"image": "ترتيب_6.png", "answer": "03489"},
            {"image": "ترتيب_7.png", "answer": "123589"},
            {"image": "ترتيب_8.png", "answer": "24567"},
            {"image": "ترتيب_9.png", "answer": "013489"},
            {"image": "ترتيب_10.png", "answer": "23489"},
            {"image": "ترتيب_11.png", "answer": "012679"},
            {"image": "ترتيب_12.png", "answer": "12345"},
            {"image": "ترتيب_13.png", "answer": "345689"},
            {"image": "ترتيب_14.png", "answer": "01489"},
            {"image": "ترتيب_15.png", "answer": "45678"},
            {"image": "ترتيب_16.png", "answer": "23489"},
            {"image": "ترتيب_17.png", "answer": "015689"},
            {"image": "ترتيب_18.png", "answer": "23467"},
            {"image": "ترتيب_19.png", "answer": "012389"},
            {"image": "ترتيب_20.png", "answer": "14578"},
            {"image": "ترتيب_21.png", "answer": "02349"},
            {"image": "ترتيب_22.png", "answer": "125678"},
            {"image": "ترتيب_23.png", "answer": "03459"},
            {"image": "ترتيب_24.png", "answer": "124578"},
            {"image": "ترتيب_25.png", "answer": "34679"},
            {"image": "ترتيب_26.png", "answer": "012389"},
            {"image": "ترتيب_27.png", "answer": "12457"},
            {"image": "ترتيب_28.png", "answer": "014569"},
            {"image": "ترتيب_29.png", "answer": "23578"},
            {"image": "ترتيب_30.png", "answer": "01269"},
            {"image": "ترتيب_31.png", "answer": "45678"},
            {"image": "ترتيب_32.png", "answer": "012349"},
            {"image": "ترتيب_33.png", "answer": "12356"},
            {"image": "ترتيب_34.png", "answer": "014589"},
            {"image": "ترتيب_35.png", "answer": "34789"},
            {"image": "ترتيب_36.png", "answer": "01259"},
            {"image": "ترتيب_37.png", "answer": "234678"},
            {"image": "ترتيب_38.png", "answer": "12459"},
            {"image": "ترتيب_39.png", "answer": "012389"},
            {"image": "ترتيب_40.png", "answer": "45678"},
            {"image": "ترتيب_41.png", "answer": "012349"},
            {"image": "ترتيب_42.png", "answer": "12789"},
            {"image": "ترتيب_43.png", "answer": "013456"},
            {"image": "ترتيب_44.png", "answer": "23489"},
            {"image": "ترتيب_45.png", "answer": "01567"},
            {"image": "ترتيب_46.png", "answer": "02349"},
            {"image": "ترتيب_47.png", "answer": "125678"},
            {"image": "ترتيب_48.png", "answer": "34589"},
            {"image": "ترتيب_49.png", "answer": "012345"},
            {"image": "ترتيب_50.png", "answer": "06789"},
            {"image": "ترتيب_51.png", "answer": "12345"},
            {"image": "ترتيب_52.png", "answer": "016789"},
            {"image": "ترتيب_53.png", "answer": "23456"},
            {"image": "ترتيب_54.png", "answer": "012349"},
            {"image": "ترتيب_55.png", "answer": "45678"},
            {"image": "ترتيب_56.png", "answer": "012459"},
            {"image": "ترتيب_57.png", "answer": "02389"},
            {"image": "ترتيب_58.png", "answer": "123567"},
            {"image": "ترتيب_59.png", "answer": "01249"},
            {"image": "ترتيب_60.png", "answer": "34678"},
            {"image": "ترتيب_61.png", "answer": "12589"},
            {"image": "ترتيب_62.png", "answer": "124678"},
            {"image": "ترتيب_63.png", "answer": "13478"},
            {"image": "ترتيب_64.png", "answer": "123789"},
            {"image": "ترتيب_65.png", "answer": "23789"},
            {"image": "ترتيب_66.png", "answer": "12478"},
            {"image": "ترتيب_67.png", "answer": "234678"},
            {"image": "ترتيب_68.png", "answer": "12789"},
            {"image": "ترتيب_69.png", "answer": "125678"},
            {"image": "ترتيب_70.png", "answer": "01289"},
            {"image": "ترتيب_71.png", "answer": "122678"},
            {"image": "ترتيب_72.png", "answer": "23489"},
            {"image": "ترتيب_73.png", "answer": "123789"},
            {"image": "ترتيب_74.png", "answer": "34578"},
            {"image": "ترتيب_75.png", "answer": "23678"},
            {"image": "ترتيب_76.png", "answer": "12478"},
            {"image": "ترتيب_77.png", "answer": "345789"},
            {"image": "ترتيب_78.png", "answer": "12289"},
            {"image": "ترتيب_79.png", "answer": "234678"},
            {"image": "ترتيب_80.png", "answer": "12389"},
            {"image": "ترتيب_81.png", "answer": "24578"},
            {"image": "ترتيب_82.png", "answer": "012389"},
            {"image": "ترتيب_83.png", "answer": "01289"},
            {"image": "ترتيب_84.png", "answer": "124789"},
            {"image": "ترتيب_85.png", "answer": "12289"},
            {"image": "ترتيب_86.png", "answer": "345789"},
            {"image": "ترتيب_87.png", "answer": "01239"},
            {"image": "ترتيب_88.png", "answer": "245788"},
            {"image": "ترتيب_89.png", "answer": "12389"},
            {"image": "ترتيب_90.png", "answer": "24789"},
            {"image": "ترتيب_91.png", "answer": "01289"},
            {"image": "ترتيب_92.png", "answer": "234789"},
            {"image": "ترتيب_93.png", "answer": "12589"},
            {"image": "ترتيب_94.png", "answer": "234789"},
            {"image": "ترتيب_95.png", "answer": "12489"},
            {"image": "ترتيب_96.png", "answer": "34678"},
            {"image": "ترتيب_97.png", "answer": "012389"},
            {"image": "ترتيب_98.png", "answer": "12589"},
            {"image": "ترتيب_99.png", "answer": "234678"},
            {"image": "ترتيب_100.png", "answer": "12389"},
            {"image": "ترتيب_101.png", "answer": "124789"},
            {"image": "ترتيب_102.png", "answer": "12389"},
            {"image": "ترتيب_103.png", "answer": "012389"},
            {"image": "ترتيب_104.png", "answer": "12489"},
            {"image": "ترتيب_105.png", "answer": "45678"},
            {"image": "ترتيب_106.png", "answer": "12389"},
            {"image": "ترتيب_107.png", "answer": "245678"},
            {"image": "ترتيب_108.png", "answer": "01349"},
            {"image": "ترتيب_109.png", "answer": "245789"},
            {"image": "ترتيب_110.png", "answer": "02389"},
            {"image": "ترتيب_111.png", "answer": "245789"},
            {"image": "ترتيب_112.png", "answer": "01269"},
            {"image": "ترتيب_113.png", "answer": "345678"},
            {"image": "ترتيب_114.png", "answer": "01239"},
            {"image": "ترتيب_115.png", "answer": "245789"},
            {"image": "ترتيب_116.png", "answer": "23589"},
            {"image": "ترتيب_117.png", "answer": "124789"},
            {"image": "ترتيب_118.png", "answer": "03459"},
            {"image": "ترتيب_119.png", "answer": "235789"},
            {"image": "ترتيب_120.png", "answer": "12489"},
            {"image": "ترتيب_121.png", "answer": "023689"},
            {"image": "ترتيب_122.png", "answer": "12389"},
            {"image": "ترتيب_123.png", "answer": "345789"},
            {"image": "ترتيب_124.png", "answer": "02349"},
            {"image": "ترتيب_125.png", "answer": "345789"},
            {"image": "ترتيب_126.png", "answer": "34589"},
            {"image": "ترتيب_127.png", "answer": "012389"},
            {"image": "ترتيب_128.png", "answer": "34589"},
            {"image": "ترتيب_129.png", "answer": "023489"},
            {"image": "ترتيب_130.png", "answer": "34589"},
            {"image": "ترتيب_131.png", "answer": "012389"},
            {"image": "ترتيب_132.png", "answer": "24589"},
            {"image": "ترتيب_133.png", "answer": "023489"},
            {"image": "ترتيب_134.png", "answer": "34589"},
            {"image": "ترتيب_135.png", "answer": "012389"},
            {"image": "ترتيب_136.png", "answer": "23459"},
            {"image": "ترتيب_137.png", "answer": "012389"},
            {"image": "ترتيب_138.png", "answer": "12478"},
            {"image": "ترتيب_139.png", "answer": "012389"},
            {"image": "ترتيب_140.png", "answer": "12568"},
            {"image": "ترتيب_141.png", "answer": "012479"},
            {"image": "ترتيب_142.png", "answer": "12389"},
            {"image": "ترتيب_143.png", "answer": "023569"},
            {"image": "ترتيب_144.png", "answer": "12478"},
            {"image": "ترتيب_145.png", "answer": "023489"},
            {"image": "ترتيب_146.png", "answer": "23478"},
            {"image": "ترتيب_147.png", "answer": "012589"},
            {"image": "ترتيب_148.png", "answer": "12689"},
            {"image": "ترتيب_149.png", "answer": "012489"},
            {"image": "ترتيب_150.png", "answer": "23578"}
            
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

    @commands.command(name="-ترتيب")
    async def start_game_cmd(self, ctx):
        await self.run_game(ctx.channel)

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return
        if message.content.strip() == "-ترتيب":
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
    await bot.add_cog(trtrgame(bot))