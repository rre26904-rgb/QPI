import discord
from discord.ext import commands
import random

# قائمة كلمات مقترحة
WORD_BANK = [
    "أسد", "نمر", "فهد", "ذئب", "ثعلب", "دب", "فيل", "زرافة", "قرد", "غزال",
    "خنزير", "ضبع", "أرنب", "قطة", "كلب", "فأر", "حصان", "حمار", "بقرة", "ثور",
    "خروف", "ماعز", "جمل", "تمساح", "ثعبان", "سلحفاة", "ضفدع", "سمكة", "قرش", "حوت",
    "دولفين", "أخطبوط", "سلطعون", "قنديل", "محار", "عصفور", "حمامة", "صقر", "نسر", "بومة",
    "غراب", "بطة", "أوزة", "دجاجة", "ديك", "نعامة", "طاووس", "ديناصور", "تنين", "نملة",
    "نحلة", "ذبابة", "بعوضة", "فراشة", "عنكبوت", "عقرب", "دودة", "حلزون", "خنفساء", "جرادة",
    "خفاش", "سنجاب", "قنفذ", "فقمة", "بطريق", "بجعة", "لقلق", "نورس", "كنغر", "كوالا",
    "باندا", "كسلان", "راكون", "غرير", "شبل", "مها", "ظبي", "أيل", "جاموس", "رنة",
    "شمبانزي", "غوريلا", "بابون", "حرباء", "سحلية", "برص", "إغوانا", "كوبرا", "أصلة", "يرقة",
    "شرنقة", "عجل", "جرو", "مهر", "هدهد", "بلبل", "كناري", "ببغاء", "حشرة", "طائر",
    "شمس", "قمر", "نجم", "كوكب", "سماء", "أرض", "بحر", "محيط", "نهر", "بحيرة",
    "جبل", "تل", "وادي", "صحراء", "غابة", "شجرة", "زهرة", "عشب", "ورقة", "جذر",
    "غيمة", "مطر", "ثلج", "جليد", "عاصفة", "رعد", "برق", "ضباب", "رياح", "هواء",
    "فضاء", "مجرة", "نيزك", "مذنب", "ثقب", "خسوف", "كسوف", "غبار", "رمال", "صخرة",
    "حصى", "تراب", "طين", "بركان", "زلزال", "فيضان", "إعصار", "نبع", "شلال", "جزيرة",
    "شاطئ", "ساحل", "خليج", "مضيق", "قارة", "قطب", "استواء", "مدار", "نور", "ظلام",
    "ظل", "شعاع", "طاقة", "جاذبية", "غلاف", "طقس", "مناخ", "ربيع", "صيف", "خريف",
    "شتاء", "نهار", "ليل", "فجر", "صباح", "مساء", "غسق", "سراب", "واحة", "كهف",
    "مغارة", "بئر", "خندق", "جرف", "منجم", "حقل", "بستان", "حديقة", "منتزه", "غصن",
    "جذع", "ثمرة", "بذرة", "شوكة", "رحيق", "طلع", "ندى", "شرارة", "لهب", "قطرة",
    "خبز", "لحم", "دجاج", "سمك", "بيض", "حليب", "جبن", "زبدة", "زيت", "عسل",
    "سكر", "ملح", "فلفل", "بهار", "أرز", "معكرونة", "قمح", "شعير", "ذرة", "شوفان",
    "تفاح", "برتقال", "موز", "عنب", "بطيخ", "شمام", "فراولة", "خوخ", "مشمش", "كرز",
    "تمر", "تين", "رمان", "مانجو", "ليمون", "بصل", "ثوم", "بطاطس", "طماطم", "خيار",
    "جزر", "خس", "ملفوف", "سبانخ", "بازلاء", "فاصوليا", "عدس", "حمص", "فول", "فستق",
    "لوز", "جوز", "بندق", "كاجو", "ماء", "شاي", "قهوة", "عصير", "مشروب", "حساء",
    "مرق", "سلطة", "شطيرة", "بيتزا", "كعكة", "فطيرة", "بسكويت", "شوكولاتة", "حلوى", "مثلجات",
    "طبق", "وعاء", "كأس", "فنجان", "ملعقة", "شوكة", "سكين", "قدر", "مقلاة", "فرن",
    "موقد", "ثلاجة", "مجمد", "خلاط", "إبريق", "زجاجة", "علبة", "جرة", "كيس", "وجبة",
    "فطور", "غداء", "عشاء", "وليمة", "مطعم", "مقهى", "مخبز", "بقالة", "وصفة", "طعام",
    "رأس", "شعر", "وجه", "جبهة", "عين", "حاجب", "رمش", "أذن", "أنف", "فم",
    "شفة", "سن", "لسان", "فك", "خد", "ذقن", "عنق", "كتف", "ذراع", "مرفق",
    "يد", "إصبع", "إبهام", "ظفر", "صدر", "بطن", "ظهر", "عمود", "حوض", "ساق",
    "ركبة", "كاحل", "قدم", "كعب", "جلد", "عظم", "عضلة", "دم", "قلب", "رئة",
    "معدة", "كبد", "كلية", "دماغ", "عصب", "وريد", "شريان", "خلية", "نسيج", "مرض",
    "صحة", "دواء", "حبة", "شراب", "حقنة", "لقاح", "طبيب", "ممرض", "مستشفى", "عيادة",
    "صيدلية", "عملية", "جراحة", "ضمادة", "جرح", "ألم", "حمى", "سعال", "زكام", "نظارة",
    "عدسة", "سماعة", "عكاز", "كرسي", "إسعاف", "طوارئ", "فحص", "تحليل", "نوم", "حلم",
    "يقظة", "راحة", "تعب", "إرهاق", "تنفس", "نبض", "حياة", "موت", "ولادة", "طفولة",
    "شباب", "شيخوخة", "عمر", "دموع", "عرق", "لعاب", "هيكل", "جمجمة", "جبيرة", "مرهم",
    "بيت", "منزل", "شقة", "قصر", "قلعة", "خيمة", "كوخ", "مبنى", "عمارة", "برج",
    "باب", "نافذة", "جدار", "سقف", "أرضية", "غرفة", "صالة", "مطبخ", "حمام", "شرفة",
    "سلم", "مصعد", "مفتاح", "قفل", "جرس", "أثاث", "سرير", "خزانة", "طاولة", "أريكة",
    "سجادة", "ستارة", "مصباح", "ثريا", "مرآة", "لوحة", "إطار", "مزهرية", "رف", "مروحة",
    "مكيف", "مدفأة", "غسالة", "مكواة", "مكنسة", "سلة", "قمامة", "صندوق", "درج", "مطرقة",
    "مسمار", "برغي", "مفك", "منشار", "فأس", "مجرفة", "كماشة", "مقص", "حبل", "سلك",
    "خيط", "إبرة", "قماش", "صمغ", "شريط", "لاصق", "دهان", "فرشاة", "أداة", "آلة",
    "محرك", "بطارية", "شاحن", "مقبس", "كهرباء", "أنبوب", "خرطوم", "دلو", "ممسحة", "إسفنجة",
    "صابون", "شامبو", "منشفة", "معجون", "مشط", "عطر", "بخور", "شمعة", "ولاعة", "كبريت",
    "حطب", "فحم", "رماد", "دخان", "نار", "وسادة", "غطاء", "بطانية", "وتد", "شراع",
    "مدينة", "قرية", "بلدة", "عاصمة", "دولة", "بلد", "عالم", "خريطة", "بوصلة", "شارع",
    "طريق", "زقاق", "ساحة", "ميدان", "جسر", "نفق", "تقاطع", "رصيف", "محطة", "مطار",
    "ميناء", "مرفأ", "قطار", "حافلة", "سيارة", "شاحنة", "دراجة", "دباب", "سفينة", "قارب",
    "طائرة", "مروحية", "صاروخ", "مكوك", "غواصة", "دبابة", "عربة", "مزرعة", "سوق", "دكان",
    "متجر", "مول", "مجمع", "بنك", "مصرف", "شركة", "مكتب", "مصنع", "ورشة", "مخزن",
    "مستودع", "مدرسة", "جامعة", "كلية", "معهد", "صف", "مكتبة", "متحف", "معرض", "مسرح",
    "سينما", "ملعب", "نادي", "رياضة", "مسجد", "كنيسة", "معبد", "ضريح", "قبر", "مقبرة",
    "سجن", "مخفر", "شرطة", "محكمة", "فندق", "منتجع", "مخيم", "حدود", "جمارك", "جواز",
    "تأشيرة", "تذكرة", "رحلة", "سياحة", "شمال", "جنوب", "شرق", "غرب", "يمين", "يسار",
    "أمام", "خلف", "فوق", "تحت", "وسط", "مركز", "زاوية", "ركن", "قمة", "قاع",
    "رجل", "امرأة", "طفل", "ولد", "بنت", "شاب", "فتاة", "عجوز", "رضيع", "أب",
    "أم", "أخ", "أخت", "جد", "جدة", "عم", "عمة", "خال", "خالة", "حفيد",
    "زوج", "زوجة", "عريس", "عروس", "صديق", "عدو", "جار", "زميل", "رئيس", "مدير",
    "موظف", "عامل", "خادم", "حارس", "سائق", "طيار", "قبطان", "جراح", "صيدلي", "مهندس",
    "معماري", "مبرمج", "محاسب", "محامي", "قاضي", "شرطي", "جندي", "ضابط", "جيش", "بحار",
    "إطفائي", "مسعف", "معلم", "أستاذ", "طالب", "تلميذ", "باحث", "عالم", "مخترع", "كاتب",
    "شاعر", "صحفي", "مذيع", "فنان", "رسام", "نحات", "ممثل", "مخرج", "مغني", "عازف",
    "خباز", "جزار", "حلاق", "خياط", "نجار", "حداد", "سباك", "كهربائي", "فلاح", "مزارع",
    "صياد", "راعي", "تاجر", "بائع", "ملك", "أمير", "سلطان", "وزير", "سفير", "عمدة",
    "زعيم", "قائد", "بطل", "لص", "قرصان", "جاسوس", "ساحر", "مهرج", "مجرم", "ضحية",
    "قميص", "بنطال", "ثوب", "فستان", "تنورة", "سترة", "معطف", "عباءة", "وشاح", "قبعة",
    "حذاء", "جورب", "قفاز", "حزام", "ربطة", "قلادة", "خاتم", "سوار", "عقد", "قرط",
    "مجوهرات", "ماس", "زمرد", "ياقوت", "لؤلؤ", "مرجان", "ذهب", "فضة", "نحاس", "حديد",
    "صلب", "ألومنيوم", "رصاص", "خشب", "بلاستيك", "زجاج", "ورق", "كرتون", "جلد", "صوف",
    "قطن", "حرير", "كتان", "مطاط", "إسفنج", "فلين", "سيف", "رمح", "قوس", "سهم",
    "درع", "خوذة", "بندقية", "مسدس", "رصاصة", "قنبلة", "مدفع", "لغم", "فخ", "خنجر",
    "سوط", "عصا", "حجر", "مقلاع", "تاج", "عرش", "صولجان", "وسام", "بلورة", "ميدالية",
    "علم", "راية", "لافتة", "حقيبة", "شنطة", "محفظة", "جيب", "سحاب", "زر", "ياقة",
    "كم", "مظلة", "تسوق", "طرد", "رسالة", "طابع", "ختم", "وثيقة", "شيك", "فاتورة",
    "إيصال", "جريدة", "مجلة", "كتاب", "دفتر", "قلم", "ممحاة", "مسطرة", "حبر", "ريشة",
    "كمبيوتر", "حاسوب", "شاشة", "لوحة", "مفاتيح", "فأرة", "طابعة", "هاتف", "جوال", "تلفاز",
    "مذياع", "راديو", "كاميرا", "ميكروفون", "شبكة", "إنترنت", "موقع", "تطبيق", "بريد", "ملف",
    "صورة", "فيديو", "صوت", "موسيقى", "أغنية", "لحن", "إيقاع", "طبل", "مزمار", "عود",
    "جيتار", "بيانو", "كمان", "مسرحية", "فيلم", "قصة", "رواية", "مقال", "قصيدة", "حرف",
    "كلمة", "جملة", "لغة", "رقم", "عدد", "حساب", "هندسة", "فيزياء", "كيمياء", "أحياء",
    "تاريخ", "جغرافيا", "قانون", "سياسة", "اقتصاد", "تجارة", "بيع", "شراء", "مال", "نقود",
    "عملة", "دينار", "ريال", "دولار", "بورصة", "قرض", "ديون", "ربح", "خسارة", "سعر",
    "ثمن", "لون", "أبيض", "أسود", "أحمر", "أزرق", "أصفر", "أخضر", "برتقالي", "بني",
    "رمادي", "وردي", "بنفسجي", "دائرة", "مربع", "مثلث", "مستطيل", "خط", "نقطة", "شكل",
    "حجم", "وزن", "طول", "عرض", "ارتفاع", "مسافة", "كتلة", "كثافة", "سرعة", "ضغط",
    "وقت", "زمن", "ثانية", "دقيقة", "ساعة", "يوم", "أسبوع", "شهر", "سنة", "عام",
    "عقد", "قرن", "ماضي", "حاضر", "مستقبل", "بداية", "نهاية", "أول", "آخر", "حب",
    "كره", "غضب", "فرح", "حزن", "خوف", "شجاعة", "جبن", "أمل", "يأس", "نجاح",
    "فشل", "ذكاء", "غباء", "ضعف", "بطء", "جمال", "قبح", "خير", "شر", "حق",
    "باطل", "عدل", "ظلم", "حرية", "سلام", "حرب", "حقيقة", "كذب", "سر", "علن",
    "سؤال", "جواب", "فكرة", "رأي", "قرار", "شك", "يقين", "أمنية", "هدف", "خطة",
    "مشروع", "عمل", "وظيفة", "مهمة", "لعبة", "لغز", "مسابقة", "تحدي", "فوز", "جائزة",
    "هدية", "مفاجأة", "صدفة", "روح", "نفس", "عقل", "ضمير", "شخصية", "اسم", "لقب",
    "توقيع", "بصمة", "عائلة", "قبيلة", "شعب", "أمة", "مجتمع", "ثقافة", "حضارة", "تراث",
    "دين", "عقيدة", "إيمان", "دعاء", "صلاة", "صوم", "حج", "زكاة", "صدقة", "ذنب"
]

