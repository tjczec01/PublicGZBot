"""
Please understand Music bots are complex, and that even this basic example can be daunting to a beginner.
For this reason it's highly advised you familiarize yourself with discord.py, python and asyncio, BEFORE
you attempt to write a music bot.
This example makes use of: Python 3.6
For a more basic voice example please read:
    https://github.com/Rapptz/discord.py/blob/rewrite/examples/basic_voice.py
This is a very basic playlist example, which allows per guild playback of unique queues.
The commands implement very basic logic for basic usage. But allow for expansion. It would be advisable to implement
your own permissions and usage logic for commands.
e.g You might like to implement a vote before skipping the song or only allow admins to stop the player.
Music bots require lots of work, and tuning. Goodluck.
If you find any bugs feel free to ping me on discord. @Eviee#0666

Copyright (c) 2019 Valentin B.
A simple music bot written in discord.py using youtube-dl.
Though it's a simple example, music bots are complex and require much time and knowledge until they work perfectly.
Use this as an example or a base for your own bot and extend it as you want. If there are any bugs, please let me know.
Requirements:
Python 3.5+
pip install -U discord.py pynacl youtube-dl
You also need FFmpeg in your PATH environment variable or the FFmpeg.exe binary in your bot's directory on Windows.
"""

# Music bot code from: https://gist.github.com/vbe0201/ade9b80f2d3b64643d854938d40a0a2d

import os
import sys
import traceback
from functools import partial
from youtube_dl import YoutubeDL
import youtube_dl
import urllib.request
import urllib
import discord
from discord.ext import commands
from discord.utils import get
import asyncio
import random
import functools
import itertools
from async_timeout import timeout
import socket
import requests
import aiohttp
import time
import json
import ctypes.util
from asyncio import sleep

token = "{}".format(os.environ['DISCORD_BOT_TOKEN'])

a = ctypes.util.find_library('opus')
# print(a)

b = discord.opus.load_opus(a)
# print(b)

c = discord.opus.is_loaded()
# print(c)

intents = discord.Intents().all()
i2 = discord.Intents(messages=True, guilds=True, members=True, presences=True, voice_states=True, emojis=True, reactions=True, invites=True, bans=True, guild_typing=True, typing=True, webhooks=True, integrations=True, guild_reactions=True, dm_reactions=True)
intents.members = True
client = discord.Client()

bot = commands.Bot('-', description='GZ-bot', intents=intents)

global server_list

server_list = []

global server_info

server_info = []

global song_list

song_list = []

global voice_channels_list

voice_channels_list = []

global text_channels_list

text_channel_list = []

global text_home_channel

text_home_channel = None

global voice_home_channel

voice_home_channel = None

global AFK_channel

AFK_channel = None

global safe_channels

safe_channels = []

YTDL_OPTIONS = {
        'format': 'bestaudio/best',
        'extractaudio': True,
        'audioformat': 'mp3',
        'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
        'restrictfilenames': True,
        'noplaylist': True,
        'nocheckcertificate': True,
        'ignoreerrors': True,
        'logtostderr': False,
        'quiet': True,
        'no_warnings': True,
        'default_search': 'auto',
        'source_address': '0.0.0.0'}

FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}

thabois = ["Travs", "BRO TURTLEZ", "keck", "flamingdragon73", "johnwalters", "griff", "DickHardly",
           "Bionic Barry", "koreanboi" , "Striker", "AnaaliKuningas", "SIMPLE SETHWIN"]

lennylist = ["(ᵕ̣̣̣̣̣̣∀ᵕ̣̣̣̣̣̣)", "(˘̩̩̩̩̩̩n˘̩̩̩̩̩̩✿)", "⊂(´ω`⊂ )", "(•̩̥̀⌒•̩̥̀๑✿)", "(๑˃̣̣̥⌓˂̣̣̥)", "( ͡ಠ ʖ̯ ͡ಠ)",
             "(U•/ᴥ\•U)", "ᕦ( ͡° ͜ʖ ͡°)ᕤ", "( ͡☉ ͜ʖ ͡☉)", "(ﾉ◕ヮ◕)ﾉ", "(✿˶˘ 3˘)",
             "(≧o≦✿)", "(๑≧◡≦)", "(✿˘³˘)", "(°ᵕ°✿)"
, "(✿˘ ں ˘)", "(•̃͡ε•̃)", "(❀ •̀ᴗ•́ )", "(^ε^ )", "(•⌣•✿)", "凸( ಠ益ಠ)凸"]

slist = ["~~~<====3", "Ɛ====>~~~","-(====>", "<====)-"]

greek_list = ["Aaron's pixel 5",'Ͳ', 'ͳ', 'ʹ', 'Ͷ', 'ͷ', 'ͻ', 'ͼ', 'ͽ', 'Ό', 'Ύ', 'Ώ', 'ΐ', 'Α', 'Γ', 'Δ',
              'Θ', 'Λ', 'Ξ', 'Π','Σ', 'Φ', 'Ψ', 'Ω', 'Ϊ', 'Ϋ', 'ά', 'έ', 'ή', 'ί', 'ΰ', 'α', 'β', 'γ', 'δ',
              'ε', 'ζ', 'η', 'θ', 'ι', 'κ', 'λ', 'μ', 'ν', 'ξ', 'ο', 'π', 'ρ', 'ς', 'σ', 'τ', 'υ', 'φ', 'χ',
              'ψ', 'ω', 'ϊ', 'ϋ', 'ό', 'ύ', 'ώ', 'Ϗ', 'ϐ', 'ϑ', 'ϒ', 'ϓ', 'ϔ', 'ϕ', 'ϖ', 'ϗ', 'Ϙ', 'ϙ', 'Ϛ',
              'ϛ', 'ϝ', 'Ϟ', 'ϟ', 'Ϡ', 'ϡ', 'ϰ', 'ϱ', 'ϴ', 'ϵ', 'Ϸ', 'ϸ', 'ϻ', 'ϼ', 'Ͻ', 'Ͼ', 'Ͽ']

MFN_bois = ['Travs_ID', 'BRO TURTLEZ_ID', 'keck_ID', 'JtK_ID', 'PocketsLLP_ID', 'DickHardly_ID',
            'Bionic_Barry_ID', 'Bouldery_ID', 'Kabuki_Wookiee_ID', 'flamingdragon73_ID', 'griff_ID', 'Striker_ID', 'SIMPLE_SETHWIN_ID',
            'GreenSquid23_ID', 'koreanboi_ID']

# MFN_boisids = [os.environ['{}'.format(MFN_bois[i])] for i in range(len(MFN_bois))]

emoji_list = ['🌲', '🌳', '🌴', '🌵', '🌾', '🌿', '☘️', '🍀', '🍁', '🍂', '🍃', '🍇', '🍈', '🍉', '🐛', '🍞',
              '🍊', '🍋', '🍌', '🍍', '🥭', '🍎', '🍏', '🍐', '🍑', '🍒', '🍓', '🐊', '🐢', '🦎', '🐍', '🐜',
              '🐲', '🐉', '🦕', '🦖', '🐳', '🐋', '🐬',  '🐟', '🐠', '🐡', '🦈', '🐙', '🐚', '🐌', '🦋', '🐝']

# print(MFN_boisids)
# for i in range(len(MFN_bois)):
    # os.environ[MFN_bois[i]] = '{}'.format(MFN_boisids[i])
    # print("{}{}{}: {}{}{},".format('"', MFN_bois[i], '"', '"', os.environ[MFN_bois[i]], '"'))

OPUS_LIBS = ['libopus-0.x86.dll', 'libopus-0.x64.dll', 'libopus-0.dll', 'libopus.so.0', 'libopus.0.dylib']

# robot_beep = r"C:\Users\tjcze\Desktop\gz-bot\Robot_blip-Marianne_Gagnon-120342607.mp3"
robot_beep = r"/app/Robot_blip-Marianne_Gagnon-120342607.mp3"

