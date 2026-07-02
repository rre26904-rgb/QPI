import discord
from discord.ext import commands
import asyncio
import random
from collections import Counter

# --- 1. كلاس قائمة التسجيل والانضمام ---
class MafiaJoinView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=30.0)
        self.players = []

    @discord.ui.button(label="🕵️‍♂️ انضمام للعبة", style=discord.ButtonStyle.secondary)
    async def join(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user in self.players:
            await interaction.response.send_message("أنت مسجل بالفعل في القائمة! 📑", ephemeral=True)
            return

        self.players.append(interaction.user)
        await interaction.response.send_message("✅ تم تسجيلك في قائمة المقيمين بالمدينة، استعد لإنقاذها!", ephemeral=True)
        
        # تحديث الإمبيد بالعداد الجديد
        embed = discord.Embed(
            title="🕵️‍♂️ شبكة المافيا - ليلة غامضة",
            description="المدينة مهددة! اضغط على الزر بالأسفل للانضمام إلى اللعبة.\n\n⌛ **وقت التسجيل:** 30 ثانية.\n⚠️ **الحد الأدنى للعب:** 4 لاعبين (مافيا، دكتور، شايب، ومواطن).",
            color=0x2b2d31
        )
        embed.add_field(name="👥 عدد اللاعبين الحالي", value=f"📡 **{len(self.players)}** لاعبين", inline=False)
        await interaction.message.edit(embed=embed)

# --- 2. قوائم الخيارات السرية أثناء الليل ---
class NightActionSelect(discord.ui.Select):
    def __init__(self, action_type, alive_players, cog_instance, channel_id):
        self.action_type = action_type
        self.cog_instance = cog_instance
        self.channel_id = channel_id
        
        # إنشاء خيارات القائمة المنسدلة من اللاعبين الأحياء
        options = [
            discord.SelectOption(label=player.display_name, value=str(player.id), emoji="👤")
            for player in alive_players
        ]
        
        placeholder_text = "اختر هدفك الليلة..."
        if action_type == "mafia": placeholder_text = "🩸 اختر الضحية لتصفيتها..."
        elif action_type == "doctor": placeholder_text = "🧪 اختر الشخص لحمايته..."
        elif action_type == "shaib": placeholder_text = "🔍 اختر شخصاً للتشكيك فيه..."

        super().__init__(placeholder=placeholder_text, min_values=1, max_values=1, options=options)

    async def callback(self, interaction: discord.Interaction):
        game = self.cog_instance.active_games[self.channel_id]
        target_id = int(self.values[0])
        target_user = interaction.guild.get_member(target_id)

        if self.action_type == "mafia":
            game['night_actions']['killed'] = target_user
            await interaction.response.send_message(f"🩸 تم اعتماد تصفية: **{target_user.display_name}**. نم بسلام!", ephemeral=True)
        
        elif self.action_type == "doctor":
            game['night_actions']['protected'] = target_user
            await interaction.response.send_message(f"🧪 تم حظر الهجوم عن: **{target_user.display_name}** لهذه الليلة!", ephemeral=True)
        
        elif self.action_type == "shaib":
            # كشف الهوية للشايب فوراً وخاص به
            target_role = game['roles'].get(target_user)
            identity = "❌ [قاتل/مافيا]" if target_role == "مافيا" else "✅ [مواطن بريء]"
            await interaction.response.send_message(f"🔍 نتيجة التحقيق حول **{target_user.display_name}** هي: {identity}", ephemeral=True)
            game['night_actions']['shaib_done'] = True

# --- 3. لوحة التحكم الليلية الزر العام ---
class NightControlView(discord.ui.View):
    def __init__(self, cog_instance, channel_id):
        super().__init__(timeout=30.0)
        self.cog_instance = cog_instance
        self.channel_id = channel_id

    @discord.ui.button(label="⚙️ فتح لوحة التحكم السرية", style=discord.ButtonStyle.secondary)
    async def open_panel(self, interaction: discord.Interaction, button: discord.ui.Button):
        game = self.cog_instance.active_games[self.channel_id]
        user = interaction.user

        if user not in game['alive']:
            await interaction.response.send_message("أنت خارج اللعبة حالياً (ميت)! 💀", ephemeral=True)
            return

        user_role = game['roles'].get(user)
        
        # إعداد قائمة اللاعبين الأحياء المتاحين للاستهداف
        alive_list = list(game['alive'])

        view = discord.ui.View()
        
        if user_role == "مافيا":
            view.add_item(NightActionSelect("mafia", alive_list, self.cog_instance, self.channel_id))
            await interaction.response.send_message("🩸 **مكتب المافيا السري:** اختر الضحية بالأسفل:", view=view, ephemeral=True)
        
        elif user_role == "دكتور":
            view.add_item(NightActionSelect("doctor", alive_list, self.cog_instance, self.channel_id))
            await interaction.response.send_message("🧪 **مختبر الطبيب:** اختر الشخص الذي تود منحه المصل لحمايته الليلة:", view=view, ephemeral=True)
        
        elif user_role == "شايب":
            view.add_item(NightActionSelect("shaib", alive_list, self.cog_instance, self.channel_id))
            await interaction.response.send_message("🔍 **فراسة الشايب:** اختر الشخص الذي تشك بأمره لكشف حقيقته:", view=view, ephemeral=True)
        
        else:
            await interaction.response.send_message("😴 **أنت مواطن عادي:** ليس لديك مهام سرية الليلة، نم في فراشك وانتظر الصباح لمتابعة التحقيقات.", ephemeral=True)

# --- 4. نظام التصويت النهاري العام ---
class DayVoteSelect(discord.ui.Select):
    def __init__(self, alive_players, cog_instance, channel_id):
        self.cog_instance = cog_instance
        self.channel_id = channel_id
        options = [
            discord.SelectOption(label=player.display_name, value=str(player.id), emoji="⚖️")
            for player in alive_players
        ]
        super().__init__(placeholder="اضغط هنا للتصويت ضد المتهم الرئيسي...", min_values=1, max_values=1, options=options)

    async def callback(self, interaction: discord.Interaction):
        game = self.cog_instance.active_games[self.channel_id]
        voter = interaction.user

        if voter not in game['alive']:
            await interaction.response.send_message("لا يمكنك التصويت، أنت ميت! 👻", ephemeral=True)
            return

        if voter in game['day_votes']:
            await interaction.response.send_message("لقد قمت بالتصويت بالفعل في هذه الجولة! ✋", ephemeral=True)
            return

        target_id = int(self.values[0])
        target_user = interaction.guild.get_member(target_id)
        
        game['day_votes'][voter] = target_user
        await interaction.response.send_message(f"✅ تم تسجيل صوتك رسمياً ضد: **{target_user.display_name}**", ephemeral=True)
        await interaction.channel.send(f"🗳️ **{voter.mention}** أدلى بصوته في ساحة المدينة!")

# --- 5. كلاس الـ Cog الأساسي للعبة ---
class MafiaCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.active_games = {}

    @commands.command(name="مافيا")
    async def start_mafia(self, ctx):
        if ctx.channel.id in self.active_games:
            await ctx.send("❌ هناك مواجهة قائمة بالفعل في هذه المدينة، انتظر حتى تنتهي الملحمة!")
            return

        self.active_games[ctx.channel.id] = {
            'players': [],
            'roles': {},
            'alive': set(),
            'night_actions': {'killed': None, 'protected': None, 'shaib_done': False},
            'day_votes': {}
        }
        
        game = self.active_games[ctx.channel.id]

        join_embed = discord.Embed(
            title="🕵️‍♂️ شبكة المافيا - ليلة غامضة",
            description="المدينة مهددة! اضغط على الزر بالأسفل للانضمام إلى اللعبة.\n\n⌛ **وقت التسجيل:** 45 ثانية.\n⚠️ **الحد الأدنى للعب:** 4 لاعبين (مافيا، دكتور، شايب، ومواطن).",
            color=0x2b2d31
        )
        join_embed.add_field(name="👥 عدد اللاعبين الحالي", value="📡 **0** لاعبين", inline=False)
        
        join_view = MafiaJoinView()
        msg = await ctx.send(embed=join_embed, view=join_view)

        await asyncio.sleep(45)
        
        # إغلاق التسجيل
        game['players'] = join_view.players
        try:
            await msg.edit(view=None)
        except discord.HTTPException: pass

        if len(game['players']) < 4:
            await ctx.send("❌ تم إلغاء اللعبة! لم يكتمل النصاب القانوني لأهل القرية (مطلوب 4 لاعبين كحد أدنى).")
            self.active_games.pop(ctx.channel.id, None)
            return

        # --- توزيع الأدوار بشكل عشوائي وعادل ---
        shuffled_players = list(game['players'])
        random.shuffle(shuffled_players)

        # تحديد الأدوار الإلزامية الأربعة الأساسية
        game['roles'][shuffled_players[0]] = "مافيا"
        game['roles'][shuffled_players[1]] = "دكتور"
        game['roles'][shuffled_players[2]] = "شايب"
        game['roles'][shuffled_players[3]] = "مواطن"

        # إذا كان هناك لاعبين أكثر، يتم توزيعهم كمواطنين
        for extra_player in shuffled_players[4:]:
            game['roles'][extra_player] = "مواطن"

        # تهيئة قائمة الأحياء
        game['alive'] = set(game['players'])

        await ctx.send("🎭 **تم توزيع الأدوار السرية بنجاح!** اضغطوا على لوحة التحكم الليلية فور نزولها لمعرفة أدواركم والبدء.")

        # --- حلقة اللعبة الأساسية (تستمر حتى فوز أحد الطرفين) ---
        game_running = True
        round_num = 1

        try:
            while game_running:
                # 1. فحص شروط الفوز أولاً
                mafia_count = sum(1 for p in game['alive'] if game['roles'][p] == "مافيا")
                innocent_count = len(game['alive']) - mafia_count
                new_score = "+10" # النقاط التي ستظهر في الزر

                if mafia_count == 0:
                    win_embed = discord.Embed(title="🎉 انتصار المدينة البريئة!", description="👑 نجح المواطنون والشايب والدكتور في القضاء على خلايا المافيا وتطهير الأرض!", color=0x2b2d31)
                    await ctx.send(embed=win_embed)
                    
                    # استخراج وتوضيح الفائزين من القرويين
                    innocent_winners = [p.mention for p in game['players'] if game['roles'][p] != "مافيا"]
                    winners_mentions = " ".join(innocent_winners)

                    winner_embed = discord.Embed(
                        title="",
                        description=f"     فاز في العبة:\n👑 {winners_mentions} 👑",
                        color=0xfadb14
                    )
                    
                    view = discord.ui.View()
                    score_button = discord.ui.Button(
                        label=f" 𐙚        {new_score}",
                        style=discord.ButtonStyle.secondary,
                        disabled=True,
                    )
                    view.add_item(score_button)
                    
                    await ctx.send(embed=winner_embed, view=view)
                    break
                
                if mafia_count >= innocent_count:
                    win_embed = discord.Embed(title="🩸 انتصار جماعة المافيا!", description="💥 أحكمت المافيا قبضتها على المدينة وأصبحت السيادة لهم بالكامل!", color=0x2b2d31)
                    await ctx.send(embed=win_embed)
                    
                    # استخراج وتوضيح الفائزين من المافيا (كما طلبت)
                    mafia_winners = [p.mention for p in game['players'] if game['roles'][p] == "مافيا"]
                    winners_mentions = " ".join(mafia_winners)

                    winner_embed = discord.Embed(
                        title="",
                        description=f"     فاز في العبة:\n👑 {winners_mentions} 👑",
                        color=0xfadb14
                    )
                    
                    view = discord.ui.View()
                    # زر النقاط (شفاف/رمادي مع نجمة)
                    score_button = discord.ui.Button(
                        label=f" 𐙚        {new_score}",
                        style=discord.ButtonStyle.secondary,
                        disabled=True,
                    )
                    view.add_item(score_button)
                    
                    await ctx.send(embed=winner_embed, view=view)
                    break

                # 2. بدء المرحلة الليلية
                await ctx.send(f"\n--- 🌆 **الجولة {round_num} - حلول الظلام** ---")
                night_embed = discord.Embed(
                    title="💤 حل الليل.. نامت المدينة وعيون المافيا مستيقظة",
                    description="اضغط على الزر بالأسفل لفتح لوحتك الخاصة واختيار أفعالك السرية.\n⏳ ينتهي الليل بعد **40 ثانية**.",
                    color=0x2b2d31
                )
                
                game['night_actions'] = {'killed': None, 'protected': None, 'shaib_done': False}
                night_view = NightControlView(self, ctx.channel.id)
                night_msg = await ctx.send(embed=night_embed, view=night_view)

                await asyncio.sleep(40)
                try: await night_msg.delete()
                except discord.DiscordException: pass

                # 3. معالجة نتائج الليل وبدء الصباح
                await ctx.send("🌅 **أشرقت الشمس.. واستيقظ أهل المدينة في الساحة العامة!**")
                await asyncio.sleep(2)

                victim = game['night_actions']['killed']
                protector_target = game['night_actions']['protected']

                if victim:
                    if victim == protector_target:
                        # الدكتور حمى الضحية بنجاح
                        fail_embed = discord.Embed(title="🛡️ تقرير الصباح: محاولة فاشلة", description="حاولت المافيا تصفية أحد السكان الليلة، لكن الطبيب كان في الموعد وقدم مصل الحماية فوراً! لم يمت أحد.", color=0x2b2d31)
                        await ctx.send(embed=fail_embed)
                    else:
                        # نجاح عملية القتل
                        game['alive'].remove(victim)
                        kill_embed = discord.Embed(title="🩸 تقرير الصباح: جريمة نكراء", description=f"استيقظت المدينة على خبر مأساوي.. عُثر على جثة {victim.mention} ملقاة في الساحة!\n\nكان دوره في الحياة: **[{game['roles'][victim]}]**.", color=0x2b2d31)
                        await ctx.send(embed=kill_embed)
                else:
                    await ctx.send("🤫 مر الليل بسلام غريب جداً.. لم يحدث أي هجوم واكتفت الأطراف بالمراقبة.")

                # إعادة فحص شروط الفوز بعد القتل الليلي
                mafia_count = sum(1 for p in game['alive'] if game['roles'][p] == "مافيا")
                innocent_count = len(game['alive']) - mafia_count
                if mafia_count == 0 or mafia_count >= innocent_count:
                    continue

                # 4. مرحلة التصويت والمحاكمة النهارية
                await ctx.send(f"\n⚖️ **بدأت الآن مرحلة المداولات والتصويت العلني!**\nتناقشوا في الشات ثم صوتوا عبر القائمة المنسدلة بالأسفل لإقصاء المشتبه به الأول.\n⌛ تنتهي المحاكمة بعد **45 ثانية**.")
                
                game['day_votes'] = {}
                vote_view = discord.ui.View(timeout=45.0)
                vote_view.add_item(DayVoteSelect(list(game['alive']), self, ctx.channel.id))
                
                vote_msg = await ctx.send("اضغط هنا للإدلاء بصوتك للمحاكمة 👇", view=vote_view)
                await asyncio.sleep(45)
                try: await vote_msg.delete()
                except discord.DiscordException: pass

                # حساب الأصوات النهارية
                if game['day_votes']:
                    vote_counts = Counter(game['day_votes'].values())
                    most_voted, top_votes = vote_counts.most_common(1)[0]
                    
                    # التحقق من عدم وجود تعادل في المركز الأول
                    all_top = [k for k, v in vote_counts.items() if v == top_votes]
                    
                    if len(all_top) > 1:
                        await ctx.send("⚖️ انقسمت أصوات أهل القرية بالتساوي! تعادلت الأدلة وأُغلقت القضية دون طرد أحد اليوم.")
                    else:
                        game['alive'].remove(most_voted)
                        eliminated_role = game['roles'][most_voted]
                        await ctx.send(f"🏛️ قررت المحكمة بناءً على تصويت الأغلبية نفي وإقصاء **{most_voted.mention}** خارج أسوار المدينة!\n\nأوراقه الثبوتية كشفت أنه كان: **[{eliminated_role}]**.")
                else:
                    await ctx.send("💤 خيم الصمت على أهل المدينة، ولم يجرؤ أحد على التصويت لتنتهي الجلسة القضائية بلا إقصاء.")

                round_num += 1

        finally:
            # تنظيف الروم عند الانتهاء أو الخروج لحماية البوت من التعليق
            self.active_games.pop(ctx.channel.id, None)

async def setup(bot):
    await bot.add_cog(MafiaCog(bot))