class LeaderBoardButton(discord.ui.Button):
    def __init__(self, word, color, row):
        # تلوين الأزرار للقائد حسب اللون الحقيقي
        if color == "red":
            style = discord.ButtonStyle.danger
            label_text = word
        elif color == "blue":
            style = discord.ButtonStyle.primary
            label_text = word
        elif color == "black":
            style = discord.ButtonStyle.secondary
            label_text = f"💀 {word}"
        else: # الكلمات المحايدة (لا تتبع لأي فريق)
            style = discord.ButtonStyle.success
            label_text = word

        super().__init__(style=style, label=label_text, row=row, disabled=True)

class LeaderBoardView(discord.ui.View):
    def __init__(self, words_dict):
        super().__init__(timeout=None)
        row = 0
        count = 0
        for word, color in words_dict.items():
            self.add_item(LeaderBoardButton(word, color, row))
            count += 1
            if count % 5 == 0:
                row += 1

class HintModal(discord.ui.Modal, title="تقديم تلميح"):
    word = discord.ui.TextInput(
        label="كلمة التلميح",
        placeholder="اكتب كلمة واحدة فقط ترتبط بكلمات فريقك...",
        required=True
    )
    count = discord.ui.TextInput(
        label="عدد الكلمات",
        placeholder="أدخل رقماً (مثال: 2)",
        required=True,
        max_length=1
    )

    def __init__(self, game):
        super().__init__()
        self.game = game

    async def on_submit(self, interaction: discord.Interaction):
        if not self.count.value.isdigit():
            await interaction.response.send_message("❌ الرجاء إدخال رقم صحيح لعدد الكلمات.", ephemeral=True)
            return
        
        self.game.hint_word = self.word.value
        self.game.remaining_guesses = int(self.count.value)
        self.game.hint_given = True

        await interaction.response.send_message("✅ تم إرسال التلميح بنجاح!", ephemeral=True)
        await self.game.update_status_message()