ytdlopts = {
    'format': 'bestaudio/best',
    'outtmpl': 'downloads/%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0'  # ipv6 addresses cause issues sometimes
}

ffmpegopts = {
    'before_options': '-nostdin',
    'options': '-vn'
}

ytdl = YoutubeDL(ytdlopts)

class VoiceError(Exception):
    pass


class YTDLError(Exception):
    pass

class VoiceConnectionError(commands.CommandError):
    """Custom Exception class for connection errors."""


class InvalidVoiceChannel(VoiceConnectionError):
    """Exception for cases of invalid Voice Channels."""


class YTDLSource(discord.PCMVolumeTransformer):

    def __init__(self, source, *, data, requester):
        super().__init__(source)
        self.requester = requester

        self.title = data.get('title')
        self.web_url = data.get('webpage_url')

        # YTDL info dicts (data) have other useful information you might want
        # https://github.com/rg3/youtube-dl/blob/master/README.md

    def __getitem__(self, item: str):
        """Allows us to access attributes similar to a dict.
        This is only useful when you are NOT downloading.
        """
        return self.__getattribute__(item)

    @classmethod
    async def create_source(cls, ctx, search: str, *, loop, download=False):
        loop = loop or asyncio.get_event_loop()

        to_run = partial(ytdl.extract_info, url=search, download=download)
        data = await loop.run_in_executor(None, to_run)

        if 'entries' in data:
            # take first item from a playlist
            data = data['entries'][0]

        await ctx.send(f'```ini\n[Added {data["title"]} to the Queue.]\n```', delete_after=15)

        if download:
            source = ytdl.prepare_filename(data)
        else:
            return {'webpage_url': data['webpage_url'], 'requester': ctx.author, 'title': data['title']}

        return cls(discord.FFmpegPCMAudio(source), data=data, requester=ctx.author)

    @classmethod
    async def regather_stream(cls, data, *, loop):
        """Used for preparing a stream, instead of downloading.
        Since Youtube Streaming links expire."""
        loop = loop or asyncio.get_event_loop()
        requester = data['requester']

        to_run = partial(ytdl.extract_info, url=data['webpage_url'], download=False)
        data = await loop.run_in_executor(None, to_run)

        return cls(discord.FFmpegPCMAudio(data['url']), data=data, requester=requester)


class MusicPlayer:
    """A class which is assigned to each guild using the bot for Music.
    This class implements a queue and loop, which allows for different guilds to listen to different playlists
    simultaneously.
    When the bot disconnects from the Voice it's instance will be destroyed.
    """

    __slots__ = ('bot', '_guild', '_channel', '_cog', 'queue', 'next', 'current', 'np', 'volume')

    def __init__(self, ctx):
        self.bot = ctx.bot
        self._guild = ctx.guild
        self._channel = ctx.channel
        self._cog = ctx.cog

        self.queue = asyncio.Queue()
        self.next = asyncio.Event()

        self.np = None  # Now playing message
        self.volume = .5
        self.current = None

        ctx.bot.loop.create_task(self.player_loop())



    async def player_loop(self):
        """Our main player loop."""
        await self.bot.wait_until_ready()

        while not self.bot.is_closed():
            self.next.clear()

            try:
                # Wait for the next song. If we timeout cancel the player and disconnect...
                async with timeout(300):  # 5 minutes...
                    source = await self.queue.get()
            except asyncio.TimeoutError:
                return self.destroy(self._guild)

            if not isinstance(source, YTDLSource):
                # Source was probably a stream (not downloaded)
                # So we should regather to prevent stream expiration
                try:
                    source = await YTDLSource.regather_stream(source, loop=self.bot.loop)
                except Exception as e:
                    await self._channel.send(f'There was an error processing your song.\n'
                                             f'```css\n[{e}]\n```')
                    continue

            source.volume = self.volume
            self.current = source
            name_str = str("{}".format(source.requester))
            name_str_f = name_str[:-5]
            self._guild.voice_client.play(source, after=lambda _: self.bot.loop.call_soon_threadsafe(self.next.set))
            self.np = await self._channel.send(f'**Now Playing:** `{source.title}` requested by '
                                               f'`{name_str_f}`')
            await self.next.wait()

            # Make sure the FFmpeg process is cleaned up.
            source.cleanup()
            self.current = None

            try:
                # We are no longer playing this song...
                await self.np.delete()
            except discord.HTTPException:
                pass

    def destroy(self, guild):
        """Disconnect and cleanup the player."""
        return self.bot.loop.create_task(self._cog.cleanup(guild))


