import discord
from discord.ext import commands
import os
import sys
import aiohttp

# --- ضع الآيدي الخاص بك هنا ---
OWNER_ID = 123456789012345678 

# --- 1. النوافذ المنبثقة (Modals) ---
class NameModal(discord.ui.Modal, title='تغيير اسم البوت'):
    new_name = discord.ui.TextInput(label='الاسم الجديد', placeholder='أدخل الاسم...', min_length=2, max_length=32)
    async def on_submit(self, interaction: discord.Interaction):
        await interaction.client.user.edit(username=self.new_name.value)
        await interaction.response.send_message(f"✅ تم تغيير الاسم إلى: **{self.new_name.value}**", ephemeral=True)

class ImageModal(discord.ui.Modal):
    def __init__(self, action_type):
        super().__init__(title=f'تغيير {action_type}')
        self.action_type = action_type
        self.url = discord.ui.TextInput(label='رابط الصورة (URL)', placeholder='ضع رابط الصورة المباشر هنا...')
        self.add_item(self.url)
    async def on_submit(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=True)
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(self.url.value) as resp:
                    data = await resp.read()
            if self.action_type == "الأفاتار": await interaction.client.user.edit(avatar=data)
            else: await interaction.client.user.edit(banner=data)
            await interaction.followup.send(f"✅ تم تحديث {self.action_type} بنجاح!", ephemeral=True)
        except Exception as e: await interaction.followup.send(f"❌ خطأ: {e}", ephemeral=True)

# --- 2. لوحة التحكم (View) ---
class BotControlView(discord.ui.View):
    def __init__(self, bot, cog):
        super().__init__(timeout=None)
        self.bot = bot
        self.cog = cog

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        if interaction.user.id == OWNER_ID: return True
        await interaction.response.send_message("❌ هذا الأمر للمالك فقط!", ephemeral=True)
        return False

    @discord.ui.button(label="🔄 تحديث", style=discord.ButtonStyle.blurple, row=0)
    async def refresh(self, interaction: discord.Interaction, button: discord.ui.Button):
        embed = await self.cog.get_stats_embed()
        await interaction.response.edit_message(embed=embed, view=self)

    @discord.ui.button(label="اسم", style=discord.ButtonStyle.grey, row=0)
    async def change_name(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_modal(NameModal())

    @discord.ui.button(label="أفاتار", style=discord.ButtonStyle.grey, row=0)
    async def change_avatar(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_modal(ImageModal("الأفاتار"))

    @discord.ui.button(label="بانر", style=discord.ButtonStyle.grey, row=1)
    async def change_banner(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_modal(ImageModal("البانر"))

    @discord.ui.button(label="إعادة تشغيل", style=discord.ButtonStyle.green, row=1)
    async def restart(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message("🔄 جاري إعادة التشغيل...", ephemeral=True)
        os.execv(sys.executable, ['python'] + sys.argv)

    @discord.ui.button(label="إيقاف", style=discord.ButtonStyle.red, row=1)
    async def shutdown(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message("🛑 تم الإيقاف.", ephemeral=True)
        await self.bot.close()

# --- 3. الكوج الرئيسي ---
class SystemCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    async def get_stats_embed(self):
        embed = discord.Embed(title="📊 لوحة التحكم", color=discord.Color.dark_theme())
        embed.add_field(name="🌐 السيرفرات", value=f"`{len(self.bot.guilds)}`", inline=True)
        embed.add_field(name="⚡ البينج", value=f"`{round(self.bot.latency * 1000)}ms`", inline=True)
        embed.set_footer(text="مُخصص للمالك فقط")
        return embed

    # أوامر Prefix العادية
    @commands.command(name="احصاء")
    async def stats_command(self, ctx):
        if ctx.author.id != OWNER_ID: return
        await ctx.send(embed=await self.get_stats_embed(), view=BotControlView(self.bot, self))

    @commands.command(name="ping")
    async def ping_command(self, ctx):
        if ctx.author.id != OWNER_ID: return
        await ctx.send(f"🏓 `{round(self.bot.latency * 1000)}ms`")

    @commands.command(name="reload")
    async def reload_command(self, ctx, ext):
        if ctx.author.id != OWNER_ID: return
        await self.bot.reload_extension(f'cogs.{ext}')
        await ctx.send(f"🔄 تم تحديث الكوج: `{ext}`")

async def setup(bot: commands.Bot):
    await bot.add_cog(SystemCog(bot))