class ControlView(discord.ui.View):
    def __init__(self, game):
        super().__init__(timeout=None)
        self.game = game

    @discord.ui.button(label="💡 تقديم تلميح", style=discord.ButtonStyle.success, custom_id="btn_hint")
    async def hint_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        is_red_turn = self.game.current_turn == "red"
        active_leader = self.game.red_leader if is_red_turn else self.game.blue_leader
        
        if interaction.user != active_leader:
            await interaction.response.send_message("❌ هذا الزر مخصص لقائد الفريق الذي عليه الدور فقط!", ephemeral=True)
            return
        
        if self.game.hint_given:
            await interaction.response.send_message("❌ لقد قمت بتقديم تلميح بالفعل، انتظر حتى ينهي فريقك اختياراته.", ephemeral=True)
            return

        await interaction.response.send_modal(HintModal(self.game))

    @discord.ui.button(label="🗺️ عرض خريطة القائد", style=discord.ButtonStyle.secondary, custom_id="btn_show_map")
    async def show_map_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        # التحقق من أن المستخدم هو أحد القادة (أحمر أو أزرق)
        if interaction.user not in [self.game.red_leader, self.game.blue_leader]:
            await interaction.response.send_message("❌ هذا الزر مخصص للقادة فقط!", ephemeral=True)
            return
        
        # إرسال الخريطة كرسالة مخفية (ephemeral)
        await interaction.response.send_message(
            "🗺️ **هذه خريطة الكلمات الخاصة بك (لا تشاركها مع أحد):**\n🔴 أحمر | 🔵 أزرق | 🟢 محايد | 💀 أسود (خسارة فورية)", 
            view=LeaderBoardView(self.game.words_dict), 
            ephemeral=True
        )

