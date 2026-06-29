import discord
from discord.ext import commands
import random
import asyncio
import json
import os


class asrrgame(commands.Cog):
    def __init__(self, bot):    
        self.bot = bot
        self.scores_file = "global_points.json" # 🟢 اسم ملف النقاط الموحد والمشترك
        
        # 🟢 التأكد من وجود القفل العام المشترك داخل كائن البوت
        if not hasattr(self.bot, 'global_game_lock'):
            self.bot.global_game_lock = set()

        self.questions = [
            {"image": "اسرع_1.png", "answer": "شمس"},
            {"image": "اسرع_2.png", "answer": "قمر"},
            {"image": "اسرع_3.png", "answer": "بحر"},
            {"image": "اسرع_4.png", "answer": "سماء"},
            {"image": "اسرع_5.png", "answer": "أرض"},
            {"image": "اسرع_6.png", "answer": "جبل"},
            {"image": "اسرع_7.png", "answer": "نهر"},
            {"image": "اسرع_8.png", "answer": "شجرة"},
            {"image": "اسرع_9.png", "answer": "زهرة"},
            {"image": "اسرع_10.png", "answer": "وردة"},
            {"image": "اسرع_11.png", "answer": "حصان"},
            {"image": "اسرع_12.png", "answer": "كلب"},
            {"image": "اسرع_13.png", "answer": "قطة"},
            {"image": "اسرع_14.png", "answer": "أسد"},
            {"image": "اسرع_15.png", "answer": "نمر"},
            {"image": "اسرع_16.png", "answer": "فيل"},
            {"image": "اسرع_17.png", "answer": "زرافة"},
            {"image": "اسرع_18.png", "answer": "قرد"},
            {"image": "اسرع_19.png", "answer": "ثعلب"},
            {"image": "اسرع_20.png", "answer": "ذئب"},
            {"image": "اسرع_21.png", "answer": "صقر"},
            {"image": "اسرع_22.png", "answer": "نسر"},
            {"image": "اسرع_23.png", "answer": "عصفور"},
            {"image": "اسرع_24.png", "answer": "حمامة"},
            {"image": "اسرع_25.png", "answer": "غراب"},
            {"image": "اسرع_26.png", "answer": "طائرة"},
            {"image": "اسرع_27.png", "answer": "سيارة"},
            {"image": "اسرع_28.png", "answer": "قطار"},
            {"image": "اسرع_29.png", "answer": "سفينة"},
            {"image": "اسرع_30.png", "answer": "دراجة"},
            {"image": "اسرع_31.png", "answer": "تفاحة"},
            {"image": "اسرع_32.png", "answer": "برتقالة"},
            {"image": "اسرع_33.png", "answer": "موزة"},
            {"image": "اسرع_34.png", "answer": "عنب"},
            {"image": "اسرع_35.png", "answer": "بطيخ"},
            {"image": "اسرع_36.png", "answer": "فراولة"},
            {"image": "اسرع_37.png", "answer": "ليمون"},
            {"image": "اسرع_38.png", "answer": "خيار"},
            {"image": "اسرع_39.png", "answer": "طماطم"},
            {"image": "اسرع_40.png", "answer": "جزر"},
            {"image": "اسرع_41.png", "answer": "بطاطس"},
            {"image": "اسرع_42.png", "answer": "بصل"},
            {"image": "اسرع_43.png", "answer": "ثوم"},
            {"image": "اسرع_44.png", "answer": "خبز"},
            {"image": "اسرع_45.png", "answer": "جبن"},
            {"image": "اسرع_46.png", "answer": "حليب"},
            {"image": "اسرع_47.png", "answer": "بيض"},
            {"image": "اسرع_48.png", "answer": "سكر"},
            {"image": "اسرع_49.png", "answer": "ملح"},
            {"image": "اسرع_50.png", "answer": "ماء"},
            {"image": "اسرع_51.png", "answer": "عصير"},
            {"image": "اسرع_52.png", "answer": "قهوة"},
            {"image": "اسرع_53.png", "answer": "شاي"},
            {"image": "اسرع_54.png", "answer": "كتاب"},
            {"image": "اسرع_55.png", "answer": "قلم"},
            {"image": "اسرع_56.png", "answer": "دفتر"},
            {"image": "اسرع_57.png", "answer": "ممحاة"},
            {"image": "اسرع_58.png", "answer": "مسطرة"},
            {"image": "اسرع_59.png", "answer": "حقيبة"},
            {"image": "اسرع_60.png", "answer": "طاولة"},
            {"image": "اسرع_61.png", "answer": "كرسي"},
            {"image": "اسرع_62.png", "answer": "باب"},
            {"image": "اسرع_63.png", "answer": "نافذة"},
            {"image": "اسرع_64.png", "answer": "سرير"},
            {"image": "اسرع_65.png", "answer": "خزانة"},
            {"image": "اسرع_66.png", "answer": "وسادة"},
            {"image": "اسرع_67.png", "answer": "سجاد"},
            {"image": "اسرع_68.png", "answer": "هاتف"},
            {"image": "اسرع_69.png", "answer": "حاسوب"},
            {"image": "اسرع_70.png", "answer": "شاشة"},
            {"image": "اسرع_71.png", "answer": "لوحة"},
            {"image": "اسرع_72.png", "answer": "فأرة"},
            {"image": "اسرع_73.png", "answer": "نظارة"},
            {"image": "اسرع_74.png", "answer": "ساعة"},
            {"image": "اسرع_75.png", "answer": "خاتم"},
            {"image": "اسرع_76.png", "answer": "سوار"},
            {"image": "اسرع_77.png", "answer": "قلادة"},
            {"image": "اسرع_78.png", "answer": "حذاء"},
            {"image": "اسرع_79.png", "answer": "قميص"},
            {"image": "اسرع_80.png", "answer": "بنطال"},
            {"image": "اسرع_81.png", "answer": "فستان"},
            {"image": "اسرع_82.png", "answer": "قبعة"},
            {"image": "اسرع_83.png", "answer": "معطف"},
            {"image": "اسرع_84.png", "answer": "مطر"},
            {"image": "اسرع_85.png", "answer": "ثلج"},
            {"image": "اسرع_86.png", "answer": "غيم"},
            {"image": "اسرع_87.png", "answer": "ريح"},
            {"image": "اسرع_88.png", "answer": "عاصفة"},
            {"image": "اسرع_89.png", "answer": "حر"},
            {"image": "اسرع_90.png", "answer": "برد"},
            {"image": "اسرع_91.png", "answer": "شتاء"},
            {"image": "اسرع_92.png", "answer": "صيف"},
            {"image": "اسرع_93.png", "answer": "خريف"},
            {"image": "اسرع_94.png", "answer": "ربيع"},
            {"image": "اسرع_95.png", "answer": "ليل"},
            {"image": "اسرع_96.png", "answer": "نهار"},
            {"image": "اسرع_97.png", "answer": "فجر"},
            {"image": "اسرع_98.png", "answer": "صبح"},
            {"image": "اسرع_99.png", "answer": "ظهر"},
            {"image": "اسرع_100.png", "answer": "عصر"},
            {"image": "اسرع_101.png", "answer": "مغرب"},
            {"image": "اسرع_102.png", "answer": "عشاء"},
            {"image": "اسرع_103.png", "answer": "ذهب"},
            {"image": "اسرع_104.png", "answer": "أكل"},
            {"image": "اسرع_105.png", "answer": "شرب"},
            {"image": "اسرع_106.png", "answer": "نام"},
            {"image": "اسرع_107.png", "answer": "قام"},
            {"image": "اسرع_108.png", "answer": "جلس"},
            {"image": "اسرع_109.png", "answer": "قرأ"},
            {"image": "اسرع_110.png", "answer": "كتب"},
            {"image": "اسرع_111.png", "answer": "لعب"},
            {"image": "اسرع_112.png", "answer": "ركض"},
            {"image": "اسرع_113.png", "answer": "مشى"},
            {"image": "اسرع_114.png", "answer": "ضحك"},
            {"image": "اسرع_115.png", "answer": "بكى"},
            {"image": "اسرع_116.png", "answer": "ابتسم"},
            {"image": "اسرع_117.png", "answer": "غضب"},
            {"image": "اسرع_118.png", "answer": "فرح"},
            {"image": "اسرع_119.png", "answer": "حزن"},
            {"image": "اسرع_120.png", "answer": "نجح"},
            {"image": "اسرع_121.png", "answer": "فشل"},
            {"image": "اسرع_122.png", "answer": "سافر"},
            {"image": "اسرع_123.png", "answer": "عاد"},
            {"image": "اسرع_124.png", "answer": "فتح"},
            {"image": "اسرع_125.png", "answer": "أغلق"},
            {"image": "اسرع_126.png", "answer": "رفع"},
            {"image": "اسرع_127.png", "answer": "خفض"},
            {"image": "اسرع_128.png", "answer": "بدأ"},
            {"image": "اسرع_129.png", "answer": "انتهى"},
            {"image": "اسرع_130.png", "answer": "طويل"},
            {"image": "اسرع_131.png", "answer": "قصير"},
            {"image": "اسرع_132.png", "answer": "كبير"},
            {"image": "اسرع_133.png", "answer": "صغير"},
            {"image": "اسرع_134.png", "answer": "جميل"},
            {"image": "اسرع_135.png", "answer": "قبيح"},
            {"image": "اسرع_136.png", "answer": "سريع"},
            {"image": "اسرع_137.png", "answer": "بطيء"},
            {"image": "اسرع_138.png", "answer": "قوي"},
            {"image": "اسرع_139.png", "answer": "ضعيف"},
            {"image": "اسرع_140.png", "answer": "غني"},
            {"image": "اسرع_141.png", "answer": "فقير"},
            {"image": "اسرع_142.png", "answer": "ذكي"},
            {"image": "اسرع_143.png", "answer": "غبي"},
            {"image": "اسرع_144.png", "answer": "جديد"},
            {"image": "اسرع_145.png", "answer": "قديم"},
            {"image": "اسرع_146.png", "answer": "نظيف"},
            {"image": "اسرع_147.png", "answer": "متسخ"},
            {"image": "اسرع_148.png", "answer": "حار"},
            {"image": "اسرع_149.png", "answer": "بارد"},
            {"image": "اسرع_150.png", "answer": "حلو"},
            {"image": "اسرع_151.png", "answer": "مر"},
            {"image": "اسرع_152.png", "answer": "مالح"},
            {"image": "اسرع_153.png", "answer": "حامض"},
            {"image": "اسرع_154.png", "answer": "مستشفى"},
            {"image": "اسرع_155.png", "answer": "مدرسة"},
            {"image": "اسرع_156.png", "answer": "جامعة"},
            {"image": "اسرع_157.png", "answer": "مسجد"},
            {"image": "اسرع_158.png", "answer": "مطعم"},
            {"image": "اسرع_159.png", "answer": "فندق"},
            {"image": "اسرع_160.png", "answer": "حديقة"},
            {"image": "اسرع_161.png", "answer": "شارع"},
            {"image": "اسرع_162.png", "answer": "طريق"},
            {"image": "اسرع_163.png", "answer": "مدينة"},
            {"image": "اسرع_164.png", "answer": "قرية"},
            {"image": "اسرع_165.png", "answer": "دولة"},
            {"image": "اسرع_166.png", "answer": "قارة"},
            {"image": "اسرع_167.png", "answer": "عالم"},
            {"image": "اسرع_168.png", "answer": "كوكب"},
            {"image": "اسرع_169.png", "answer": "نجم"},
            {"image": "اسرع_170.png", "answer": "فضاء"},
            {"image": "اسرع_171.png", "answer": "صاروخ"},
            {"image": "اسرع_172.png", "answer": "سلاح"},
            {"image": "اسرع_173.png", "answer": "سيف"},
            {"image": "اسرع_174.png", "answer": "درع"},
            {"image": "اسرع_175.png", "answer": "رمح"},
            {"image": "اسرع_176.png", "answer": "قوس"},
            {"image": "اسرع_177.png", "answer": "سهم"},
            {"image": "اسرع_178.png", "answer": "بطل"},
            {"image": "اسرع_179.png", "answer": "ملك"},
            {"image": "اسرع_180.png", "answer": "أمير"},
            {"image": "اسرع_181.png", "answer": "وزير"},
            {"image": "اسرع_182.png", "answer": "قائد"},
            {"image": "اسرع_183.png", "answer": "جيش"},
            {"image": "اسرع_184.png", "answer": "جندي"},
            {"image": "اسرع_185.png", "answer": "شرطي"},
            {"image": "اسرع_186.png", "answer": "طبيب"},
            {"image": "اسرع_187.png", "answer": "مهندس"},
            {"image": "اسرع_188.png", "answer": "معلم"},
            {"image": "اسرع_189.png", "answer": "طالب"},
            {"image": "اسرع_190.png", "answer": "عامل"},
            {"image": "اسرع_191.png", "answer": "تاجر"},
            {"image": "اسرع_192.png", "answer": "فلاح"},
            {"image": "اسرع_193.png", "answer": "خباز"},
            {"image": "اسرع_194.png", "answer": "حداد"},
            {"image": "اسرع_195.png", "answer": "نجار"},
            {"image": "اسرع_196.png", "answer": "خياط"},
            {"image": "اسرع_197.png", "answer": "حلاق"},
            {"image": "اسرع_198.png", "answer": "طباخ"},
            {"image": "اسرع_199.png", "answer": "طيار"},
            {"image": "اسرع_200.png", "answer": "سائق"},
            {"image": "اسرع_201.png", "answer": "حب"},
            {"image": "اسرع_202.png", "answer": "سلام"},
            {"image": "اسرع_203.png", "answer": "عدل"},
            {"image": "اسرع_204.png", "answer": "ظلم"},
            {"image": "اسرع_205.png", "answer": "حق"},
            {"image": "اسرع_206.png", "answer": "باطل"},
            {"image": "اسرع_207.png", "answer": "خير"},
            {"image": "اسرع_208.png", "answer": "شر"},
            {"image": "اسرع_209.png", "answer": "صدق"},
            {"image": "اسرع_210.png", "answer": "كذب"},
            {"image": "اسرع_211.png", "answer": "أمانة"},
            {"image": "اسرع_212.png", "answer": "خيانة"},
            {"image": "اسرع_213.png", "answer": "علم"},
            {"image": "اسرع_214.png", "answer": "جهل"},
            {"image": "اسرع_215.png", "answer": "نور"},
            {"image": "اسرع_216.png", "answer": "ظلام"},
            {"image": "اسرع_217.png", "answer": "حياة"},
            {"image": "اسرع_218.png", "answer": "موت"},
            {"image": "اسرع_219.png", "answer": "أمل"},
            {"image": "اسرع_220.png", "answer": "يأس"},
            {"image": "اسرع_221.png", "answer": "شجاعة"},
            {"image": "اسرع_222.png", "answer": "خوف"},
            {"image": "اسرع_223.png", "answer": "كرم"},
            {"image": "اسرع_224.png", "answer": "بخل"},
            {"image": "اسرع_225.png", "answer": "صبر"},
            {"image": "اسرع_226.png", "answer": "عقل"},
            {"image": "اسرع_227.png", "answer": "قلب"},
            {"image": "اسرع_228.png", "answer": "روح"},
            {"image": "اسرع_229.png", "answer": "جسد"},
            {"image": "اسرع_230.png", "answer": "رأس"},
            {"image": "اسرع_231.png", "answer": "شعر"},
            {"image": "اسرع_232.png", "answer": "وجه"},
            {"image": "اسرع_233.png", "answer": "عين"},
            {"image": "اسرع_234.png", "answer": "أذن"},
            {"image": "اسرع_235.png", "answer": "أنف"},
            {"image": "اسرع_236.png", "answer": "فم"},
            {"image": "اسرع_237.png", "answer": "لسان"},
            {"image": "اسرع_238.png", "answer": "سن"},
            {"image": "اسرع_239.png", "answer": "يد"},
            {"image": "اسرع_240.png", "answer": "رجل"},
            {"image": "اسرع_241.png", "answer": "إصبع"},
            {"image": "اسرع_242.png", "answer": "ظفر"},
            {"image": "اسرع_243.png", "answer": "ذراع"},
            {"image": "اسرع_244.png", "answer": "ساق"},
            {"image": "اسرع_245.png", "answer": "بطن"},
            {"image": "اسرع_246.png", "answer": "ظهر"},
            {"image": "اسرع_247.png", "answer": "صدر"},
            {"image": "اسرع_248.png", "answer": "رقبة"},
            {"image": "اسرع_249.png", "answer": "دم"},
            {"image": "اسرع_250.png", "answer": "لحم"},
            {"image": "اسرع_251.png", "answer": "عظم"},
            {"image": "اسرع_252.png", "answer": "جلد"},
            {"image": "اسرع_253.png", "answer": "ثوب"},
            {"image": "اسرع_254.png", "answer": "عباءة"},
            {"image": "اسرع_255.png", "answer": "شماغ"},
            {"image": "اسرع_256.png", "answer": "عقال"},
            {"image": "اسرع_257.png", "answer": "بشت"},
            {"image": "اسرع_258.png", "answer": "عمامة"},
            {"image": "اسرع_259.png", "answer": "خيمة"},
            {"image": "اسرع_260.png", "answer": "قصر"},
            {"image": "اسرع_261.png", "answer": "كوخ"},
            {"image": "اسرع_262.png", "answer": "مبنى"},
            {"image": "اسرع_263.png", "answer": "برج"},
            {"image": "اسرع_264.png", "answer": "جسر"},
            {"image": "اسرع_265.png", "answer": "نفق"},
            {"image": "اسرع_266.png", "answer": "جدار"},
            {"image": "اسرع_267.png", "answer": "سقف"},
            {"image": "اسرع_268.png", "answer": "أرضية"},
            {"image": "اسرع_269.png", "answer": "بلاط"},
            {"image": "اسرع_270.png", "answer": "رخام"},
            {"image": "اسرع_271.png", "answer": "خشب"},
            {"image": "اسرع_272.png", "answer": "حديد"},
            {"image": "اسرع_273.png", "answer": "نحاس"},
            {"image": "اسرع_274.png", "answer": "ذهب"},
            {"image": "اسرع_275.png", "answer": "فضة"},
            {"image": "اسرع_276.png", "answer": "ألماس"},
            {"image": "اسرع_277.png", "answer": "زمرد"},
            {"image": "اسرع_278.png", "answer": "ياقوت"},
            {"image": "اسرع_279.png", "answer": "لؤلؤ"},
            {"image": "اسرع_280.png", "answer": "مرجان"},
            {"image": "اسرع_281.png", "answer": "زجاج"},
            {"image": "اسرع_282.png", "answer": "ورق"},
            {"image": "اسرع_283.png", "answer": "كرتون"},
            {"image": "اسرع_284.png", "answer": "بلاستيك"},
            {"image": "اسرع_285.png", "answer": "قماش"},
            {"image": "اسرع_286.png", "answer": "حرير"},
            {"image": "اسرع_287.png", "answer": "قطن"},
            {"image": "اسرع_288.png", "answer": "صوف"},
            {"image": "اسرع_289.png", "answer": "مطاط"},
            {"image": "اسرع_290.png", "answer": "حبل"},
            {"image": "اسرع_291.png", "answer": "خيط"},
            {"image": "اسرع_292.png", "answer": "إبرة"},
            {"image": "اسرع_293.png", "answer": "مقص"},
            {"image": "اسرع_294.png", "answer": "سكين"},
            {"image": "اسرع_295.png", "answer": "ملعقة"},
            {"image": "اسرع_296.png", "answer": "شوكة"},
            {"image": "اسرع_297.png", "answer": "طبق"},
            {"image": "اسرع_298.png", "answer": "كأس"},
            {"image": "اسرع_299.png", "answer": "فنجان"},
            {"image": "اسرع_300.png", "answer": "قدر"}
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

    @commands.command(name="-اسرع")
    async def start_game_cmd(self, ctx):
        await self.run_game(ctx.channel)

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return
        if message.content.strip() == "-اسرع":
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
    await bot.add_cog(asrrgame(bot))