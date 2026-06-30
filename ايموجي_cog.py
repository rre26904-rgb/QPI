import discord
from discord.ext import commands
import random
import asyncio
import json
import os


class qwergame(commands.Cog):
    def __init__(self, bot):    
        self.bot = bot
        self.scores_file = "global_points.json" # 🟢 اسم ملف النقاط الموحد والمشترك
        
        # 🟢 التأكد من وجود القفل العام المشترك داخل كائن البوت
        if not hasattr(self.bot, 'global_game_lock'):
            self.bot.global_game_lock = set()

        self.questions = [
            {"image": "ايموجي_1.png", "answer": "😀"},
            {"image": "ايموجي_2.png", "answer": "😃"},
            {"image": "ايموجي_3.png", "answer": "😄"},
            {"image": "ايموجي_4.png", "answer": "😁"},
            {"image": "ايموجي_5.png", "answer": "😆"},
            {"image": "ايموجي_6.png", "answer": "😅"},
            {"image": "ايموجي_7.png", "answer": "😂"},
            {"image": "ايموجي_8.png", "answer": "🤣"},
            {"image": "ايموجي_9.png", "answer": "🥲"},
            {"image": "ايموجي_10.png", "answer": "☺️"},
            {"image": "ايموجي_11.png", "answer": "😊"},
            {"image": "ايموجي_12.png", "answer": "😇"},
            {"image": "ايموجي_13.png", "answer": "🙂"},
            {"image": "ايموجي_14.png", "answer": "🙃"},
            {"image": "ايموجي_15.png", "answer": "😉"},
            {"image": "ايموجي_16.png", "answer": "😌"},
            {"image": "ايموجي_17.png", "answer": "😍"},
            {"image": "ايموجي_18.png", "answer": "🥰"},
            {"image": "ايموجي_19.png", "answer": "😘"},
            {"image": "ايموجي_20.png", "answer": "😗"},
            {"image": "ايموجي_21.png", "answer": "😙"},
            {"image": "ايموجي_22.png", "answer": "😚"},
            {"image": "ايموجي_23.png", "answer": "😋"},
            {"image": "ايموجي_24.png", "answer": "😛"},
            {"image": "ايموجي_25.png", "answer": "😝"},
            {"image": "ايموجي_26.png", "answer": "😜"},
            {"image": "ايموجي_27.png", "answer": "🤪"},
            {"image": "ايموجي_28.png", "answer": "🤨"},
            {"image": "ايموجي_29.png", "answer": "🧐"},
            {"image": "ايموجي_30.png", "answer": "🤓"},
            {"image": "ايموجي_31.png", "answer": "😎"},
            {"image": "ايموجي_32.png", "answer": "🥸"},
            {"image": "ايموجي_33.png", "answer": "🤩"},
            {"image": "ايموجي_34.png", "answer": "🥳"},
            {"image": "ايموجي_35.png", "answer": "😏"},
            {"image": "ايموجي_36.png", "answer": "😒"},
            {"image": "ايموجي_37.png", "answer": "😞"},
            {"image": "ايموجي_38.png", "answer": "😔"},
            {"image": "ايموجي_39.png", "answer": "😟"},
            {"image": "ايموجي_40.png", "answer": "😕"},
            {"image": "ايموجي_41.png", "answer": "🙁"},
            {"image": "ايموجي_42.png", "answer": "☹️"},
            {"image": "ايموجي_43.png", "answer": "😣"},
            {"image": "ايموجي_44.png", "answer": "😖"},
            {"image": "ايموجي_45.png", "answer": "😫"},
            {"image": "ايموجي_46.png", "answer": "😩"},
            {"image": "ايموجي_47.png", "answer": "🥺"},
            {"image": "ايموجي_48.png", "answer": "😢"},
            {"image": "ايموجي_49.png", "answer": "😭"},
            {"image": "ايموجي_50.png", "answer": "😤"},
            {"image": "ايموجي_51.png", "answer": "😠"},
            {"image": "ايموجي_52.png", "answer": "😡"},
            {"image": "ايموجي_53.png", "answer": "🤬"},
            {"image": "ايموجي_54.png", "answer": "🤯"},
            {"image": "ايموجي_55.png", "answer": "😳"},
            {"image": "ايموجي_56.png", "answer": "🥵"},
            {"image": "ايموجي_57.png", "answer": "🥶"},
            {"image": "ايموجي_58.png", "answer": "😱"},
            {"image": "ايموجي_59.png", "answer": "😨"},
            {"image": "ايموجي_60.png", "answer": "😰"},
            {"image": "ايموجي_61.png", "answer": "😥"},
            {"image": "ايموجي_62.png", "answer": "😓"},
            {"image": "ايموجي_63.png", "answer": "🤗"},
            {"image": "ايموجي_64.png", "answer": "🤔"},
            {"image": "ايموجي_65.png", "answer": "🤭"},
            {"image": "ايموجي_66.png", "answer": "🤫"},
            {"image": "ايموجي_67.png", "answer": "🤥"},
            {"image": "ايموجي_68.png", "answer": "😶"},
            {"image": "ايموجي_69.png", "answer": "😐"},
            {"image": "ايموجي_70.png", "answer": "😑"},
            {"image": "ايموجي_71.png", "answer": "😬"},
            {"image": "ايموجي_72.png", "answer": "🙄"},
            {"image": "ايموجي_73.png", "answer": "😯"},
            {"image": "ايموجي_74.png", "answer": "😦"},
            {"image": "ايموجي_75.png", "answer": "😧"},
            {"image": "ايموجي_76.png", "answer": "😮"},
            {"image": "ايموجي_77.png", "answer": "😲"},
            {"image": "ايموجي_78.png", "answer": "🥱"},
            {"image": "ايموجي_79.png", "answer": "😴"},
            {"image": "ايموجي_80.png", "answer": "🤤"},
            {"image": "ايموجي_81.png", "answer": "😪"},
            {"image": "ايموجي_82.png", "answer": "😵"},
            {"image": "ايموجي_83.png", "answer": "🤐"},
            {"image": "ايموجي_84.png", "answer": "🥴"},
            {"image": "ايموجي_85.png", "answer": "🤢"},
            {"image": "ايموجي_86.png", "answer": "🤮"},
            {"image": "ايموجي_87.png", "answer": "🤧"},
            {"image": "ايموجي_88.png", "answer": "😷"},
            {"image": "ايموجي_89.png", "answer": "🤒"},
            {"image": "ايموجي_90.png", "answer": "🤕"},
            {"image": "ايموجي_91.png", "answer": "🤑"},
            {"image": "ايموجي_92.png", "answer": "🤠"},
            {"image": "ايموجي_93.png", "answer": "😈"},
            {"image": "ايموجي_94.png", "answer": "👿"},
            {"image": "ايموجي_95.png", "answer": "👹"},
            {"image": "ايموجي_96.png", "answer": "👺"},
            {"image": "ايموجي_97.png", "answer": "🤡"},
            {"image": "ايموجي_98.png", "answer": "💩"},
            {"image": "ايموجي_99.png", "answer": "👻"},
            {"image": "ايموجي_100.png", "answer": "💀"},
            {"image": "ايموجي_101.png", "answer": "👋"},
            {"image": "ايموجي_102.png", "answer": "🤚"},
            {"image": "ايموجي_103.png", "answer": "🖐️"},
            {"image": "ايموجي_104.png", "answer": "✋"},
            {"image": "ايموجي_105.png", "answer": "🖖"},
            {"image": "ايموجي_106.png", "answer": "👌"},
            {"image": "ايموجي_107.png", "answer": "🤌"},
            {"image": "ايموجي_108.png", "answer": "🤏"},
            {"image": "ايموجي_109.png", "answer": "✌️"},
            {"image": "ايموجي_110.png", "answer": "🤞"},
            {"image": "ايموجي_111.png", "answer": "🤟"},
            {"image": "ايموجي_112.png", "answer": "🤘"},
            {"image": "ايموجي_113.png", "answer": "🤙"},
            {"image": "ايموجي_114.png", "answer": "👈"},
            {"image": "ايموجي_115.png", "answer": "👉"},
            {"image": "ايموجي_116.png", "answer": "👆"},
            {"image": "ايموجي_117.png", "answer": "🖕"},
            {"image": "ايموجي_118.png", "answer": "👇"},
            {"image": "ايموجي_119.png", "answer": "☝️"},
            {"image": "ايموجي_120.png", "answer": "👍"},
            {"image": "ايموجي_121.png", "answer": "👎"},
            {"image": "ايموجي_122.png", "answer": "✊"},
            {"image": "ايموجي_123.png", "answer": "👊"},
            {"image": "ايموجي_124.png", "answer": "🤛"},
            {"image": "ايموجي_125.png", "answer": "🤜"},
            {"image": "ايموجي_126.png", "answer": "👏"},
            {"image": "ايموجي_127.png", "answer": "🙌"},
            {"image": "ايموجي_128.png", "answer": "👐"},
            {"image": "ايموجي_129.png", "answer": "🤲"},
            {"image": "ايموجي_130.png", "answer": "🤝"},
            {"image": "ايموجي_131.png", "answer": "🙏"},
            {"image": "ايموجي_132.png", "answer": "✍️"},
            {"image": "ايموجي_133.png", "answer": "💅"},
            {"image": "ايموجي_134.png", "answer": "🤳"},
            {"image": "ايموجي_135.png", "answer": "💪"},
            {"image": "ايموجي_136.png", "answer": "🦵"},
            {"image": "ايموجي_137.png", "answer": "🦶"},
            {"image": "ايموجي_138.png", "answer": "👂"},
            {"image": "ايموجي_139.png", "answer": "🦻"},
            {"image": "ايموجي_140.png", "answer": "👃"},
            {"image": "ايموجي_141.png", "answer": "🧠"},
            {"image": "ايموجي_142.png", "answer": "🫀"},
            {"image": "ايموجي_143.png", "answer": "🫁"},
            {"image": "ايموجي_144.png", "answer": "🦷"},
            {"image": "ايموجي_145.png", "answer": "🦴"},
            {"image": "ايموجي_146.png", "answer": "👀"},
            {"image": "ايموجي_147.png", "answer": "👁️"},
            {"image": "ايموجي_148.png", "answer": "👅"},
            {"image": "ايموجي_149.png", "answer": "👄"},
            {"image": "ايموجي_150.png", "answer": "💋"},
            {"image": "ايموجي_151.png", "answer": "🩸"},
            {"image": "ايموجي_152.png", "answer": "👶"},
            {"image": "ايموجي_153.png", "answer": "👧"},
            {"image": "ايموجي_154.png", "answer": "🧒"},
            {"image": "ايموجي_155.png", "answer": "👦"},
            {"image": "ايموجي_156.png", "answer": "👩"},
            {"image": "ايموجي_157.png", "answer": "🧑"},
            {"image": "ايموجي_158.png", "answer": "👨"},
            {"image": "ايموجي_159.png", "answer": "👩‍🦱"},
            {"image": "ايموجي_160.png", "answer": "🧑‍🦱"},
            {"image": "ايموجي_161.png", "answer": "👨‍🦱"},
            {"image": "ايموجي_162.png", "answer": "👩‍🦰"},
            {"image": "ايموجي_163.png", "answer": "🧑‍🦰"},
            {"image": "ايموجي_164.png", "answer": "👨‍🦰"},
            {"image": "ايموجي_165.png", "answer": "👱‍♀️"},
            {"image": "ايموجي_166.png", "answer": "👱"},
            {"image": "ايموجي_167.png", "answer": "👱‍♂️"},
            {"image": "ايموجي_168.png", "answer": "👩‍🦳"},
            {"image": "ايموجي_169.png", "answer": "🧑‍🦳"},
            {"image": "ايموجي_170.png", "answer": "👨‍🦳"},
            {"image": "ايموجي_171.png", "answer": "👩‍🦲"},
            {"image": "ايموجي_172.png", "answer": "🧑‍🦲"},
            {"image": "ايموجي_173.png", "answer": "👨‍🦲"},
            {"image": "ايموجي_174.png", "answer": "🧔‍♀️"},
            {"image": "ايموجي_175.png", "answer": "🧔"},
            {"image": "ايموجي_176.png", "answer": "🧔‍♂️"},
            {"image": "ايموجي_177.png", "answer": "👵"},
            {"image": "ايموجي_178.png", "answer": "🧓"},
            {"image": "ايموجي_179.png", "answer": "👴"},
            {"image": "ايموجي_180.png", "answer": "👲"},
            {"image": "ايموجي_181.png", "answer": "👳‍♀️"},
            {"image": "ايموجي_182.png", "answer": "👳"},
            {"image": "ايموجي_183.png", "answer": "👳‍♂️"},
            {"image": "ايموجي_184.png", "answer": "🧕"},
            {"image": "ايموجي_185.png", "answer": "👮‍♀️"},
            {"image": "ايموجي_186.png", "answer": "👮"},
            {"image": "ايموجي_187.png", "answer": "👮‍♂️"},
            {"image": "ايموجي_188.png", "answer": "👷‍♀️"},
            {"image": "ايموجي_189.png", "answer": "👷"},
            {"image": "ايموجي_190.png", "answer": "👷‍♂️"},
            {"image": "ايموجي_191.png", "answer": "💂‍♀️"},
            {"image": "ايموجي_192.png", "answer": "💂"},
            {"image": "ايموجي_193.png", "answer": "💂‍♂️"},
            {"image": "ايموجي_194.png", "answer": "🕵️‍♀️"},
            {"image": "ايموجي_195.png", "answer": "🕵️"},
            {"image": "ايموجي_196.png", "answer": "🕵️‍♂️"},
            {"image": "ايموجي_197.png", "answer": "👩‍⚕️"},
            {"image": "ايموجي_198.png", "answer": "🧑‍⚕️"},
            {"image": "ايموجي_199.png", "answer": "👨‍⚕️"},
            {"image": "ايموجي_200.png", "answer": "👩‍🌾"},
            {"image": "ايموجي_201.png", "answer": "🐶"},
            {"image": "ايموجي_202.png", "answer": "🐱"},
            {"image": "ايموجي_203.png", "answer": "🐭"},
            {"image": "ايموجي_204.png", "answer": "🐹"},
            {"image": "ايموجي_205.png", "answer": "🐰"},
            {"image": "ايموجي_206.png", "answer": "🦊"},
            {"image": "ايموجي_207.png", "answer": "🐻"},
            {"image": "ايموجي_208.png", "answer": "🐼"},
            {"image": "ايموجي_209.png", "answer": "🐻‍❄️"},
            {"image": "ايموجي_210.png", "answer": "🐨"},
            {"image": "ايموجي_211.png", "answer": "🐯"},
            {"image": "ايموجي_212.png", "answer": "🦁"},
            {"image": "ايموجي_213.png", "answer": "🐮"},
            {"image": "ايموجي_214.png", "answer": "🐷"},
            {"image": "ايموجي_215.png", "answer": "🐽"},
            {"image": "ايموجي_216.png", "answer": "🐸"},
            {"image": "ايموجي_217.png", "answer": "🐵"},
            {"image": "ايموجي_218.png", "answer": "🙈"},
            {"image": "ايموجي_219.png", "answer": "🙉"},
            {"image": "ايموجي_220.png", "answer": "🙊"},
            {"image": "ايموجي_221.png", "answer": "🐒"},
            {"image": "ايموجي_222.png", "answer": "🐔"},
            {"image": "ايموجي_223.png", "answer": "🐧"},
            {"image": "ايموجي_224.png", "answer": "🐦"},
            {"image": "ايموجي_225.png", "answer": "🐤"},
            {"image": "ايموجي_226.png", "answer": "🐣"},
            {"image": "ايموجي_227.png", "answer": "🐥"},
            {"image": "ايموجي_228.png", "answer": "🦆"},
            {"image": "ايموجي_229.png", "answer": "🦅"},
            {"image": "ايموجي_230.png", "answer": "🦉"},
            {"image": "ايموجي_231.png", "answer": "🦇"},
            {"image": "ايموجي_232.png", "answer": "🐺"},
            {"image": "ايموجي_233.png", "answer": "🐗"},
            {"image": "ايموجي_234.png", "answer": "🐴"},
            {"image": "ايموجي_235.png", "answer": "🦄"},
            {"image": "ايموجي_236.png", "answer": "🐝"},
            {"image": "ايموجي_237.png", "answer": "🪱"},
            {"image": "ايموجي_238.png", "answer": "🐛"},
            {"image": "ايموجي_239.png", "answer": "🦋"},
            {"image": "ايموجي_240.png", "answer": "🐌"},
            {"image": "ايموجي_241.png", "answer": "🐞"},
            {"image": "ايموجي_242.png", "answer": "🐜"},
            {"image": "ايموجي_243.png", "answer": "🪰"},
            {"image": "ايموجي_244.png", "answer": "🪲"},
            {"image": "ايموجي_245.png", "answer": "🪳"},
            {"image": "ايموجي_246.png", "answer": "🦟"},
            {"image": "ايموجي_247.png", "answer": "🦗"},
            {"image": "ايموجي_248.png", "answer": "🕷️"},
            {"image": "ايموجي_249.png", "answer": "🕸️"},
            {"image": "ايموجي_250.png", "answer": "🦂"},
            {"image": "ايموجي_251.png", "answer": "🐢"},
            {"image": "ايموجي_252.png", "answer": "🐍"},
            {"image": "ايموجي_253.png", "answer": "🦎"},
            {"image": "ايموجي_254.png", "answer": "🦖"},
            {"image": "ايموجي_255.png", "answer": "🦕"},
            {"image": "ايموجي_256.png", "answer": "🐙"},
            {"image": "ايموجي_257.png", "answer": "🦑"},
            {"image": "ايموجي_258.png", "answer": "🦐"},
            {"image": "ايموجي_259.png", "answer": "🦞"},
            {"image": "ايموجي_260.png", "answer": "🦀"},
            {"image": "ايموجي_261.png", "answer": "🐡"},
            {"image": "ايموجي_262.png", "answer": "🐠"},
            {"image": "ايموجي_263.png", "answer": "🐟"},
            {"image": "ايموجي_264.png", "answer": "🐬"},
            {"image": "ايموجي_265.png", "answer": "🐳"},
            {"image": "ايموجي_266.png", "answer": "🐋"},
            {"image": "ايموجي_267.png", "answer": "🦈"},
            {"image": "ايموجي_268.png", "answer": "🦭"},
            {"image": "ايموجي_269.png", "answer": "🐊"},
            {"image": "ايموجي_270.png", "answer": "🐅"},
            {"image": "ايموجي_271.png", "answer": "🐆"},
            {"image": "ايموجي_272.png", "answer": "🦓"},
            {"image": "ايموجي_273.png", "answer": "🦍"},
            {"image": "ايموجي_274.png", "answer": "🦧"},
            {"image": "ايموجي_275.png", "answer": "🦣"},
            {"image": "ايموجي_276.png", "answer": "🐘"},
            {"image": "ايموجي_277.png", "answer": "🦛"},
            {"image": "ايموجي_278.png", "answer": "🦏"},
            {"image": "ايموجي_279.png", "answer": "🐪"},
            {"image": "ايموجي_280.png", "answer": "🐫"},
            {"image": "ايموجي_281.png", "answer": "🦒"},
            {"image": "ايموجي_282.png", "answer": "🦘"},
            {"image": "ايموجي_283.png", "answer": "🦬"},
            {"image": "ايموجي_284.png", "answer": "🐃"},
            {"image": "ايموجي_285.png", "answer": "🐂"},
            {"image": "ايموجي_286.png", "answer": "🐄"},
            {"image": "ايموجي_287.png", "answer": "🐎"},
            {"image": "ايموجي_288.png", "answer": "🐖"},
            {"image": "ايموجي_289.png", "answer": "🐏"},
            {"image": "ايموجي_290.png", "answer": "🐑"},
            {"image": "ايموجي_291.png", "answer": "🦙"},
            {"image": "ايموجي_292.png", "answer": "🐐"},
            {"image": "ايموجي_293.png", "answer": "🦌"},
            {"image": "ايموجي_294.png", "answer": "🐕"},
            {"image": "ايموجي_295.png", "answer": "🐩"},
            {"image": "ايموجي_296.png", "answer": "🦮"},
            {"image": "ايموجي_297.png", "answer": "🐕‍🦺"},
            {"image": "ايموجي_298.png", "answer": "🐈"},
            {"image": "ايموجي_299.png", "answer": "🐈‍⬛"},
            {"image": "ايموجي_300.png", "answer": "🐓"},
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

    @commands.command(name="-ايموجي")
    async def start_game_cmd(self, ctx):
        await self.run_game(ctx.channel)

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return
        if message.content.strip() == "-ايموجي":
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
    await bot.add_cog(qwergame(bot))