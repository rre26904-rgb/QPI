import discord
from discord.ext import commands
import asyncio
import random
import io
import math
from PIL import Image, ImageDraw, ImageFont

class RouletteGame:
    def __init__(self, ctx):
        self.ctx = ctx
        self.players = []
        self.is_registration_open = True

    # 🎨 دالة سحرية لتوليد عجلة روليت حقيقية متحركة (GIF) بصور اللاعبين
    def generate_wheel_gif(self, active_players, avatar_bytes_list):
        frames = []
        size = (400, 400)
        num_sectors = len(active_players)
        
        # الألوان المستخدمة في تقسيم العجلة
        colors = [(231, 76, 60), (46, 204, 113), (52, 152, 219), (241, 196, 15), (155, 89, 182), (26, 188, 156)]
        
        # حساب الزوايا لكل لاعب
        sector_angle = 360 / num_sectors
        
        # توليد 12 إطار للحركة الدائرية (GIF)
        for frame_idx in range(12):
            image = Image.new("RGBA", size, (44, 47, 51, 255)) # خلفية داكنة تناسب الديسكورد
            draw = ImageDraw.Draw(image)
            
            # دوران وهمي بكل إطار
            rotation_offset = frame_idx * 30 
            
            for i, player in enumerate(active_players):
                start_angle = (i * sector_angle) + rotation_offset
                end_angle = start_angle + sector_angle
                
                # رسم قطاع اللاعب
                color = colors[i % len(colors)]
                draw.pieslice([20, 20, 380, 380], start=start_angle, end=end_angle, fill=color, outline=(255,255,255))
                
                # حساب موقع الصورة في منتصف القطاع
                mid_angle = math.radians(start_angle + (sector_angle / 2))
                avatar_size = 40
                img_x = 200 + 110 * math.cos(mid_angle) - (avatar_size / 2)
                img_y = 200 + 110 * math.sin(mid_angle) - (avatar_size / 2)
                
                # رسم صورة اللاعب (Avatar) بدلاً من الرقم
                if avatar_bytes_list[i]:
                    try:
                        avatar_img = Image.open(io.BytesIO(avatar_bytes_list[i])).convert("RGBA")
                        avatar_img = avatar_img.resize((avatar_size, avatar_size))
                        
                        # إنشاء قناع دائري لقص الصورة
                        mask = Image.new('L', (avatar_size, avatar_size), 0)
                        draw_mask = ImageDraw.Draw(mask)
                        draw_mask.ellipse((0, 0, avatar_size, avatar_size), fill=255)
                        
                        # لصق الصورة في العجلة
                        image.paste(avatar_img, (int(img_x), int(img_y)), mask)
                    except Exception:
                        # في حال فشل تحميل الصورة لسبب ما، نضع رقم احتياطي
                        draw.text((int(img_x) + 15, int(img_y) + 10), str(i+1), fill=(255,255,255))
                else:
                    draw.text((int(img_x) + 15, int(img_y) + 10), str(i+1), fill=(255,255,255))
            
            # رسم المؤشر الثابت في الأعلى لبيان من ستقف عليه العجلة
            draw.polygon([(190, 10), (210, 10), (200, 40)], fill=(255, 215, 0))
            frames.append(image)
            
        # حفظ الإطارات في ملف بايتات بصيغة GIF متحرك
        out_buf = io.BytesIO()
        frames[0].save(out_buf, format='GIF', save_all=True, append_images=frames[1:], duration=100, loop=0)
        out_buf.seek(0)
        return out_buf

# 🔘 كلاس أزرار تصويت الإقصاء عند وجود أكثر من لاعبين
class VoteEliminationView(discord.ui.View):
    def __init__(self, target_player, active_players, ctx):
        super().__init__(timeout=20.0)
        self.target_player = target_player
        self.active_players = active_players
        self.ctx = ctx
        self.votes = {}
        
        # إنشاء زر لكل لاعب متبقي ليتم التصويت على طرده
        for p in active_players:
            if p.id != target_player.id:
                btn = discord.ui.Button(label=f"طرد {p.name}", style=discord.ButtonStyle.danger, custom_id=str(p.id))
                btn.callback = self.vote_callback
                self.add_item(btn)
                
    async def vote_callback(self, interaction: discord.Interaction):
        self.votes[interaction.user.id] = int(interaction.data['custom_id'])
        await interaction.response.send_message("✅ تم تسجيل صوتك بنجاح!", ephemeral=True)

class RouletteCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.active_games = {}

    # 🟢 دالة وهمية لإضافة النقاط، استبدلها بكود حفظ النقاط الفعلي في ملف الجيسون الخاص بك
    def add_score(self, user_id: int):
        return "+10"

    @commands.command(name="روليت")
    async def start_roulette(self, ctx):
        if ctx.channel.id in self.active_games:
            return await ctx.send("❌ توجد مباراة روليت قائمة بالفعل في هذا الروم!")

        game = RouletteGame(ctx)
        self.active_games[ctx.channel.id] = game

        # ⏱️ 1. مرحلة فتح التسجيل والوقت
        embed = discord.Embed(
            title="🎡 بدأت لعبة عجلة الروليت الإقصائية 🎡",
            description="⏱️ أمامكم **30 ثانية** للتسجيل للمشاركة في الفعالية!\n\n**المشاركين حالياً:**\nلا يوجد أحد بعد.",
            color=discord.Color.blurple()
        )
        
        class RegisterView(discord.ui.View):
            def __init__(self):
                super().__init__(timeout=30.0)
            @discord.ui.button(label="تسجيل دخول 🎮", style=discord.ButtonStyle.success)
            async def join_btn(self, interaction: discord.Interaction, button: discord.ui.Button):
                if interaction.user in game.players:
                    return await interaction.response.send_message("❌ أنت مسجل بالفعل!", ephemeral=True)
                game.players.append(interaction.user)
                
                # تحديث قائمة المشاركين في الإمبد فوراً
                players_list = "\n".join([f"🔹 {p.mention}" for p in game.players])
                embed.description = f"⏱️ أمامكم **30 ثانية** للتسجيل للمشاركة في الفعالية!\n\n**المشاركين حالياً ({len(game.players)}):**\n{players_list}"
                await interaction.response.edit_message(embed=embed)

        view = RegisterView()
        msg = await ctx.send(embed=embed, view=view)
        
        await asyncio.sleep(30) # انتهاء وقت التسجيل
        game.is_registration_open = False
        view.stop()

        if len(game.players) < 2:
            del self.active_games[ctx.channel.id]
            return await ctx.send("❌ تم إلغاء اللعبة بسبب عدم وجود لاعبين كافيين (اقل شي 2).")

        # 🏁 2. بدء حلقات اللف والإقصاء المتتالي
        active_list = list(game.players)
        
        while len(active_list) > 1:
            await ctx.send(f"🔄 **جاري تجهيز العجلة ولفها بين {len(active_list)} لاعبين متبقين...**")
            
            # تحميل صور اللاعبين (Avatars) قبل إرسالها للدالة
            avatar_bytes_list = []
            for p in active_list:
                try:
                    # تنظيف الصورة بحجم صغير لسرعة المعالجة
                    av_bytes = await p.display_avatar.replace(size=64, format="png").read()
                except Exception:
                    av_bytes = None
                avatar_bytes_list.append(av_bytes)

            # توليد وإرسال ملف الـ GIF الحقيقي للعجلة وهي تلف بصورهم
            wheel_gif = await self.bot.loop.run_in_executor(None, game.generate_wheel_gif, active_list, avatar_bytes_list)
            file = discord.File(fp=wheel_gif, filename="roulette.gif")
            await ctx.send(file=file)
            await asyncio.sleep(3) # وقت اللف الوهمي للحماس
            
            # اختيار الشخص التي وقعت عليه العجلة عشوائياً
            selected_idx = random.randint(0, len(active_list) - 1)
            chosen_player = active_list[selected_idx]
            
            # 👥 الحالة الأولى: بقاء آخر لاعبين اثنين (تحديد الفائز مباشرة)
            if len(active_list) == 2:
                # الشخص الذي تقع عليه العجلة يخسر، والثاني يفوز
                winner = active_list[1] if selected_idx == 0 else active_list[0]
                
                # 🟢 تحديث وحفظ النقاط في ملف الجيسون الموحد
                new_score = self.add_score(winner.id)

                win_embed = discord.Embed(
                    title="",
                    description=f" {winner.mention} فاز في اللعبة!",
                    color=discord.Color.green(),
                )

                win_view = discord.ui.View()
                
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
                win_view.add_item(score_button)
                win_view.add_item(magic_button)
                
                await ctx.send(content=f"العجلة استقرت على {chosen_player.mention} وتم إقصاؤه!", embed=win_embed, view=win_view)
                break
                
            # 👥 الحالة الثانية: عدد اللاعبين أكثر من 2 (الشخص المختار يصوت على طرد غيره)
            else:
                announcement = discord.Embed(
                    title="🎯 وقع الاختيار السهم! 🎯",
                    description=f"العجلة استقرت على رقم **{selected_idx + 1}** وهو اللاعب: {chosen_player.mention}\n\n⚠️ {chosen_player.mention} لديك الآن 20 ثانية لاختيار لاعب آخر تود إقصاءه فوراً من الفعالية عبر الأزرار، أو سيتم اختيار لاعب عشوائي إذا انتهى الوقت!",
                    color=discord.Color.orange()
                )
                announcement.set_thumbnail(url=chosen_player.display_avatar.url)
                
                vote_view = VoteEliminationView(chosen_player, active_list, ctx)
                vote_msg = await ctx.send(content=f"{chosen_player.mention}", embed=announcement, view=vote_view)
                
                await asyncio.sleep(20) # انتظار تصويت صاحب الدور
                vote_view.stop()
                
                eliminated_player = None
                if vote_view.votes:
                    # جلب أكثر شخص تم التصويت عليه من قبل صاحب الدور
                    most_voted_id = max(set(vote_view.votes.values()), key=list(vote_view.votes.values()).count)
                    eliminated_player = next((p for p in active_list if p.id == most_voted_id), None)
                
                # إذا لم يصوت أو انتهى الوقت يختار البوت عشوائياً شخصاً غير صاحب الدور ليطرده
                if not eliminated_player:
                    possible_targets = [p for p in active_list if p.id != chosen_player.id]
                    eliminated_player = random.choice(possible_targets)
                    await ctx.send(f"⏱️ انتهى وقت التصويت! البوت اختار عشوائياً وطرد: {eliminated_player.mention} 🪓")
                else:
                    await ctx.send(f"🪓 {chosen_player.mention} قرر تصفية وإقصاء اللاعب: {eliminated_player.mention} من الجولة!")
                
                # إزالة الشخص المقصى من قائمة اللعب الحالية
                active_list.remove(eliminated_player)
                await ctx.send(f"📉 المتبقين في الحلبة الآن: {len(active_list)} لاعبين.")
                await asyncio.sleep(2)

        # تنظيف الغرفة بعد انتهاء اللعبة
        if ctx.channel.id in self.active_games:
            del self.active_games[ctx.channel.id]

async def setup(bot):
    await bot.add_cog(RouletteCog(bot))
    print("✅ تم تحميل كوج لعبة الروليت الحقيقية الديناميكية المتقدمة (GIF)!")