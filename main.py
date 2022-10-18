#author wildan phidrai-ngam
#self study project
import discord
from discord.utils import get
from discord import FFmpegPCMAudio
import youtube_dl
import asyncio
from async_timeout import timeout
from functools import partial
from discord.ext import commands
import itertools

bot = commands.Bot(command_prefix='/', intents=discord.Intents.all(),help_command=None)

# Bot arived!
@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

# บอกคำสั่งทั้งหมด
@bot.command()
async def help(ctx):
    emBed = discord.Embed(title="คำสั่ง!",description="แสดงผลคำสั่งทั้งหมด",color=0xFE6F5E)
    emBed.add_field(name="/help", value="คำสั่งทั้งหมด", inline="False")
    emBed.add_field(name="/music", value="คำสั่งร้องเพลงทั้งหมด", inline="False")
    emBed.add_field(name="/hello", value="ทักทายนายข้า", inline="False")
    emBed.add_field(name="/say", value="นายข้าอยากให้ข้าน้อยพูดว่า...", inline="False")
    emBed.add_field(name="/leave", value="เตะข้าน้อยออกจากห้อง", inline="False")
    emBed.set_thumbnail(url='https://static.wikia.nocookie.net/tensei-shitara-slime-datta-ken/images/c/cf/Diablo_Demon_Peer_Anime.png/revision/latest?cb=20210905033415')
    emBed.set_footer(text="IKUZO101", icon_url='https://img.wattpad.com/d77e6d3447dfa755cf818235aaec7a031bbd7ca1/68747470733a2f2f73332e616d617a6f6e6177732e636f6d2f776174747061642d6d656469612d736572766963652f53746f7279496d6167652f5848447069787237564f69454d773d3d2d3739373835393635372e313564303934663636633965626562373332353738383337313132342e6a7067?s=fit&w=720&h=720')
    await ctx.channel.send(embed=emBed)

# บอกคำสั่งเล่นเพลงทั้งหมด
@bot.command()
async def music(ctx):
    emBed = discord.Embed(title="คำสั่งร้องเพลง", description="แสดงผลคำสั่งเพลงทั้งหมด", color=0xc48bd0)
    emBed.add_field(name="/p", value="ข้าน้อยร้องเพลง", inline="False")
    emBed.add_field(name="/stop", value="หยุดเพลงถาวร", inline="False")
    emBed.add_field(name="/pause", value="หยุดเพลงชั่วคราว", inline="False")
    emBed.add_field(name="/resume", value="เริ่มเพลง", inline="False")
    emBed.add_field(name="/skip", value="ข้ามเพลง", inline="False")
    emBed.add_field(name="/queue", value="คิวเพลง", inline="False")
    emBed.set_thumbnail(url='https://static.wikia.nocookie.net/tensei-shitara-slime-datta-ken/images/c/cf/Diablo_Demon_Peer_Anime.png/revision/latest?cb=20210905033415')
    emBed.set_footer(text="IKUZO101", icon_url='https://img.wattpad.com/d77e6d3447dfa755cf818235aaec7a031bbd7ca1/68747470733a2f2f73332e616d617a6f6e6177732e636f6d2f776174747061642d6d656469612d736572766963652f53746f7279496d6167652f5848447069787237564f69454d773d3d2d3739373835393635372e313564303934663636633965626562373332353738383337313132342e6a7067?s=fit&w=720&h=720')
    await ctx.channel.send(embed=emBed)

# คำสั่ง /say
@bot.command()
async def say(ctx, *, par):
    await ctx.channel.send("นายท่านสั่งให้ข้าน้อยพูดว่า {0}".format(par))

#ให้บอทตอบกลับ
@bot.event
async def on_message(message):
    if message.content == '/hello':
        await message.channel.send('ยินดีที่ได้รับใช้นายท่าน ' + str(message.author.name) + ' ข้าน้อยมีนามว่า ' + str(
            bot.user.name))
    elif message.content == '/exit':
        await bot.logout()
    await bot.process_commands(message)

##############################################################

youtube_dl.utils.bug_reports_message = lambda: ''

ytdl_format_options = {
    'format': 'bestaudio/best',
    'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0'  # bind to ipv4 since ipv6 addresses cause issues sometimes
}

