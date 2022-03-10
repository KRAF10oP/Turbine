import discord
from discord.ext import commands
from discord.ui import Button, View
import requests
from nekobot import NekoBot
api = NekoBot()

class memeView(View):

    def __init__(self, ctx):
        super().__init__(timeout=20)
        self.ctx = ctx

    @discord.ui.button(label='Next Meme', style=discord.ButtonStyle.green, custom_id='meme')
    async def meme_callback(self, button, interaction):
        if interaction.user != self.ctx.author:
            embeda = discord.Embed(
            description=f"Sorry, but this interaction can only be used by **{self.ctx.author.name}**.", color=0x3498DB)
            return await interaction.response.send_message(embed=embeda, ephemeral=True)
        r = requests.get('https://memes.blademaker.tv/api?lang=en')
        res = r.json()
        title = res["title"]
        image = res["image"]
        ups = res["ups"]

        memeEmbed = discord.Embed(title=title, color=discord.Color.blue())
        memeEmbed.set_image(url=image)
        memeEmbed.set_footer(text=f'👍 {ups}')

        await interaction.response.edit_message(embed=memeEmbed, view=self)
    
    @discord.ui.button(label='End Interaction', style=discord.ButtonStyle.danger, custom_id='end')
    async def end_callback(self, button, interaction):
        if interaction.user != self.ctx.author:
            embeda = discord.Embed(
            description=f"Sorry, but this interaction can only be used by **{self.ctx.author.name}**.", color=0x3498DB)
            return await interaction.response.send_message(embed=embeda, ephemeral=True)
        self.stop()
    