class BoardButton(discord.ui.Button):
    def __init__(self, word, color, row, game):
        super().__init__(style=discord.ButtonStyle.secondary, label=word, row=row)
        self.word = word
        self.real_color = color
        self.game = game

    async def callback(self, interaction: discord.Interaction):
        if self.game.is_processing:
            await interaction.response.send_message("⏳ يتم الآن معالجة ضغطة أخرى...", ephemeral=True)
            return

        if interaction.user in [self.game.red_leader, self.game.blue_leader]:
            await interaction.response.send_message("❌ القادة لا يمكنهم اختيار الكلمات! الأعضاء فقط من يضغطون الأزرار.", ephemeral=True)
            return

        is_red_turn = self.game.current_turn == "red"
        active_members = self.game.red_members if is_red_turn else self.game.blue_members
        
        if interaction.user not in active_members:
            await interaction.response.send_message("❌ ليس دور فريقك أو أنك لست عضواً في هذا الفريق!", ephemeral=True)
            return

        if not self.game.hint_given:
            await interaction.response.send_message("❌ القائد لم يعطِ تلميحاً بعد!", ephemeral=True)
            return
        
        if self.game.remaining_guesses <= 0:
            await interaction.response.send_message("❌ لقد استنفدتم عدد المحاولات المتاحة لهذا التلميح!", ephemeral=True)
            return

        self.game.is_processing = True
        
        try:
            self.disabled = True
            self.game.remaining_guesses -= 1

            if self.real_color == "red":
                self.style = discord.ButtonStyle.danger
                self.game.red_score += 1
            elif self.real_color == "blue":
                self.style = discord.ButtonStyle.primary
                self.game.blue_score += 1
            elif self.real_color == "black":
                self.style = discord.ButtonStyle.secondary
                self.label = f"💀 {self.word}"
            else:
                self.style = discord.ButtonStyle.success 
                self.label = f"⬜ {self.word}"

            await interaction.response.edit_message(view=self.view)

            # حالة الخسارة الفورية
            if self.real_color == "black":
                loser = "🔴 الأحمر" if is_red_turn else "🔵 الأزرق"
                winner = "🔵 الأزرق" if is_red_turn else "🔴 الأحمر"
                await self.game.end_game(f"💀 **كارثة!** قام فريق {loser} باختيار الكلمة السوداء!\n🏆 **الفريق الفائز هو {winner}!**")
                return

            # حالة الفوز (الوصول لـ 10 نقاط)
            if self.game.red_score == 10:
                await self.game.end_game("🏆 **فاز الفريق الأحمر 🔴 بجميع كلماته (10/10)!**")
                return
            elif self.game.blue_score == 10:
                await self.game.end_game("🏆 **فاز الفريق الأزرق 🔵 بجميع كلماته (10/10)!**")
                return

            # تغيير الدور إذا ضغط لون خاطئ أو انتهت المحاولات
            if (is_red_turn and self.real_color != "red") or (not is_red_turn and self.real_color != "blue") or (self.game.remaining_guesses <= 0):
                await self.game.switch_turn()
            else:
                # تحديث العداد فقط في الرسالة الأساسية
                await self.game.update_status_message()
        
        finally:
            self.game.is_processing = False

