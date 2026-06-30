import discord
from discord.ext import commands
import random
import asyncio
import json
import os


class asabgame(commands.Cog):
    def __init__(self, bot):    
        self.bot = bot
        self.scores_file = "global_points.json" # 🟢 اسم ملف النقاط الموحد والمشترك
        
        # 🟢 التأكد من وجود القفل العام المشترك داخل كائن البوت
        if not hasattr(self.bot, 'global_game_lock'):
            self.bot.global_game_lock = set()

        self.questions = [
            {"image": "حساب_1.png", "answer": "39"},
            {"image": "حساب_2.png", "answer": "25"},
            {"image": "حساب_3.png", "answer": "30"},
            {"image": "حساب_4.png", "answer": "5"},
            {"image": "حساب_5.png", "answer": "50"},
            {"image": "حساب_6.png", "answer": "55"},
            {"image": "حساب_7.png", "answer": "72"},
            {"image": "حساب_8.png", "answer": "10"},
            {"image": "حساب_9.png", "answer": "155"},
            {"image": "حساب_10.png", "answer": "76"},
            {"image": "حساب_11.png", "answer": "48"},
            {"image": "حساب_12.png", "answer": "9"},
            {"image": "حساب_13.png", "answer": "92"},
            {"image": "حساب_14.png", "answer": "42"},
            {"image": "حساب_15.png", "answer": "49"},
            {"image": "حساب_16.png", "answer": "10"},
            {"image": "حساب_17.png", "answer": "97"},
            {"image": "حساب_18.png", "answer": "75"},
            {"image": "حساب_19.png", "answer": "45"},
            {"image": "حساب_20.png", "answer": "6"},
            {"image": "حساب_21.png", "answer": "55"},
            {"image": "حساب_22.png", "answer": "44"},
            {"image": "حساب_23.png", "answer": "54"},
            {"image": "حساب_24.png", "answer": "7"},
            {"image": "حساب_25.png", "answer": "100"},
            {"image": "حساب_26.png", "answer": "26"},
            {"image": "حساب_27.png", "answer": "32"},
            {"image": "حساب_28.png", "answer": "8"},
            {"image": "حساب_29.png", "answer": "88"},
            {"image": "حساب_30.png", "answer": "16"},
            {"image": "حساب_31.png", "answer": "55"},
            {"image": "حساب_32.png", "answer": "12"},
            {"image": "حساب_33.png", "answer": "95"},
            {"image": "حساب_34.png", "answer": "50"},
            {"image": "حساب_35.png", "answer": "60"},
            {"image": "حساب_36.png", "answer": "5"},
            {"image": "حساب_37.png", "answer": "90"},
            {"image": "حساب_38.png", "answer": "45"},
            {"image": "حساب_39.png", "answer": "45"},
            {"image": "حساب_40.png", "answer": "8"},
            {"image": "حساب_41.png", "answer": "85"},
            {"image": "حساب_42.png", "answer": "48"},
            {"image": "حساب_43.png", "answer": "50"},
            {"image": "حساب_44.png", "answer": "15"},
            {"image": "حساب_45.png", "answer": "106"},
            {"image": "حساب_46.png", "answer": "22"},
            {"image": "حساب_47.png", "answer": "28"},
            {"image": "حساب_48.png", "answer": "12"},
            {"image": "حساب_49.png", "answer": "80"},
            {"image": "حساب_50.png", "answer": "88"},
            {"image": "حساب_51.png", "answer": "40"},
            {"image": "حساب_52.png", "answer": "7"},
            {"image": "حساب_53.png", "answer": "80"},
            {"image": "حساب_54.png", "answer": "45"},
            {"image": "حساب_55.png", "answer": "100"},
            {"image": "حساب_56.png", "answer": "7"},
            {"image": "حساب_57.png", "answer": "98"},
            {"image": "حساب_58.png", "answer": "19"},
            {"image": "حساب_59.png", "answer": "28"},
            {"image": "حساب_60.png", "answer": "10"},
            {"image": "حساب_61.png", "answer": "77"},
            {"image": "حساب_62.png", "answer": "18"},
            {"image": "حساب_63.png", "answer": "27"},
            {"image": "حساب_64.png", "answer": "7"},
            {"image": "حساب_65.png", "answer": "85"},
            {"image": "حساب_66.png", "answer": "32"},
            {"image": "حساب_67.png", "answer": "72"},
            {"image": "حساب_68.png", "answer": "7"},
            {"image": "حساب_69.png", "answer": "99"},
            {"image": "حساب_70.png", "answer": "40"},
            {"image": "حساب_71.png", "answer": "75"},
            {"image": "حساب_72.png", "answer": "5"},
            {"image": "حساب_73.png", "answer": "100"},
            {"image": "حساب_74.png", "answer": "26"},
            {"image": "حساب_75.png", "answer": "56"},
            {"image": "حساب_76.png", "answer": "10"},
            {"image": "حساب_77.png", "answer": "95"},
            {"image": "حساب_78.png", "answer": "40"},
            {"image": "حساب_79.png", "answer": "36"},
            {"image": "حساب_80.png", "answer": "9"},
            {"image": "حساب_81.png", "answer": "21"},
            {"image": "حساب_82.png", "answer": "39"},
            {"image": "حساب_83.png", "answer": "36"},
            {"image": "حساب_84.png", "answer": "5"},
            {"image": "حساب_85.png", "answer": "99"},
            {"image": "حساب_86.png", "answer": "20"},
            {"image": "حساب_87.png", "answer": "121"},
            {"image": "حساب_88.png", "answer": "8"},
            {"image": "حساب_89.png", "answer": "93"},
            {"image": "حساب_90.png", "answer": "22"},
            {"image": "حساب_91.png", "answer": "60"},
            {"image": "حساب_92.png", "answer": "8"},
            {"image": "حساب_93.png", "answer": "100"},
            {"image": "حساب_94.png", "answer": "22"},
            {"image": "حساب_95.png", "answer": "56"},
            {"image": "حساب_96.png", "answer": "4"},
            {"image": "حساب_97.png", "answer": "44"},
            {"image": "حساب_98.png", "answer": "15"},
            {"image": "حساب_99.png", "answer": "45"},
            {"image": "حساب_100.png", "answer": "8"},
            {"image": "حساب_101.png", "answer": "80"},
            {"image": "حساب_102.png", "answer": "22"},
            {"image": "حساب_103.png", "answer": "120"},
            {"image": "حساب_104.png", "answer": "9"},
            {"image": "حساب_105.png", "answer": "70"},
            {"image": "حساب_106.png", "answer": "69"},
            {"image": "حساب_107.png", "answer": "56"},
            {"image": "حساب_108.png", "answer": "6"},
            {"image": "حساب_109.png", "answer": "90"},
            {"image": "حساب_110.png", "answer": "66"},
            {"image": "حساب_111.png", "answer": "45"},
            {"image": "حساب_112.png", "answer": "3"},
            {"image": "حساب_113.png", "answer": "84"},
            {"image": "حساب_114.png", "answer": "38"},
            {"image": "حساب_115.png", "answer": "32"},
            {"image": "حساب_116.png", "answer": "4"},
            {"image": "حساب_117.png", "answer": "60"},
            {"image": "حساب_118.png", "answer": "36"},
            {"image": "حساب_119.png", "answer": "60"},
            {"image": "حساب_120.png", "answer": "8"},
            {"image": "حساب_121.png", "answer": "80"},
            {"image": "حساب_122.png", "answer": "10"},
            {"image": "حساب_123.png", "answer": "42"},
            {"image": "حساب_124.png", "answer": "8"},
            {"image": "حساب_125.png", "answer": "100"},
            {"image": "حساب_126.png", "answer": "30"},
            {"image": "حساب_127.png", "answer": "90"},
            {"image": "حساب_128.png", "answer": "9"},
            {"image": "حساب_129.png", "answer": "110"},
            {"image": "حساب_130.png", "answer": "44"},
            {"image": "حساب_131.png", "answer": "60"},
            {"image": "حساب_132.png", "answer": "3"},
            {"image": "حساب_133.png", "answer": "83"},
            {"image": "حساب_134.png", "answer": "35"},
            {"image": "حساب_135.png", "answer": "63"},
            {"image": "حساب_136.png", "answer": "11"},
            {"image": "حساب_137.png", "answer": "90"},
            {"image": "حساب_138.png", "answer": "19"},
            {"image": "حساب_139.png", "answer": "100"},
            {"image": "حساب_140.png", "answer": "50"},
            {"image": "حساب_141.png", "answer": "72"},
            {"image": "حساب_142.png", "answer": "11"},
            {"image": "حساب_143.png", "answer": "50"},
            {"image": "حساب_144.png", "answer": "50"},
            {"image": "حساب_145.png", "answer": "77"},
            {"image": "حساب_146.png", "answer": "5"},
            {"image": "حساب_147.png", "answer": "74"},
            {"image": "حساب_148.png", "answer": "100"}
                        
                        
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

    @commands.command(name="-حساب")
    async def start_game_cmd(self, ctx):
        await self.run_game(ctx.channel)

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return
        if message.content.strip() == "-حساب":
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
    await bot.add_cog(asabgame(bot))