import discord
from discord.ext import commands
import asyncio

# --- 1. كلاس زر قبول التحدي والدخول ---
class ChallengeView(discord.ui.View):
    def __init__(self, challenger):
        super().__init__(timeout=60.0)
        self.challenger = challenger
        self.opponent = None

    @discord.ui.button(label="⚔️ قبول التحدي", style=discord.ButtonStyle.secondary) # زر شفاف لقَبول التحدي
    async def accept_challenge(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user == self.challenger:
            await interaction.response.send_message("لا يمكنك تحدي نفسك! ابحث عن خصم حقيقي 😉", ephemeral=True)
            return

        self.opponent = interaction.user
        self.stop() # إيقاف الانتظار لبدء اللعبة
        await interaction.response.defer()

# --- 2. كلاس أزرار اللعب الشفافة (حجرة، ورقة، مقص) ---
class RPSGameView(discord.ui.View):
    def __init__(self, p1, p2):
        super().__init__(timeout=30.0)
        self.p1 = p1
        self.p2 = p2
        self.choices = {p1: None, p2: None}

    async def handle_choice(self, interaction: discord.Interaction, choice: str):
        user = interaction.user
        
        # التحقق من أن الضاغط هو أحد المتحديين
        if user != self.p1 and user != self.p2:
            await interaction.response.send_message("أنت لست طرفاً في هذا التحدي! 🥊", ephemeral=True)
            return

        # التحقق إذا كان قد اختار مسبقاً
        if self.choices[user] is not None:
            await interaction.response.send_message("لقد قمت باختيار سلاحك بالفعل! انتظر الخصم 🔒", ephemeral=True)
            return

        # تسجيل الاختيار وإرسال رسالة مخفية تأكيدية
        self.choices[user] = choice
        await interaction.response.send_message(f"✅ اخترت **[{choice}]** بنجاح! انتظر اختيار خصمك...", ephemeral=True)

        # إذا اختار كلا اللاعبين، تنتهي مرحلة الضغط لحساب النتيجة
        if all(v is not None for v in self.choices.values()):
            self.stop()

    @discord.ui.button(label="🪨 حجرة", style=discord.ButtonStyle.secondary) # أزرار شفافة تماماً
    async def rock(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.handle_choice(interaction, "حجرة")

    @discord.ui.button(label="📄 ورقة", style=discord.ButtonStyle.secondary)
    async def paper(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.handle_choice(interaction, "ورقة")

    @discord.ui.button(label="✂️ مقص", style=discord.ButtonStyle.secondary)
    async def scissors(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.handle_choice(interaction, "مقص")

# --- 3. كلاس الـ Cog الأساسي للمحرك ---
class RPSCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="حجرة")
    async def rock_paper_scissors(self, ctx):
        # إمبيد طلب التحدي المبدئي
        init_embed = discord.Embed(
            title="🪨 ورقة مقص - تحدي جديد!",
            description=f"قام {ctx.author.mention} بإصدار تحدي ساحق!\nاضغط على الزر الشفاف بالأسفل لقَبول التحدي ودخول المعركة. 🥊",
            color=0x2b2d31
        )
        
        challenge_view = ChallengeView(ctx.author)
        msg = await ctx.send(embed=init_embed, view=challenge_view)

        await challenge_view.wait()

        # في حال انتهى الوقت ولم يدخل أحد
        if challenge_view.opponent is None:
            timeout_embed = discord.Embed(
                title="⌛ انتهى وقت التحدي",
                description="لم يقبل أحد التحدي، يبدو أن الجميع خائف! 😎",
                color=0x2b2d31
            )
            await msg.edit(embed=timeout_embed, view=None)
            return

        p1 = challenge_view.challenger
        p2 = challenge_view.opponent

        # حلقة اللعبة الأساسية (تستمر وتعيد في حال التعادل)
        while True:
            play_embed = discord.Embed(
                title="⚔️ بدأت المواجهة الحاسمة!",
                description=f"المباراة بين:\n👤 {p1.mention}\n👤 {p2.mention}\n\nاختر حركتك القادمة بسرّية من الأزرار بالأسفل! 👀",
                color=0x2b2d31
            )
            await msg.edit(embed=play_embed, view=None)
            
            game_view = RPSGameView(p1, p2)
            await msg.edit(view=game_view)

            await game_view.wait()

            # التحقق من عدم سحب أحد اللاعبين (Timeout)
            if any(v is None for v in game_view.choices.values()):
                await ctx.send("⌛ تعطلت المعركة بسبب عدم اختيار أحد اللاعبين في الوقت المحدد!")
                break

            c1 = game_view.choices[p1]
            c2 = game_view.choices[p2]

            # --- حالة التعادل ---
            if c1 == c2:
                tie_embed = discord.Embed(
                    title="🤝 تعادل غريب!",
                    description=f"كلاكما اختار نفس السلاح: **[{c1}]**!\n\n**جاري إعادة الجولة تلقائياً خلال 3 ثوانٍ... ⏳**",
                    color=0x2b2d31
                )
                await msg.edit(embed=tie_embed, view=None)
                await asyncio.sleep(3) # العد التنازلي لإعادة الجولة
                continue # الرجوع لأول الحلقة لبدء جولة جديدة

            # --- تحديد الفائز والخاسر ---
            # الحالات التي يفوز فيها اللاعب الأول (c1)
            if (c1 == "حجرة" and c2 == "مقص") or (c1 == "ورقة" and c2 == "حجرة") or (c1 == "مقص" and c2 == "ورقة"):
                winner = p1
                winner_choice = c1
                loser_choice = c2
            else:
                winner = p2
                winner_choice = c2
                loser_choice = c1

            # إمبيد النتيجة النهائية الذهبي
            result_embed = discord.Embed(
                title="🏆 انتهاء الملحمة وفوز البطل!",
                description=f"الفائز الساحق هو: {winner.mention} 🎉\n\n"
                            f"👤 {p1.display_name}: **[{c1}]**\n"
                            f"👤 {p2.display_name}: **[{c2}]**\n\n"
                            f"🔥 انتصرت الـ **{winner_choice}** على الـ **{loser_choice}** بجدارة!",
                color=0xfadb14 # لون ذهبي مخصص للفائز
            )
            await msg.edit(embed=result_embed, view=None)
            break # الخروج من الحلقة بعد فوز أحد الطرفين

async def setup(bot):
    await bot.add_cog(RPSCog(bot))