class BoardView(discord.ui.View):
    def __init__(self, game):
        super().__init__(timeout=None)
        self.game = game
        row = 0
        count = 0
        for word, color in self.game.words_dict.items():
            self.add_item(BoardButton(word, color, row, game))
            count += 1
            if count % 5 == 0:
                row += 1

class GameSession:
    def __init__(self, channel, red_leader, blue_leader, red_members, blue_members):
        self.channel = channel
        self.red_leader = red_leader
        self.blue_leader = blue_leader
        self.red_members = red_members
        self.blue_members = blue_members
        
        self.red_score = 0
        self.blue_score = 0
        self.current_turn = random.choice(["red", "blue"])
        
        self.hint_word = None
        self.remaining_guesses = 0
        self.hint_given = False
        self.is_processing = False 
        
        self.status_msg = None
        self.board_msg = None
        self.control_msg = None
        self.words_dict = self.generate_board()

    def generate_board(self):
        chosen_words = random.sample(WORD_BANK, 25)
        # 10 حمراء، 10 زرقاء، 1 سوداء، 4 محايدة
        colors = ['red']*10 + ['blue']*10 + ['black']*1 + ['neutral']*4
        random.shuffle(colors)
        return dict(zip(chosen_words, colors))

    def get_status_text(self):
        turn_str = "🔴 الفريق الأحمر" if self.current_turn == "red" else "🔵 الفريق الأزرق"
        text = f"🎮 **الدور الحالي:** {turn_str}\n"
        text += f"📊 **النقاط:** 🔴 الأحمر: {self.red_score}/10 | 🔵 الأزرق: {self.blue_score}/10\n"
        text += "──────────────\n"
        
        if self.hint_given:
            text += f"💡 **تلميح القائد:** ( **{self.hint_word}** ) | **المحاولات المتبقية:** {self.remaining_guesses}\n"
            text += "👈 **يمكن لأعضاء الفريق الآن الضغط على الأزرار.**"
        else:
            text += "⏳ **بانتظار القائد لتقديم تلميح...**"
            
        return text

    async def start(self):
        # لم يعد هناك إرسال للخاص، كل شيء يتم عبر الأزرار في السيرفر
        self.status_msg = await self.channel.send(self.get_status_text())
        self.board_msg = await self.channel.send(view=BoardView(self))
        self.control_msg = await self.channel.send("⚙️ **لوحة تحكم القادة**", view=ControlView(self))

    async def switch_turn(self):
        self.current_turn = "blue" if self.current_turn == "red" else "red"
        self.hint_given = False
        self.hint_word = None
        self.remaining_guesses = 0
        await self.update_status_message()

    async def update_status_message(self):
        if self.status_msg:
            await self.status_msg.edit(content=self.get_status_text())

    async def end_game(self, final_message):
        if self.status_msg:
            await self.status_msg.edit(content=final_message)
        if self.control_msg:
            await self.control_msg.delete()

