import discord
from discord.ext import commands
from discord import FFmpegPCMAudio
from discord_components import Button, ButtonStyle, Select, SelectOption
from discord.utils import get as getvoice
import yt_dlp as youtube_dl
import asyncio
from async_timeout import timeout
from functools import partial
import itertools
import random
import copy

######################################################################################

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
    'source_address': '0.0.0.0', # bind to ipv4 since ipv6 addresses cause issues sometimes\
    'geo_bypass_country':'TH',
    # 'proxy':'101.109.245.200:4153'
}

ytdl5_format_options = {
    'format': 'bestaudio/best',
    'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'ytsearch5',
    'source_address': '0.0.0.0', # bind to ipv4 since ipv6 addresses cause issues sometimes\
    'requested_entries' : 5,
    'geo_bypass_country':'TH',
    # 'proxy':'180.180.152.98:4145'
}

ffmpeg_options = {
    'options': "-vn",
    "before_options": "-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5"#, ## song will end if no this line
    #"after_options" : "firequalizer=gain_entry='entry(0,-23);entry(250,-11.5);entry(1000,0);entry(4000,8);entry(16000,16)'"
}

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)
ytdl5 = youtube_dl.YoutubeDL(ytdl5_format_options)

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
    async def create_source(cls, ctx, search: str, *, loop, download=False, chat=True):
        loop = loop or asyncio.get_event_loop()

        to_run = partial(ytdl.extract_info, url=search, download=download)

        try:
            data = await loop.run_in_executor(None, to_run)
        except:
            await ctx.message.delete()
            print("Video Error")
            data = await loop.run_in_executor(None, to_run)
        else:
            await ctx.message.delete()
        if 'entries' in data:
            # take first item from a playlist
            data = data['entries'][0]

        if chat:
            print(data['thumbnail'])
            emBed = discord.Embed(title=f'Queued', description=f'**[{data["title"]}]({data["webpage_url"]})**')
            emBed.set_thumbnail(url=data['thumbnail'])
            await ctx.send(embed=emBed, delete_after=10)
            # await ctx.send(f'```ini\nเพิ่ม [{data["title"]}] โดย {ctx.author.name}\n```', delete_after=10) #delete after can be added


        if download:
            source = ytdl.prepare_filename(data)
        else:
            return {'webpage_url': data['webpage_url'], 'requester': ctx.author, 'title': data['title']}
        print(source)
        return cls(discord.FFmpegPCMAudio(source, **ffmpeg_options), data=data, requester=ctx.author)

    @classmethod
    async def select_source(cls, ctx, search: str, *, loop, download=False, chat=True):
        def check(context):
            if context.author == ctx.author:
                if context.content in ["1","2","3","4","5"]:
                    return True
            return False

        loop = loop or asyncio.get_event_loop()

        to_run = partial(ytdl5.extract_info, url=search, download=download)
        data = await loop.run_in_executor(None, to_run)

        if 'entries' in data:
            # take first item from a
            playlist = data['entries'][:5]
            name = [f"{n+1}.{e['title']}" for n, e in enumerate(playlist)]
            emBed = discord.Embed(title="Select one", description="\n".join(name))
            song_select = await ctx.send(embed=emBed)

        try:
            msg = await ctx.bot.wait_for('message', check=check, timeout=30)
            data = data['entries'][int(msg.content)-1]
            await msg.delete()
        except TimeoutError:
            data = data['entries'][0]

        await song_select.delete()

        if chat:
            await ctx.send(f'```ini\nเพิ่ม [{data["title"]}] โดย {ctx.author.name}\n```', delete_after=10) #delete after can be added

        if download:
            source = ytdl.prepare_filename(data)
        else:
            return {'webpage_url': data['webpage_url'], 'requester': ctx.author, 'title': data['title']}
        print(source)
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

    __slots__ = ('bot', '_guild', '_channel', '_cog', 'queue', 'next', 'current', 'np', 'volume', 'music_loop', 'ctx', 'last_play')

    def __init__(self, ctx):
        self.ctx = ctx
        self.bot = ctx.bot
        self._guild = ctx.guild
        self._channel = ctx.channel
        self._cog = ctx.cog

        self.queue = asyncio.Queue()
        self.next = asyncio.Event()

        self.np = None  # Now playing message
        self.volume = .5
        self.current = None
        self.music_loop = False

        ctx.bot.loop.create_task(self.player_loop())

    async def player_loop(self):
        """create button callback"""
        async def callback(interaction):
            guild_click = self.bot.get_guild(interaction.guild_id)
            channel_click = getvoice(guild_click.channels, id=interaction.channel_id)
            voice_client = getvoice(self.bot.voice_clients, guild=guild_click)

            try:
                clicker = interaction.author.voice.channel

            except AttributeError:
                return await interaction.send("อย่าไปกดของคนอื่นสิ")


            print(f"{interaction.author.name} click {interaction.custom_id}")

            if not hasattr(voice_client, "channel"):
                return await interaction.message.delete()

            if clicker == voice_client.channel:

                if interaction.custom_id == "queue":
                    player = YoutubePlay.players[interaction.guild.id]
                    if player.queue.empty():
                        return await interaction.send('ตอนนี้คิวว่าง')
                    # 1 2 3
                    upcoming = list(itertools.islice(player.queue._queue,0,player.queue.qsize()))
                    fmt = '\n'.join(f'**`{_["title"]}`**' for _ in upcoming)
                    embed = discord.Embed(title=f'Upcoming - Next {len(upcoming)}', description=fmt)
                    await interaction.send(embed=embed)
                    #########################################
                else:
                    await interaction.edit_origin()
                    # if interaction.custom_id == "pause":
                    #     voice_client.pause()
                    #     await channel_click.send(f'**`{interaction.author.name}`**: หยุดเพลง', delete_after=20)
                        #########################################
                    if interaction.custom_id == "resume":
                        try:
                            playing = getvoice(self.bot.voice_clients, guild=self._guild).is_playing()
                            if not playing:
                                voice_client.resume()
                                await channel_click.send(f'**`{interaction.author.name}`**: เล่นเพลงต่อ', delete_after=20)
                            else:
                                voice_client.pause()
                                await channel_click.send(f'**`{interaction.author.name}`**: หยุดเพลง', delete_after=20)
                        except Exception as e:
                            await channel_click.send(f"[ERROR] {e}")
                        #########################################
                    elif interaction.custom_id == "loop":
                        if self.music_loop == False:
                            self.music_loop = True
                            await self._channel.send("Now Looping", delete_after=3)
                        else:
                            self.music_loop = False
                            await self._channel.send("Loop stopped", delete_after=3)
                        ###########################################
                    elif interaction.custom_id == "skip":
                        voice_client.stop()
                        await channel_click.send(f'**`{interaction.author.name}`**: ข้ามเพลง', delete_after=20)
                        #########################################
                    elif interaction.custom_id == "leave":
                        self.music_loop = False
                        try:
                            await voice_client.disconnect()
                        except AttributeError:
                            pass

                        try:
                            del YoutubePlay.players[guild_click.id]
                        except KeyError:
                            pass
                        #########################################

            else:
                await interaction.send("อย่าไปกดของคนอื่นสิ")

        """Our main player loop."""
        await self.bot.wait_until_ready()

        while not self.bot.is_closed():

            # await self._channel.send(self.next)

            self.next.clear()

            try:
                # Wait for the next song. If we timeout cancel the player and disconnect...
                async with timeout(180):  # 3 minutes...
                    source = await self.queue.get()
                    self.last_play = copy.copy(source)
            except asyncio.TimeoutError:
                # del players[self._guild.id]
                # return await self.destroy(self._guild)

                try:
                    playing = getvoice(self.bot.voice_clients, guild=self._guild).is_playing()
                    if not playing and not hasattr(self.current, 'title'):
                        print("Queue empty 2")
                        return await self.destroy(self._guild)
                    else:
                        continue

                except AttributeError:
                    print("Queue empty 1")
                    return await self.destroy(self._guild)

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

            try:
                self._guild.voice_client.play(source, after=lambda _: self.bot.loop.call_soon_threadsafe(self.next.set))
            except AttributeError:
                voice_client = getvoice(self.bot.voice_clients, guild=self._guild)
                try:
                    channel = self.ctx.author.voice.channel
                except AttributeError:
                    await ctx.send("เข้าห้องก่อนครับ", delete_after=7)
                    return

                if voice_client == None:
                    await channel.connect()
                    voice_client = getvoice(self.bot.voice_clients, guild=self._guild)

                voice_client.play(source, after=lambda _: self.bot.loop.call_soon_threadsafe(self.next.set))

            if self.np == None:
                self.np = await self._channel.send(
                    f'**กำลังเล่น : ** {source.web_url}',
                    components=[[
                        self.bot.components_manager.add_callback(
                            Button(style=ButtonStyle.green, label="PLAY/PAUSE", custom_id="resume"),callback
                        ),
                        # self.bot.components_manager.add_callback(
                        #     Button(style=ButtonStyle.grey, label="PAUSE", custom_id="pause"),callback
                        # ),
                        self.bot.components_manager.add_callback(
                            Button(style=ButtonStyle.blue, label="SKIP", custom_id="skip"),callback
                        ),
                        self.bot.components_manager.add_callback(
                            Button(style=ButtonStyle.red, label="LEAVE", custom_id="leave"),callback
                        ),
                        self.bot.components_manager.add_callback(
                            Button(style=ButtonStyle.grey, label="QUEUE", custom_id="queue"),callback
                        ),
                        self.bot.components_manager.add_callback(
                            Button(style=ButtonStyle.grey, label="LOOP", custom_id="loop"),callback
                        )
                    ]
                    # ,[
                    #     self.bot.components_manager.add_callback(
                    #         Button(style=ButtonStyle.grey, label="LOOP", custom_id="loop"),callback
                    #     ),
                    # ]
                    ]
                )

            # await self._channel.send(source.title)
            await self.next.wait()

            if self.music_loop == True:
                await self.queue.put(self.last_play)
            # Make sure the FFmpeg process is cleaned up.
            source.cleanup()
            self.current = None

            try:
                # We are no longer playing this song...
                if self.music_loop and False:
                    pass
                else:
                    await self.np.delete()
                    self.np = None
            except discord.HTTPException:
                print("error")
                pass

    async def destroy(self, guild):
        """Disconnect and cleanup the player."""
        try:
            await self._guild.voice_client.disconnect()
        except Exception as e:
            print(e)
        else:
            print("cleaned here")
            return self.bot.loop.create_task(self._cog.cleanup(guild))