ffmpeg_options = {
    'options': '-vn',
    "before_options": "-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5"
}

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)


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

        await ctx.send(f'```ini\n[✅ เพิ่มเพลง {data["title"]} ไว้ในคิว]\n```')  # delete after can be added

        if download:
            source = ytdl.prepare_filename(data)
        else:
            return {'webpage_url': data['webpage_url'], 'requester': ctx.author, 'title': data['title']}

        return cls(discord.FFmpegPCMAudio(source, **ffmpeg_options), data=data, requester=ctx.author)

    @classmethod
    async def regather_stream(cls, data, *, loop):
        """Used for preparing a stream, instead of downloading.
        Since Youtube Streaming links expire."""
        loop = loop or asyncio.get_event_loop()
        requester = data['requester']

        to_run = partial(ytdl.extract_info, url=data['webpage_url'], download=False)
        data = await loop.run_in_executor(None, to_run)

        return cls(discord.FFmpegPCMAudio(data['url'], **ffmpeg_options), data=data, requester=requester)


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
                del players[self._guild]
                return await self.destroy(self._guild)

            if not isinstance(source, YTDLSource):
                # Source was probably a stream (not downloaded)
                # So we should regather to prevent stream expiration
                try:
                    source = await YTDLSource.regather_stream(source, loop=self.bot.loop)
                except Exception as e:
                    await self._channel.send(f'❌ เกิดข้อผิดพลาดในการประมวลผลเพลง\n'
                                             f'```css\n[{e}]\n```')
                    continue

            source.volume = self.volume
            self.current = source

            self._guild.voice_client.play(source, after=lambda _: self.bot.loop.call_soon_threadsafe(self.next.set))
            self.np = await self._channel.send(f'**🔊 กำลังเล่นเพลง : ** `{source.title}` เปิดโดยนายท่าน '
                                               f'`{source.requester}`')
            await self.next.wait()

            # Make sure the FFmpeg process is cleaned up.
            source.cleanup()
            self.current = None

            try:
                # We are no longer playing this song...
                await self.np.delete()
            except discord.HTTPException:
                pass

    async def destroy(self, guild):
        """Disconnect and cleanup the player."""
        del players[self._guild]
        await self._guild.voice_client.disconnect()
        return self.bot.loop.create_task(self._cog.cleanup(guild))

#######################################################################

# เพลง
@bot.command()
async def p(ctx, *, search: str):  # เล่นเพลง
    channel = ctx.author.voice.channel
    voice_client = get(bot.voice_clients, guild=ctx.guild)

    if voice_client == None:
        await ctx.channel.send("🎤 น้องเมดเริ่มร้องเพลง!")
        await channel.connect()
        voice_client = get(bot.voice_clients, guild=ctx.guild)
    await ctx.trigger_typing()

    _player = get_player(ctx)
    source = await YTDLSource.create_source(ctx, search, loop=bot.loop, download=False)
    await _player.queue.put(source)

players = {}

def get_player(ctx):
    try:
        player = players[ctx.guild.id]
    except:
        player = MusicPlayer(ctx)
        players[ctx.guild.id] = player
    return player

# หยุดเพลงถาวร
@bot.command()
async def stop(ctx):
    voice_client = get(bot.voice_clients, guild=ctx.guild)
    if voice_client == None:
        await ctx.channel.send("หยุดเพลง")
        return
    if voice_client.channel != ctx.author.voice.channel:
        await ctx.channel.send("📢 น้องเมดอยู่ห้อง {0}".format(voice_client.channel) + " ไม่สามารถหยุดเพลงได้!")
        return
    voice_client.stop()

# หยุดเพลงชั่วคราว
@bot.command()
async def pause(ctx):
    voice_client = get(bot.voice_clients, guild=ctx.guild)
    if voice_client == None:
        await ctx.channel.send("หยุดเพลง")
        return
    if voice_client.channel != ctx.author.voice.channel:
        await ctx.channel.send("📢 น้องเมดอยู่ห้อง {0}".format(voice_client.channel) + " ไม่สามารถหยุดเพลงชั่วคราวได้!")
        return
    voice_client.pause()

# เริ่มเพลงเดิม
@bot.command()
async def resume(ctx):
    voice_client = get(bot.voice_clients, guild=ctx.guild)
    if voice_client == None:
        await ctx.channel.send("เริ่มเพลง")
        return
    if voice_client.channel != ctx.author.voice.channel:
        await ctx.channel.send("📢 น้องเมดอยู่ห้อง {0}".format(voice_client.channel) + " ไม่สามารถเริ่มเพลงได้!")
        return
    voice_client.resume()

# คิวเพลง
@bot.command()
async def queue(ctx):
    voice_client = get(bot.voice_clients, guild=ctx.guild)
    if voice_client == None or not voice_client.is_connected():
        await ctx.channel.send("คิวเพลง", delete_after=10)
        return
    player = get_player(ctx)
    if player.queue.empty():
        return await ctx.send('❌ ไม่มีเพลงในคิว')

    upcoming = list(itertools.islice(player.queue._queue, 0, player.queue.qsize()))
    fmt = '\n'.join(f'**`{_["title"]}`**' for _ in upcoming)
    embed = discord.Embed(title=f'เพลงในคิว {len(upcoming)} เพลง', description=fmt)
    await ctx.send(embed=embed)

# ข้ามเพลง
@bot.command()
async def skip(ctx):
    voice_client = get(bot.voice_clients, guild=ctx.guild)
    if voice_client == None or not voice_client.is_connected():
        await ctx.channel.send("ข้ามเพลง", delete_after=10)
        return
    if voice_client.is_paused():
        pass
    elif not voice_client.is_playing():
        return
    voice_client.stop()
    await ctx.send(f'**`{ctx.author}`** : ข้ามเพลง!')

# เอาบอทออก
@bot.command()
async def leave(ctx):
    del players[ctx.guild.id]
    await ctx.voice_client.disconnect()

bot.run('#ใส่ token here')
