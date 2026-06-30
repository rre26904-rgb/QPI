import discord
from discord.ext import commands
import asyncio
import random
import json
import os

# قائمة كلمات الرصيد والاقتصاد
ECONOMY_WORDS = [
    "استثمار", "اقتصاد", "مليونير", "ميزانية", "بورصة", "ارباح", "تجارة", "تمويل", "رصيد", "حوالة", "سيولة", "ثروة", "أسهم", "سندات", "صكوك", "عقارات", "ضرائب", "جمارك", "تضخم", "ركود", "فائدة", "قرض", "مديونية", "وديعة", "مصرف", "خزينة", "عملات", "دولار", "يورو", "ذهب", "نفط", "طاقة", "صناعة", "زراعة", "إنتاج", "تصدير", "استيراد", "شحن", "مخازن", "توزيع", "مبيعات", "مشتريات", "تسويق", "إعلانات", "عميل", "مستهلك", "منافسة", "احتكار", "شركة", "مؤسسة", "مشروع", "صفقة", "عقد", "شراكة", "اندماج", "استحواذ", "إفلاس", "خسارة", "تصفية", "مخاطرة", "تأمين", "معاش", "رواتب", "حوافز", "مكافأة", "وظيفة", "بطالة", "عمالة", "إنتاجية", "كفاءة", "جودة", "تطوير", "ابتكار", "تكنولوجيا", "بيانات", "إحصائيات", "مؤشر", "رسم_بياني", "تحليل", "تقرير", "تدقيق", "محاسبة", "فواتير", "إيصال", "دفع", "نقدا", "بطاقة", "ائتمان", "محفظة", "مدخرات", "استهلاك", "نفقات", "مصاريف", "تكلفة", "سعر", "قيمة", "خصم", "عرض", "طلب", "سوق"
]

class RevealWordCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.scores_file = "global_points.json" # اسم ملف النقاط الموحد
        
        # 🟢 ربط القفل العام المشترك داخل البوت
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
            
        if message.content.strip() == "-اكشف":
            # 🟢 الفحص باستخدام القفل العام للبوت
            if message.channel.id in self.bot.global_game_lock:
                await message.channel.send("⚠️ هناك لعبة أخرى جارية بالفعل في هذا الروم! انتظر حتى تنتهي.")
                return
                
            # قفل الروم في البوت كاملاً لمنع تشغيل لعبة أخرى
            self.bot.global_game_lock.add(message.channel.id)
            
            word = random.choice(ECONOMY_WORDS)
            hidden_word = ["_" for _ in word]
            
            # إنشاء أرقام تمثل أماكن الحروف، ثم لخبطتها ليكون الكشف عشوائي
            hidden_indices = list(range(len(word)))
            random.shuffle(hidden_indices) 
            
            embed = discord.Embed(
                title="🔍 لعبة اكشف الكلمة",
                description=f"الكلمة: `{' '.join(hidden_word)}`\n\nأول شخص يكتب الكلمة كاملة هو الفائز!",
                color=discord.Color.blurple()
            )
            game_msg = await message.channel.send(embed=embed)
            
            async def reveal_loop():
                try:
                    # اللوب بيشتغل كل ثانيتين، ويوقف إذا بقى حرف واحد فقط (عشان ما يحلها البوت)
                    while len(hidden_indices) > 1:
                        await asyncio.sleep(2)
                        
                        # سحب حرف عشوائي من القائمة الملخبطة وكشفه
                        idx = hidden_indices.pop()
                        hidden_word[idx] = word[idx]
                        
                        embed.description = f"الكلمة: `{' '.join(hidden_word)}`\n\nأول شخص يكتب الكلمة كاملة هو الفائز!"
                        await game_msg.edit(embed=embed)
                except asyncio.CancelledError:
                    pass

            # تشغيل وظيفة كشف الحروف في الخلفية
            reveal_task = asyncio.create_task(reveal_loop())
            
            def check_answer(m):
                return m.channel == message.channel and m.content.strip() == word and not m.author.bot

            try:
                # ننتظر 30 ثانية للإجابة
                winner_msg = await self.bot.wait_for('message', check=check_answer, timeout=30.0)
                
                # نوقف اللوب حق التعديل لأن فيه شخص فاز
                reveal_task.cancel()
                
                # تحديث وحفظ النقاط في الملف الموحد
                new_score = self.add_score(winner_msg.author.id)
                
                # --- تعديل رسالة الفوز لتطابق التصميم المطلوب ---
                win_embed = discord.Embed(
                    title="",
                    description=f" {winner_msg.author.mention} فاز في اللعبة!\nالكلمة كانت: **{word}**",
                    color=discord.Color.green()
                )
                
                view = discord.ui.View()
                
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
                async def magic_callback(interaction: discord.Interaction):
                    await interaction.response.send_message(
                        "👋 أهلاً بك! هذا سيرفر الدعم الفني الخاص بنا. حياك الله:\nhttps://discord.gg/zkJpxjk2rN", 
                        ephemeral=True 
                    )
                
                # ربط الدالة بالزر
                magic_button.callback = magic_callback
                
                # إضافة الأزرار للرسالة
                view.add_item(score_button)
                view.add_item(magic_button)
                
                await message.channel.send(embed=win_embed, view=view)

            except asyncio.TimeoutError:
                reveal_task.cancel()
                timeout_embed = discord.Embed(
                    title="⏳ انتهى الوقت!",
                    description=f"محد قدر يكتشف الكلمة في الوقت المحدد.\nالكلمة كانت: **{word}**",
                    color=discord.Color.red()
                )
                await message.channel.send(embed=timeout_embed)
                
            finally:
                # 🟢 فتح القفل العام المشترك بعد انتهاء اللعبة
                if message.channel.id in self.bot.global_game_lock:
                    self.bot.global_game_lock.remove(message.channel.id)

async def setup(bot):
    await bot.add_cog(RevealWordCog(bot))