class Music(commands.Cog):
    """Music related commands."""

    __slots__ = ('bot', 'players')

    def __init__(self, bot):
        self.bot = bot
        self.players = {}

    async def cleanup(self, guild):
        try:
            await guild.voice_client.disconnect()
        except AttributeError:
            pass

        try:
            del self.players[guild.id]
        except KeyError:
            pass

    async def __local_check(self, ctx):
        """A local check which applies to all commands in this cog."""
        if not ctx.guild:
            raise commands.NoPrivateMessage
        return True

    async def __error(self, ctx, error):
        """A local error handler for all errors arising from commands in this cog."""
        if isinstance(error, commands.NoPrivateMessage):
            try:
                return await ctx.send('This command can not be used in Private Messages.')
            except discord.HTTPException:
                pass
        elif isinstance(error, InvalidVoiceChannel):
            await ctx.send('Error connecting to Voice Channel. '
                           'Please make sure you are in a valid channel or provide me with one')

        print('Ignoring exception in command {}:'.format(ctx.command), file=sys.stderr)
        traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)

    def get_player(self, ctx):
        """Retrieve the guild player, or generate one."""
        try:
            player = self.players[ctx.guild.id]
        except KeyError:
            player = MusicPlayer(ctx)
            self.players[ctx.guild.id] = player

        return player

    @commands.command(name='connect', aliases=['join'])
    async def connect_(self, ctx, *, channel: discord.VoiceChannel=None):
        """Connect to voice.
        Parameters
        ------------
        channel: discord.VoiceChannel [Optional]
            The channel to connect to. If a channel is not specified, an attempt to join the voice channel you are in
            will be made.
        This command also handles moving the bot to different channels.
        """
        if not channel:
            try:
                channel = ctx.author.voice.channel
            except AttributeError:
                raise InvalidVoiceChannel('No channel to join. Please either specify a valid channel or join one.')

        vc = ctx.voice_client

        if vc:
            if vc.channel.id == channel.id:
                return
            try:
                await vc.move_to(channel)
            except asyncio.TimeoutError:
                raise VoiceConnectionError(f'Moving to channel: <{channel}> timed out.')
        else:
            try:
                await channel.connect()
            except asyncio.TimeoutError:
                raise VoiceConnectionError(f'Connecting to channel: <{channel}> timed out.')

        await ctx.send(f'Connected to: **{channel}**', delete_after=20)

    @commands.command(name='gplay', aliases=['sing', 'gp'])
    async def play_(self, ctx, *, search: str):
        """Request a song and add it to the queue.
        This command attempts to join a valid voice channel if the bot is not already in one.
        Uses YTDL to automatically search and retrieve a song.
        Parameters
        ------------
        search: str [Required]
            The song to search and retrieve using YTDL. This could be a simple search, an ID or URL.
        """
        await ctx.trigger_typing()

        vc = ctx.voice_client

        if not vc:
            await ctx.invoke(self.connect_)

        player = self.get_player(ctx)

        # If download is False, source will be a dict which will be used later to regather the stream.
        # If download is True, source will be a discord.FFmpegPCMAudio with a VolumeTransformer.
        source = await YTDLSource.create_source(ctx, search, loop=self.bot.loop, download=False)

        await player.queue.put(source)

    @commands.command(name='pause', aliases=['pa', 'gpa'])
    async def pause_(self, ctx):
        """Pause the currently playing song."""
        vc = ctx.voice_client

        if not vc or not vc.is_playing():
            return await ctx.send('I am not currently playing anything!', delete_after=20)
        elif vc.is_paused():
            return

        vc.pause()
        name_stra = str("{}".format(ctx.author))
        name_str_fb = name_stra[:-5]
        await ctx.send(f'**`{name_str_fb}`**: Paused the song!', delete_after=20)

    @commands.command(name='resume', aliases=['res', 'gr'])
    async def resume_(self, ctx):
        """Resume the currently paused song."""
        vc = ctx.voice_client

        if not vc or not vc.is_connected():
            return await ctx.send('I am not currently playing anything!', delete_after=20)
        elif not vc.is_paused():
            return

        vc.resume()
        name_stra = str("{}".format(ctx.author))
        name_str_fb = name_stra[:-5]
        await ctx.send(f'**`{name_str_fb}`**: Resumed the song!', delete_after=20)

    @commands.command(name='skip', aliases=['gk', 'gskip', 'gs'])
    async def skip_(self, ctx):
        """Skip the song."""
        vc = ctx.voice_client

        if not vc or not vc.is_connected():
            return await ctx.send('I am not currently playing anything!', delete_after=20)

        if vc.is_paused():
            pass
        elif not vc.is_playing():
            return

        vc.stop()
        name_stra = str("{}".format(ctx.author))
        name_str_fb = name_stra[:-5]
        await ctx.send(f'**`{name_str_fb}`**: Skipped the song!', delete_after=20)

    @commands.command(name='queue', aliases=['q', 'playlist', 'gq'])
    async def queue_info(self, ctx):
        """Retrieve a basic queue of upcoming songs."""
        vc = ctx.voice_client

        if not vc or not vc.is_connected():
            return await ctx.send('I am not currently connected to voice!', delete_after=20)

        player = self.get_player(ctx)
        if player.queue.empty():
            return await ctx.send('There are currently no more queued songs.', delete_after=20)

        # Grab up to 5 entries from the queue...
        upcoming = list(itertools.islice(player.queue._queue, 0, 5))

        fmt = '\n'.join(f'**`{_["title"]}`**' for _ in upcoming)
        embed = discord.Embed(title=f'Upcoming - Next {len(upcoming)}', description=fmt)

        await ctx.send(embed=embed, delete_after=20)

    @commands.command(name='now_playing', aliases=['np', 'current', 'currentsong', 'playing', 'ng'])
    async def now_playing_(self, ctx):
        """Display information about the currently playing song."""
        vc = ctx.voice_client

        if not vc or not vc.is_connected():
            return await ctx.send('I am not currently connected to voice!', delete_after=20)

        player = self.get_player(ctx)
        if not player.current:
            return await ctx.send('I am not currently playing anything!')

        try:
            # Remove our previous now_playing message.
            await player.np.delete()
        except discord.HTTPException:
            pass
        name_str = str("{}".format(vc.source.requester))
        name_str_f= name_str[:-5]
        player.np = await ctx.send(f'**Now Playing:** `{vc.source.title}` '
                                   f'`{name_str_f}`')

    @commands.command(name='volume', aliases=['vol', 'gv'])
    async def change_volume(self, ctx, *, vol: float):
        """Change the player volume.
        Parameters
        ------------
        volume: float or int [Required]
            The volume to set the player to in percentage. This must be between 1 and 100.
        """
        vc = ctx.voice_client

        if not vc or not vc.is_connected():
            return await ctx.send('I am not currently connected to voice!', delete_after=20)

        if not 0 < vol < 101:
            return await ctx.send('Please enter a value between 1 and 100.', delete_after=20)

        player = self.get_player(ctx)

        if vc.source:
            vc.source.volume = vol / 100

        player.volume = vol / 100
        await ctx.send(f'**`{ctx.author}`**: Set the volume to **{vol}%**', delete_after=20)

    @commands.command(name='stop', aliases=['gstop', 'gstp'])
    async def stop_(self, ctx):
        """Stop the currently playing song and destroy the player.
        !Warning!
            This will destroy the player assigned to your guild, also deleting any queued songs and settings.
        """
        vc = ctx.voice_client

        if not vc or not vc.is_connected():
            return await ctx.send('I am not currently playing anything!', delete_after=20)

        await self.cleanup(ctx.guild)

@bot.event
async def on_voice_state_update(member, before, after):
    voice_state = member.guild.voice_client
    vc_before = before.channel
    vc_after = after.channel
    name = str("{}".format(member.name))
    if name == "GZ-bot":
        c = 0
        try:
            vc = await after.channel.connect()
            c = 1
        except Exception:
            voice = member.guild.voice_client
            try:
                if voice and voice.is_connected():
                    voice_channel = member.voice.channel
                    voice = member.guild.voice_client
                    await voice.disconnect()
                    voice = await voice_channel.connect()
                    audio_source = discord.FFmpegPCMAudio(robot_beep)
                    voice.play(audio_source)
                    while voice.is_playing():
                        await asyncio.sleep(1)
                else:
                    voice_channel = member.voice.channel
                    voice = member.guild.voice_client
                    audio_source = discord.FFmpegPCMAudio(robot_beep)
                    voice = await voice_channel.connect()
                    voice.play(audio_source)
                    while voice.is_playing():
                        await asyncio.sleep(1)
                channel = member.voice.channel
            except Exception:
                pass  # break
        if (c == 1):
            try:
                audio_source = discord.FFmpegPCMAudio(robot_beep)
                vc.play(audio_source)
                while vc.is_playing():
                    await asyncio.sleep(1)
            except Exception:
                pass
        else:
            pass
    else:
        pass

@bot.command(name='addrole', pass_context=True, aliases=['role', 'add_role', "ar", "roleadd", "gadd", "grole"])
@commands.has_role("admin")
async def addrole(ctx, user: discord.Member, message):
    message_str = str("{}".format(ctx.message.content))
    removetable = str.maketrans('', '', '@#!%<>')
    message_strf = message_str.translate(removetable)
    str_list = message_strf.split()
    mem_number = int(str_list[-2])
    mem_info = await ctx.message.guild.fetch_member(mem_number)
    mem_roles = [r.name for r in list(mem_info.roles)]
    member_name = mem_info.name
    role_name = str_list[-1]
    user = await ctx.message.guild.fetch_member(ctx.message.author.id)
    usr = list(user.roles)
    user_role_names = [r.name for r in usr]
    GUILD_ID = ctx.message.guild.id
    guild = await bot.fetch_guild(GUILD_ID)
    roles_names = [r.name for r in guild.roles]
    if discord.utils.get(user.roles, name="admin") is None:
        return

    role = discord.utils.get(ctx.guild.roles, name=role_name)

    if get(ctx.guild.roles, name=role_name) and "{}".format(role_name) in mem_roles:
        await ctx.message.channel.purge(limit=1)
        await ctx.message.channel.send("**{}** already has role".format(member_name), delete_after=20)

    elif get(ctx.guild.roles, name=role_name):
        if role in mem_info.roles:
            await ctx.message.channel.purge(limit=1)
            await ctx.message.channel.send("**{}** already has role".format(member_name), delete_after=20)
        else:
            await mem_info.add_roles(role)
            await ctx.message.channel.purge(limit=1)
            await ctx.message.channel.send("**{}** was given **{}** role".format(member_name, role_name), delete_after=20)
    elif "{}".format(role_name) not in roles_names:
        role = await ctx.message.guild.create_role(name=role_name, colour=discord.Colour.from_rgb(random.randrange(255),
                                                                                              random.randrange(255),
                                                                                              random.randrange(255)))
        await mem_info.add_roles(role)
        await ctx.message.channel.purge(limit=1)
        await ctx.message.channel.send(
            "**{}** role was created and **{}** was given **{}** role".format(role_name, member_name, role_name), delete_after=20)

