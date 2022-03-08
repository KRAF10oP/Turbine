import re
from discord.ui import Button, View
import discord
import lavalink
from discord.ext import commands
import math
import asyncio
from utils.util import Pag

url_rx = re.compile(r'https?://(?:www\.)?.+')

class LavalinkVoiceClient(discord.VoiceClient):
    """
    This is the preferred way to handle external voice sending
    This client will be created via a cls in the connect method of the channel
    see the following documentation:
    https://discordpy.readthedocs.io/en/latest/api.html#voiceprotocol
    """

    def __init__(self, client: discord.Client, channel: discord.abc.Connectable):
        self.client = client
        self.channel = channel
        # ensure there exists a client already
        if hasattr(self.client, 'lavalink'):
            self.lavalink = self.client.lavalink
        else:
            self.client.lavalink = lavalink.Client(client.user.id)
            self.client.lavalink.add_node(
                    'nyc1.koalahost.xyz',
                    9004,
                    'youshallnotpass',
                    'us',
                    'main')
            self.lavalink = self.client.lavalink

    async def on_voice_server_update(self, data):
        # the data needs to be transformed before being handed down to
        # voice_update_handler
        lavalink_data = {
                't': 'VOICE_SERVER_UPDATE',
                'd': data
                }
        await self.lavalink.voice_update_handler(lavalink_data)

    async def on_voice_state_update(self, data):
        # the data needs to be transformed before being handed down to
        # voice_update_handler
        lavalink_data = {
                't': 'VOICE_STATE_UPDATE',
                'd': data
                }
        await self.lavalink.voice_update_handler(lavalink_data)

    async def connect(self, *, timeout: float, reconnect: bool) -> None:
        """
        Connect the bot to the voice channel and create a player_manager
        if it doesn't exist yet.
        """
        # ensure there is a player_manager when creating a new voice_client
        self.lavalink.player_manager.create(guild_id=self.channel.guild.id)
        await self.channel.guild.change_voice_state(channel=self.channel, self_deaf=True)


    async def disconnect(self, *, force: bool) -> None:
        """
        Handles the disconnect.
        Cleans up running player and leaves the voice client.
        """
        player = self.lavalink.player_manager.get(self.channel.guild.id)

        # no need to disconnect if we are not connected
        if not force and not player.is_connected:
            return

        # None means disconnect
        await self.channel.guild.change_voice_state(channel=None)

        # update the channel_id of the player to None
        # this must be done because the on_voice_state_update that
        # would set channel_id to None doesn't get dispatched after the 
        # disconnect
        player.channel_id = None
        self.cleanup()

class MyView(View):
    @discord.ui.button(label="Skip", style=discord.ButtonStyle.secondary)
    async def button_callback(self, button, interaction):
        player = self.bot.lavalink.player_manager.get(interaction.guild.id)

        if not player.is_connected:
            # We can't disconnect, if we're not connected.
            return await interaction.response.send_message('I\'m not connected to any VC.')

        if not interaction.user.voice or (player.is_connected and interaction.user.voice.channel.id != int(player.channel_id)):
            # Abuse prevention. Users not in voice channels, or not in the same voice channel as the bot
            # may not disconnect the bot.
            return await interaction.response.send_message('You\'re not in my voicechannel!')
        
        # await interaction.message.add_reaction('<a:tick:940816615237357608>')

        await player.skip()
        
        await interaction.reponse.send_message('*⃣ | Skipped !')

