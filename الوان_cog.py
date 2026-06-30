import discord
from discord.ext import commands
import random
import json
import os

# قاموس يحتوي على 100 لون مع درجات الـ RGB الدقيقة الخاصة بها
COLORS_DICT = {
    # أحمر ومشتقاته
    "أحمر": (255, 0, 0), "قرمزي": (220, 20, 60), "عنابي": (128, 0, 0), "كرزي": (222, 49, 99),
    "ياقوتي": (224, 17, 95), "طماطمي": (255, 99, 71), "ماروني": (128, 0, 0), "نبيذي": (114, 47, 55),
    "أحمر فاتح": (255, 102, 102), "أحمر داكن": (139, 0, 0), "أحمر دموي": (102, 0, 0), "أحمر ناري": (226, 88, 34),
    
    # أزرق ومشتقاته
    "أزرق": (0, 0, 255), "سماوي": (135, 206, 235), "كحلي": (0, 0, 128), "فيروزي": (64, 224, 208),
    "نيلي": (75, 0, 130), "لازوردي": (0, 127, 255), "كوبالت": (0, 71, 171), "أزرق بحري": (0, 105, 148),
    "أزرق فاتح": (173, 216, 230), "أزرق داكن": (0, 0, 139), "تيفاني": (10, 186, 181), "أزرق ثلجي": (175, 238, 238),
    "سيان": (0, 255, 255), "أكوامارين": (127, 255, 212), "كحلي غامق": (28, 40, 65),
    
    # أخضر ومشتقاته
    "أخضر": (0, 128, 0), "زيتوني": (128, 128, 0), "زمردي": (80, 200, 120), "ليموني": (0, 255, 0),
    "فستقي": (147, 197, 114), "عشبي": (124, 252, 0), "نعناعي": (152, 255, 152), "تفاحي": (141, 182, 0),
    "جيشي": (75, 83, 32), "أخضر فاتح": (144, 238, 144), "أخضر داكن": (0, 100, 0), "أخضر مزرق": (0, 128, 128),
    "أخضر ربيعي": (0, 255, 127), "أخضر فسفوري": (57, 255, 20),
    
    # أصفر ومشتقاته
    "أصفر": (255, 255, 0), "ذهبي": (255, 215, 0), "خردلي": (255, 219, 88), "كناري": (255, 255, 153),
    "زعفراني": (244, 196, 48), "شمسي": (253, 184, 19), "أصفر فاتح": (255, 255, 224), "كريمي": (255, 253, 208),
    "موزي": (255, 225, 53), "أصفر فاقع": (255, 234, 0),
    
    # برتقالي وبني
    "برتقالي": (255, 165, 0), "خوخي": (255, 204, 153), "مشمشي": (251, 206, 177), "برونزي": (205, 127, 50),
    "نحاسي": (184, 115, 51), "بني": (165, 42, 42), "شوكولاته": (210, 105, 30), "بندقي": (201, 160, 220),
    "طوبي": (178, 34, 34), "كراميل": (255, 221, 175), "كاكي": (195, 176, 145), "بيج": (245, 245, 220),
    "بني فاتح": (210, 180, 140), "بني داكن": (101, 67, 33), "رملي": (194, 178, 128), "عنبري": (255, 191, 0),
    "برتقالي محروق": (204, 85, 0), "قهوة": (111, 78, 55), "كستنائي": (149, 69, 53),
    
    # بنفسجي ووردي
    "بنفسجي": (128, 0, 128), "وردي": (255, 192, 203), "فوشي": (255, 0, 255), "أرجواني": (160, 32, 240),
    "ليلكي": (200, 162, 200), "باذنجاني": (97, 64, 81), "زهري": (255, 105, 180), "توتي": (135, 38, 87),
    "لافندر": (230, 230, 250), "وردي فاتح": (255, 182, 193), "وردي داكن": (255, 20, 147), "بنفسجي فاتح": (216, 191, 216),
    "بنفسجي داكن": (148, 0, 211), "ماجنتا": (255, 0, 255), "بطيخي": (252, 108, 133), "وردي باستيل": (255, 209, 220),
    
    # أبيض، أسود، رمادي
    "أسود": (0, 0, 0), "أبيض": (255, 255, 255), "رمادي": (128, 128, 128), "فضي": (192, 192, 192),
    "رصاصي": (112, 128, 144), "فحمي": (54, 69, 79), "لؤلؤي": (234, 230, 202), "عاجي": (255, 255, 240),
    "رمادي فاتح": (211, 211, 211), "رمادي داكن": (169, 169, 169), "أسود مطفي": (40, 40, 43), "أبيض ثلجي": (255, 250, 250),
    "دخاني": (115, 130, 118), "بلاتيني": (229, 228, 226)
}