@bot.command(name='removerole', pass_context=True, aliases=['remove_role', "rr", "rrole", "grr", "grrole"])
@commands.has_role("admin")
async def removerole(ctx, user: discord.Member, message):
    message_str = str("{}".format(ctx.message.content))
    removetable = str.maketrans('', '', '@#!%<>')
    message_strf = message_str.translate(removetable)
    str_list = message_strf.split()
    mem_number = int(str_list[-2])
    mem_info = ctx.message.author.guild.get_member(mem_number)
    member_name = mem_info.name
    role_name = str_list[-1]
    user = await ctx.message.guild.fetch_member(ctx.message.author.id)
    usr = list(user.roles)
    user_role_names = [r.name for r in usr]
    roles = list(ctx.guild.roles)
    GUILD_ID= ctx.message.guild.id
    guild = await bot.fetch_guild(GUILD_ID)
    roles_names = [r.name for r in guild.roles]
    if discord.utils.get(user.roles, name="admin") is None:
        return

    role = discord.utils.get(ctx.guild.roles, name=role_name)

    if get(ctx.guild.roles, name=role_name) and "{}".format(role_name) in user_role_names:
        await user.remove_roles(role)
        await ctx.message.channel.purge(limit=1)
        await ctx.message.channel.send("**{}** has had **{}** role revoked".format(member_name, role_name, delete_after=10))

    elif get(ctx.guild.roles, name=str("{}".format(role_name))):
        if role in mem_info.roles:
            await user.remove_roles(role)
            await ctx.message.channel.purge(limit=1)
            await ctx.message.channel.send("**{}** has had **{}** role revoked".format(member_name, role_name, delete_after=10))
        else:
            await user.remove_roles(role)
            await ctx.message.channel.purge(limit=1)
            await ctx.message.channel.send("**{}** does not have **{}** role ".format(member_name, role_name), delete_after=10)

    elif "{}".format(role_name) not in roles_names:
        await ctx.message.channel.purge(limit=1)
        await ctx.message.channel.send("**{}** role does not exist".format(role_name, delete_after=10))

@bot.command(name="deleterole", pass_context=True)
@commands.has_role("admin")
async def deleterole(ctx, role):
    try:
        role = discord.utils.get(ctx.guild.roles, name=role)
        await role.delete(reason='Removed by command')
        await ctx.message.channel.purge(limit=1)
        await ctx.message.channel.send("**{}** role was deleted".format(role.name), delete_after=20)

    except Exception:
        pass

@bot.command(name='gc', description='Price checks game on Steam.', pass_context=True)
async def gc(ctx, message):
    CHS = ctx.message.channel
    game_b = str(ctx.message.content)
    game = game_b[4:]
    gres = requests.get('https://api.steampowered.com/ISteamApps/GetAppList/v2/')
    gdata = gres.json()
    game_found = False
    for i in gdata["applist"]["apps"]:
        if (i["name"] == game):
            game_found = True
            app = (i["appid"])
            session = aiohttp.ClientSession()
            priceres = await session.get("https://store.steampowered.com/api/appdetails/?appids={}".format(app))
            priced = await priceres.json()
            await session.close()
            price = (priced["{}".format(app)]["data"]["price_overview"].get("final"))
            pricef = price / 100
            msg = "{} is currently ${:,.2f} on Steam.".format(game, pricef)
            await CHS.send(msg)
    if not game_found:
        await CHS.send("Could not find info on {}.".format(game))


@bot.command(name='g2a', description='Price checks game on G2a.', pass_context=True)
async def g2a(ctx, message):
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; CrOS x86_64 12871.102.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.141 Safari/537.36",
        'Accept-Language': 'en-US;q=0.7,en;q=0.3'}
    base_g2a_url = "https://www.g2a.com/lucene/search/filter?&search="
    base_g2a_urlid = "https://www.g2a.com/marketplace/product/auctions/?id="
    game_nameb = str(ctx.message.content)  # "The Elder Scrolls V: Skyrim"
    game_name = game_nameb[5:]
    strf = game_name  # "A computer science portal for geeks"
    # Traverse the string character by character.
    try:
        for i in range(0, len(strf), 1):

            # Changing the ith character
            # to '-' if it's a space.
            if (strf[i] == ' '):
                strf = strf.replace(strf[i], '+')

                # Print the modified string.
                # print(strf)
            game_name_fixed = strf  # re.sub(' ', '+', game_nameb.rstrip())

        g2a_r = requests.get("{}{}".format(base_g2a_url, game_name_fixed), headers=headers).text
        game_id = json.loads(g2a_r)['docs'][0]['id']  # data['docs'][0]['id']
        g2a_r_id = requests.get("{}{}".format(base_g2a_urlid, game_id), headers=headers).text
        game_price_g2a = json.loads(g2a_r_id)["lowest_price"]
        await ctx.message.channel.send("**{}** is currently **${}** on g2a.com.".format(game_name, game_price_g2a))
    except Exception:
        await ctx.message.channel.send("Could not find info on {}.".format(game_name))

@bot.command(name='ghelp', description='GZ-bot help.', pass_context=True)
async def ghelp(ctx):
    embedVar = discord.Embed(title="GZ-bot Help", description="GZ-bot command references", color=0x00ff00)
    embedVar.add_field(name="GZ-bot Join", value="jn", inline=False)
    embedVar.add_field(name="GZ-bot Leave", value="lv", inline=False)                    
    embedVar.add_field(name="Play music", value="-gp [link] or -gplay [link]", inline=False)
    embedVar.add_field(name="Pause song", value="-gpa", inline=False)
    embedVar.add_field(name="Resume song: ", value="-gr", inline=False)
    embedVar.add_field(name="Queue_info", value="-gq", inline=False)
    embedVar.add_field(name="Now playing", value="-ng", inline=False)
    embedVar.add_field(name="Change Volume", value="-gv [1 - 100]", inline=False)
    embedVar.add_field(name="Skip song", value="-gk", inline=False)
    embedVar.add_field(name="Stop song", value="-gstp", inline=False)
    embedVar.add_field(name="Erase messages", value="clear [number of messages to erase]", inline=False)
    embedVar.add_field(name="Nap Time", value="-g nap [@User]", inline=False)
    embedVar.add_field(name="Jimbo Time", value="jimbo", inline=False)
    embedVar.add_field(name="Game Pricecheck on Steam", value="-gc [game]", inline=False)
    embedVar.add_field(name="Game Pricecheck on G2a", value="-g2a [game]", inline=False)
    embedVar.add_field(name="Create/Give role", value="-addrole [User] [Role]", inline=False)
    embedVar.add_field(name="Remove role", value="-grr [User] [Role]", inline=False)
    embedVar.add_field(name="Delete role", value="-deleterole [Role]", inline=False)
    await ctx.message.channel.send(embed=embedVar)

@bot.command(pass_context=True)
async def adr(ctx):
     member = ctx.author
     role = discord.utils.get(member.guild.roles, name="Server")
     await discord.Member.add_roles(member, role)

@bot.command(pass_context=True)
async def dEv(ctx):
     member = ctx.author
     role = discord.utils.get(member.guild.roles, name="Dev")
     await discord.Member.add_roles(member, role)

@bot.command(pass_context=True)
async def check(ctx):
    if not ctx.author.voice or not ctx.author.voice.channel:
        #raise commands.CommandError('You are not connected to any voice channel.')
        pass

    elif ctx.voice_client:
        if ctx.voice_client.channel != ctx.author.voice.channel:
            pass
            #raise commands.CommandError('Bot is already in a voice channel.')
    else:
        pass # await ctx.send("GZ-bot is online now.")

# Code I actually wrote my self starts here

@bot.command(name="set_safe", pass_context=True, aliases=['set all safe', "s s", "safe", "s s all", "ss", "set safe channel"])
async def set_ssafe(message):
    global safe_channels
    global text_home_channel
    global server_info
    cguild = message.guild.id
    for ggg in server_info:
        gid = ggg["Server ID"]
        if gid == cguild:
            text_home_channel = ggg["Server Home Text Channel ID"]
            voice_home_channel = ggg["Server Home Voice Channel ID"]
    channels = bot.get_channel(text_home_channel)
    # ctxv = await bot.get_context(message)
    channel = message.author.voice.channel
    safe_channels_ch = message.author.voice.channel.id

    safe_channels.append(safe_channels_ch)
    await channels.send(
        "Safe Channels: **{}**".format(safe_channels))
    for si in safe_channels:
        print("Safe Channel Name: **{}**, Safe Channel ID: **{}**".format((bot.get_channel(safe_channels_ch)).name, (bot.get_channel(safe_channels_ch)).id))