############################################################################################################

class YoutubePlay(commands.Cog):
    players = {}

    def __init__(self, bot):
        self.bot = bot

    def get_player(self, ctx):
        try:
            player = YoutubePlay.players[ctx.guild.id]
        except KeyError:
            player = MusicPlayer(ctx)
            YoutubePlay.players[ctx.guild.id] = player

        return player

    async def cleanup(self, guild):
        print("cleaned")
        try:
            await guild.voice_client.disconnect()
        except AttributeError:
            pass

        try:
            del YoutubePlay.players[guild.id]
        except KeyError:
            pass

    @commands.command(aliases=["p"])
    async def play(self, ctx, *, search=None):

        if search == None:
            text = await ctx.channel.fetch_message(ctx.message.reference.message_id)
            search = text.content

        voice_client = getvoice(self.bot.voice_clients, guild=ctx.guild)
        try:
            channel = ctx.author.voice.channel
        except AttributeError:
            await ctx.send("เข้าห้องก่อนครับ", delete_after=7)
            return

        if voice_client == None:
            await channel.connect()
            voice_client = getvoice(self.bot.voice_clients, guild=ctx.guild)

        await ctx.trigger_typing()

        _player = self.get_player(ctx)

        if "open.spotify.com" in search:
            await ctx.send("อาจจะไม่เจอเพลงบ้างนะงับ", delete_after=7)
            from spotify_track import get_name, get_episode, get_playlist
            if "track" in search:
                search = get_name(search)

            elif "episode" in search:
                search = get_episode(search)

            elif "playlist" in search:
                playlist = get_playlist(search)
                await ctx.send(f"Playlist : {playlist['playlist_name']}", delete_after=180)
                for song in playlist['tracks']:
                    source = await YTDLSource.create_source(ctx, song, loop=self.bot.loop, download=False, chat=False)
                    print(f"{source['webpage_url']} from {source['requester']}")
                    await _player.queue.put(source)
                _player.music_loop = False
                await ctx.message.delete()
                return

        source = await YTDLSource.create_source(ctx, search, loop=self.bot.loop, download=False)

        print(f"{source['webpage_url']} from {source['requester']}")
        await _player.queue.put(source)
        _player.music_loop = False

    @commands.command(aliases=["tp"])
    async def testplay(self, ctx, *, search: str):
        voice_client = getvoice(self.bot.voice_clients, guild=ctx.guild)
        try:
            channel = ctx.author.voice.channel
        except AttributeError:
            await ctx.send("เข้าห้องก่อนครับ", delete_after=7)
            return

        if voice_client == None:
            await channel.connect()
            voice_client = getvoice(self.bot.voice_clients, guild=ctx.guild)

        await ctx.trigger_typing()

        _player = self.get_player(ctx)
        source = await YTDLSource.select_source(ctx, search, loop=self.bot.loop, download=False)

        print(f"{source['webpage_url']} from {source['requester']}")
        await _player.queue.put(source)
        await ctx.message.delete()
        _player.music_loop = False

    @commands.command()
    async def join(self, ctx):
        try:
            target = ctx.message.author.voice.channel
        except:
            target = None
        voice = getvoice(self.bot.voice_clients, guild=ctx.guild)
        if target and voice:
            await voice.move_to(target)
        elif not target:
            print(2)
            await ctx.send("เข้าห้องก่อนซิ")
        else:
            print(3)
            await target.connect()
        await ctx.message.delete()

    @commands.command()
    async def leave(self, ctx):
        _player = self.get_player(ctx)
        _player.music_loop = False
        await ctx.message.delete()
        try:
            voice_client = getvoice(self.bot.voice_clients, guild=ctx.guild)
        except AttributeError:
            await ctx.send("ยัง", delete_after=5)
            return

        try:
            _user = ctx.author.voice.channel

            if voice_client.channel == _user:
                await self.cleanup(ctx.guild)

            else:
                await ctx.send(f"อย่าไปกดของคนอื่นซิ {ctx.author.mention}", delete_after=5)
                return

        except AttributeError:
            await ctx.send(f"เข้ามาก่อน {ctx.author.mention}", delete_after=5)


    @commands.command()
    async def stop(self, ctx):
        try:
            voice_client = getvoice(self.bot.voice_clients, guild=ctx.guild)
        except AttributeError:
            await ctx.send("ยัง", delete_after=5)
            return

        try:
            _user = ctx.author.voice.channel

            if voice_client.channel == _user:
                try:
                    del YoutubePlay.players[guild.id]
                except KeyError:
                    pass
                else:
                    await voice_client.stop()

            else:
                await ctx.send(f"อย่าไปกดของคนอื่นซิ {ctx.author.mention}", delete_after=5)
                return

        except AttributeError:
            await ctx.send(f"เข้ามาก่อน {ctx.author.mention}", delete_after=5)
        finally :
            await ctx.message.delete()

    @commands.command()
    async def pause(self, ctx):
        voice_client = getvoice(self.bot.voice_clients, guild=ctx.guild)
        if voice_client == None:
            await ctx.send("ยัง")
            return

        if voice_client.channel != ctx.author.voice.channel:
            await ctx.send("ไม่")
            return

        voice_client.pause()
        await ctx.message.delete()

    @commands.command()
    async def resume(self, ctx):
        voice_client = getvoice(self.bot.voice_clients, guild=ctx.guild)
        if voice_client == None:
            await ctx.send("ยัง")
            return

        if voice_client.channel != ctx.author.voice.channel:
            await ctx.send("ไม่")
            return
        voice_client.resume()
        await ctx.message.delete()

    @commands.command(aliases=["queue", "queuelist", "q", "Q"])
    async def queueList(self, ctx):
        voice_client = getvoice(self.bot.voice_clients, guild=ctx.guild)

        if voice_client == None or not voice_client.is_connected():
            await ctx.channel.send("ยังไม่ทันเข้าเลย", delete_after=10)
            return

        player = self.get_player(ctx)
        if player.queue.empty():
            return await ctx.send('ตอนนี้คิวว่าง')

        # 1 2 3
        upcoming = list(itertools.islice(player.queue._queue,0,player.queue.qsize()))
        fmt = '\n'.join(f'**`{_["title"]}`**' for _ in upcoming)
        embed = discord.Embed(title=f'Upcoming - Next {len(upcoming)}', description=fmt)
        await ctx.send(embed=embed)
        await ctx.message.delete()

    @commands.command()
    async def skip(self, ctx):
        voice_client = getvoice(self.bot.voice_clients, guild=ctx.guild)

        if voice_client == None or not voice_client.is_connected():
            await ctx.channel.send("ยังไม่ทันเข้าเลย", delete_after=10)
            return

        if voice_client.is_paused():
            pass
        elif not voice_client.is_playing():
            return

        voice_client.stop()
        await ctx.send(f'**`{ctx.author}`**: ข้ามเพลง')
        await ctx.message.delete()

    @commands.command(aliases=["guild", "playing"])
    async def guild_players(self, ctx):
        _player = self.get_player(ctx)
        await ctx.send(dir(YoutubePlay.players[ctx.guild.id].eq))

    @commands.command()
    async def refresh(self, ctx):
        try:
            voice_client = getvoice(self.bot.voice_clients, guild=ctx.guild)
            await voice_client.stop()
            await voice_client.disconnect()
        except:
            pass
        YoutubePlay.players[ctx.guild.id] = MusicPlayer(ctx)
        await ctx.send("refreshing...", delete_after=5)
        #await ctx.send(dir(YoutubePlay.players[ctx.guild.id]))
        await ctx.message.delete()

    @commands.command()
    async def loop(self, ctx):
        _player = self.get_player(ctx)
        if _player.music_loop == False:
            _player.music_loop = True
            await ctx.send("Now Looping")
        else:
            _player.music_loop = False
            await ctx.send("Loop stoped")
        await ctx.message.delete()