class SetupView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=30.0) 
        self.red_leader = None
        self.blue_leader = None
        self.red_members = set()
        self.blue_members = set()
        self.message = None 

    async def on_timeout(self):
        for item in self.children:
            item.disabled = True
        if self.message:
            await self.message.edit(content="⏳ **انتهى وقت الانضمام (30 ثانية) وتم إلغاء اللعبة لعدم اكتمال العدد.**", view=self)

    @discord.ui.button(label="قائد أحمر 🔴", style=discord.ButtonStyle.danger)
    async def btn_red_leader(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.red_leader = interaction.user
        if interaction.user in self.red_members: self.red_members.remove(interaction.user)
        button.disabled = True # التعديل هنا: قفل الزر
        await interaction.message.edit(view=self) # التعديل هنا: تحديث واجهة الأزرار
        await interaction.response.send_message("✅ أصبحت قائد الفريق الأحمر!", ephemeral=True)

    @discord.ui.button(label="عضو أحمر 🔴", style=discord.ButtonStyle.secondary)
    async def btn_red_member(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.red_members.add(interaction.user)
        if self.red_leader == interaction.user: self.red_leader = None
        await interaction.response.send_message("✅ انضممت كعضو للفريق الأحمر!", ephemeral=True)

    @discord.ui.button(label="قائد أزرق 🔵", style=discord.ButtonStyle.primary)
    async def btn_blue_leader(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.blue_leader = interaction.user
        if interaction.user in self.blue_members: self.blue_members.remove(interaction.user)
        button.disabled = True # التعديل هنا: قفل الزر
        await interaction.message.edit(view=self) # التعديل هنا: تحديث واجهة الأزرار
        await interaction.response.send_message("✅ أصبحت قائد الفريق الأزرق!", ephemeral=True)

    @discord.ui.button(label="عضو أزرق 🔵", style=discord.ButtonStyle.secondary)
    async def btn_blue_member(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.blue_members.add(interaction.user)
        if self.blue_leader == interaction.user: self.blue_leader = None
        await interaction.response.send_message("✅ انضممت كعضو للفريق الأزرق!", ephemeral=True)

    @discord.ui.button(label="بدء اللعبة ▶️", style=discord.ButtonStyle.success, row=1)
    async def btn_start(self, interaction: discord.Interaction, button: discord.ui.Button):
        if not self.red_leader or not self.blue_leader:
            await interaction.response.send_message("❌ يجب أن يكون هناك قائد لكل فريق لبدء اللعبة!", ephemeral=True)
            return
        if not self.red_members or not self.blue_members:
            await interaction.response.send_message("❌ يجب أن يكون هناك عضو واحد على الأقل في كل فريق!", ephemeral=True)
            return

        await interaction.response.send_message("✅ جاري تجهيز اللعبة...", ephemeral=True)
        self.stop() 
        
        game = GameSession(
            interaction.channel, 
            self.red_leader, 
            self.blue_leader, 
            list(self.red_members), 
            list(self.blue_members)
        )
        await game.start()

class CodenamesCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="كودنيمز", aliases=["كودنيم"])
    async def start_setup(self, ctx):
        embed = discord.Embed(
            title="🎯 لعبة Codenames", 
            description="اضغط على الأزرار بالأسفل للانضمام إلى الفرق.\n⏳ **لديك 30 ثانية لتجميع اللاعبين وبدء اللعبة.**",
            color=discord.Color.dark_theme()
        )
        view = SetupView()
        view.message = await ctx.send(embed=embed, view=view)

async def setup(bot):
    await bot.add_cog(CodenamesCog(bot))