@bot.command(name="set voice", pass_context=True, aliases=['set v', "sv", "home voice", "home v", "set home voice", "set home v"])
async def set_home_voice(message):
    global server_info
    ctxv = await bot.get_context(message)
    cguild = ctxv.message.guild.id
    for ggg in server_info:
        gid = ggg["Server ID"]
        if gid == cguild:
            global voice_home_channel
            ggg["Server Home Voice Channel ID"] = ctxv.message.author.voice.channel.id
            ggg["Server Home Voice Channel Name"] = ctxv.message.author.voice.channel.name
        else:
            pass


@bot.command(name="set text", pass_context=True)
async def set_home_text(message):
    global server_info
    ctxt = await bot.get_context(message)
    cguild = ctxt.message.guild.id
    for ggg in server_info:
        gid = ggg["Server ID"]
        if gid == cguild:
            channel_text = ctxt.message.channel
            global text_home_channel
            ggg["Server Home Text Channel ID"] = channel_text.id
            ggg["Server Home Text Channel Name"] = channel_text.name
        else:
            pass


@bot.command(name="set home", pass_context=True)
async def set_home(message):
    global text_home_channel
    global server_info
    global voice_home_channel

    ctx = await bot.get_context(message)
    cguild = ctx.message.guild.id
    for ggg in server_info:
        gid = ggg.get("Server ID")
        if gid == cguild:
            channel_text = ctx.message.channel
            ggg["Server Home Text Channel ID"] = channel_text.id
            ggg["Server Home Text Channel Name"] = channel_text.name

            channel_voice = ctx.message.author.voice.channel  # voice_home_ch = ctx.message.author.voice.channel.id
            ggg["Server Home Voice Channel ID"] = channel_voice.id
            ggg["Server Home Voice Channel Name"] = channel_voice.name

            CH = bot.get_channel(ggg["Server Home Text Channel ID"])
            await CH.send("Text Home Channel Name: **{}**, Text Home Channel ID: **{}**".format(ggg["Server Home Text Channel Name"],
                                                                                                ggg["Server Home Text Channel ID"]))
            await CH.send("Voice Home Channel Name: **{}**, Voice Home Channel ID: **{}**".format(ggg["Server Home Voice Channel Name"],
                                                                                                  ggg["Server Home Voice Channel ID"]))
        else:
            pass


@bot.command(pass_context=True)
async def nap(message, member: discord.Member):
    ctx = await bot.get_context(message)
    global AFK_channel
    try:
        voice_channel = bot.get_channel(AFK_channel)
        await member.move_to(voice_channel)
    except Exception:
        pass

@bot.command(pass_context=True)
async def n(message, member: discord.Member):
    ctx = await bot.get_context(message)
    global AFK_channel
    try:
        voice_channel = bot.get_channel(AFK_channel)
        await member.move_to(voice_channel)
    except Exception:
        pass

@bot.command(pass_context=True)
async def party(ctx, member: discord.Member, idf):
    voice_channel = bot.get_channel(idf)
    await member.move_to(voice_channel)

@bot.command(name="server", pass_context=True)
async def server(ctx):
    global server_info
    global text_home_channel
    cguild = ctx.message.guild.id
    for ggg in server_info:
        gid = ggg["Server ID"]
        if gid == cguild:
            text_home_channel = ggg["Server Home Text Channel ID"]
            voice_home_channel = ggg["Server Home Voice Channel ID"]
    CH = bot.get_channel(text_home_channel)
    external_ip = requests.get('https://api.ipify.org').text
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    local_ip = s.getsockname()[0]
    await CH.send('Server **external public** IP address is: **{}**'.format(external_ip))
    await CH.send('Server **local** network IP address is: **{}**'.format(local_ip))
    await CH.send('If connecting from outside my house use the **external public** IP address')
    await CH.send('If connecting from inside my house use the **local** IP address')
    await CH.send('Windows 10 Minecraft Server Name: **GuyLand** IP: **{}**'.format(external_ip))
    await CH.send('Minecraft Server Ports (Try both): **25565** **19132**')
    await CH.send('Flamingdragon73{}s Java Minecraft Server: **flaming123.minehut.gg**'.format("'"))
    await CH.send('Vanilla Minecraft Server Java: **guylandog.minecraftnoob.com:25565**')

@bot.command(name="guys", pass_context=True)
async def guys(ctx, message):
    x = ctx.message.guild.members
    for member in x:
        if member.name in thabois:
            await ctx.message.channel.send("**{} is a guy on planet earth**".format(member.name))
        else:
            await ctx.message.channel.send("*{}*".format(member.name))

@bot.event
async def on_ready():
    global text_home_channel
    global voice_home_channel
    global text_channels_list
    global voice_channels_list
    global AFK_channel
    global server_list
    global server_info
    # voice_channel_list = ctx.guild.voice_channels
    bguilds = bot.guilds
    current_guild = []
    guild_list = await bot.fetch_guilds(limit=1000).flatten()
    guild_list_ids = [g.id for g in guild_list]
    # current_text_ids = [t.id for t in guild.text_channels]
    # current_text_names = [t.name for t in guild.text_channels]
    # current_voice_ids = [v.id for v in guild.voice_channels]
    # current_voice_names = [v.name for v in guild.voice_channels]
    for guild in bguilds:
        # if not guild.id in guild_list_ids:
            current_text_ids = [t.id for t in guild.text_channels]
            current_text_names = [t.name for t in guild.text_channels]
            current_voice_ids = [v.id for v in guild.voice_channels]
            current_voice_names = [v.name for v in guild.voice_channels]
            server_list.append(guild.id) # current_guild.append(guild.id)
            afkchannel = discord.utils.get(guild.channels, name="{}".format(guild.afk_channel))
            server_info_dict = {"Server Name:": "{}".format(guild.name),
                                "Server ID": guild.id,
                                "Server Home Text Channel ID": current_text_ids[0],
                                "Server Home Text Channel Name": "{}".format(current_text_names[0]),
                                "Server Home Voice Channel ID": current_voice_ids[0],
                                "Server Home Voice Channel Name": "{}".format(current_voice_names[0]),
                                "AFK Channel ID": afkchannel.id,
                                "AFK Channel Name": "{}".format(afkchannel.name)}
            server_info.append(server_info_dict)
            text_home_channel = server_info_dict.get("Server Home Text Channel ID")
            voice_home_channel = server_info_dict["Server Home Voice Channel ID"]
        # server_list.append({"{}".format(guild.name): "{}".format(guild.id)})
        # if not guild in current_guild:
        #     current_guild.append(guild.id)
    TCL = []
    VCL = []
    ML = list(bot.get_all_members())
    # CL = list(bot.get_all_channels())
    for guild in bot.guilds:
        for tchannel in guild.text_channels:
            TCL.append(tchannel)
    for guild in bot.guilds:
        for vchannel in guild.voice_channels:
            VCL.append(vchannel)
    TCLids = [tci.id for tci in list(bguilds[0].text_channels)]
    text_channels_list = TCLids
    VCLids = [vci.id for vci in list(bguilds[0].voice_channels)]
    voice_channels_list = VCLids
    # TCLnames = [tci.name for tci in list(bguilds[0].text_channels)]
    # VCLnames = [vci.name for vci in list(bguilds[0].voice_channels)]
    afkchannel = discord.utils.get(bguilds[0].channels, name="{}".format(bguilds[0].afk_channel))
    AFK_channel = afkchannel.id
    for MEM in ML:
         isbot = MEM.bot
         if isbot == False or str("{}".format(isbot)) == str("False"):
             MFN_bois.append(MEM.name)
             # MFN_boisids.append(MEM.id)
         else:
             pass
    # dictionary = dict(zip(MFN_bois, MFN_boisids))
    # currentGuild = bot.get_guild(current_guild[-1])
    # server_info_dict = {"Server Name:": "{}".format(currentGuild.name), "Server ID": "{}".format(currentGuild.id),
    #                     "Server Home Text Channel": "{}".format(guild.id),
    #                     "Server Home Voice Channel": "{}".format(guild.id)}
    botsn = []
    botsm = []
    # memids = []  # ints
    memnames = []  # strings
    memnamesm = []  # strings
    # memnamesf = []  # strings
    # membersf = []
    membersoff = []
    cvs = []
    cvsn = []
    for guildg in server_info:
        CH = bot.get_channel(guildg.get("Server Home Text Channel ID"))
        await CH.send("**GZ-bot** is now online.", delete_after=10)

        voice_channels_listf = []
        for vchannel in guild.voice_channels:
            voice_channels_listf.append(vchannel.id)
        for chsi in voice_channels_listf:
            guildd = bot.get_channel(chsi)
            lll = list(guildd.members)

            cvs.append(guildd.members)
            for inx in cvs[-1]:
                cvsn.append(inx.name)
            for member in lll:
                if member.status == discord.Status.online:  # the member is in the server, do something #
                    if member.bot is False or str("{}".format(member.bot)) == str("False"):
                        memnames.append(member.name)
                        memnamesm.append(member)
                    elif member.bot is True or str("{}".format(member.bot)) == str("True"):
                        botsn.append(member.name)
                        botsm.append(member)

                else:
                    membersoff.append(member.name)
        Names = [sa for sa in cvsn if not any(sb in sa for sb in botsn)]

        # print(Names, botsn, memnames, cvs)

        try:
            await CH.send("**{}** is full of **cum** (**{}** lol).".format(random.choice(Names), random.choice(greek_list)), delete_after=10)
        except Exception:
            pass  # await CH.send("No one is currently online.")
        # print('Logged in as:\n{0.user.name}\n{0.user.id}'.format(bot))