################################  shouting #################################################
    async def shout(self, ctx, shouting:str):
        voice_client = getvoice(self.bot.voice_clients, guild=ctx.guild)
        try:
            channel = ctx.author.voice.channel
        except AttributeError:
            await ctx.send("เข้าห้องก่อนครับ", delete_after=3)
            return

        if voice_client == None:
            await channel.connect()

        voice_client = getvoice(self.bot.voice_clients, guild=ctx.guild)
        _player = self.get_player(ctx)


        if not voice_client.is_playing():
            try:
                playing = _player.current.title()
            except:
                playing = None

            if (playing != None) or (not _player.queue.empty()):
                await ctx.send("ไม่ว่าง", delete_after=3)
                return
            else:
                source = await YTDLSource.create_source(ctx, shouting, loop=self.bot.loop, download=False, chat=False)
                print(source)
                await _player.queue.put(source)

        else:
            await ctx.send("ไม่ว่าง", delete_after=3)

        await ctx.message.delete()


    @commands.command()
    async def amogus(self, ctx):
        await self.shout(ctx, "https://www.youtube.com/watch?v=2FfSu_B2_-8&ab_channel=TheBarman")

    @commands.command()
    async def thomas(self, ctx):
        await self.shout(ctx, "https://www.youtube.com/watch?v=-jEIfaPbUXk&ab_channel=No_MercYfdgdhfhdf")

    @commands.command()
    async def alarm(self, ctx):
        await self.shout(ctx, "https://www.youtube.com/watch?v=3A6CDFmknio&ab_channel=LegoJKL")

    @commands.command()
    async def boo(self, ctx):
        await self.shout(ctx, "https://www.youtube.com/watch?v=bDFa_K9PDUA&ab_channel=AlanGrant")

    @commands.command()
    async def cotton(self, ctx):
        await self.shout(ctx, "https://youtu.be/s8YJD-7LEsU")

def setup(bot):
    bot.add_cog(YoutubePlay(bot))
