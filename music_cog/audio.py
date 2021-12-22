import asyncio
from nextcord.errors import ClientException
from src.utility import msg
import youtube_dl
import pafy
import nextcord

from src import goldy_func, goldy_error, goldy_cache

from .platforms import youtube
from . import msg as music_msg
from .. import music as ext #Music Cog

goldy_cache.main_cache_object["goldy_music"] = {}

"""
Audio: The module that offers methods like playing audio and vc join/leave functions.
"""

class goldy():

    @staticmethod
    async def join_vc(ctx): #Goldy Bot joins the vc your connected to.
        #Checks if member is in vc.
        if ctx.author.voice == None:
            await ctx.send((music_msg.music.error.you_not_in_vc).format(ctx.author.mention))
            return False

        if not ctx.voice_client == None: #Checks if bot is already in another vc.
            if not ctx.voice_client.channel == ctx.author.voice.channel:
                await ctx.voice_client.disconnect()

        if ctx.voice_client == None:
            await ctx.author.voice.channel.connect()

        return ctx.voice_client

    @staticmethod
    async def leave_vc(ctx): #Goldy Bot leaves the vc it is connected to.
        if not ctx.voice_client == None: #Disconnects if goldy bot is in a vc.
            ctx.voice_client.pause()
            await ctx.voice_client.disconnect()
            return True
        else:
            await ctx.send((music_msg.music.error.not_connected_to_vc).format(ctx.author.mention))

    class checks():
        @staticmethod
        async def in_vc(ctx): #Checks if goldy bot is already in a vc in the guild.
            if ctx.voice_client.source == None:
                return False #Goldy is not in vc.
            else:
                return True #Goldy is in vc.

class song(): #Class that creates song object.
    def __init__(self, ctx, url, stream_object):
        self.ctx = ctx
        self.url = url
        self.platform = stream_object.platform
        self.name = stream_object.title
        self.duration = stream_object.duration
        self.thumbnail = stream_object.thumbnail
        self.stream_object = stream_object

class queue():
    def __init__(self, ctx):
        self.ctx = ctx
        try: #Test to see if cache exists.
            goldy_cache.main_cache_object["goldy_music"][ctx.guild.id]
            goldy_cache.main_cache_object["goldy_music"][ctx.guild.id]["song_queue"]
        except KeyError:
            goldy_func.print_and_log("info", f"[{ext.cog_name}] Created queue for '{ctx.guild.name}'.")
            goldy_cache.main_cache_object["goldy_music"][ctx.guild.id] = {}
            goldy_cache.main_cache_object["goldy_music"][ctx.guild.id]["song_queue"] = [] #Creates queue for guild if there isn't already.

    async def get(self): #Returns the actual song queue itself.
        return goldy_cache.main_cache_object["goldy_music"][self.ctx.guild.id]["song_queue"]

    async def add(self, song_object:song): #Adds a song to queue.
        song = song_object
        goldy_cache.main_cache_object["goldy_music"][song.ctx.guild.id]["song_queue"].append(song)

    async def remove(self, song_object:song): #Remove a specific song.
        song = song_object
        goldy_cache.main_cache_object["goldy_music"][song.ctx.guild.id]["song_queue"].remove(song)
        #Work in progress

    async def remove_first(self): #Removes first song in the queue.
        goldy_cache.main_cache_object["goldy_music"][self.ctx.guild.id]["song_queue"].pop(0)

    @property
    def length(self): #Returns amount songs left in queue.
        return len(goldy_cache.main_cache_object["goldy_music"][self.ctx.guild.id]["song_queue"])

class player: #Goldy Bot player class, an instence of this is made whenever music is needed to be played in a vc.
    def __init__(self, ctx, client, voice_client, queue:queue):
        self.ctx = ctx
        self.client = client
        self.voice_client = voice_client #The Discord voice connection.
        self.queue = queue #The queue of songs to play.

        self.checks = self._checks(voice_client) #Checks class
        
        try:
            goldy_cache.main_cache_object["goldy_music"][ctx.guild.id]["player_instance"]
        except KeyError:
            goldy_cache.main_cache_object["goldy_music"][ctx.guild.id]["player_instance"] = self

        if not voice_client.is_playing() == True: #Unpauses music if paused.
            if voice_client.is_paused():
                voice_client.resume()

    class _checks():
        def __init__(self, voice_client):
            self.voice_client = voice_client

        async def is_playing(self): #Checks if a song is already playing.
            if self.voice_client.is_playing(): return True
            else: return False

        async def is_paused(self): #Checks if a song is already playing.
            if self.voice_client.is_paused(): return True
            else: return False

    async def play(self, stream_object): #Play stream object.
        try:
            if not await self.checks.is_paused(): #Checking if any song is currently playing.
                loop = asyncio.get_event_loop()
                self.ctx.voice_client.play(nextcord.PCMVolumeTransformer(nextcord.FFmpegPCMAudio(stream_object.url, executable="./ffmpeg.exe")), 
                after=lambda e: loop.create_task(self.next()))
                self.ctx.voice_client.source.volume = 0.13 #Default Volume
                goldy_func.print_and_log(None, f"[{ext.cog_name.upper()}] Playing '{stream_object.title}' in '{self.ctx.voice_client.channel.name}'.")
            else:
                await self.resume()
        except Exception as e:
            await goldy_error.log(self.ctx, self.client, e, None)
            return False

    async def pause(self):
        self.ctx.voice_client.pause()

    async def resume(self):
        self.ctx.voice_client.resume()

    async def next(self): #Remove last song and plays next song in queue.
        last_song_object = (await self.queue.get())[0]
        await last_song_object.np_msg.edit(embed=await ext.music.embed.crossed_out_playing(last_song_object)) #Crossout last now playing embed.
        await self.queue.remove_first() #Removes last song.

        if self.queue.length >= 1: #If there is 1 or more songs in queue, play them.
            next_song_object = (await self.queue.get())[0]
            await self.play(next_song_object.stream_object)
            msg = await self.ctx.send(embed=await ext.music.embed.playing(next_song_object))
            setattr(next_song_object, "np_msg", msg)
            

    @property
    def old_instance(self): #Returns the previous instance of the player.
        return goldy_cache.main_cache_object["goldy_music"][self.ctx.guild.id]["player_instance"]

    @property
    async def song_object(self): #Returns the song object for the song currently playing.
        return (await self.queue.get())[0]