totalgz = [0]

def setup(bot):
    bot.add_cog(Music(bot))


bot.add_cog(Music(bot))


@bot.event
async def on_message(message):


    if message.author.bot: return

    else:


        global text_channels_list
        global voice_channels_list
        cguild = message.guild.id
        for ggg in server_info:
            # print(ggg)
            gid = ggg.get("Server ID")
            if gid == cguild:
                global text_home_channel
                global voice_home_channel
                text_home_channel = ggg.get("Server Home Text Channel ID")
                voice_home_channel = ggg.get("Server Home Voice Channel ID")
            else:
                pass
        CTX = await bot.get_context(message)
        if (message.content.startswith('jn')):
            channels = bot.get_channel(text_home_channel)
            if (message.author.voice):  # If the person is in a channel
                channel = message.author.voice.channel
                vc = await channel.connect()
                audio_source = discord.FFmpegPCMAudio(robot_beep)
                vc.play(audio_source)
                while vc.is_playing():
                    await asyncio.sleep(1)
                await channels.purge(limit=1)
                
            else:  # But is (s)he isn't in a voice channel
                try:
                    channelv = bot.get_channel(voice_home_channel)
                    vc = await channelv.connect()
                    audio_source = discord.FFmpegPCMAudio(robot_beep)
                    vc.play(audio_source)
                    while vc.is_playing():
                        await asyncio.sleep(1)
                    await channels.purge(limit=1)
                except Exception:
                    await message.channel.send(
                        "You must be in a voice channel first so I can join it, you dum ass fucking bot.")
                    await asyncio.sleep(5)
                    await channels.purge(limit=2)


        elif message.content.startswith('lv'):  # Saying lv~ will make bot leave channel
            channels = bot.get_channel(text_home_channel)
            if (message.guild.voice_client):  # If the bot is in a voice channel
                await message.guild.voice_client.disconnect()  # Leave the channel
                await channels.purge(limit=1)
            else:  # But if it isn't
                await message.channel.send("I'm not in a voice channel, **you dum bot**.")
                await asyncio.sleep(5)
                await channels.purge(limit=2)

        elif "jimbo" in message.content or "yo jimbo" in message.content or "wuss boppin" in message.content:
            ctxb = await bot.get_context(message)
            await Music(bot).play_(ctxb, ctx=ctxb, search=str("https://www.youtube.com/watch?v=IhcO-e5Zmd8"))

        elif "roach" in message.content or "dancing roach" in message.content or "-r" in message.content:
            await roach(message)

        elif "g set" in message.content or "set home" in message.content or "-g set" in message.content:
            await set_home(message)

        elif "Server" in message.content:
            ctxs = await bot.get_context(message)
            await server(ctxs)

        elif "gn griffin" in message.content:
            ij = 0
            while ij < 5:
                await message.channel.send("gn griffin")  # Lol gn griffin
                ij += 1
        elif 'say' in message.content or "say " in message.content:
            channels = bot.get_channel(text_home_channel)
            SS = str("{}".format(message.content))
            SF = SS.strip('say')
            await  message.channel.send("{}".format(SF), tts=True)
            await channels.purge(limit=2)

        elif 'cum' in message.content:
            bots = []
            CH = bot.get_channel(text_home_channel)
            for i in voice_channels_list:
                memids = []  # ints
                memnames = []  # strings
                channelc = bot.get_channel(i)
                membersc = channelc.members  # Current members connected to the channel
                membersf = []
                if len(membersc) > 0:
                    for member in membersc:
                        if member.bot == False:
                            memnames.append(member.name)
                            memids.append(member.id)
                            membersf.append(member)
                        else:
                            bots.append(member.name)
            Names = [sa for sa in memnames if not any(sb in sa for sb in bots)]
            try:
                await CH.send(
                    "**{}** is full of **cum** (**{}** lol).".format(random.choice(Names), random.choice(greek_list)))
            except Exception:
                await CH.send("No one is currently online.")

        elif 'games' in message.content:
            bots = []
            for i in voice_channels_list:
                memids = []  # ints
                memnames = []  # strings
                channelc = bot.get_channel(i)
                membersc = channelc.members  # Current members connected to the channel
                membersf = []
                if len(membersc) > 0:
                    for member in membersc:
                        if member.bot == False:
                            memnames.append(member.name)
                            memids.append(member.id)
                            membersf.append(member)
                        else:
                            bots.append(member.name)
            Names = [sa for sa in memnames if not any(sb in sa for sb in bots)]
            for ij in range(len(membersf)):
                NAME = membersc[ij]
                try:
                    if membersf[ij].activity.name != None:
                        await message.channel.send(
                            "**{}** is playing {}".format(memnames[ij], membersf[ij].activity.name))
                    else:
                        await message.channel.send(
                            "**{}** is just chillin with a big **cock**/tight **puss**".format(memnames[ij]))
                except Exception:
                    await message.channel.send("**{}** is just chillin".format(memnames[ij]))

        elif 'party' in message.content:
            # global text_home_channel
            # global voice_home_channel
            # global text_channels_list
            # global voice_channels_list
            main_list = []
            for element in voice_channels_list:
                if element not in safe_channels:
                    main_list.append(element)

            # main_list = [item for item in voice_channels_list if item not in safe_channels]

            for i in main_list:
                memids = []  # ints
                memnames = []  # strings
                channelc = bot.get_channel(i)
                membersc = channelc.members  # Current members connected to the channel
                if len(membersc) > 0:
                    for member in membersc:
                        memnames.append(member.name)
                        memids.append(member.id)
            for ij in range(len(membersc)):
                await party(message, random.choice(membersc), random.choice(voice_channels_list))
                await message.channel.send("{}".format(random.choice(lennylist)))

        elif "nap @" in message.content:
            # global text_home_channel
            # global voice_home_channel
            # global text_channels_list
            # global voice_channels_list
            main_list = []
            for element in voice_channels_list:
                if element not in safe_channels:
                    main_list.append(element)
            # main_list = [item for item in VCLids if item not in safe_channels]
            SS = str("{}".format(message.content))
            SFA = SS.strip('nap ')
            removetable = str.maketrans('', '', '@#!%<>')
            removetableb = str.maketrans('', '', '0123456789')
            try:
                SFf = SFA.translate(removetable)
                SF = SFf.strip(" ")
                for i in main_list:
                    memids = []  # ints
                    memnames = []  # strings
                    channelc = bot.get_channel(i)
                    membersc = channelc.members  # Current members connected to the channel
                    if len(membersc) > 0:
                        for member in membersc:
                            memnames.append(member.name)
                            memids.append(member.id)
                        for ij in range(len(membersc)):
                            if str("{}".format(memnames[ij])) == str("{}".format(SF)):
                                await nap(message, membersc[ij])
                            else:

                                try:
                                    if memids[ij] == int(SF):
                                        await nap(message, membersc[ij])
                                    else:
                                        pass
                                except:
                                    pass
            except Exception:
                SFa = SFA.translate(removetable)
                SFf = SFa.translate(removetableb)
                SF = SFf.strip(" ")
                for i in main_list:
                    memids = []  # ints
                    memnames = []  # strings
                    channelc = bot.get_channel(i)
                    membersc = channelc.members  # Current members connected to the channel
                    if len(membersc) > 0:
                        for member in membersc:
                            memnames.append(member.name)
                            memids.append(member.id)
                        for ij in range(len(membersc)):
                            if str("{}".format(memnames[ij])) == str("{}".format(SF)):
                                await nap(message, membersc[ij])
                            else:

                                try:
                                    if memids[ij] == int(SF):
                                        await nap(message, membersc[ij])
                                    else:
                                        pass
                                except:
                                    pass

        elif 'nap' in message.content or "nap " in message.content:
            # global text_home_channel
            # global voice_home_channel
            # global text_channels_list
            # global voice_channels_list
            main_list = []
            for element in voice_channels_list:
                if element not in safe_channels:
                    main_list.append(element)
            # main_list = [item for item in voice_channels_list if item not in safe_channels]
            ctx = await bot.get_context(message)
            SS = str("{}".format(message.content))
            removetable2 = str.maketrans('', '', '@#%<>!')
            removetable2b = str.maketrans('', '', '0123456789')
            try:
                SFA = SS.strip('nap ')

                try:
                    SFf = SFA.translate(removetable2)
                    SF = SFf.strip(" ")
                    for ik in main_list:
                        memids2 = []  # ints
                        memnames2 = []  # strings
                        channeld = bot.get_channel(ik)
                        membersd = channeld.members  # Current members connected to the channel
                        if len(membersd) > 0:
                            for member2 in membersd:
                                memnames2.append(member2.name)
                                memids2.append(member2.id)
                            for il in range(len(membersd)):
                                if str("{}".format(memnames2[il])) == str("{}".format(SF)):
                                    await nap(message, membersd[il])
                                else:

                                    try:
                                        if memids2[il] == int(SF):
                                            await nap(message, membersd[il])
                                        else:
                                            pass
                                    except:
                                        pass
                except Exception:
                    SFa = SFA.translate(removetable2)
                    SFf = SFa.translate(removetable2b)
                    SF = SFf.strip(" ")
                    for ik in main_list:
                        memids2 = []  # ints
                        memnames2 = []  # strings
                        channeld = bot.get_channel(ik)
                        membersd = channeld.members  # Current members connected to the channel
                        if len(membersd) > 0:
                            for member2 in membersd:
                                memnames2.append(member2.name)
                                memids2.append(member2.id)
                            if str("{}".format(memnames2[il])) == str("{}".format(SF)):
                                await nap(message, membersd[il])
                            else:

                                try:
                                    if memids2[il] == int(SF):
                                        await nap(message, membersd[il])
                                    else:
                                        pass
                                except:
                                    pass

            except Exception:
                SFD = SS.strip('nap')
                try:
                    SF = SFD.translate(removetable2)
                    for ik in main_list:
                        memids2 = []  # ints
                        memnames2 = []  # strings
                        channeld = bot.get_channel(ik)
                        membersd = channeld.members  # Current members connected to the channel
                        if len(membersd) > 0:
                            for member2 in membersd:
                                memnames2.append(member2.name)
                                memids2.append(member2.id)
                            for il in range(len(membersd)):
                                if str("{}".format(memnames2[il])) == str("{}".format(SF)):
                                    await nap(message, membersd[il])
                                else:

                                    try:
                                        if memids2[il] == int(SF):
                                            await nap(message, membersd[il])
                                        else:
                                            pass
                                    except:
                                        pass
                except Exception:
                    SFd = SFD.translate(removetable2)
                    SFd = SFd.translate(removetable2b)
                    SF = SFd.strip(" ")
                    for ik in main_list:
                        memids2 = []  # ints
                        memnames2 = []  # strings
                        channeld = bot.get_channel(ik)
                        membersd = channeld.members  # Current members connected to the channel
                        if len(membersd) > 0:
                            for member2 in membersd:
                                memnames2.append(member2.name)
                                memids2.append(member2.id)
                            for il in range(len(membersd)):
                                if str("{}".format(memnames2[il])) == str("{}".format(SF)):
                                    await nap(message, membersd[il])
                                else:

                                    try:
                                        if memids2[il] == int(SF):
                                            await nap(message, membersd[il])
                                        else:
                                            pass
                                    except:
                                        pass

            for ik in main_list:
                memids2 = []  # ints
                memnames2 = []  # strings
                channeld = bot.get_channel(ik)
                membersd = channeld.members  # Current members connected to the channel
                if len(membersd) > 0:
                    for member2 in membersd:
                        memnames2.append(member2.name)
                        memids2.append(member2.id)
                    for il in range(len(membersd)):
                        if str("{}".format(memnames2[il])) == str("{}".format(SF)):
                            await nap(message, membersd[il])
                        else:
                            try:
                                if memids2[il] == int(SF):
                                    await nap(message, membersd[il])
                                else:
                                    pass
                            except:
                                pass

        elif 'seth' in message.content or 'Seth' in message.content:
            await message.channel.send("**{}** is just chillin with a big **cock**".format("Seth"))

        elif 'keck' in message.content or 'Keck' in message.content:
            await message.channel.send("**{}** is just chillin with a big **cock**".format("Mr keck jason"))

        elif 'hard' in message.content or 'gaming' in message.content:
            channel = bot.get_channel(message.author.voice.channel)  # gets the channel you want to get the list from

            members = channel.members  # finds members connected to the channel

            memids = []  # (list)
            for member in members:
                memids.append(member.name)
            for mm3 in memids:
                await message.channel.send(
                    "**{}** is **GAMING HARD** **{}** **{}** **{}**".format(mm3, random.choice(lennylist),
                                                                            random.choice(slist),
                                                                            random.choice(lennylist)))

        elif 'gma' in message.content:
            channel = bot.get_channel(voice_home_channel)  # gets the channel you want to get the list from

            members = channel.members  # finds members connected to the channel

            memids = []  # (list)
            for member in members:
                memids.append(member.name)
            for mm1 in memids:
                await message.channel.send("**{}** is **honestly** abusing the fuck out of their gma".format(mm1))

        elif 'twitch chat go wild' in message.content:
            x = message.guild.members
            xn = [xi.name for xi in x]
            tt = random.randint(1, 25)
            for xi in range(tt):
                await message.channel.send("**{}** YUH".format(random.choice(xn)))

        elif "nap time" in message.content or "gn bois" in message.content:
            ij = 0
            while ij < 5:
                await message.channel.send("travis be sleepin")  # Lol gn griffin
                ij += 1

        elif "yo griffin" in message.content:
            ij = 0
            while ij < 5:
                await message.channel.send("yo griffin get on the mfn disc")  # Lol get on the mfn disc
                ij += 1

        elif "the griffin" in message.content:
            ij = 0
            while ij < 5:
                await message.channel.send(
                    "ALL HAIL GRIFFIN, LE ROI DES GAIS, protektor of the posssums, " +
                    "HE WHO GO AHH, HAVER OF TATOOS, guys who crashers planes")  # Lol get on the mfn disc
                ij += 1

        elif "cock sucking fish" in message.content or "csf" in message.content:
            for i in voice_channels_list:
                memids = []  # ints
                memnames = []  # strings
                channelc = bot.get_channel(i)
                membersc = channelc.members  # Current members connected to the channel
                if len(membersc) > 0:
                    for member in membersc:
                        memnames.append(member.name)
                        memids.append(member.id)
            ijj = 0
            tt = [i for i in range(1, len(memids) + 1, 1)]
            while ijj <= random.choice(tt):
                await message.channel.send("{}{}{}{} is a **cock sucking fish**".format("<", "@", random.choice(memids),
                                                                                        ">"))  # Lol get on the mfn disc
                ijj += 1

        elif "bussy lickin fish" in message.content or "blf" in message.content:
            for i in voice_channels_list:
                memids = []  # ints
                memnames = []  # strings
                channelc = bot.get_channel(i)
                membersc = channelc.members  # Current members connected to the channel
                if len(membersc) > 0:
                    for member in membersc:
                        memnames.append(member.name)
                        memids.append(member.id)
            ijj = 0
            tt = [i for i in range(1, len(memids) + 1, 1)]
            while ijj <= random.choice(tt):
                await message.channel.send("{}{}{}{} is a **bussy lickin fish**".format("<", "@", random.choice(memids),
                                                                                        ">"))  # Lol get on the mfn disc
                ijj += 1

        elif "pussy lickin fish" in message.content or "plf" in message.content:
            for i in voice_channels_list:
                memids = []  # ints
                memnames = []  # strings
                channelc = bot.get_channel(i)
                membersc = channelc.members  # Current members connected to the channel
                if len(membersc) > 0:
                    for member in membersc:
                        memnames.append(member.name)
                        memids.append(member.id)
            ijj = 0
            tt = [i for i in range(1, len(memids) + 1, 1)]
            while ijj <= random.choice(tt):
                await message.channel.send("{}{}{}{} is a **pussy lickin fish**".format("<", "@", random.choice(memids),
                                                                                        ">"))  # Lol get on the mfn disc
                ijj += 1

        elif 'clear' in message.content or 'Clear' in message.content:
            ctxc = await bot.get_context(message)
            SS = str("{}".format(message.content))
            SF = SS.strip('clear ')

            try:
                # channels = bot.get_channel(text_home_channel)
                channels = ctxc.message.channel

                # print(channels, channelss.id)
                # print("1 {}".format(channels))
            except Exception:
                channels = ctxc.message.channel

                # print("2 {}".format(channels))

            try:
                SINT = int(SF)  # + 1
                SINTb = int(SF)

            except Exception:
                await message.channel.send("Input was not entered correctly, " +
                                           "argument after {} must be int value of desired messages to erase".format(
                                               "clear"))
            try:
                SINT = int(SF)  # + 1
                SINTb = int(SF)
                if SINTb % 5 == 0:
                    await channels.purge(limit=1)
                    while SINTb >= 5:
                        await channels.purge(limit=5)
                        SINTb -= 5
                else:
                    await channels.purge(limit=1)
                    while SINT >= 1:
                        await channels.purge(limit=1)
                        SINT -= 1
            except Exception:
                await message.channel.send("Couldn't find desired text channel.")

        elif "-p" in message.content:
            SS = str("{}".format(message.content))
            SF = SS.strip('-p ')
            params = {"format": "json", "url": SF}
            url = "https://www.youtube.com/oembed"
            query_string = urllib.parse.urlencode(params)
            url = url + "?" + query_string

            with urllib.request.urlopen(url) as response:
                response_text = response.read()
                data = json.loads(response_text.decode())
                ST = str(data['title'])
            if "Big Bootie" in ST or "big booty" in ST or "Big Booty" in ST:
                ij = 0
                while ij < 5:
                    await message.channel.send("Big booty time woop wopp")  # Lol Gz
                    ij += 1

        elif "-play" in message.content:
            SS = str("{}".format(message.content))
            SF = SS.strip('-p ')
            params = {"format": "json", "url": SF}
            url = "https://www.youtube.com/oembed"
            query_string = urllib.parse.urlencode(params)
            url = url + "?" + query_string

            with urllib.request.urlopen(url) as response:
                response_text = response.read()
                data = json.loads(response_text.decode())
                ST = str(data['title'])
            if "Big Bootie" in ST or "big booty" in ST or "Big Booty" in ST:
                ij = 0
                while ij < 5:
                    await message.channel.send("gz")  # Lol Gz
                    await message.channel.send("Big booty time woop wopp")  # Lol Gz
                    ij += 1

        elif "gz " in message.content:
            SS = str("{}".format(message.content))
            SF = SS.strip('gz ')
            try:
                try:
                    SI = int(SF)
                    totalgz[0] += SI
                    while totalgz[0] >= 1:
                        totalgz[0] -= 1
                        await message.channel.send("gz")
                except:
                    SI = float(SF)
                    F_str = "Argument after gz command needs to be type **int**. Argument is type **{}**".format(
                        type(SI))
                    await message.channel.send(F_str)

            except:
                SS = str("{}".format(message.content))
                SF = SS.strip('gz ')
                try:
                    SI = float(SF)
                    try:
                        SI = bool(SF)
                    except:
                        pass
                except:
                    SI = str(SF)
                SX = str("{}".format(type(SI)))
                SXXA = SX.replace("class ", "")
                SXXB = SXXA.replace("<", "")
                SXXC = SXXB.replace(">", "")
                SXXD = SXXC.replace("{}".format("'"), "")
                await message.channel.send(
                    "Argument after gz command needs to be type **int**. Argument is type **{}**".format(SXXD))

        elif 'Total' in message.content:
            await message.channel.send("**{}** gzs remaining.".format(totalgz[0]))
            if totalgz[0] < 0:
                totalgz[0] = 0

        elif "angler " in message.content or "angler" in message.content:
            try:
                SI = str("{}".format(message.content))
                SIF = ''.join(filter(str.isdigit, SI))
                SII = int(SIF)
                BASE_URL = 'http://services.runescape.com/m=itemdb_oldschool'
                URL = BASE_URL + '/api/catalogue/detail.json?item='
                items = [13439]
                prices = []
                names = []
                for it in items:
                    final_url = URL + str(it)
                    urllibcall = urllib.request.urlopen(final_url)
                    data = json.loads(urllibcall.read().decode())
                    with urllib.request.urlopen(final_url) as url:
                        price = data["item"]["current"]["price"]
                        NAME = data["item"]["name"]
                        names.append(NAME)
                        prices.append(price)
                pp = str(prices[0])
                ppp = pp.replace(',', '')
                totalp = float(SII) * int(ppp)
                Tp = int(totalp)

                await message.channel.send("{} price: {}".format(names[0], prices[0]))  # Anglerfish prices
                await message.channel.send("Total gp: {}".format(format(Tp, ",")))

            except Exception:
                SS = str("{}".format(message.content))
                SF = SS.strip('angler ')
                SX = str("{}".format(type(SF)))
                SXXA = SX.replace("class ", "")
                SXXB = SXXA.replace("<", "")
                SXXC = SXXB.replace(">", "")
                SXXD = SXXC.replace("{}".format("'"), "")
                removetable3 = str.maketrans('', '', '@#%<>{}cla'.format("'"))
                SXXF = SXXA.translate(removetable3)
                SXXXF = SXXF.replace("ss ", "")
                await message.channel.send("Argument after gz command needs to be type **int**. " +
                                           "Argument is type **{}**".format(SXXD))



    await bot.process_commands(message)  # Always put this at the bottom of on_message to make commands work properly

bot.run(token)

client.run(token)
