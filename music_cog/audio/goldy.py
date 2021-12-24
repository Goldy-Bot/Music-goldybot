from src import goldy_cache

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