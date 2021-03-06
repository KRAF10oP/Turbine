import discord
from discord.ext import commands
import platform
import time
import datetime
from discord.ui import Button, View
import calendar
import psutil
from collections import Counter
from datetime import datetime, timedelta, timezone
from utils.git import format_relative, truncate_string, format_relative
import pygit2
import itertools
import random

class Utilities(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("Utilities Cog has been loaded\n-------------------------")
    global start_time
    start_time = int(time.time())

    # @commands.command(aliases=['announce'], usage='embed [channel]')
    # async def embed(self, ctx, channel: discord.TextChannel=None):
    #     """Make a beautiful Embed for your Channels"""
    #     embed = discord.Embed(color=discord.Colour.blue(), description='*Use buttons to Customize this embed.*')
    #     title = Button(label='Set Title', style=discord.ButtonStyle.blurple)
    #     content = Button(label='Set Content', style=discord.ButtonStyle.blurple)
    #     description = Button(label='Set Description', style=discord.ButtonStyle.blurple)
    #     image = Button(label='Set Image', style=discord.ButtonStyle.blurple)
    #     thumbnail = Button(label='Set Thumbnail', style=discord.ButtonStyle.blurple)
    #     color = Button(label='Set Color', style=discord.ButtonStyle.blurple)
    #     send = Button(label='Send', style=discord.ButtonStyle.green)
    #     abort = Button(label='Abort', style=discord.ButtonStyle.danger)

        # aa = View()
        # aa.add_item(content)
        # aa.add_item(title)
        # aa.add_item(description)
        # aa.add_item(image)
        # aa.add_item(thumbnail)
        # aa.add_item(color)
        # aa.add_item(abort)
        # aa.add_item(send)
        # await ctx.send(embed=embed, view=aa)
    
    @commands.command(aliases=["av"], usage='avatar [member]')
    async def avatar(self, ctx, member: discord.Member=None):
        if member == None:
            member = ctx.author
        embed = discord.Embed(color=discord.Color.blue(), description=f'[`PNG`]({member.display_avatar.replace(static_format="png").url}) | [`JPG`]({member.display_avatar.replace(static_format="jpg").url})')
        embed.set_author(name=member.name, icon_url=member.display_avatar.url)
        embed.set_image(url=member.display_avatar.url)
        embed.set_footer(text=f'Requested By {ctx.author}', icon_url=ctx.author.display_avatar.url)

        await ctx.send(embed=embed)
    
    @commands.command(name='invite', aliases=['inv'], brief='-invite')
    async def invite(self, ctx):
        """
        Invite ME : )
        """
        button = Button(label='Invite Me', style=discord.ButtonStyle.link, url='https://discord.com/api/oauth2/authorize?client_id=896631647104024616&permissions=21175985838&scope=bot%20applications.commands' )
        view = View()
        view.add_item(button)
        embed = discord.Embed(description='Wanna Invite me to your Server ?', color=0x3498DB)
        embed.set_author(name='Invite Me', icon_url=self.bot.user.display_avatar)

        await ctx.send(embed=embed, view=view)
        
    # @commands.command(name="userinfo", aliases=["memberinfo", "ui", "mi"], usage='userinfo <user>', brief='-userinfo @anshuman..!!')
    # @commands.bot_has_permissions(embed_links=True)
    # @commands.cooldown(1, 5, commands.BucketType.member)
    # async def user_info(self, ctx: commands.Context, *, member: discord.Member = None):
    #     """To get the info regarding the mentioned user"""
    #     target = member or ctx.author
    #     roles = list(target.roles)
    #     embed = discord.Embed(
    #         title="User information",
    #         colour=target.colour,
    #         timestamp=datetime.datetime.utcnow(),
    #     )

    #     embed.set_thumbnail(url=target.display_avatar.url)
    #     embed.set_footer(text=f"ID: {target.id}")
        # fields = [
        #     ("Name", str(target), True),
        #     ("Created at", f"<t:{int(target.created_at.timestamp())}>", True),
        #     ("Status", f"{str(target.status).title()}", True),
        #     (
        #         "Activity",
        #         f"{str(target.activity.type).split('.')[-1].title() if target.activity else 'No Activity'} {target.activity.name if target.activity else ''}",
        #         True,
        #     ),
        #     ("Joined at", f"<t:{int(target.joined_at.timestamp())}>", True),
        #     ("Boosted", bool(target.premium_since), True),
        #     ("Bot?", target.bot, True),
        #     ("Nickname", target.display_name, True),
        #     (f"Top Role", target.top_role.mention, True),
        # ]
        # perms = []
        # for name, value, inline in fields:
        #     embed.add_field(name=name, value=value, inline=inline)
        # if target.guild_permissions.administrator:
        #     perms.append("Administrator")
        # if (
        #     target.guild_permissions.kick_members
        #     and target.guild_permissions.ban_members
        #     and target.guild_permissions.manage_messages
        # ):
        #     perms.append("Server Moderator")
        # if target.guild_permissions.manage_guild:
        #     perms.append("Server Manager")
        # if target.guild_permissions.manage_roles:
        #     perms.append("Role Manager")
        # embed.description = f"Key perms: {', '.join(perms if perms else ['NA'])}"
        # if target.banner:
        #     embed.set_image(url=target.banner.url)
        # await ctx.reply(embed=embed)
    
    @commands.command(name='whois', usage='whois [member]', brief='-whois @user', aliases=['ui', 'userinfo'])
    async def whois(self, ctx, member: discord.Member=None):
        member = member or ctx.author
        perms = []
        if member.guild_permissions.administrator:
            perms.append('Administrator')
        if member.guild_permissions.ban_members:
            perms.append('Ban Members')
        if member.guild_permissions.kick_members:
            perms.append('Kick Members')
        if member.guild_permissions.manage_channels:
            perms.append('Manage Channels')
        if member.guild_permissions.manage_emojis:
            perms.append('Manage Emojis')
        if member.guild_permissions.manage_events:
            perms.append('Manage Events')
        if member.guild_permissions.manage_messages:
            perms.append('Manage Messages')
        if member.guild_permissions.manage_nicknames:
            perms.append('Manage Nicknames')
        if member.guild_permissions.manage_permissions:
            perms.append('Manage Permissions')
        if member.guild_permissions.manage_roles:
            perms.append('Manage Roles')
        if member.guild_permissions.manage_threads:
            perms.append('Manage Threads')
        if member.guild_permissions.manage_webhooks:
            perms.append('Manage Webhooks')
        if member.guild_permissions.mention_everyone:
            perms.append('Mention Everyone')

        if len(perms):
            perms = sorted(perms)
        else:
            perms.append('No Permissions')

        if member.color.value != 0:
            col = member.color
        else:
            col = 0x3498DB

        emb = discord.Embed(color=col)
        if member.bot:
            mem = '<a:tick:940816615237357608> Yes'
        else:
            mem = '<a:cross1:941287490986315776> No'
        
        ti = calendar.timegm(time.strptime(member.created_at.strftime("%b %d, %Y @ %H:%M:%S UTC"), '%b %d, %Y @ %H:%M:%S UTC'))
        sj = calendar.timegm(time.strptime(member.joined_at.strftime("%b %d, %Y @ %H:%M:%S UTC"), '%b %d, %Y @ %H:%M:%S UTC'))

        if member.nick:
            nick = member.nick
        else:
            nick = 'No Nickname'
        
        roles = []
        for role in member.roles:
            roles.append(role.mention)
        
        roles = sorted(roles)
        
        if len([role for role in member.roles])-1 == 0:
            memrole = 'No Roles'
        else:
            memrole = ", ".join(roles[1:])

        if member.top_role.name == '@everyone':
            hrole = 'No Role'
        else:
            hrole = member.top_role.mention
        
        emb.set_thumbnail(url=member.display_avatar.url)
        emb.set_author(name=f'{member}\'s Information', icon_url=member.display_avatar.url)

        try:
            banner_user = await self.bot.fetch_user(member.id)
            banner_url = banner_user.banner.url
            emb.set_image(url=banner_url)
        except:
            pass
        emb.set_footer(text=f'Requested By {ctx.author}', icon_url=ctx.author.display_avatar.url)
        
        if member.id == 548163406537162782:
            ach = "Quotient Bot Developer"
        elif member.id == 380697024120487939:
            ach = "Flantic Bot Developer"
        elif member.id == 939887303403405402:
            ach = "My Developer"
        elif member.id == 741614468546560092:
            ach = "Parrot Bot Developer"
        elif member.id == ctx.guild.owner_id:
            ach = 'Server Owner'
        elif member.guild_permissions.administrator:
            ach = 'Server Admin'
        else:
            ach = 'No Acknowledgements'

        emb.add_field(name='__**General Information**__', value=f'**Name :** {member.name}\n**ID** : {member.id}\n**Username :** {member}\n**Mention :** {member.mention}\n**Nickname :** {nick}\n**Status :** {str(member.status).title()}\n**Join Position :** {sum(m.joined_at < member.joined_at for m in ctx.guild.members if m.joined_at is not None)}/{len(ctx.guild.members)}\n**Account Created :** <t:{ti}>\n**Server Joined :** <t:{sj}:R>\n**Is Bot ? :** {mem}\n\n')
        if len([role for role in member.roles])-1 != 0 and len([role for role in member.roles])-1 <= 25:
            emb.add_field(name='**__Role Information__**', value=f'**Highest Role :** {hrole}\n**Roles ({len([role for role in member.roles])-1}) :** {memrole}', inline=False)
        elif len([role for role in member.roles])-1 != 0 and len([role for role in member.roles])-1 > 25:
            emb.add_field(name='**__Role Information__**', value=f'**Highest Role :** {hrole}\n**Roles ({len([role for role in member.roles])-1}) :** Too Many Roles to Display.', inline=False)
        emb.add_field(name='**__Permissions__**', value=f'{", ".join(perms)}', inline=False)
        emb.add_field(name='**__Acknowledgements__**', value=ach, inline=False)
        await ctx.send(embed=emb)

    @commands.command(name='membercount', aliases=['mc'], usage='$membercount')
    async def mc(self, ctx):
        """
        Get the MemberCount of the Server
        """
        embed = discord.Embed(title='Member Count', description=f'**<:partner:941603900685975642> Total - {len(ctx.guild.members)}\n<:human:941603080082952202> Humans - {len([member for member in ctx.guild.members if not member.bot])}\n<:blurple_bot:941601824379645953> Bots - {len([member for member in ctx.guild.members if member.bot])}**', color=0x3498DB)
        await ctx.send(embed=embed)
    
    @commands.command(name="uptime")
    async def uptime(self, ctx):
        embed = discord.Embed(color=discord.Color.blue(), description=f'I am Online from : **<t:{start_time}:R>**')

        await ctx.send(embed=embed)
    
    @commands.command(name="ping", aliases=["latency", "speed"], usage='ping', brief='-ping')
    @commands.cooldown(1, 5, commands.BucketType.member)
    async def ping(self, ctx: commands.Context):
        """Shows the Latency of the bot"""
        start = time.time()
        message = await ctx.reply("Pinging...")
        end = time.time()
        await message.edit(
            content=f"Pong! latency: {self.bot.latency*1000:,.0f} ms. Response time: {(end-start)*1000:,.0f} ms."
        )   
    @commands.command(name="prefix", aliases=["pre"], usage='prefix [newprefix]', brief='-prefix !')
    @commands.has_permissions(administrator=True)
    @commands.cooldown(1, 5, commands.BucketType.guild)
    async def prefix(self, ctx, *, prefix=None):
        """To check the current prefix or change it to a new one"""
        if(prefix == None):
            data = await self.bot.db.fetchrow('SELECT * FROM prefix WHERE guild_id = $1', ctx.guild.id)
            if not data:
                prefix = "-"
                await self.bot.db.execute("INSERT INTO prefix (guild_id, prefix) VALUES ($1,$2)", ctx.guild.id, '-')
            else:
                prefix = data["prefix"]
            await ctx.send(f'My prefix for this server is `{prefix}`\nYou can start with `{prefix}help`')
        else:        
            record = await self.bot.db.fetchrow("SELECT * FROM prefix WHERE guild_id = $1", ctx.guild.id)
            if not record:
                await self.bot.db.execute("INSERT INTO prefix (guild_id, prefix) VALUES ($1,$2)", ctx.guild.id, prefix)
                return await ctx.send(f"The guild prefix has been set to `{prefix}`. Use `{prefix}prefix [prefix]` to change it again!")
                
            await self.bot.db.execute("UPDATE prefix SET prefix = $2 WHERE guild_id = $1", ctx.guild.id, prefix)
            await ctx.send(f"The guild prefix has been set to `{prefix}`. Use `{prefix}prefix [prefix]` to change it again!")



    
    @prefix.error
    async def prefix_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            embed = discord.Embed(description='**<a:cross1:941287490986315776> You lack Administrator Permissions to use this command.**', color=0xfe4d49)
            await ctx.send(embed=embed)


    def format_commit(self, commit):  # source: R danny
        short, _, _ = commit.message.partition("\n")
        short_sha2 = commit.hex[0:6]
        commit_tz = timezone(timedelta(minutes=commit.commit_time_offset))
        commit_time = datetime.fromtimestamp(commit.commit_time).astimezone(commit_tz)

        # [`hash`](url) message (offset)
        offset = format_relative(commit_time.astimezone(timezone.utc))
        return f"[`{short_sha2}`](https://github.com/Vader-Op/PyBot/commit/{commit.hex}) {truncate_string(short,40)} ({offset})"

    def get_last_commits(self, count=3):
        repo = pygit2.Repository(".git")
        commits = list(itertools.islice(repo.walk(repo.head.target, pygit2.GIT_SORT_TOPOLOGICAL), count))
        return "\n".join(self.format_commit(c) for c in commits)
    
    @commands.command(name="stats", aliases=["statistics", "st", "info"], usage='stats', brief='-stats')
    async def stats(self, ctx):
        """Shows some usefull information about PyBot"""
        pythonVersion = platform.python_version()
        dpyVersion = discord.__version__
        serverCount = len(self.bot.guilds)
        memberCount = sum(g.member_count for g in self.bot.guilds if g.member_count != None)
        # revision = self.get_last_commits()
        t1 = time.perf_counter()
        await self.bot.db.fetchval("SELECT 1;")
        t2 = time.perf_counter() - t1
        db_latency = f"{t2*1000:.2f} ms"

        total_memory = psutil.virtual_memory().total >> 20
        used_memory = psutil.virtual_memory().used >> 20
        cpu_used = str(psutil.cpu_percent())

        msgs_seen = self.bot.seen_messages
        
        total_members = sum(g.member_count for g in self.bot.guilds if g.member_count != None)
        cached_members = len(self.bot.users)

        chnl_count = Counter(map(lambda ch: ch.type, self.bot.get_all_channels()))

        b = Button(label='Invite Me', style=discord.ButtonStyle.link, url='https://discord.com/api/oauth2/authorize?client_id=896631647104024616&permissions=21175985838&scope=bot%20applications.commands')
        view = View()
        view.add_item(b)

        embed = discord.Embed(colour=0x2f3136)

        # start_time = calendar.timegm(time.strptime(start_time.strftime("%Y-%m-%d %H:%M:%S+00:00"), '%Y-%m-%d %H:%M:%S+00:00'))

        embed.add_field(name='Servers', value=f'{serverCount} Total\n{len(self.bot.shards)} Shards')
        embed.add_field(name='Uptime', value=f'<t:{start_time}:R>\n{self.bot.seen_messages} Messages Seen')
        embed.add_field(name='Members', value=f'{total_members} - Total\n{cached_members} - Cached')
        embed.add_field(
            name="Channels",
            value=f"{chnl_count[discord.ChannelType.text]:,} text\n{chnl_count[discord.ChannelType.voice]:,} voice")
        embed.add_field(name="System", value=f"**RAM**: {used_memory}/{total_memory} MB\n**CPU:** {cpu_used}% used."),
        embed.add_field(name='Version', value=f'Python - {pythonVersion}\nDiscordpy - {dpyVersion}')
        embed.add_field(
            name="Stats",
            value=f"Ping: {round(self.bot.latency * 1000, 2)}ms\nDataBase: {db_latency}")
        # embed.add_field(name="System", value=f"**RAM**: {used_memory}/{total_memory} MB\n**CPU:** {cpu_used}% used.", inline=False),
        # embed.add_field(name='Version', value=f'Python - {pythonVersion}\nDiscordPY - {dpyVersion}', inline=False)
        jash = await self.bot.fetch_user(749559849460826112)
        anshuman = await self.bot.fetch_user(939887303403405402)
        if anshuman in ctx.guild.members:
            a = f'{anshuman.mention}'
        else:
            a = f'{anshuman}'
        embed.add_field(name='Bot Developer:', value=f"{a}")
        embed.set_author(name=f"{self.bot.user.name} Stats", icon_url=self.bot.user.display_avatar.url)
        # embed.add_field(name='Latest Changes', value=revision, inline=False)
        
        embed.set_footer(text='Made with ???? by Anshuman..!!', icon_url='https://cdn.discordapp.com/avatars/939887303403405402/0ac574b14a954715efe8cd81196cb042.png')

        await ctx.send(embed=embed, view=view)

    
    # @commands.command(name="roleinfo", aliases=["ri"], usage='roleinfo <role>', brief='-roleinfo @owner')
    # @commands.bot_has_permissions(embed_links=True)
    # @commands.cooldown(1, 5, commands.BucketType.member)
    # async def roleinfo(self, ctx: commands.Context, *, role: discord.Role):
    #     """To get the info regarding the mentioned role"""
    #     embed = discord.Embed(
    #         title=f"Role Information: {role.name}",
    #         description=f"ID: `{role.id}`",
    #         color=role.color,
    #         timestamp=datetime.datetime.utcnow(),
    #     )
    #     data = [
    #         ("Created At", f"<t:{int(role.created_at.timestamp())}>", True),
    #         ("Is Hoisted?", role.hoist, True),
        #     ("Position", role.position, True),
        #     ("Managed", role.managed, True),
        #     ("Mentionalble?", role.mentionable, True),
        #     ("Members", len(role.members), True),
        # #     ("Mention", role.mention, True),
        #     ("Is Boost role?", role.is_premium_subscriber(), True),
        #     ("Is Bot role?", role.is_bot_managed(), True),
        # ]
        # for name, value, inline in data:
        #     embed.add_field(name=name, value=value, inline=inline)
        # perms = []
        # if role.permissions.administrator:
        #     perms.append("Administrator")
        # if (
        #     role.permissions.kick_members
        #     and role.permissions.ban_members
        #     and role.permissions.manage_messages
        # ):
        #     perms.append("Server Moderator")
        # if role.permissions.manage_guild:
        #     perms.append("Server Manager")
        # if role.permissions.manage_roles:
        #     perms.append("Role Manager")
        # embed.description = f"Key perms: {', '.join(perms if perms else ['NA'])}"
        # embed.set_footer(text=f"ID: {role.id}")
        # await ctx.reply(embed=embed)
        
    # @commands.command(name="channelstats", aliases=["channelinfo", "cs", "ci"], usage='channelstats [channel]', brief='-channelstats #general')
    # @commands.bot_has_permissions(embed_links=True)
    # @commands.cooldown(1, 5, commands.BucketType.member)
    # async def channel_info(
    #     self,
    #     ctx: commands.Context,
    #     *,
    #     channel: typing.Union[
    #         discord.TextChannel,
    #         discord.VoiceChannel,
    #         discord.CategoryChannel,
    #         discord.StageChannel,
    #     ] = None,
    # ):
    #     channel = channel or ctx.channel
    #     embed = discord.Embed(title=f"Stats for **{channel.name}**", description=f"{'Category: {}'.format(channel.category.name) if channel.category else 'This channel is not in a category'}", color=random.choice(self.bot.color_list))
    #     embed.add_field(name="Channel Guild", value=ctx.guild.name, inline=False)
    #     embed.add_field(name="Channel Id", value=channel.id, inline=False)
    #     embed.add_field(name="Channel Topic", value=f"{channel.topic if channel.topic else 'No topic.'}", inline=False)
    #     embed.add_field(name="Channel Position", value=channel.position, inline=False)
    #     embed.add_field(name="Channel Slowmode Delay", value=channel.slowmode_delay, inline=False)
        # embed.add_field(name="Channel is nsfw?", value=channel.is_nsfw(), inline=False)
        # embed.add_field(name="Channel is news?", value=channel.is_news(), inline=False)
        # embed.add_field(name="Channel Creation Time", value=channel.created_at, inline=False)
        # embed.add_field(name="Channel Permissions Synced", value=channel.permissions_synced, inline=False)
        # embed.add_field(name="Channel Hash", value=hash(channel), inline=False)
        # await ctx.send(embed=embed)
    
    # @commands.command(name="serverinfo", aliases=["guildinfo", "si", "gi"], usage='serverinfo', brief='-serverinfo')
    # @commands.bot_has_permissions(embed_links=True)
    # @commands.cooldown(1, 5, commands.BucketType.member)
    # async def server_info(self, ctx: commands.Context):
    #     """
    #     Get the basic stats about the server
    #     """
    #     guild = ctx.guild
    #     embed = discord.Embed(
    #         title=f"Server Info: {ctx.guild.name}",
    #         colour=ctx.guild.owner.colour,
        #     timestamp=datetime.datetime.utcnow(),
        # )

        # embed.set_thumbnail(url=ctx.guild.icon.url)
        # embed.set_footer(text=f"ID: {ctx.guild.id}")
        # statuses = [
        #     len(list(filter(lambda m: str(m.status) == "online", ctx.guild.members))),
        #     len(list(filter(lambda m: str(m.status) == "idle", ctx.guild.members))),
        #     len(list(filter(lambda m: str(m.status) == "dnd", ctx.guild.members))),
        #     len(list(filter(lambda m: str(m.status) == "offline", ctx.guild.members))),
        # ]

        # fields = [
        #     ("Owner", ctx.guild.owner, True),
        #     ("Region", str(ctx.guild.region).capitalize(), True),
        #     ("Created at", f"<t:{int(ctx.guild.created_at.timestamp())}>", True),
        #     (
            #     "Total Members",
            #     f"Members: {len(ctx.guild.members)}\nHumans: {len(list(filter(lambda m: not m.bot, ctx.guild.members)))}\nBots: {len(list(filter(lambda m: m.bot, ctx.guild.members)))} ",
            #     True,
            # ),
            # (
            #     "Total channels",
            #     f"Categories: {len(ctx.guild.categories)}\nText: {len(ctx.guild.text_channels)}\nVoice:{len(ctx.guild.voice_channels)}",
            #     True,
            # ),
            # (
            #     "General",
            #     f"Roles: {len(ctx.guild.roles)}\nEmojis: {len(ctx.guild.emojis)}\nBoost Level: {ctx.guild.premium_tier}",
            #     True,
            # ),
            # (
            #     "Statuses",
            #     f":green_circle: {statuses[0]}\n:yellow_circle: {statuses[1]}\n:red_circle: {statuses[2]}\n:black_circle: {statuses[3]} [Blame Discord]",
        #         True,
        #     ),
        # ]

        # for name, value, inline in fields:
        #     embed.add_field(name=name, value=value, inline=inline)

        # info = []
        # features = set(ctx.guild.features)
        # all_features = {
        #     "PARTNERED": "Partnered",
        #     "VERIFIED": "Verified",
        #     "DISCOVERABLE": "Server Discovery",
        #     "COMMUNITY": "Community Server",
        #     "FEATURABLE": "Featured",
        #     "WELCOME_SCREEN_ENABLED": "Welcome Screen",
        #     "INVITE_SPLASH": "Invite Splash",
        #     "VIP_REGIONS": "VIP Voice Servers",
        #     "VANITY_URL": "Vanity Invite",
        #     "COMMERCE": "Commerce",
        #     "LURKABLE": "Lurkable",
        #     "NEWS": "News Channels",
        #     "ANIMATED_ICON": "Animated Icon",
        #     "BANNER": "Banner",
        # }

        # for feature, label in all_features.items():
        #     if feature in features:
        #         info.append(f":ballot_box_with_check: {label}")

        # if info:
        #     embed.add_field(name="Features", value="\n".join(info))

        # if guild.premium_tier != 0:
        #     boosts = (
        #         f"Level {guild.premium_tier}\n{guild.premium_subscription_count} boosts"
        #     )
        #     last_boost = max(
        #         guild.members, key=lambda m: m.premium_since or guild.created_at
        #     )
        #     if last_boost.premium_since is not None:
        #         boosts = f"{boosts}\nLast Boost: {last_boost} ({commands.format_relative(last_boost.premium_since)})"
        #     embed.add_field(name="Boosts", value=boosts, inline=True)
        # else:
        #     embed.add_field(name="Boosts", value="Level 0", inline=True)

        

        # if ctx.guild.me.guild_permissions.ban_members:
        #     embed.add_field(
        #         name="Banned Members",
        #         value=f"{len(await ctx.guild.bans())}",
        #         inline=True,
        #     )
        # if ctx.guild.me.guild_permissions.manage_guild:
    #         embed.add_field(
    #             name="Invites", value=f"{len(await ctx.guild.invites())}", inline=True
    #         )

    #     if ctx.guild.banner:
    #         embed.set_image(url=ctx.guild.banner.url)

    #     await ctx.send(embed=embed)
        
    # @commands.command(name="emojiinfo", aliases=["emoji", "ei", "emo"],  usage='emojiinfo <emoji>', brief='-emojiinfo ????')
    # @commands.bot_has_permissions(embed_links=True)
    # @commands.cooldown(1, 5, commands.BucketType.member)
    # async def emojiinfo(self, ctx: commands.Context, *, emoji: discord.Emoji):
    #     """To get the info regarding the server emoji"""
    #     em = discord.Embed(
    #         title="Emoji Info",
    #         description=f"??? [Download the emoji]({emoji.url})\n??? Emoji ID: `{emoji.id}`",
    #         timestamp=datetime.datetime.utcnow(),
    #         color=ctx.author.color,
        # )
        # data = [
        #     ("Name", emoji.name, True),
        #     ("Is Animated?", emoji.animated, True),
        #     ("Created At", f"<t:{int(emoji.created_at.timestamp())}>", True),
        #     ("Server Owned", emoji.guild.name, True),
        #     ("Server ID", emoji.guild_id, True),
        #     ("Created By", emoji.user if emoji.user else "User Not Found", True),
        #     ("Available?", emoji.available, True),
        #     ("Managed by Twitch?", emoji.managed, True),
        #     ("Require Colons?", emoji.require_colons, True),
        # ]
        # em.set_footer(text=f"{ctx.author}")
        # em.set_thumbnail(url=emoji.url)
        # for name, value, inline in data:
        #     em.add_field(name=name, value=f"{value}", inline=inline)
        # await ctx.reply(embed=em)

    @commands.command(usage='snipe [channel]', brief=["-snipe #general"])
    async def snipe(self, ctx, channel: discord.TextChannel=None):
        """Get a Message Deleted by Someone"""
        channel = channel or ctx.channel
        data = await self.bot.db.fetchrow('SELECT * FROM snipe WHERE channel_id = $1', channel.id)
        if not data:
            embed = discord.Embed(description=f'<a:cross1:941287490986315776> Nothing to snipe in {channel.mention}', color=0xfe4d49)
            return await ctx.send(embed=embed)
        ch = ctx.guild.get_channel(data["channel_id"])
        embed = discord.Embed(description=f'Message sent by **{data["author"]}** was deleted in **{ch.name}**\n<t:{data["time"]}:R>', color=discord.Color.blue(), timestamp=datetime.fromtimestamp(data["time"]))
        embed.add_field(name='**__Message Content__**', value=data["content"])
        embed.set_footer(text='Deleted')

        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Utilities(bot))
