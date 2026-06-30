import discord
from discord.ext import commands
import random
import asyncio
import json
import os


class aaagame(commands.Cog):
    def __init__(self, bot):    
        self.bot = bot
        self.scores_file = "global_points.json" # 🟢 اسم ملف النقاط الموحد والمشترك
        
        # 🟢 التأكد من وجود القفل العام المشترك داخل كائن البوت
        if not hasattr(self.bot, 'global_game_lock'):
            self.bot.global_game_lock = set()

        self.questions = [
            {"image": "ارقام_1.png", "answer": "73489"},
            {"image": "ارقام_2.png", "answer": "210948"},
            {"image": "ارقام_3.png", "answer": "56473"},
            {"image": "ارقام_4.png", "answer": "982310"},
            {"image": "ارقام_5.png", "answer": "45612"},
            {"image": "ارقام_6.png", "answer": "89034"},
            {"image": "ارقام_7.png", "answer": "123985"},
            {"image": "ارقام_8.png", "answer": "67452"},
            {"image": "ارقام_9.png", "answer": "349081"},
            {"image": "ارقام_10.png", "answer": "23894"},
            {"image": "ارقام_11.png", "answer": "761209"},
            {"image": "ارقام_12.png", "answer": "54321"},
            {"image": "ارقام_13.png", "answer": "895634"},
            {"image": "ارقام_14.png", "answer": "10984"},
            {"image": "ارقام_15.png", "answer": "65748"},
            {"image": "ارقام_16.png", "answer": "34892"},
            {"image": "ارقام_17.png", "answer": "109586"},
            {"image": "ارقام_18.png", "answer": "76234"},
            {"image": "ارقام_19.png", "answer": "901283"},
            {"image": "ارقام_20.png", "answer": "45871"},
            {"image": "ارقام_21.png", "answer": "23904"},
            {"image": "ارقام_22.png", "answer": "876512"},
            {"image": "ارقام_23.png", "answer": "54903"},
            {"image": "ارقام_24.png", "answer": "128745"},
            {"image": "ارقام_25.png", "answer": "67349"},
            {"image": "ارقام_26.png", "answer": "892310"},
            {"image": "ارقام_27.png", "answer": "45127"},
            {"image": "ارقام_28.png", "answer": "904561"},
            {"image": "ارقام_29.png", "answer": "23875"},
            {"image": "ارقام_30.png", "answer": "61092"},
            {"image": "ارقام_31.png", "answer": "87456"},
            {"image": "ارقام_32.png", "answer": "219034"},
            {"image": "ارقام_33.png", "answer": "56231"},
            {"image": "ارقام_34.png", "answer": "984501"},
            {"image": "ارقام_35.png", "answer": "34789"},
            {"image": "ارقام_36.png", "answer": "12095"},
            {"image": "ارقام_37.png", "answer": "678342"},
            {"image": "ارقام_38.png", "answer": "54129"},
            {"image": "ارقام_39.png", "answer": "890123"},
            {"image": "ارقام_40.png", "answer": "45678"},
            {"image": "ارقام_41.png", "answer": "234901"},
            {"image": "ارقام_42.png", "answer": "78912"},
            {"image": "ارقام_43.png", "answer": "105634"},
            {"image": "ارقام_44.png", "answer": "89234"},
            {"image": "ارقام_45.png", "answer": "56710"},
            {"image": "ارقام_46.png", "answer": "23094"},
            {"image": "ارقام_47.png", "answer": "871256"},
            {"image": "ارقام_48.png", "answer": "45983"},
            {"image": "ارقام_49.png", "answer": "102345"},
            {"image": "ارقام_50.png", "answer": "67890"},
            {"image": "ارقام_51.png", "answer": "34512"},
            {"image": "ارقام_52.png", "answer": "908761"},
            {"image": "ارقام_53.png", "answer": "56234"},
            {"image": "ارقام_54.png", "answer": "123490"},
            {"image": "ارقام_55.png", "answer": "87654"},
            {"image": "ارقام_56.png", "answer": "450912"},
            {"image": "ارقام_57.png", "answer": "23890"},
            {"image": "ارقام_58.png", "answer": "765123"},
            {"image": "ارقام_59.png", "answer": "90124"},
            {"image": "ارقام_60.png", "answer": "34876"},
            {"image": "ارقام_61.png", "answer": "51928"},
            {"image": "ارقام_62.png", "answer": "847261"},
            {"image": "ارقام_63.png", "answer": "18374"},
            {"image": "ارقام_64.png", "answer": "392817"},
            {"image": "ارقام_65.png", "answer": "92837"},
            {"image": "ارقام_66.png", "answer": "47182"},
            {"image": "ارقام_67.png", "answer": "283746"},
            {"image": "ارقام_68.png", "answer": "81927"},
            {"image": "ارقام_69.png", "answer": "572618"},
            {"image": "ارقام_70.png", "answer": "10928"},
            {"image": "ارقام_71.png", "answer": "627182"},
            {"image": "ارقام_72.png", "answer": "29384"},
            {"image": "ارقام_73.png", "answer": "718293"},
            {"image": "ارقام_74.png", "answer": "38475"},
            {"image": "ارقام_75.png", "answer": "82736"},
            {"image": "ارقام_76.png", "answer": "47281"},
            {"image": "ارقام_77.png", "answer": "938475"},
            {"image": "ارقام_78.png", "answer": "28192"},
            {"image": "ارقام_79.png", "answer": "647382"},
            {"image": "ارقام_80.png", "answer": "19283"},
            {"image": "ارقام_81.png", "answer": "57482"},
            {"image": "ارقام_82.png", "answer": "382910"},
            {"image": "ارقام_83.png", "answer": "82910"},
            {"image": "ارقام_84.png", "answer": "472819"},
            {"image": "ارقام_85.png", "answer": "28192"},
            {"image": "ارقام_86.png", "answer": "938475"},
            {"image": "ارقام_87.png", "answer": "10293"},
            {"image": "ارقام_88.png", "answer": "584728"},
            {"image": "ارقام_89.png", "answer": "39281"},
            {"image": "ارقام_90.png", "answer": "74829"},
            {"image": "ارقام_91.png", "answer": "81920"},
            {"image": "ارقام_92.png", "answer": "374829"},
            {"image": "ارقام_93.png", "answer": "58192"},
            {"image": "ارقام_94.png", "answer": "293847"},
            {"image": "ارقام_95.png", "answer": "48192"},
            {"image": "ارقام_96.png", "answer": "64738"},
            {"image": "ارقام_97.png", "answer": "102938"},
            {"image": "ارقام_98.png", "answer": "58291"},
            {"image": "ارقام_99.png", "answer": "837462"},
            {"image": "ارقام_100.png", "answer": "29183"},
            {"image": "ارقام_101.png", "answer": "748291"},
            {"image": "ارقام_102.png", "answer": "38291"},
            {"image": "ارقام_103.png", "answer": "910283"},
            {"image": "ارقام_104.png", "answer": "48291"},
            {"image": "ارقام_105.png", "answer": "65748"},
            {"image": "ارقام_106.png", "answer": "29183"},
            {"image": "ارقام_107.png", "answer": "847562"},
            {"image": "ارقام_108.png", "answer": "10394"},
            {"image": "ارقام_109.png", "answer": "592847"},
            {"image": "ارقام_110.png", "answer": "83920"},
            {"image": "ارقام_111.png", "answer": "485729"},
            {"image": "ارقام_112.png", "answer": "60192"},
            {"image": "ارقام_113.png", "answer": "384756"},
            {"image": "ارقام_114.png", "answer": "29103"},
            {"image": "ارقام_115.png", "answer": "748592"},
            {"image": "ارقام_116.png", "answer": "58392"},
            {"image": "ارقام_117.png", "answer": "192847"},
            {"image": "ارقام_118.png", "answer": "30495"},
            {"image": "ارقام_119.png", "answer": "857392"},
            {"image": "ارقام_120.png", "answer": "49281"},
            {"image": "ارقام_121.png", "answer": "683920"},
            {"image": "ارقام_122.png", "answer": "19283"},
            {"image": "ارقام_123.png", "answer": "574839"},
            {"image": "ارقام_124.png", "answer": "20394"},
            {"image": "ارقام_125.png", "answer": "847593"},
            {"image": "ارقام_126.png", "answer": "39485"},
            {"image": "ارقام_127.png", "answer": "102938"},
            {"image": "ارقام_128.png", "answer": "58493"},
            {"image": "ارقام_129.png", "answer": "203948"},
            {"image": "ارقام_130.png", "answer": "48593"},
            {"image": "ارقام_131.png", "answer": "103928"},
            {"image": "ارقام_132.png", "answer": "58492"},
            {"image": "ارقام_133.png", "answer": "203948"},
            {"image": "ارقام_134.png", "answer": "48593"},
            {"image": "ارقام_135.png", "answer": "102938"},
            {"image": "ارقام_136.png", "answer": "54923"},
            {"image": "ارقام_137.png", "answer": "810293"},
            {"image": "ارقام_138.png", "answer": "47182"},
            {"image": "ارقام_139.png", "answer": "930182"},
            {"image": "ارقام_140.png", "answer": "56281"},
            {"image": "ارقام_141.png", "answer": "749201"},
            {"image": "ارقام_142.png", "answer": "38192"},
            {"image": "ارقام_143.png", "answer": "650293"},
            {"image": "ارقام_144.png", "answer": "18472"},
            {"image": "ارقام_145.png", "answer": "920384"},
            {"image": "ارقام_146.png", "answer": "37482"},
            {"image": "ارقام_147.png", "answer": "591028"},
            {"image": "ارقام_148.png", "answer": "68291"},
            {"image": "ارقام_149.png", "answer": "104928"},
            {"image": "ارقام_150.png", "answer": "57382"}
            
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

    @commands.command(name="-ارقام")
    async def start_game_cmd(self, ctx):
        await self.run_game(ctx.channel)

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return
        if message.content.strip() == "-ارقام":
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
    await bot.add_cog(aaagame(bot))