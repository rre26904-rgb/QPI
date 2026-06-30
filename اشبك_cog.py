import discord
from discord.ext import commands
import random
import asyncio
import json
import os


class ashbkgame(commands.Cog):
    def __init__(self, bot):    
        self.bot = bot
        self.scores_file = "global_points.json" # 🟢 اسم ملف النقاط الموحد والمشترك
        
        # 🟢 التأكد من وجود القفل العام المشترك داخل كائن البوت
        if not hasattr(self.bot, 'global_game_lock'):
            self.bot.global_game_lock = set()

        self.questions = [
            {"image": "اشبك_1.png", "answer": "أسد"},
            {"image": "اشبك_2.png", "answer": "نمر"},
            {"image": "اشبك_3.png", "answer": "فهد"},
            {"image": "اشبك_4.png", "answer": "قطة"},
            {"image": "اشبك_5.png", "answer": "كلب"},
            {"image": "اشبك_6.png", "answer": "ذئب"},
            {"image": "اشبك_7.png", "answer": "ثعلب"},
            {"image": "اشبك_8.png", "answer": "غزال"},
            {"image": "اشبك_9.png", "answer": "فيل"},
            {"image": "اشبك_10.png", "answer": "زرافة"},
            {"image": "اشبك_11.png", "answer": "قرد"},
            {"image": "اشبك_12.png", "answer": "حصان"},
            {"image": "اشبك_13.png", "answer": "بقرة"},
            {"image": "اشبك_14.png", "answer": "خروف"},
            {"image": "اشبك_15.png", "answer": "ماعز"},
            {"image": "اشبك_16.png", "answer": "جمل"},
            {"image": "اشبك_17.png", "answer": "دجاجة"},
            {"image": "اشبك_18.png", "answer": "ديك"},
            {"image": "اشبك_19.png", "answer": "حمامة"},
            {"image": "اشبك_20.png", "answer": "عصفور"},
            {"image": "اشبك_21.png", "answer": "صقر"},
            {"image": "اشبك_22.png", "answer": "نسر"},
            {"image": "اشبك_23.png", "answer": "غراب"},
            {"image": "اشبك_24.png", "answer": "بومة"},
            {"image": "اشبك_25.png", "answer": "ببغاء"},
            {"image": "اشبك_26.png", "answer": "طاووس"},
            {"image": "اشبك_27.png", "answer": "نعامة"},
            {"image": "اشبك_28.png", "answer": "سمكة"},
            {"image": "اشبك_29.png", "answer": "قرش"},
            {"image": "اشبك_30.png", "answer": "حوت"},
            {"image": "اشبك_31.png", "answer": "دولفين"},
            {"image": "اشبك_32.png", "answer": "أخطبوط"},
            {"image": "اشبك_33.png", "answer": "سلحفاة"},
            {"image": "اشبك_34.png", "answer": "تمساح"},
            {"image": "اشبك_35.png", "answer": "ثعبان"},
            {"image": "اشبك_36.png", "answer": "حية"},
            {"image": "اشبك_37.png", "answer": "عقرب"},
            {"image": "اشبك_38.png", "answer": "عنكبوت"},
            {"image": "اشبك_39.png", "answer": "نحلة"},
            {"image": "اشبك_40.png", "answer": "فراشة"},
            {"image": "اشبك_41.png", "answer": "نملة"},
            {"image": "اشبك_42.png", "answer": "ذبابة"},
            {"image": "اشبك_43.png", "answer": "بعوضة"},
            {"image": "اشبك_44.png", "answer": "جرادة"},
            {"image": "اشبك_45.png", "answer": "شجرة"},
            {"image": "اشبك_46.png", "answer": "زهرة"},
            {"image": "اشبك_47.png", "answer": "وردة"},
            {"image": "اشبك_48.png", "answer": "نبات"},
            {"image": "اشبك_49.png", "answer": "عشب"},
            {"image": "اشبك_50.png", "answer": "ثمرة"},
            {"image": "اشبك_51.png", "answer": "جذر"},
            {"image": "اشبك_52.png", "answer": "جذع"},
            {"image": "اشبك_53.png", "answer": "غصن"},
            {"image": "اشبك_54.png", "answer": "ورقة"},
            {"image": "اشبك_55.png", "answer": "تفاح"},
            {"image": "اشبك_56.png", "answer": "برتقال"},
            {"image": "اشبك_57.png", "answer": "موز"},
            {"image": "اشبك_58.png", "answer": "عنب"},
            {"image": "اشبك_59.png", "answer": "تين"},
            {"image": "اشبك_60.png", "answer": "خوخ"},
            {"image": "اشبك_61.png", "answer": "مشمش"},
            {"image": "اشبك_62.png", "answer": "بطيخ"},
            {"image": "اشبك_63.png", "answer": "فراولة"},
            {"image": "اشبك_64.png", "answer": "توت"},
            {"image": "اشبك_65.png", "answer": "كرز"},
            {"image": "اشبك_66.png", "answer": "مانجو"},
            {"image": "اشبك_67.png", "answer": "أناناس"},
            {"image": "اشبك_68.png", "answer": "رمان"},
            {"image": "اشبك_69.png", "answer": "كيوي"},
            {"image": "اشبك_70.png", "answer": "بصل"},
            {"image": "اشبك_71.png", "answer": "ثوم"},
            {"image": "اشبك_72.png", "answer": "جزر"},
            {"image": "اشبك_73.png", "answer": "خيار"},
            {"image": "اشبك_74.png", "answer": "طماطم"},
            {"image": "اشبك_75.png", "answer": "بطاطس"},
            {"image": "اشبك_76.png", "answer": "خس"},
            {"image": "اشبك_77.png", "answer": "بقدونس"},
            {"image": "اشبك_78.png", "answer": "نعناع"},
            {"image": "اشبك_79.png", "answer": "فلفل"},
            {"image": "اشبك_80.png", "answer": "ذرة"},
            {"image": "اشبك_81.png", "answer": "باذنجان"},
            {"image": "اشبك_82.png", "answer": "كوسا"},
            {"image": "اشبك_83.png", "answer": "ملفوف"},
            {"image": "اشبك_84.png", "answer": "سبانخ"},
            {"image": "اشبك_85.png", "answer": "سماء"},
            {"image": "اشبك_86.png", "answer": "أرض"},
            {"image": "اشبك_87.png", "answer": "ماء"},
            {"image": "اشبك_88.png", "answer": "نار"},
            {"image": "اشبك_89.png", "answer": "هواء"},
            {"image": "اشبك_90.png", "answer": "بحر"},
            {"image": "اشبك_91.png", "answer": "نهر"},
            {"image": "اشبك_92.png", "answer": "جبل"},
            {"image": "اشبك_93.png", "answer": "تل"},
            {"image": "اشبك_94.png", "answer": "وادي"},
            {"image": "اشبك_95.png", "answer": "صحراء"},
            {"image": "اشبك_96.png", "answer": "غابة"},
            {"image": "اشبك_97.png", "answer": "جزيرة"},
            {"image": "اشبك_98.png", "answer": "سحاب"},
            {"image": "اشبك_99.png", "answer": "مطر"},
            {"image": "اشبك_100.png", "answer": "ثلج"},
            {"image": "اشبك_101.png", "answer": "بيت"},
            {"image": "اشبك_102.png", "answer": "منزل"},
            {"image": "اشبك_103.png", "answer": "غرفة"},
            {"image": "اشبك_104.png", "answer": "صالة"},
            {"image": "اشبك_105.png", "answer": "مطبخ"},
            {"image": "اشبك_106.png", "answer": "حمام"},
            {"image": "اشبك_107.png", "answer": "سرير"},
            {"image": "اشبك_108.png", "answer": "دولاب"},
            {"image": "اشبك_109.png", "answer": "مائدة"},
            {"image": "اشبك_110.png", "answer": "كرسي"},
            {"image": "اشبك_111.png", "answer": "مكتب"},
            {"image": "اشبك_112.png", "answer": "سجادة"},
            {"image": "اشبك_113.png", "answer": "لوحة"},
            {"image": "اشبك_114.png", "answer": "مصباح"},
            {"image": "اشبك_115.png", "answer": "شباك"},
            {"image": "اشبك_116.png", "answer": "باب"},
            {"image": "اشبك_117.png", "answer": "سقف"},
            {"image": "اشبك_118.png", "answer": "جدار"},
            {"image": "اشبك_119.png", "answer": "بلاط"},
            {"image": "اشبك_120.png", "answer": "ستارة"},
            {"image": "اشبك_121.png", "answer": "قميص"},
            {"image": "اشبك_122.png", "answer": "بنطلون"},
            {"image": "اشبك_123.png", "answer": "فستان"},
            {"image": "اشبك_124.png", "answer": "تنورة"},
            {"image": "اشبك_125.png", "answer": "حذاء"},
            {"image": "اشبك_126.png", "answer": "جورب"},
            {"image": "اشبك_127.png", "answer": "قبعة"},
            {"image": "اشبك_128.png", "answer": "وشاح"},
            {"image": "اشبك_129.png", "answer": "معطف"},
            {"image": "اشبك_130.png", "answer": "حزام"},
            {"image": "اشبك_131.png", "answer": "خاتم"},
            {"image": "اشبك_132.png", "answer": "عقد"},
            {"image": "اشبك_133.png", "answer": "ساعة"},
            {"image": "اشبك_134.png", "answer": "نظارة"},
            {"image": "اشبك_135.png", "answer": "حقيبة"},
            {"image": "اشبك_136.png", "answer": "طبيب"},
            {"image": "اشبك_137.png", "answer": "مهندس"},
            {"image": "اشبك_138.png", "answer": "معلم"},
            {"image": "اشبك_139.png", "answer": "طيار"},
            {"image": "اشبك_140.png", "answer": "نجار"},
            {"image": "اشبك_141.png", "answer": "حداد"},
            {"image": "اشبك_142.png", "answer": "خباز"},
            {"image": "اشبك_143.png", "answer": "صياد"},
            {"image": "اشبك_144.png", "answer": "جزار"},
            {"image": "اشبك_145.png", "answer": "خياط"},
            {"image": "اشبك_146.png", "answer": "محامي"},
            {"image": "اشبك_147.png", "answer": "قاضي"},
            {"image": "اشبك_148.png", "answer": "ضابط"},
            {"image": "اشبك_149.png", "answer": "جندي"},
            {"image": "اشبك_150.png", "answer": "شرطي"},
            {"image": "اشبك_151.png", "answer": "سيارة"},
            {"image": "اشبك_152.png", "answer": "قطار"},
            {"image": "اشبك_153.png", "answer": "طائرة"},
            {"image": "اشبك_154.png", "answer": "سفينة"},
            {"image": "اشبك_155.png", "answer": "قارب"},
            {"image": "اشبك_156.png", "answer": "حافلة"},
            {"image": "اشبك_157.png", "answer": "دراجة"},
            {"image": "اشبك_158.png", "answer": "صاروخ"},
            {"image": "اشبك_159.png", "answer": "دبابة"},
            {"image": "اشبك_160.png", "answer": "غواصة"},
            {"image": "اشبك_161.png", "answer": "شاحنة"},
            {"image": "اشبك_162.png", "answer": "مصنع"},
            {"image": "اشبك_163.png", "answer": "شركة"},
            {"image": "اشبك_164.png", "answer": "مكتبة"},
            {"image": "اشبك_165.png", "answer": "مدرسة"},
            {"image": "اشبك_166.png", "answer": "جامعة"},
            {"image": "اشبك_167.png", "answer": "مستشفى"},
            {"image": "اشبك_168.png", "answer": "عيادة"},
            {"image": "اشبك_169.png", "answer": "صيدلية"},
            {"image": "اشبك_170.png", "answer": "مخبز"},
            {"image": "اشبك_171.png", "answer": "بقالة"},
            {"image": "اشبك_172.png", "answer": "سوق"},
            {"image": "اشبك_173.png", "answer": "متجر"},
            {"image": "اشبك_174.png", "answer": "ملعب"},
            {"image": "اشبك_175.png", "answer": "حديقة"},
            {"image": "اشبك_176.png", "answer": "متحف"},
            {"image": "اشبك_177.png", "answer": "سينما"},
            {"image": "اشبك_178.png", "answer": "مسرح"},
            {"image": "اشبك_179.png", "answer": "فندق"},
            {"image": "اشبك_180.png", "answer": "مطعم"},
            {"image": "اشبك_181.png", "answer": "خبز"},
            {"image": "اشبك_182.png", "answer": "جبن"},
            {"image": "اشبك_183.png", "answer": "لحم"},
            {"image": "اشبك_184.png", "answer": "بيض"},
            {"image": "اشبك_185.png", "answer": "عسل"},
            {"image": "اشبك_186.png", "answer": "مربى"},
            {"image": "اشبك_187.png", "answer": "حليب"},
            {"image": "اشبك_188.png", "answer": "قهوة"},
            {"image": "اشبك_189.png", "answer": "شاي"},
            {"image": "اشبك_190.png", "answer": "عصير"},
            {"image": "اشبك_191.png", "answer": "سكر"},
            {"image": "اشبك_192.png", "answer": "ملح"},
            {"image": "اشبك_193.png", "answer": "فيزياء,"},
            {"image": "اشبك_194.png", "answer": "كيمياء"},
            {"image": "اشبك_195.png", "answer": "أحياء"},
            {"image": "اشبك_196.png", "answer": "هندسة"},
            {"image": "اشبك_197.png", "answer": "جغرافيا"},
            {"image": "اشبك_198.png", "answer": "تاريخ"},
            {"image": "اشبك_199.png", "answer": "حاسوب"},
            {"image": "اشبك_200.png", "answer": "شبكة"},
            {"image": "اشبك_201.png", "answer": "رأس"},
            {"image": "اشبك_202.png", "answer": "شعر"},
            {"image": "اشبك_203.png", "answer": "وجه"},
            {"image": "اشبك_204.png", "answer": "عين"},
            {"image": "اشبك_205.png", "answer": "حاجب"},
            {"image": "اشبك_206.png", "answer": "أنف"},
            {"image": "اشبك_207.png", "answer": "فم"},
            {"image": "اشبك_208.png", "answer": "شفة"},
            {"image": "اشبك_209.png", "answer": "أسنان"},
            {"image": "اشبك_210.png", "answer": "لسان"},
            {"image": "اشبك_211.png", "answer": "أذن"},
            {"image": "اشبك_212.png", "answer": "خد"},
            {"image": "اشبك_213.png", "answer": "رقبة"},
            {"image": "اشبك_214.png", "answer": "كتف"},
            {"image": "اشبك_215.png", "answer": "ذراع"},
            {"image": "اشبك_216.png", "answer": "يد"},
            {"image": "اشبك_217.png", "answer": "إصبع"},
            {"image": "اشبك_218.png", "answer": "ظفر"},
            {"image": "اشبك_219.png", "answer": "صدر"},
            {"image": "اشبك_220.png", "answer": "بطن"},
            {"image": "اشبك_221.png", "answer": "ظهر"},
            {"image": "اشبك_222.png", "answer": "قدم"},
            {"image": "اشبك_223.png", "answer": "كعب"},
            {"image": "اشبك_224.png", "answer": "ركبة"},
            {"image": "اشبك_225.png", "answer": "كبد"},
            {"image": "اشبك_226.png", "answer": "قلب"},
            {"image": "اشبك_227.png", "answer": "رئة"},
            {"image": "اشبك_228.png", "answer": "كلية"},
            {"image": "اشبك_229.png", "answer": "معدة"},
            {"image": "اشبك_230.png", "answer": "دم"},
            {"image": "اشبك_231.png", "answer": "أحمر"},
            {"image": "اشبك_232.png", "answer": "أصفر"},
            {"image": "اشبك_233.png", "answer": "أزرق"},
            {"image": "اشبك_234.png", "answer": "أخضر"},
            {"image": "اشبك_235.png", "answer": "بنفسجي"},
            {"image": "اشبك_236.png", "answer": "أسود"},
            {"image": "اشبك_237.png", "answer": "أبيض"},
            {"image": "اشبك_238.png", "answer": "رمادي"},
            {"image": "اشبك_239.png", "answer": "بني"},
            {"image": "اشبك_240.png", "answer": "وردي"},
            {"image": "اشبك_241.png", "answer": "قمر"},
            {"image": "اشبك_242.png", "answer": "شمس"},
            {"image": "اشبك_243.png", "answer": "نجم"},
            {"image": "اشبك_244.png", "answer": "كوكب"},
            {"image": "اشبك_245.png", "answer": "نيزك"},
            {"image": "اشبك_246.png", "answer": "مجرة"},
            {"image": "اشبك_247.png", "answer": "فضاء"},
            {"image": "اشبك_248.png", "answer": "كون"},
            {"image": "اشبك_249.png", "answer": "ربيع"},
            {"image": "اشبك_250.png", "answer": "صيف"},
            {"image": "اشبك_251.png", "answer": "خريف"},
            {"image": "اشبك_252.png", "answer": "شتاء"},
            {"image": "اشبك_253.png", "answer": "صباح"},
            {"image": "اشبك_254.png", "answer": "مساء"},
            {"image": "اشبك_255.png", "answer": "ليل"},
            {"image": "اشبك_256.png", "answer": "نهار"},
            {"image": "اشبك_257.png", "answer": "سنة"},
            {"image": "اشبك_258.png", "answer": "شهر"},
            {"image": "اشبك_259.png", "answer": "أسبوع"},
            {"image": "اشبك_260.png", "answer": "يوم"},
            {"image": "اشبك_261.png", "answer": "دقيقة"},
            {"image": "اشبك_262.png", "answer": "ثانية"},
            {"image": "اشبك_263.png", "answer": "حب"},
            {"image": "اشبك_264.png", "answer": "كره"},
            {"image": "اشبك_265.png", "answer": "فرح"},
            {"image": "اشبك_266.png", "answer": "حزن"},
            {"image": "اشبك_267.png", "answer": "خوف"},
            {"image": "اشبك_268.png", "answer": "أمن"},
            {"image": "اشبك_269.png", "answer": "صدق"},
            {"image": "اشبك_270.png", "answer": "كذب"},
            {"image": "اشبك_271.png", "answer": "كرم"},
            {"image": "اشبك_272.png", "answer": "بخل"},
            {"image": "اشبك_273.png", "answer": "شجاعة"},
            {"image": "اشبك_274.png", "answer": "جبن"},
            {"image": "اشبك_275.png", "answer": "صبر"},
            {"image": "اشبك_276.png", "answer": "غضب"},
            {"image": "اشبك_277.png", "answer": "رحمة"},
            {"image": "اشبك_278.png", "answer": "قسوة"},
            {"image": "اشبك_279.png", "answer": "نجاح"},
            {"image": "اشبك_280.png", "answer": "فشل"},
            {"image": "اشبك_281.png", "answer": "أمل"},
            {"image": "اشبك_282.png", "answer": "يأس"},
            {"image": "اشبك_283.png", "answer": "رياضة"},
            {"image": "اشبك_284.png", "answer": "كرة"},
            {"image": "اشبك_285.png", "answer": "سباحة"},
            {"image": "اشبك_286.png", "answer": "ركض"},
            {"image": "اشبك_287.png", "answer": "قفز"},
            {"image": "اشبك_288.png", "answer": "رماية"},
            {"image": "اشبك_289.png", "answer": "هدف"},
            {"image": "اشبك_290.png", "answer": "نقطة"},
            {"image": "اشبك_291.png", "answer": "جائزة"},
            {"image": "اشبك_292.png", "answer": "كأس"},
            {"image": "اشبك_293.png", "answer": "ميدالية"},
            {"image": "اشبك_294.png", "answer": "قاموس"},
            {"image": "اشبك_295.png", "answer": "قلم"},
            {"image": "اشبك_296.png", "answer": "كتاب"},
            {"image": "اشبك_297.png", "answer": "دفتر"},
            {"image": "اشبك_298.png", "answer": "ممحاة"},
            {"image": "اشبك_299.png", "answer": "مسطرة"},
            {"image": "اشبك_300.png", "answer": "طبشورة"}
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

    @commands.command(name="-اشبك")
    async def start_game_cmd(self, ctx):
        await self.run_game(ctx.channel)

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return
        if message.content.strip() == "-اشبك":
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
    await bot.add_cog(ashbkgame(bot))