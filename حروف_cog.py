import discord
from discord.ext import commands
import random
import asyncio
import json
import os


class arofgame(commands.Cog):
    def __init__(self, bot):    
        self.bot = bot
        self.scores_file = "global_points.json" # 🟢 اسم ملف النقاط الموحد والمشترك
        
        # 🟢 التأكد من وجود القفل العام المشترك داخل كائن البوت
        if not hasattr(self.bot, 'global_game_lock'):
            self.bot.global_game_lock = set()

        self.questions = [
            {"image": "حروف_1.png", "answer": "3"},
            {"image": "حروف_2.png", "answer": "3"},
            {"image": "حروف_3.png", "answer": "3"},
            {"image": "حروف_4.png", "answer": "3"},
            {"image": "حروف_5.png", "answer": "3"},
            {"image": "حروف_6.png", "answer": "3"},
            {"image": "حروف_7.png", "answer": "4"},
            {"image": "حروف_8.png", "answer": "4"},
            {"image": "حروف_9.png", "answer": "3"},
            {"image": "حروف_10.png", "answer": "5"},
            {"image": "حروف_11.png", "answer": "3"},
            {"image": "حروف_12.png", "answer": "4"},
            {"image": "حروف_13.png", "answer": "4"},
            {"image": "حروف_14.png", "answer": "4"},
            {"image": "حروف_15.png", "answer": "4"},
            {"image": "حروف_16.png", "answer": "3"},
            {"image": "حروف_17.png", "answer": "5"},
            {"image": "حروف_18.png", "answer": "3"},
            {"image": "حروف_19.png", "answer": "5"},
            {"image": "حروف_20.png", "answer": "5"},
            {"image": "حروف_21.png", "answer": "3"},
            {"image": "حروف_22.png", "answer": "3"},
            {"image": "حروف_23.png", "answer": "4"},
            {"image": "حروف_24.png", "answer": "4"},
            {"image": "حروف_25.png", "answer": "5"},
            {"image": "حروف_26.png", "answer": "5"},
            {"image": "حروف_27.png", "answer": "5"},
            {"image": "حروف_28.png", "answer": "4"},
            {"image": "حروف_29.png", "answer": "3"},
            {"image": "حروف_30.png", "answer": "3"},
            {"image": "حروف_31.png", "answer": "6"},
            {"image": "حروف_32.png", "answer": "6"},
            {"image": "حروف_33.png", "answer": "6"},
            {"image": "حروف_34.png", "answer": "5"},
            {"image": "حروف_35.png", "answer": "5"},
            {"image": "حروف_36.png", "answer": "3"},
            {"image": "حروف_37.png", "answer": "4"},
            {"image": "حروف_38.png", "answer": "6"},
            {"image": "حروف_39.png", "answer": "4"},
            {"image": "حروف_40.png", "answer": "5"},
            {"image": "حروف_41.png", "answer": "4"},
            {"image": "حروف_42.png", "answer": "5"},
            {"image": "حروف_43.png", "answer": "5"},
            {"image": "حروف_44.png", "answer": "5"},
            {"image": "حروف_45.png", "answer": "4"},
            {"image": "حروف_46.png", "answer": "4"},
            {"image": "حروف_47.png", "answer": "4"},
            {"image": "حروف_48.png", "answer": "4"},
            {"image": "حروف_49.png", "answer": "3"},
            {"image": "حروف_50.png", "answer": "4"},
            {"image": "حروف_51.png", "answer": "3"},
            {"image": "حروف_52.png", "answer": "3"},
            {"image": "حروف_53.png", "answer": "3"},
            {"image": "حروف_54.png", "answer": "4"},
            {"image": "حروف_55.png", "answer": "4"},
            {"image": "حروف_56.png", "answer": "6"},
            {"image": "حروف_57.png", "answer": "3"},
            {"image": "حروف_58.png", "answer": "3"},
            {"image": "حروف_59.png", "answer": "3"},
            {"image": "حروف_60.png", "answer": "3"},
            {"image": "حروف_61.png", "answer": "4"},
            {"image": "حروف_62.png", "answer": "4"},
            {"image": "حروف_63.png", "answer": "6"},
            {"image": "حروف_64.png", "answer": "3"},
            {"image": "حروف_65.png", "answer": "3"},
            {"image": "حروف_66.png", "answer": "5"},
            {"image": "حروف_67.png", "answer": "6"},
            {"image": "حروف_68.png", "answer": "4"},
            {"image": "حروف_69.png", "answer": "4"},
            {"image": "حروف_70.png", "answer": "3"},
            {"image": "حروف_71.png", "answer": "3"},
            {"image": "حروف_72.png", "answer": "3"},
            {"image": "حروف_73.png", "answer": "4"},
            {"image": "حروف_74.png", "answer": "5"},
            {"image": "حروف_75.png", "answer": "5"},
            {"image": "حروف_76.png", "answer": "2"},
            {"image": "حروف_77.png", "answer": "6"},
            {"image": "حروف_78.png", "answer": "5"},
            {"image": "حروف_79.png", "answer": "4"},
            {"image": "حروف_80.png", "answer": "3"},
            {"image": "حروف_81.png", "answer": "7"},
            {"image": "حروف_82.png", "answer": "4"},
            {"image": "حروف_83.png", "answer": "5"},
            {"image": "حروف_84.png", "answer": "5"},
            {"image": "حروف_85.png", "answer": "4"},
            {"image": "حروف_86.png", "answer": "3"},
            {"image": "حروف_87.png", "answer": "3"},
            {"image": "حروف_88.png", "answer": "3"},
            {"image": "حروف_89.png", "answer": "4"},
            {"image": "حروف_90.png", "answer": "3"},
            {"image": "حروف_91.png", "answer": "3"},
            {"image": "حروف_92.png", "answer": "3"},
            {"image": "حروف_93.png", "answer": "2"},
            {"image": "حروف_94.png", "answer": "4"},
            {"image": "حروف_95.png", "answer": "5"},
            {"image": "حروف_96.png", "answer": "4"},
            {"image": "حروف_97.png", "answer": "5"},
            {"image": "حروف_98.png", "answer": "4"},
            {"image": "حروف_99.png", "answer": "3"},
            {"image": "حروف_100.png", "answer": "3"},
            {"image": "حروف_101.png", "answer": "3"},
            {"image": "حروف_102.png", "answer": "4"},
            {"image": "حروف_103.png", "answer": "4"},
            {"image": "حروف_104.png", "answer": "4"},
            {"image": "حروف_105.png", "answer": "4"},
            {"image": "حروف_106.png", "answer": "4"},
            {"image": "حروف_107.png", "answer": "4"},
            {"image": "حروف_108.png", "answer": "5"},
            {"image": "حروف_109.png", "answer": "5"},
            {"image": "حروف_110.png", "answer": "4"},
            {"image": "حروف_111.png", "answer": "4"},
            {"image": "حروف_112.png", "answer": "5"},
            {"image": "حروف_113.png", "answer": "4"},
            {"image": "حروف_114.png", "answer": "5"},
            {"image": "حروف_115.png", "answer": "4"},
            {"image": "حروف_116.png", "answer": "3"},
            {"image": "حروف_117.png", "answer": "3"},
            {"image": "حروف_118.png", "answer": "4"},
            {"image": "حروف_119.png", "answer": "4"},
            {"image": "حروف_120.png", "answer": "5"},
            {"image": "حروف_121.png", "answer": "4"},
            {"image": "حروف_122.png", "answer": "6"},
            {"image": "حروف_123.png", "answer": "5"},
            {"image": "حروف_124.png", "answer": "5"},
            {"image": "حروف_125.png", "answer": "4"},
            {"image": "حروف_126.png", "answer": "4"},
            {"image": "حروف_127.png", "answer": "4"},
            {"image": "حروف_128.png", "answer": "4"},
            {"image": "حروف_129.png", "answer": "4"},
            {"image": "حروف_130.png", "answer": "4"},
            {"image": "حروف_131.png", "answer": "4"},
            {"image": "حروف_132.png", "answer": "3"},
            {"image": "حروف_133.png", "answer": "4"},
            {"image": "حروف_134.png", "answer": "5"},
            {"image": "حروف_135.png", "answer": "5"},
            {"image": "حروف_136.png", "answer": "4"},
            {"image": "حروف_137.png", "answer": "5"},
            {"image": "حروف_138.png", "answer": "4"},
            {"image": "حروف_139.png", "answer": "4"},
            {"image": "حروف_140.png", "answer": "4"},
            {"image": "حروف_141.png", "answer": "4"},
            {"image": "حروف_142.png", "answer": "4"},
            {"image": "حروف_143.png", "answer": "4"},
            {"image": "حروف_144.png", "answer": "4"},
            {"image": "حروف_145.png", "answer": "4"},
            {"image": "حروف_146.png", "answer": "5"},
            {"image": "حروف_147.png", "answer": "4"},
            {"image": "حروف_148.png", "answer": "4"},
            {"image": "حروف_149.png", "answer": "4"},
            {"image": "حروف_150.png", "answer": "4"},
            {"image": "حروف_151.png", "answer": "5"},
            {"image": "حروف_152.png", "answer": "4"},
            {"image": "حروف_153.png", "answer": "5"},
            {"image": "حروف_154.png", "answer": "5"},
            {"image": "حروف_155.png", "answer": "4"},
            {"image": "حروف_156.png", "answer": "5"},
            {"image": "حروف_157.png", "answer": "5"},
            {"image": "حروف_158.png", "answer": "5"},
            {"image": "حروف_159.png", "answer": "5"},
            {"image": "حروف_160.png", "answer": "5"},
            {"image": "حروف_161.png", "answer": "5"},
            {"image": "حروف_162.png", "answer": "4"},
            {"image": "حروف_163.png", "answer": "4"},
            {"image": "حروف_164.png", "answer": "5"},
            {"image": "حروف_165.png", "answer": "5"},
            {"image": "حروف_166.png", "answer": "5"},
            {"image": "حروف_167.png", "answer": "6"},
            {"image": "حروف_168.png", "answer": "5"},
            {"image": "حروف_169.png", "answer": "6"},
            {"image": "حروف_170.png", "answer": "4"},
            {"image": "حروف_171.png", "answer": "5"},
            {"image": "حروف_172.png", "answer": "3"},
            {"image": "حروف_173.png", "answer": "4"},
            {"image": "حروف_174.png", "answer": "4"},
            {"image": "حروف_175.png", "answer": "5"},
            {"image": "حروف_176.png", "answer": "4"},
            {"image": "حروف_177.png", "answer": "5"},
            {"image": "حروف_178.png", "answer": "4"},
            {"image": "حروف_179.png", "answer": "4"},
            {"image": "حروف_180.png", "answer": "4"},
            {"image": "حروف_181.png", "answer": "3"},
            {"image": "حروف_182.png", "answer": "3"},
            {"image": "حروف_183.png", "answer": "3"},
            {"image": "حروف_184.png", "answer": "3"},
            {"image": "حروف_185.png", "answer": "3"},
            {"image": "حروف_186.png", "answer": "4"},
            {"image": "حروف_187.png", "answer": "4"},
            {"image": "حروف_188.png", "answer": "4"},
            {"image": "حروف_189.png", "answer": "3"},
            {"image": "حروف_190.png", "answer": "4"},
            {"image": "حروف_191.png", "answer": "3"},
            {"image": "حروف_192.png", "answer": "3"},
            {"image": "حروف_193.png", "answer": "6"},
            {"image": "حروف_194.png", "answer": "6"},
            {"image": "حروف_195.png", "answer": "5"},
            {"image": "حروف_196.png", "answer": "5"},
            {"image": "حروف_197.png", "answer": "7"},
            {"image": "حروف_198.png", "answer": "5"},
            {"image": "حروف_199.png", "answer": "5"},
            {"image": "حروف_200.png", "answer": "4"},
            {"image": "حروف_201.png", "answer": "3"},
            {"image": "حروف_202.png", "answer": "3"},
            {"image": "حروف_203.png", "answer": "3"},
            {"image": "حروف_204.png", "answer": "3"},
            {"image": "حروف_205.png", "answer": "4"},
            {"image": "حروف_206.png", "answer": "3"},
            {"image": "حروف_207.png", "answer": "2"},
            {"image": "حروف_208.png", "answer": "3"},
            {"image": "حروف_209.png", "answer": "5"},
            {"image": "حروف_210.png", "answer": "4"},
            {"image": "حروف_211.png", "answer": "3"},
            {"image": "حروف_212.png", "answer": "2"},
            {"image": "حروف_213.png", "answer": "4"},
            {"image": "حروف_214.png", "answer": "3"},
            {"image": "حروف_215.png", "answer": "4"},
            {"image": "حروف_216.png", "answer": "2"},
            {"image": "حروف_217.png", "answer": "4"},
            {"image": "حروف_218.png", "answer": "3"},
            {"image": "حروف_219.png", "answer": "3"},
            {"image": "حروف_220.png", "answer": "3"},
            {"image": "حروف_221.png", "answer": "3"},
            {"image": "حروف_222.png", "answer": "3"},
            {"image": "حروف_223.png", "answer": "3"},
            {"image": "حروف_224.png", "answer": "4"},
            {"image": "حروف_225.png", "answer": "3"},
            {"image": "حروف_226.png", "answer": "3"},
            {"image": "حروف_227.png", "answer": "3"},
            {"image": "حروف_228.png", "answer": "4"},
            {"image": "حروف_229.png", "answer": "4"},
            {"image": "حروف_230.png", "answer": "2"},
            {"image": "حروف_231.png", "answer": "4"},
            {"image": "حروف_232.png", "answer": "4"},
            {"image": "حروف_233.png", "answer": "4"},
            {"image": "حروف_234.png", "answer": "4"},
            {"image": "حروف_235.png", "answer": "6"},
            {"image": "حروف_236.png", "answer": "4"},
            {"image": "حروف_237.png", "answer": "4"},
            {"image": "حروف_238.png", "answer": "5"},
            {"image": "حروف_239.png", "answer": "3"},
            {"image": "حروف_240.png", "answer": "4"},
            {"image": "حروف_241.png", "answer": "3"},
            {"image": "حروف_242.png", "answer": "3"},
            {"image": "حروف_243.png", "answer": "3"},
            {"image": "حروف_244.png", "answer": "4"},
            {"image": "حروف_245.png", "answer": "4"},
            {"image": "حروف_246.png", "answer": "4"},
            {"image": "حروف_247.png", "answer": "4"},
            {"image": "حروف_248.png", "answer": "3"},
            {"image": "حروف_249.png", "answer": "4"},
            {"image": "حروف_250.png", "answer": "3"},
            {"image": "حروف_251.png", "answer": "4"},
            {"image": "حروف_252.png", "answer": "4"},
            {"image": "حروف_253.png", "answer": "4"},
            {"image": "حروف_254.png", "answer": "4"},
            {"image": "حروف_255.png", "answer": "3"},
            {"image": "حروف_256.png", "answer": "4"},
            {"image": "حروف_257.png", "answer": "3"},
            {"image": "حروف_258.png", "answer": "3"},
            {"image": "حروف_259.png", "answer": "5"},
            {"image": "حروف_260.png", "answer": "3"},
            {"image": "حروف_261.png", "answer": "5"},
            {"image": "حروف_262.png", "answer": "5"},
            {"image": "حروف_263.png", "answer": "2"},
            {"image": "حروف_264.png", "answer": "3"},
            {"image": "حروف_265.png", "answer": "3"},
            {"image": "حروف_266.png", "answer": "3"},
            {"image": "حروف_267.png", "answer": "3"},
            {"image": "حروف_268.png", "answer": "3"},
            {"image": "حروف_269.png", "answer": "3"},
            {"image": "حروف_270.png", "answer": "3"},
            {"image": "حروف_271.png", "answer": "3"},
            {"image": "حروف_272.png", "answer": "3"},
            {"image": "حروف_273.png", "answer": "5"},
            {"image": "حروف_274.png", "answer": "3"},
            {"image": "حروف_275.png", "answer": "3"},
            {"image": "حروف_276.png", "answer": "3"},
            {"image": "حروف_277.png", "answer": "4"},
            {"image": "حروف_278.png", "answer": "4"},
            {"image": "حروف_279.png", "answer": "4"},
            {"image": "حروف_280.png", "answer": "3"},
            {"image": "حروف_281.png", "answer": "3"},
            {"image": "حروف_282.png", "answer": "3"},
            {"image": "حروف_283.png", "answer": "5"},
            {"image": "حروف_284.png", "answer": "3"},
            {"image": "حروف_285.png", "answer": "5"},
            {"image": "حروف_286.png", "answer": "3"},
            {"image": "حروف_287.png", "answer": "3"},
            {"image": "حروف_288.png", "answer": "5"},
            {"image": "حروف_289.png", "answer": "3"},
            {"image": "حروف_290.png", "answer": "4"},
            {"image": "حروف_291.png", "answer": "5"},
            {"image": "حروف_292.png", "answer": "3"},
            {"image": "حروف_293.png", "answer": "7"},
            {"image": "حروف_294.png", "answer": "5"},
            {"image": "حروف_295.png", "answer": "3"},
            {"image": "حروف_296.png", "answer": "4"},
            {"image": "حروف_297.png", "answer": "4"},
            {"image": "حروف_298.png", "answer": "5"},
            {"image": "حروف_299.png", "answer": "5"},
            {"image": "حروف_300.png", "answer": "6"}
            
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

    @commands.command(name="-حروف")
    async def start_game_cmd(self, ctx):
        await self.run_game(ctx.channel)

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return
        if message.content.strip() == "-حروف":
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
    await bot.add_cog(arofgame(bot))