class ColorGameView(discord.ui.View):
    def __init__(self, correct_name, options, cog, channel_id):
        super().__init__(timeout=30.0) 
        self.correct_name = correct_name
        self.cog = cog
        self.channel_id = channel_id
        self.message_obj = None # سيتم إسناده فور إرسال الرسالة للتحكم بها عند انتهاء الوقت
        self.winner = None
        
        # إنشاء 4 أزرار بناءً على الخيارات
        for option in options:
            btn = discord.ui.Button(
                label=option,
                style=discord.ButtonStyle.primary,
                custom_id=f"color_{option}" 
            )
            btn.callback = self.check_answer
            self.add_item(btn)

    async def check_answer(self, interaction: discord.Interaction):
        if self.winner:
            return

        clicked_color = interaction.data["custom_id"].replace("color_", "")
        
        if clicked_color == self.correct_name:
            self.winner = interaction.user
            
            # فتح القفل العام في البوت فور الإجابة الصحيحة للسماح بألعاب أخرى
            self.cog.bot.global_game_lock.discard(self.channel_id)
            
            # تعطيل جميع الأزرار وتلوين الصحيح
            for child in self.children:
                child.disabled = True
                if child.label == self.correct_name:
                    child.style = discord.ButtonStyle.success
                else:
                    child.style = discord.ButtonStyle.secondary
            
            # تحديث رسالة الأزرار الأصلية
            await interaction.message.edit(view=self)
            
            # إضافة وحفظ النقاط في ملف الجيسون الموحد
            new_score = self.cog.add_score(interaction.user.id)
            
            # --- تعديل رسالة الفوز والأزرار لتطابق الشكل المطلوب ---
            
            win_embed = discord.Embed(
                title="",
                description=f" {interaction.user.mention} فاز في اللعبة!",
                color=discord.Color.green()
            )
            
            points_view = discord.ui.View()
            
            # زر النقاط (شفاف/رمادي مع نجمة)
            score_button = discord.ui.Button(
                label=f" 𐙚        {new_score}",
                style=discord.ButtonStyle.secondary,
                disabled=True
            )
            
            # الزر السحري (للدعم)
            magic_button = discord.ui.Button(
                label="⋆. 𐙚 ˚",
                style=discord.ButtonStyle.secondary  
            )
            
            # الدالة اللي تتنفذ لما ينضغط الزر السحري
            async def magic_callback(btn_interaction: discord.Interaction):
                await btn_interaction.response.send_message(
                    "👋 أهلاً بك! هذا سيرفر الدعم الفني الخاص بنا. حياك الله:\nhttps://discord.gg/zkJpxjk2rN", 
                    ephemeral=True # هذي تخلي الرسالة تطلع للي ضغط الزر بس
                )
            
            # ربط الدالة بالزر
            magic_button.callback = magic_callback
            
            # إضافة الأزرار
            points_view.add_item(score_button)
            points_view.add_item(magic_button)
            
            # إرسال رسالة الفوز
            await interaction.response.send_message(embed=win_embed, view=points_view)
            self.stop()
            
        else:
            await interaction.response.send_message("خطأ! مو هذا اللون ❌، ركز وحاول أسرع.", ephemeral=True)

    # دالة تعمل تلقائياً في حال انتهى وقت الأزرار (30 ثانية) دون إجابة صحيحة
    async def on_timeout(self):
        # فتح القفل العام في البوت
        self.cog.bot.global_game_lock.discard(self.channel_id)
        
        # تعطيل الأزرار
        for child in self.children:
            child.disabled = True
            
        if self.message_obj:
            try:
                timeout_embed = discord.Embed(
                    title="⌛ انتهى الوقت!",
                    description=f"محد قدر يكتشف اللون الصحيح في الوقت المحدد.\nاللون الصحيح كان: **{self.correct_name}** 🎨",
                    color=discord.Color.red()
                )
                await self.message_obj.edit(embed=timeout_embed, view=self)
            except:
                pass

class ColorGameCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.scores_file = "global_points.json" # اسم ملف النقاط الموحد
        
        # التأكد من ربط القفل العام المشترك داخل كائن البوت
        if not hasattr(self.bot, 'global_game_lock'):
            self.bot.global_game_lock = set()

    # دالة قراءة النقاط وتحديثها في الملف الموحد مباشرة
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

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author.bot:
            return
            
        if message.content.strip() == "-الوان":
            # 🟢 الفحص باستخدام القفل العام المشترك لمنع التداخل
            if message.channel.id in self.bot.global_game_lock:
                await message.channel.send("⚠️ هناك لعبة جارية بالفعل في هذا الروم! انتظر حتى تنتهي.")
                return
                
            # قفل الروم في البوت كاملاً لمنع أي لعبة أخرى من البدء
            self.bot.global_game_lock.add(message.channel.id)
            
            all_colors = list(COLORS_DICT.keys())
            
            # سحب 4 ألوان عشوائية
            options = random.sample(all_colors, 4)
            correct_name = random.choice(options)
            
            # استخراج قيم RGB للون الصحيح
            r, g, b = COLORS_DICT[correct_name]
            
            # تحويل الـ RGB إلى صيغة HEX عشان نولد منها صورة للون
            hex_color = f"{r:02x}{g:02x}{b:02x}"
            image_url = f"https://singlecolorimage.com/get/{hex_color}/200x200"
            
            # إعداد الإمبد
            embed = discord.Embed(
                title="🎨 لعبة الألوان",
                description="خمن وش هذا اللون المعروض بالصورة بأسرع وقت؟",
                color=discord.Color.from_rgb(r, g, b)
            )
            embed.set_thumbnail(url=image_url) 
            
            view = ColorGameView(correct_name, options, self, message.channel.id)
            msg = await message.channel.send(embed=embed, view=view)
            view.message_obj = msg # تمرير الرسالة للكلاس للتحكم بها عند الـ timeout

async def setup(bot):
    await bot.add_cog(ColorGameCog(bot))