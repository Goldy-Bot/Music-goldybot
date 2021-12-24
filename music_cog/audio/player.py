import asyncio
import nextcord

from src import goldy_cache, goldy_func, goldy_error

from ... import music as ext
from . import queue

class player: #Goldy Bot player class, an instence of this should be made whenever music is needed to be played in a vc.
    def __init__(self, ctx, client, voice_client, queue:queue.queue):
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
                self.ctx.voice_client.play(nextcord.PCMVolumeTransformer(nextcord.FFmpegPCMAudio(stream_object.url, executable="./ffmpeg.exe", 
                options='-aq 8 -ac 2 -af bass=g=2.8')), 
                after=lambda e: loop.create_task(self.next(e)))
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

    async def skip(self):
        self.voice_client.stop()
        await self.next()

    async def next(self, e=None): #Remove last song and plays next song in queue.
        if e == None:
            last_song_object = (await self.queue.get())[0]
            await last_song_object.np_msg.edit(embed=await ext.music.embed.crossed_out_playing(last_song_object)) #Crossout last now playing embed.
            await self.queue.remove_first() #Removes last song.

            if self.queue.length >= 1: #If there is 1 or more songs in queue, play them.
                next_song_object = (await self.queue.get())[0]
                await self.play(next_song_object.stream_object)
                msg = await self.ctx.send(embed=await ext.music.embed.playing(next_song_object))
                setattr(next_song_object, "np_msg", msg)
        else:
            await goldy_error.log(self.ctx, self.client, e)
            
    @property
    def old_instance(self): #Returns the previous instance of the player.
        return goldy_cache.main_cache_object["goldy_music"][self.ctx.guild.id]["player_instance"]

    @property
    async def song_object(self): #Returns the song object for the song currently playing.
        return (await self.queue.get())[0]

async def get(ctx, client, voice_client, queue): #Creates instance of player to use.
    return player(ctx, client, voice_client, queue)