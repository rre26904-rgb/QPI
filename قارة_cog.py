import discord
from discord.ext import commands
import random
import asyncio
import json
import os


class qarhgame(commands.Cog):
    def __init__(self, bot):    
        self.bot = bot
        self.scores_file = "global_points.json" # 🟢 اسم ملف النقاط الموحد والمشترك
        
        # 🟢 التأكد من وجود القفل العام المشترك داخل كائن البوت
        if not hasattr(self.bot, 'global_game_lock'):
            self.bot.global_game_lock = set()

        self.questions = [
            {"image": "قارة_1.png", "answer": "اسيا"},
            {"image": "قارة_2.png", "answer": "امريكا الجنوبية"},
            {"image": "قارة_3.png", "answer": "اسيا"},
            {"image": "قارة_4.png", "answer": "اسيا"},
            {"image": "قارة_5.png", "answer": "افريقيا"},
            {"image": "قارة_6.png", "answer": "اوروبا"},
            {"image": "قارة_7.png", "answer": "اوقيانوسيا"},
            {"image": "قارة_8.png", "answer": "اوروبا"},
            {"image": "قارة_9.png", "answer": "اسيا"},
            {"image": "قارة_10.png", "answer": "اوروبا"},
            {"image": "قارة_11.png", "answer": "اوروبا"},
            {"image": "قارة_12.png", "answer": "اسيا"},
            {"image": "قارة_13.png", "answer": "اسيا"},
            {"image": "قارة_14.png", "answer": "افريقيا"},
            {"image": "قارة_15.png", "answer": "اوروبا"},
            {"image": "قارة_16.png", "answer": "امريكا الجنوبية"},
            {"image": "قارة_17.png", "answer": "اسيا"},
            {"image": "قارة_18.png", "answer": "افريقيا"},
            {"image": "قارة_19.png", "answer": "اوروبا"},
            {"image": "قارة_20.png", "answer": "اسيا"},
            {"image": "قارة_21.png", "answer": "اوروبا"},
            {"image": "قارة_22.png", "answer": "اوروبا"},
            {"image": "قارة_23.png", "answer": "اسيا"},
            {"image": "قارة_24.png", "answer": "اسيا"},
            {"image": "قارة_25.png", "answer": "امريكا الجنوبية"},
            {"image": "قارة_26.png", "answer": "اوروبا"},
            {"image": "قارة_27.png", "answer": "اسيا"},
            {"image": "قارة_28.png", "answer": "اوروبا"},
            {"image": "قارة_29.png", "answer": "اوروبا"},
            {"image": "قارة_30.png", "answer": "امريكا الشمالية"},
            {"image": "قارة_31.png", "answer": "اسيا"},
            {"image": "قارة_32.png", "answer": "افريقيا"},
            {"image": "قارة_33.png", "answer": "اوروبا"},
            {"image": "قارة_34.png", "answer": "اوروبا"},
            {"image": "قارة_35.png", "answer": "امريكا الجنوبية"},
            {"image": "قارة_36.png", "answer": "امريكا الجنوبية"},
            {"image": "قارة_37.png", "answer": "اوروبا"},
            {"image": "قارة_38.png", "answer": "اسيا"},
            {"image": "قارة_39.png", "answer": "اسيا"},
            {"image": "قارة_40.png", "answer": "افريقيا"},
            {"image": "قارة_41.png", "answer": "امريكا الجنوبية"},
            {"image": "قارة_42.png", "answer": "افريقيا"},
            {"image": "قارة_43.png", "answer": "افريقيا"},
            {"image": "قارة_44.png", "answer": "افريقيا"},
            {"image": "قارة_45.png", "answer": "اسيا"},
            {"image": "قارة_46.png", "answer": "افريقيا"},
            {"image": "قارة_47.png", "answer": "امريكا الشمالية"},
            {"image": "قارة_48.png", "answer": "افريقيا"},
            {"image": "قارة_49.png", "answer": "اوقيانوسيا"},
            {"image": "قارة_50.png", "answer": "اوقيانوسيا"},
            {"image": "قارة_51.png", "answer": "اسيا"},
            {"image": "قارة_52.png", "answer": "افريقيا"},
            {"image": "قارة_53.png", "answer": "افريقيا"},
            {"image": "قارة_54.png", "answer": "افريقيا"},
            {"image": "قارة_55.png", "answer": "امريكا الشمالية"},
            {"image": "قارة_56.png", "answer": "امريكا الشمالية"},
            {"image": "قارة_57.png", "answer": "اوروبا"},
            {"image": "قارة_58.png", "answer": "افريقيا"},
            {"image": "قارة_59.png", "answer": "اوروبا"},
            {"image": "قارة_60.png", "answer": "اوروبا"},
            {"image": "قارة_61.png", "answer": "افريقيا"},
            {"image": "قارة_62.png", "answer": "افريقيا"},
            {"image": "قارة_63.png", "answer": "افريقيا"},
            {"image": "قارة_64.png", "answer": "اسيا"},
            {"image": "قارة_65.png", "answer": "اسيا"},
            {"image": "قارة_66.png", "answer": "امريكا الشمالية"},
            {"image": "قارة_67.png", "answer": "اوروبا"},
            {"image": "قارة_68.png", "answer": "اوروبا"},
            {"image": "قارة_69.png", "answer": "اسيا"},
            {"image": "قارة_70.png", "answer": "افريقيا"},
            {"image": "قارة_71.png", "answer": "افريقيا"},
            {"image": "قارة_72.png", "answer": "اسيا"},
            {"image": "قارة_73.png", "answer": "امريكا الجنوبية"},
            {"image": "قارة_74.png", "answer": "افريقيا"},
            {"image": "قارة_75.png", "answer": "اوروبا"},
            {"image": "قارة_76.png", "answer": "افريقيا"},
            {"image": "قارة_77.png", "answer": "افريقيا"},
            {"image": "قارة_78.png", "answer": "اوروبا"},
            {"image": "قارة_79.png", "answer": "اوروبا"},
            {"image": "قارة_80.png", "answer": "افريقيا"},
            {"image": "قارة_81.png", "answer": "اسيا"},
            {"image": "قارة_82.png", "answer": "اسيا"},
            {"image": "قارة_83.png", "answer": "اسيا"},
            {"image": "قارة_84.png", "answer": "اسيا"},
            {"image": "قارة_85.png", "answer": "افريقيا"},
            {"image": "قارة_86.png", "answer": "افريقيا"},
            {"image": "قارة_87.png", "answer": "افريقيا"},
            {"image": "قارة_88.png", "answer": "افريقيا"},
            {"image": "قارة_89.png", "answer": "اوقيانوسيا"},
            {"image": "قارة_90.png", "answer": "اوروبا"},
            {"image": "قارة_91.png", "answer": "اسيا"},
            {"image": "قارة_92.png", "answer": "اسيا"},
            {"image": "قارة_93.png", "answer": "اوروبا"},
            {"image": "قارة_94.png", "answer": "اسيا"},
            {"image": "قارة_95.png", "answer": "اوقيانوسيا"},
            {"image": "قارة_96.png", "answer": "اوروبا"},
            {"image": "قارة_97.png", "answer": "اسيا"},
            {"image": "قارة_98.png", "answer": "اسيا"},
            {"image": "قارة_99.png", "answer": "اسيا"},
            {"image": "قارة_100.png", "answer": "افريقيا"},
            {"image": "قارة_101.png", "answer": "امريكا الشمالية"},
            {"image": "قارة_102.png", "answer": "امريكا الشمالية"},
            {"image": "قارة_103.png", "answer": "اسيا"},
            {"image": "قارة_104.png", "answer": "امريكا الجنوبية"},
            {"image": "قارة_105.png", "answer": "افريقيا"},
            {"image": "قارة_106.png", "answer": "امريكا الشمالية"},
            {"image": "قارة_107.png", "answer": "اوروبا"},
            {"image": "قارة_108.png", "answer": "اسيا"},
            {"image": "قارة_109.png", "answer": "افريقيا"},
            {"image": "قارة_110.png", "answer": "اوروبا"},
            {"image": "قارة_111.png", "answer": "اسيا"},
            {"image": "قارة_112.png", "answer": "اسيا"},
            {"image": "قارة_113.png", "answer": "افريقيا"},
            {"image": "قارة_114.png", "answer": "افريقيا"},
            {"image": "قارة_115.png", "answer": "اوروبا"},
            {"image": "قارة_116.png", "answer": "اوروبا"},
            {"image": "قارة_117.png", "answer": "اوروبا"},
            {"image": "قارة_118.png", "answer": "اوروبا"},
            {"image": "قارة_119.png", "answer": "اسيا"},
            {"image": "قارة_120.png", "answer": "اوروبا"},
            {"image": "قارة_121.png", "answer": "افريقيا"},
            {"image": "قارة_122.png", "answer": "اسيا"},
            {"image": "قارة_123.png", "answer": "افريقيا"},
            {"image": "قارة_124.png", "answer": "امريكا الشمالية"},
            {"image": "قارة_125.png", "answer": "افريقيا"},
            {"image": "قارة_126.png", "answer": "افريقيا"},
            {"image": "قارة_127.png", "answer": "افريقيا"},
            {"image": "قارة_128.png", "answer": "اوروبا"},
            {"image": "قارة_129.png", "answer": "اوروبا"},
            {"image": "قارة_130.png", "answer": "اسيا"},
            {"image": "قارة_131.png", "answer": "اسيا"},
            {"image": "قارة_132.png", "answer": "افريقيا"},
            {"image": "قارة_133.png", "answer": "امريكا الشمالية"},
            {"image": "قارة_134.png", "answer": "اوقيانوسيا"},
            {"image": "قارة_135.png", "answer": "افريقيا"},
            {"image": "قارة_136.png", "answer": "اوروبا"},
            {"image": "قارة_137.png", "answer": "اوروبا"},
            {"image": "قارة_138.png", "answer": "امريكا الشمالية"},
            {"image": "قارة_139.png", "answer": "اسيا"},
            {"image": "قارة_140.png", "answer": "اوروبا"},
            {"image": "قارة_141.png", "answer": "امريكا الشمالية"},
            {"image": "قارة_142.png", "answer": "اسيا"},
            {"image": "قارة_143.png", "answer": "اسيا"},
            {"image": "قارة_144.png", "answer": "اوروبا"},
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

    @commands.command(name="-قارة")
    async def start_game_cmd(self, ctx):
        await self.run_game(ctx.channel)

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return
        if message.content.strip() == "-قارة":
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
    await bot.add_cog(qarhgame(bot))