import discord
from discord.ext import commands
import asyncio
from typing import List, Optional

# 1. كلاس لوحة اللعب الحسابية
class TicTacToeView(discord.ui.View):
    X = 1
    O = -1
    Tie = 2

    def __init__(self, player_x: discord.Member, player_o: discord.Member, starter: Optional[discord.Member] = None):
        super().__init__(timeout=60.0)
        self.player_x = player_x  # لاعب X
        self.player_o = player_o  # لاعب O
        
        # 🔄 تحديد من سيبدأ الجولة الحالية (الافتراضي للجولة الأولى هو player_x)
        self.initial_starter = starter if starter else player_x
        self.current_player = self.initial_starter

        # بناء مصفوفة اللوحة 3x3 حسابياً
        self.board: List[List[int]] = [
            [0, 0, 0],
            [0, 0, 0],
            [0, 0, 0],
        ]

        # توليد الأزرار التسعة في اللوحة
        for x in range(3):
            for y in range(3):
                self.add_item(TicTacToeButton(x, y))

    # دالة التحقق من الفوز
    def check_board_winner(self):
        # فحص الصفوف الأفقية
        for row in self.board:
            value = sum(row)
            if value == 3:
                return self.X
            elif value == -3:
                return self.O

        # فحص الأعمدة العمودية
        for col in range(3):
            value = self.board[0][col] + self.board[1][col] + self.board[2][col]
            if value == 3:
                return self.X
            elif value == -3:
                return self.O

        # فحص القطرين
        diag1 = self.board[0][0] + self.board[1][1] + self.board[2][2]
        diag2 = self.board[0][2] + self.board[1][1] + self.board[2][0]
        if diag1 == 3 or diag2 == 3:
            return self.X
        elif diag1 == -3 or diag2 == -3:
            return self.O

        # فحص التعادل
        if all(cell != 0 for row in self.board for cell in row):
            return self.Tie

        return None


# 2. كلاس الزر داخل لوحة الـ XO
class TicTacToeButton(discord.ui.Button['TicTacToeView']):
    def __init__(self, x: int, y: int):
        super().__init__(style=discord.ButtonStyle.secondary, label='\u200b', row=y)
        self.x = x
        self.y = y

    async def callback(self, interaction: discord.Interaction):
        assert self.view is not None
        view: TicTacToeView = self.view
        
        # التحقق من أن اللاعب صاحب الدور هو من ضغط الزر
        if interaction.user.id != view.current_player.id:
            await interaction.response.send_message('❌ ليس دورك الآن للعب!', ephemeral=True)
            return

        # تعيين العلامة وتغيير الدور للاعب الآخر
        if view.current_player == view.player_x:
            self.label = '❌'
            self.style = discord.ButtonStyle.danger
            view.board[self.y][self.x] = view.X
            view.current_player = view.player_o
            content = f"🎮 دور اللاعب التالي: {view.player_o.mention} (⭕)"
        else:
            self.label = '⭕'
            self.style = discord.ButtonStyle.success
            view.board[self.y][self.x] = view.O
            view.current_player = view.player_x
            content = f"🎮 دور اللاعب التالي: {view.player_x.mention} (❌)"

        self.disabled = True

        # التحقق من النتيجة
        winner = view.check_board_winner()
        if winner is not None:
            if winner == view.X:
                content = f'🏆 مبروك الفوز! {view.player_x.mention} (❌) انتصر في المواجهة!'
                for child in view.children:
                    child.disabled = True
                view.stop()
            elif winner == view.O:
                content = f'🏆 مبروك الفوز! {view.player_o.mention} (⭕) انتصر في المواجهة!'
                for child in view.children:
                    child.disabled = True
                view.stop()
            elif winner == view.Tie:
                # 🔄 لتطبيق فكرتك بدقة: الخصم الذي لم يبدأ الجولة الحالية هو من سيبدأ جولة الإعادة
                next_starter = view.player_o if view.initial_starter == view.player_x else view.player_x
                
                content = '🤝 **تعادل!** جاري بدء مباراة الإعادة تلقائياً وعكس دور البداية...'
                for child in view.children:
                    child.disabled = True
                view.stop()
                
                await interaction.response.edit_message(content=content, view=view)
                await asyncio.sleep(2)
                
                # إنشاء اللوحة الجديدة وتمرير اللاعب الثاني كبادئ
                new_view = TicTacToeView(view.player_x, view.player_o, starter=next_starter)
                
                starter_sign = "❌" if next_starter == view.player_x else "⭕"
                await interaction.channel.send(
                    content=f"🔄 **مباراة الإعادة! (تم تبديل دور البداية لإنصاف اللاعب الثاني)**\nالدور الافتتاحي الآن: {next_starter.mention} ({starter_sign})", 
                    view=new_view
                )
                return

        await interaction.response.edit_message(content=content, view=view)


# 3. كلاس زر الانضمام والمشاركة
class JoinGameView(discord.ui.View):
    def __init__(self, p1):
        super().__init__(timeout=15.0)
        self.p1 = p1
        self.is_started = False

    @discord.ui.button(label="انضمام للمشاركة 🎮", style=discord.ButtonStyle.primary)
    async def join_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id == self.p1.id:
            await interaction.response.send_message("❌ لا يمكنك اللعب ضد نفسك! انتظر خصماً.", ephemeral=True)
            return
        
        self.is_started = True
        self.stop()
        
        game_view = TicTacToeView(self.p1, interaction.user)
        await interaction.response.edit_message(
            content=f"🏁 **بدأت المباراة!**\n{self.p1.mention} (❌)  **Vs** {interaction.user.mention} (⭕)\n\nالدور الحالي: {self.p1.mention} (❌)", 
            view=game_view
        )

    async def on_timeout(self):
        if not self.is_started:
            self.stop()


# 4. كلاس الكوج الأساسي لبوت الـ XO
class XOCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(name="xo", aliases=["اكس_او", "اكس او"])
    async def start_xo(self, ctx: commands.Context):
        join_view = JoinGameView(ctx.author)
        msg = await ctx.send(f"⚔️ {ctx.author.mention} يطلب تحدي **XO**!\n⏱️ اضغط على زر (انضمام للمشاركة) بالأسفل للعب (لديك 15 ثانية)...", view=join_view)
        
        await join_view.wait()
        
        if not join_view.is_started:
            try:
                await msg.edit(content="❌ انتهى الوقت (15 ثانية) ولم ينضم أحد للمشاركة في اللعبة.", view=None)
            except:
                pass


async def setup(bot: commands.Bot):
    await bot.add_cog(XOCog(bot))