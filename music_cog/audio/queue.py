from logging import exception
from src import goldy_cache, goldy_func, goldy_error

from ... import music as ext

class song(): #Class that creates song object.
    def __init__(self, ctx, url, stream_object):
        self.ctx = ctx
        self.url = url
        self.platform = stream_object.platform
        self.name = stream_object.title
        self.short_name = self.name
        self.duration = stream_object.duration
        self.thumbnail = stream_object.thumbnail
        self.bitrate = stream_object.bitrate
        self.stream_object = stream_object

        if len(self.name) > 36:
            self.short_name = self.name[:23] + "..."

class playlist(): #Class that creates playlist object.
    def __init__(self, ctx, url, song_urls:list, stream_objects:list):
        self.ctx = ctx
        self.url = url
        self.songs:list = []

        count = 0
        for stream_object in stream_objects:
            self.songs.append(ext.queue.song(ctx, song_urls[count], stream_object))
            count += 1

class queue():
    def __init__(self, ctx):
        self.ctx = ctx
        self.remove = self._remove(ctx) #Remove class
        self.song:song = song #Song class
        try: #Test to see if cache exists.
            goldy_cache.main_cache_object["goldy_music"][ctx.guild.id]
            goldy_cache.main_cache_object["goldy_music"][ctx.guild.id]["song_queue"]
        except KeyError:
            goldy_func.print_and_log("info", f"[{ext.cog_name}] Created queue for '{ctx.guild.name}'.")
            goldy_cache.main_cache_object["goldy_music"][ctx.guild.id] = {}
            goldy_cache.main_cache_object["goldy_music"][ctx.guild.id]["song_queue"] = [] #Creates queue for guild if there isn't already.

    async def get(self): #Returns the actual song queue itself.
        return goldy_cache.main_cache_object["goldy_music"][self.ctx.guild.id]["song_queue"]

    async def add(self, song_object:song=None, playlist_object:playlist=None): #Adds a song or playlist to queue.
        
        if not playlist_object == None: #Playlist
            for song in playlist_object.songs:
                goldy_cache.main_cache_object["goldy_music"][song.ctx.guild.id]["song_queue"].append(song)
            return True
        
        if not song_object == None: #Single Song
            song = song_object
            goldy_cache.main_cache_object["goldy_music"][song.ctx.guild.id]["song_queue"].append(song)
            return True

        return False
    
    class _remove(): #Class with all remove methods.
        def __init__(self, ctx):
            self.ctx = ctx
            pass

        async def by_object(self, song_object:song): #Removes specific song from the queue using song object. (BETTER)
            try:
                goldy_cache.main_cache_object["goldy_music"][song.ctx.guild.id]["song_queue"].remove(song_object)
                goldy_func.print_and_log(None, f"[{ext.cog_name.upper()}] Removed '{song_object.name}' from '{song_object.ctx.guild.name}'s queue.")
                return True
            except ValueError as e:
                await goldy_error.log(self.ctx, error=e)
                return False

        async def by_queue_num(self, queue_num:int): #Removes specific song from the queue using current queue num of song.
            try:
                song_queue:list = goldy_cache.main_cache_object["goldy_music"][self.ctx.guild.id]["song_queue"]
                song_object:song = song_queue[queue_num - 1]
                goldy_cache.main_cache_object["goldy_music"][self.ctx.guild.id]["song_queue"].remove(song_object)
                goldy_func.print_and_log(None, f"[{ext.cog_name.upper()}] Removed '{song_object.name}' from '{song_object.ctx.guild.name}'s queue.")
                return True, song_object
            except ValueError as e:
                await goldy_error.log(self.ctx, error=e)
                return False

    async def remove_first(self): #Removes first song in the queue.
        goldy_cache.main_cache_object["goldy_music"][self.ctx.guild.id]["song_queue"].pop(0)
        goldy_func.print_and_log(None, f"[{ext.cog_name.upper()}] Removed first song from '{self.ctx.guild.name}'s queue.")

    async def remove_all(self): #Removes all songs from the queue except the one currently playing.
        try:
            song_queue:list = (self.get())[1:]
            song:ext.queue.song
            
            for song in song_queue:
                goldy_cache.main_cache_object["goldy_music"][self.ctx.guild.id]["song_queue"].pop(1)
                goldy_func.print_and_log(None, f"[{ext.cog_name.upper()}] Removed '{song.name}' from '{song.ctx.guild.name}'s queue.")

            return True
        except Exception:
            await goldy_error.log(self.ctx)

    @property
    def length(self): #Returns amount songs left in queue.
        return len(goldy_cache.main_cache_object["goldy_music"][self.ctx.guild.id]["song_queue"])

async def get(ctx): #Returns queue class.
    return queue(ctx)