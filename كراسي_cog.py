import discord
from discord.ext import commands
import asyncio
import random

# --- كلاس زر الانضمام مع العداد الديناميكي الشفاف ---
class JoinView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=20.0)
        self.players = []

    @discord.ui.button(label="🎮 انضمام للعبة", style=discord.ButtonStyle.secondary)
    async def join(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user in self.players:
            await interaction.response.send_message("أنت مسجل بالفعل في القائمة! 🏎️", ephemeral=True)
            return

        self.players.append(interaction.user)
        # رسالة انضمام خاصة ومخفية للاعب نفسه
        await interaction.response.send_message("✅ انضممت للعبة الكراسي بنجاح! استعد 🪑", ephemeral=True)
        
        # تحديث الـ Embed الأساسي بالعداد
        updated_embed = discord.Embed(
            title="🎮 لعبة الكراسي",
            description="اضغط على الزر بالأسفل للاشتراك في اللعبة.\nتبدأ اللعبة خلال 30 ثانية (مطلوب لاعبين على الأقل).",
            color=0x2b2d31
        )
        updated_embed.add_field(name="👥 عدد المشاركين الحالي", value=f"📡 **{len(self.players)}** لاعبين", inline=False)
        
        try:
            await interaction.message.edit(embed=updated_embed)
        except discord.HTTPException:
            pass

# --- كلاس زر الكرسي (تم التعديل لتصبح رسالة النجاح خاصة باللاعب فقط) ---
class ChairButton(discord.ui.View):
    def __init__(self, players, max_chairs):
        super().__init__(timeout=15.0)
        self.players = players
        self.max_chairs = max_chairs
        self.saved_players = []

    @discord.ui.button(label="🪑 اجلس هنا بسرعة!", style=discord.ButtonStyle.secondary)
    async def click_chair(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user not in self.players:
            await interaction.response.send_message("عذراً، أنت لست من ضمن اللاعبين في هذه الجولة! ❌", ephemeral=True)
            return

        if interaction.user in self.saved_players:
            await interaction.response.send_message("أنت حاجز كرسي بالفعل، انتظر باقي اللاعبين! 🛋️", ephemeral=True)
            return

        if len(self.saved_players) < self.max_chairs:
            self.saved_players.append(interaction.user)
            # التعديل الجديد: الرسالة أصبحت مخفية وخاصة بالشخص الذي لحق على الكرسي
            await interaction.response.send_message("⚡ لحقت على كرسي وحميت نفسك! 🪑", ephemeral=True)
            
            if len(self.saved_players) == self.max_chairs:
                self.stop()
        else:
            await interaction.response.send_message("للأسف امتلأت الكراسي! 😭", ephemeral=True)

# --- كلاس الـ Cog الأساسي ---
class KrasiCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.active_games = {}

    @commands.command(name="كراسي")
    async def musical_chairs(self, ctx):
        if ctx.channel.id in self.active_games:
            await ctx.send("❌ هناك لعبة قائمة بالفعل في هذا الروم، انتظر حتى تنتهي!")
            return

        self.active_games[ctx.channel.id] = True

        try:
            start_embed = discord.Embed(
                title="🎮 لعبة الكراسي",
                description="اضغط على الزر بالأسفل للاشتراك في اللعبة.\nتبدأ اللعبة خلال 30 ثانية (مطلوب لاعبين على الأقل).",
                color=0x2b2d31
            )
            start_embed.add_field(name="👥 عدد المشاركين الحالي", value="📡 **0** لاعبين", inline=False)

            join_view = JoinView()
            init_msg = await ctx.send(embed=start_embed, view=join_view)

            await asyncio.sleep(30)
            
            try:
                end_embed = discord.Embed(
                    title="🎮 لعبة الكراسي",
                    description="⌛ **انتهى وقت التسجيل!**",
                    color=0x2b2d31
                )
                end_embed.add_field(name="👥 إجمالي المشاركين", value=f"🏆 **{len(join_view.players)}** لاعبين", inline=False)
                await init_msg.edit(embed=end_embed, view=None)
            except discord.HTTPException:
                pass

            players = join_view.players

            if len(players) < 2:
                await ctx.send("❌ تم إلغاء اللعبة لعدم وجود عدد كافٍ من اللاعبين.")
                return

            round_num = 1
            while len(players) > 1:
                await asyncio.sleep(2)
                
                round_embed = discord.Embed(
                    title=f"✨ الجولة {round_num}",
                    description="**استعدوا... ⏳**",
                    color=0x2b2d31
                )
                round_msg = await ctx.send(embed=round_embed)

                await asyncio.sleep(random.randint(4, 9))

                max_chairs = len(players) - 1
                chair_view = ChairButton(players, max_chairs)

                chair_embed = discord.Embed(
                    title="🛑 إلحق الكرسي!!!",
                    description=f"اضغط على الزر بالأسفل فوراً!\nالكراسي المتبقية: **{max_chairs}** فقط! 🏃‍♂️",
                    color=0x2b2d31
                )
                
                alert_msg = await ctx.send(embed=chair_embed, view=chair_view)
                
                try:
                    await round_msg.delete()
                except discord.DiscordException:
                    pass

                await chair_view.wait()

                # فرز الخاسرين
                eliminated = [p for p in players if p not in chair_view.saved_players]

                # رسالة الإقصاء (تظهر للكل في الروم بشكل عام)
                for p in eliminated:
                    players.remove(p)
                    await ctx.send(f"💀 للأسف {p.mention} ما لحق وتم إقصاؤه!")

                try:
                    await alert_msg.edit(view=None)
                except discord.HTTPException:
                    pass
                
                round_num += 1

            # إعلان الفائز النهائي للجميع
            winner = players[0]
            
            # --- الإضافة الجديدة ---
            # تحديث النقاط (تأكد أن دالة add_score موجودة في نفس الكلاس الخاص بالكراسي)
            try:
                new_score = self.add_score(winner.id)
            except AttributeError:
                # إذا لم تقم بنقل دالة add_score إلى هذا الكلاس بعد
                new_score = "؟"

            winner_embed = discord.Embed(
                title="",
                description=f"     فاز في العبة:\n👑 {winner.mention} 👑",
                color=0xfadb14
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
                    ephemeral=True # تظهر للشخص اللي ضغط بس
                )
            
            # ربط الدالة بالزر
            magic_button.callback = magic_callback

            # إضافة الأزرار للرسالة
            view.add_item(score_button)
            view.add_item(magic_button)

            await ctx.send(embed=winner_embed, view=view)
            # -----------------------

        finally:
            self.active_games.pop(ctx.channel.id, None)

async def setup(bot):
    await bot.add_cog(KrasiCog(bot))