from src import goldy_cache, goldy_error
from src.utility import cmds, members
from src.utility import msg

from .. import msg as music_msg
from ... import music as ext #Music Cog

#Creates cache dict if not already avalible.
try:
    goldy_cache.main_cache_object["goldy_music"]
except KeyError:
    goldy_cache.main_cache_object["goldy_music"] = {}

"""
Goldy: 
"""

async def join_vc(ctx): #Goldy Bot joins the vc your connected to.
    #Checks if member is in vc.
    if ctx.author.voice == None: #Member is not in vc.
        await ctx.send((music_msg.error.you_not_in_vc).format(ctx.author.mention))
        return False

    if not ctx.voice_client == None: #Checks if bot is already in another vc.
        if not ctx.voice_client.channel == ctx.author.voice.channel:
            if not ctx.voice_client.is_playing():
                await ctx.voice_client.disconnect()

    if ctx.voice_client == None:
        await ctx.author.voice.channel.connect()

    return ctx.voice_client

async def leave_vc(ctx): #Goldy Bot leaves the vc it is connected to.
    if not ctx.voice_client == None: #Disconnects if goldy bot is in a vc.
        ctx.voice_client.pause()
        await ctx.voice_client.disconnect()
        return True
    else:
        await ctx.send((music_msg.error.not_connected_to_vc).format(ctx.author.mention))

async def play(ctx, client, song=None): #Finds and plays song.
    try:
        if await members.checks.in_vc(ctx): #If member in vc.
            await join_vc(ctx)
            song_queue:ext.queue.queue = await ext.queue.get(ctx)
            player:ext.player.player = await ext.player.get(ctx, client, ctx.voice_client, song_queue)
            song_object = None
            playlist_object = None

            if not song == None:
                url = await ext.youtube.search(ctx, client, song)
                stream_object = await ext.youtube.stream(ctx, client, url).create()
            
                if isinstance(stream_object, tuple): #Playlist
                    (url_list, stream_objects) = stream_object
                    playlist_object = ext.queue.playlist(ctx, url, url_list, stream_objects)
                    type = "playlist"
                    
                else: #Single Song
                    song_object = ext.queue.song(ctx, url, stream_object)
                    type = "song"

                await song_queue.add(song_object, playlist_object) #Adds song to guild's music queue.

                if song_queue.length > 1:
                    if type == "song":
                        embed = await ext.music.embed.added_to_queue(song_object)
                        await ctx.send(embed=embed)
                        return True

                    if type == "playlist":  
                        embed = await ext.music.embed.added_to_queue_playlist(playlist_object.songs)
                        await ctx.send(embed=embed)
                        return True
                else:
                    #Plays song now.
                    message = await ctx.send(embed=await ext.music.embed.playing(song_object))
                    setattr(song_object, "np_msg", message)
                    if type == "playlist":
                        (x, stream_objects) = stream_object
                        await player.play(stream_objects[0])

                    if type == "song":
                        await player.play(stream_object)

                    return True
            
            else:
                if song_queue.length >= 1:
                    if not await (player.old_instance).checks.is_playing():
                        message = await ctx.send(embed=await ext.music.embed.playing(await (player.old_instance).song_object))
                        setattr(await (player.old_instance).song_object, "np_msg", message)
                        await player.play((await song_queue.get())[0].stream_object)
                        return True

            return False

        else:
            if await checks.in_vc(ctx):
                if ctx.voice_client.is_playing():
                    player:ext.player.player = goldy_cache.main_cache_object["goldy_music"][ctx.guild.id]["player_instance"]
                    await ctx.send(music_msg.error.another_vc.format(ctx.author.mention, player.voice_client.channel.mention))
                    return

            else:
                await ctx.send(music_msg.error.not_connected_to_vc.format(ctx.author.mention))
                return

    except Exception as e:
        await goldy_error.log(ctx, client=client, error=e)

class checks():
    @staticmethod
    async def in_vc(ctx): #Checks if goldy bot is already in a vc in the guild.
        try:
            if ctx.voice_client.source == None:
                return False #Goldy is not in vc.
            else:
                return True #Goldy is in vc.
        except AttributeError:
            return False