class Fun(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("Owner Only Cog has been loaded\n-------------------------")

    @commands.command(usage='meme')
    @commands.cooldown(1, 10, commands.BucketType.member)
    async def meme(self, ctx):
        view = memeView(ctx)
        r = requests.get('https://memes.blademaker.tv/api?lang=en')
        res = r.json()
        title = res["title"]
        image = res["image"]
        ups = res["ups"]

        memeEmbed = discord.Embed(title=f'{title}', color=discord.Color.blue())
        memeEmbed.set_image(url=image)
        memeEmbed.set_footer(text=f'👍 {ups}')

        msg = await ctx.send(embed=memeEmbed, view=view)

        await view.wait()
        m = [x for x in view.children if x.custom_id == 'meme'][0]
        e = [x for x in view.children if x.custom_id == 'end'][0]
        m.disabled = True
        e.disabled = True
        await msg.edit(view=view)
    
    @commands.command(usage='threats [member]')
    @commands.cooldown(1, 5, commands.BucketType.member)
    async def threats(self, ctx, member: discord.Member=None):
        if member is None:
            member = ctx.author

        avatar = member.display_avatar.replace(size=2048, format="png").url
        img = (api.threats(avatar))
        embed = discord.Embed(color=discord.Color.blue())
        embed.set_image(url=img.message)
        embed.set_footer(text=f'Requested by {ctx.author}')
        await ctx.send(embed=embed)
    
    @commands.command(usage='bauguette [member]')
    @commands.cooldown(1, 5, commands.BucketType.member)
    async def bauguette(self, ctx, member: discord.Member=None):
        if member is None:
            member = ctx.author

        avatar = member.display_avatar.replace(size=2048, format="png").url
        img = (api.baguette(avatar))
        embed = discord.Embed(color=discord.Color.blue())
        embed.set_image(url=img.message)
        embed.set_footer(text=f'Requested by {ctx.author}')
        await ctx.send(embed=embed)
    

    @commands.command(usage='cylde [member] [text]')
    @commands.cooldown(1, 5, commands.BucketType.member)
    async def clyde(self, ctx, *, text=None):
        if text is None:
            text = 'Turbine is OP'

        img = (api.clyde(f"{text}"))
        embed = discord.Embed(color=discord.Color.blue())
        embed.set_image(url=img.message)
        embed.set_footer(text=f'Requested by {ctx.author}') 
        await ctx.send(embed=embed)   

    @commands.command(usage='captcha [member]')
    @commands.cooldown(1, 5, commands.BucketType.member)
    async def captcha(self, ctx, member: discord.Member=None):
        if member is None:
            member = ctx.author

        avatar = member.display_avatar.replace(size=2048, format="png").url
        img = (api.captcha(avatar, f"{member.name}"))
        embed = discord.Embed(color=discord.Color.blue())
        embed.set_image(url=img.message)
        embed.set_footer(text=f'Requested by {ctx.author}')
        await ctx.send(embed=embed)
    
    @commands.command(usage='trash [member]')
    @commands.cooldown(1, 5, commands.BucketType.member)
    async def trash(self, ctx, member: discord.Member=None):
        if member is None:
            member = ctx.author

        avatar = member.display_avatar.replace(size=2048, format="png").url
        img = (api.trash(avatar))
        embed = discord.Embed(color=discord.Color.blue())
        embed.set_image(url=img.message)
        embed.set_footer(text=f'Requested by {ctx.author}')
        await ctx.send(embed=embed)
    
    @commands.command(usage='iphone [member]')
    @commands.cooldown(1, 5, commands.BucketType.member)
    async def iphone(self, ctx, member: discord.Member=None):
        if member is None:
            member = ctx.author

        avatar = member.display_avatar.replace(size=2048, format="png").url
        img = (api.iphonex(avatar))
        embed = discord.Embed(color=discord.Color.blue())
        embed.set_image(url=img.message)
        embed.set_footer(text=f'Requested by {ctx.author}')
        await ctx.send(embed=embed)
    
    @commands.command(usage='tweet [member] [text]')
    @commands.cooldown(1, 5, commands.BucketType.member)
    async def tweet(self, ctx, member: discord.Member=None, *, text='Turbine is OP'):
        if member is None:
            member = ctx.author

        img = (api.tweet(f"{member.name}", f"{text}"))
        embed = discord.Embed(color=discord.Color.blue())
        embed.set_image(url=img.message)
        embed.set_footer(text=f'Requested by {ctx.author}')
        await ctx.send(embed=embed)
    
    @commands.command(usage='awooify [member]')
    @commands.cooldown(1, 5, commands.BucketType.member)
    async def awooify(self, ctx, member: discord.Member=None):
        if member is None:
            member = ctx.author

        avatar = member.display_avatar.replace(size=2048, format="png").url
        img = (api.awooify(avatar))
        embed = discord.Embed(color=discord.Color.blue())
        embed.set_image(url=img.message)
        embed.set_footer(text=f'Requested by {ctx.author}')
        await ctx.send(embed=embed)
    
    @commands.command(usage='deepfry [member]')
    @commands.cooldown(1, 5, commands.BucketType.member)
    async def deepfry(self, ctx, member: discord.Member=None):
        if member is None:
            member = ctx.author

        avatar = member.display_avatar.replace(size=2048, format="png").url
        img = (api.deepfry(avatar))
        embed = discord.Embed(color=discord.Color.blue())
        embed.set_image(url=img.message)
        embed.set_footer(text=f'Requested by {ctx.author}')
        await ctx.send(embed=embed)
    
    @commands.command(usage='stickbug [member]')
    @commands.cooldown(1, 5, commands.BucketType.member)
    async def stickbug(self, ctx, member: discord.Member=None):
        if member is None:
            member = ctx.author

        avatar = member.display_avatar.replace(size=2048, format="png").url
        img = (api.stickbug(avatar))
        embed = discord.Embed(color=discord.Color.blue())
        embed.set_image(url=img.message)
        embed.set_footer(text=f'Requested by {ctx.author}')
        await ctx.send(embed=embed)

    @commands.command(usage='magik [member]')
    @commands.cooldown(1, 5, commands.BucketType.member)
    async def magik(self, ctx, member: discord.Member=None):
        if member is None:
            member = ctx.author

        m = await ctx.send(" <a:Loadbounce:950647698640478218> Processing Command, Please Wait…")
        async with ctx.channel.typing():

           avatar = member.display_avatar.replace(size=2048, format="png").url
           embed = discord.Embed(color=discord.Color.blue())
           img = (api.magik(avatar))
           embed.set_image(url=img.message)
           embed.set_footer(text=f'Requested by {ctx.author}')
           return await m.edit(embed=embed)


    api.close()

def setup(bot):
    bot.add_cog(Fun(bot))