class Music(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.__class__.__name__} Cog has been loaded\n-------------------------")

        if not hasattr(self, 'lavalink'):  # This ensures the client isn't overwritten during cog reloads.
            self.bot.lavalink = lavalink.Client(self.bot.user.id)
            self.bot.lavalink.add_node('paid1.cattohost.xyz', 26883, 'youshallnotpass', 'eu', 'main')  # Host, Port, Password, Region, Name

        lavalink.add_event_hook(self.track_hook)

    def cog_unload(self):
        """ Cog unload handler. This removes any event hooks that were registered. """
        self.bot.lavalink._event_hooks.clear()

    async def cog_before_invoke(self, ctx):
        """ Command before-invoke handler. """
        guild_check = ctx.guild is not None
        #  This is essentially the same as `@commands.guild_only()`
        #  except it saves us repeating ourselves (and also a few lines).

        if guild_check:
            await self.ensure_voice(ctx)
            #  Ensure that the bot and command author share a mutual voicechannel.

        return guild_check

    async def cog_command_error(self, ctx, error):
        if isinstance(error, commands.CommandInvokeError):
            await ctx.send(error.original)
            # The above handles errors thrown in this cog and shows them to the user.
            # This shouldn't be a problem as the only errors thrown in this cog are from `ensure_voice`
            # which contain a reason string, such as "Join a voicechannel" etc. You can modify the above
            # if you want to do things differently.

    async def ensure_voice(self, ctx):
        """ This check ensures that the bot and command author are in the same voicechannel. """
        player = self.bot.lavalink.player_manager.create(ctx.guild.id)
        # Create returns a player if one exists, otherwise creates.
        # This line is important because it ensures that a player always exists for a guild.

        # Most people might consider this a waste of resources for guilds that aren't playing, but this is
        # the easiest and simplest way of ensuring players are created.

        # These are commands that require the bot to join a voicechannel (i.e. initiating playback).
        # Commands such as volume/skip etc don't require the bot to be in a voicechannel so don't need listing here.
        should_connect = ctx.command.name in ('play', 'join', 'stop', 'disconnect')

        if not ctx.author.voice or not ctx.author.voice.channel:
            # Our cog_command_error handler catches this and sends it to the voicechannel.
            # Exceptions allow us to "short-circuit" command invocation via checks so the
            # execution state of the command goes no further.
            raise commands.CommandInvokeError('Join a voicechannel first.')

        if not player.is_connected:
            if not should_connect:
                raise commands.CommandInvokeError('Not connected.')

            permissions = ctx.author.voice.channel.permissions_for(ctx.me)

            if not permissions.connect or not permissions.speak:  # Check user limit too?
                raise commands.CommandInvokeError('I need the `CONNECT` and `SPEAK` permissions.')

            player.store('channel', ctx.channel.id)
            await ctx.author.voice.channel.connect(cls=LavalinkVoiceClient)
        else:
            if int(player.channel_id) != ctx.author.voice.channel.id:
                raise commands.CommandInvokeError('You need to be in my voicechannel.')

    async def track_hook(self, event):
        if isinstance(event, lavalink.events.QueueEndEvent):
            # When this track_hook receives a "QueueEndEvent" from lavalink.py
            # it indicates that there are no tracks left in the player's queue.
            # To save on resources, we can tell the bot to disconnect from the voicechannel.
            guild_id = int(event.player.guild_id)
            guild = self.bot.get_guild(guild_id)

        
    # async def trackStart(self, event):
    #     if isinstance(event, lavalink.events.TrackStartEvent):

    #         guild_id = int(event.player.guild_id)
    #         guild = self.bot.get_guild(guild_id)
    #         player = self.bot.lavalink.player_manager.get(guild.id)
            # channel = player.channel
            # print(channel)
            # seconds=(player.current.duration/1000)%60
            # minutes=(player.current.duration/(1000*60))%60
            # hours=(player.current.duration/(1000*60*60))%24
            # if int(hours) == 0:
            #     time = f'{int(minutes)}:{int(seconds)}'
            # else:
            #     time = f'{int(hours)}:{int(minutes)}:{int(seconds)}'

            # embed = discord.Embed(color=discord.Color.blue(), description=f'[{player.current.title}]({player.current.uri})')
            # embed.set_author(name='Now Playing', url=self.bot.display_avatar.url)
            # requester = await self.bot.fetch_user(player.current.requester)
            # embed.add_field(name='**Requested By**', value=f'`{requester.name}`')
            # embed.add_field(name='**Duration**', value=f'`{time}`')

            # await 


                # [CreateEmbed('info', `[${track.title}](${track.uri})`).setAuthor('Now Playing', 'https://cdn.discordapp.com/avatars/516289475865739294/82d504d54a7f04ce268e97376efc292a.png?size=1024').addField('**Requested By**', `${track.requester}`, true).addField('**Duration**', `\`${prettyMilliseconds(track.duration, { colonNotation: true })}\``, true)]});

    @commands.command(aliases=['connect'])
    async def join(self, ctx):
        """Join a VC"""
        player = self.bot.lavalink.player_manager.get(ctx.guild.id)
        await ctx.message.add_reaction('<a:tick:940816615237357608>')
    
    @commands.command(name='queue')
    async def queue(self, ctx, page: int = 1):
        player = self.bot.lavalink.player_manager.get(ctx.guild.id)

        items_per_page = 10000000000000000000000000000000000000000000000000
        pages = math.ceil(len(player.queue) / items_per_page)

        start = (page - 1) * items_per_page
        end = start + items_per_page

        queue_list = []
        for index, track in enumerate(player.queue):
            seconds=(track.duration/1000)%60
            minutes=(track.duration/(1000*60))%60
            hours=(track.duration/(1000*60*60))%24
            if int(hours) == 0:
                time = f'{int(minutes)}:{int(seconds)}'
            else:
                time = f'{int(hours)}:{int(minutes)}:{int(seconds)}'
            requester = await self.bot.fetch_user(track.requester)
            queue_list.append(f'`{index + 1}.` [**{track.title}**]({track.uri})\n`{time}` • Requested By `{requester.name}`\n')

        embed = discord.Embed(colour=discord.Color.blurple(),
                            description=f'**{len(player.queue)} tracks**\n\n{queue_list}')
        embed.set_footer(text=f'Viewing page {page}/{pages}')
        # await Pag
        # msg = await ctx.send(embed=embed)
        try:
            await Pag(title=f'{ctx.guild.name}\'s Queue',color=discord.Color.blue(), entries=queue_list, length=5).start(ctx)
        except:
            await ctx.send('No More Songs in the Queue')
        # await msg.add_reaction('⬅️')
        # await msg.add_reaction('⏹️')
        # await msg.add_reaction('➡️')
        # def check(reaction, user):
        #     return reaction.message.id == msg.id and user == ctx.author 
        # while True:
        #     try:
        #         reaction, _ = await self.bot.wait_for('reaction_add', timeout= 20.0, check=check)
        #         if reaction.emoji == '⬅️' and page > 0:
        #             page -= 1
        #             embed = discord.Embed(title='Title Here', description=pages[page])
        #             await msg.edit(embed=embed)
            #     if reaction.emoji == '➡️' and page < len(pages) -1:
            #         page += 1
            #         embed = discord.Embed(title='Title Here', description= pages[page])
            #         await msg.edit(embed=embed)
            #     if reaction.emoji == '⏹️':
            #         await msg.delete()
            # except asyncio.TimeoutError:
            #     await msg.delete()

    @commands.command(aliases=['p'])
    async def play(self, ctx, *, query: str):
        """ Searches and plays a song from a given query. """
        # Get the player for this guild from cache.
        button = Button(style=discord.ButtonStyle.blurple, label='Skip')
        MyView = View()
        MyView.add_item(button)
        player = self.bot.lavalink.player_manager.get(ctx.guild.id)
        # Remove leading and trailing <>. <> may be used to suppress embedding links in Discord.
        query = query.strip('<>')

        # Check if the user input might be a URL. If it isn't, we can Lavalink do a YouTube search for it instead.
        # SoundCloud searching is possible by prefixing "scsearch:" instead.
        if not url_rx.match(query):
            query = f'ytsearch:{query}'

        # Get the results for the query from Lavalink.
        results = await player.node.get_tracks(query)

        # Results could be None if Lavalink returns an invalid response (non-JSON/non-200 (OK)).
        # ALternatively, resullts['tracks'] could be an empty array if the query yielded no tracks.
        if not results or not results['tracks']:
            return await ctx.send('Nothing found!')

        await ctx.message.add_reaction('<a:tick:940816615237357608>')
        embed = discord.Embed(color=discord.Color.blue())

        # Valid loadTypes are:
        #   TRACK_LOADED    - single video/direct URL)
        #   PLAYLIST_LOADED - direct URL to playlist)
        #   SEARCH_RESULT   - query prefixed with either ytsearch: or scsearch:.
        #   NO_MATCHES      - query yielded no results
        #   LOAD_FAILED     - most likely, the video encountered an exception during loading.
        if results['loadType'] == 'PLAYLIST_LOADED':
            tracks = results['tracks']

            for track in tracks:
                # Add all of the tracks from the playlist to the queue.
                player.add(requester=ctx.author.id, track=track)
            
            url = results["playlistInfo"]["uri"]
            exp = "^.*((youtu.be\/)|(v\/)|(\/u\/\w\/)|(embed\/)|(watch\?))\??v?=?([^#&?]*).*"
            s = re.findall(exp,url)[0][-1]
            thumbnail = f"https://i.ytimg.com/vi/{s}/maxresdefault.jpg"

            try:
                embed.set_image(url=thumbnail)
            except:
                pass

            embed.title = 'Playlist Enqueued!'
            embed.description = f'{results["playlistInfo"]["name"]} - {len(tracks)} tracks'
        else:
            track = results['tracks'][0]

            url = track["info"]["uri"]
            exp = "^.*((youtu.be\/)|(v\/)|(\/u\/\w\/)|(embed\/)|(watch\?))\??v?=?([^#&?]*).*"
            s = re.findall(exp,url)[0][-1]
            thumbnail = f"https://i.ytimg.com/vi/{s}/maxresdefault.jpg"

            try:
                embed.set_image(url=thumbnail)
            except:
                pass

            embed.title = 'Track Enqueued'
            embed.description = f'[{track["info"]["title"]}]({track["info"]["uri"]})'
            # embed.add_field(name="Requested By", value=f'{track["info"]["requester"]}')
            # You can attach additional information to audiotracks through kwargs, however this involves
            # constructing the AudioTrack class yourself.
            track = lavalink.models.AudioTrack(track, ctx.author.id, recommended=True)
            player.add(requester=ctx.author.id, track=track)

        await ctx.send(embed=embed)

        # We don't want to call .play() if the player is playing as that will effectively skip
        # the current track.
        if not player.is_playing:
            await player.play()
    
    @commands.command()
    async def skip(self, ctx):
        """Didnt like the Current Song ? Skip it!"""
        player = self.bot.lavalink.player_manager.get(ctx.guild.id)

        if not player.is_connected:
            # We can't disconnect, if we're not connected.
            return await ctx.send('I\'m not connected to any VC.')

        if not ctx.author.voice or (player.is_connected and ctx.author.voice.channel.id != int(player.channel_id)):
            # Abuse prevention. Users not in voice channels, or not in the same voice channel as the bot
            # may not disconnect the bot.
            return await ctx.send('You\'re not in my voicechannel!')
        
        await ctx.message.add_reaction('<a:tick:940816615237357608>')

        await player.skip()
        
        await ctx.send('*⃣ | Skipped !')
    
    @commands.command()
    async def stop(self, ctx):
        """Stops the Player and clears the Queue"""
        player = self.bot.lavalink.player_manager.get(ctx.guild.id)
        player.queue.clear()
        await player.stop()
        await ctx.message.add_reaction('<a:tick:940816615237357608>')


    @commands.command(aliases=['dc'])
    async def disconnect(self, ctx):
        """ Disconnects the player from the voice channel and clears its queue. """
        player = self.bot.lavalink.player_manager.get(ctx.guild.id)

        if not player.is_connected:
            # We can't disconnect, if we're not connected.
            return await ctx.send('Not connected.')

        if not ctx.author.voice or (player.is_connected and ctx.author.voice.channel.id != int(player.channel_id)):
            # Abuse prevention. Users not in voice channels, or not in the same voice channel as the bot
            # may not disconnect the bot.
            return await ctx.send('You\'re not in my voicechannel!')

        # Clear the queue to ensure old tracks don't start playing
        # when someone else queues something.
        player.queue.clear()
        # Stop the current track so Lavalink consumes less resources.
        await player.stop()
        # Disconnect from the voice channel.
        await ctx.voice_client.disconnect(force=True)

        await ctx.send('*⃣ | Disconnected.')


def setup(bot):
    bot.add_cog(Music(bot))
