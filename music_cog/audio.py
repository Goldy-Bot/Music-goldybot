from nextcord.errors import ClientException
from config import msg
import youtube_dl
import pafy
import nextcord

import goldy_utility

"""
Audio: The module that offers methods like playing audio and just vc join/leave functions.
"""

class goldy():

    @staticmethod
    async def join_vc(ctx): #Goldy Bot joins the vc your connected to.
        #Checks
        if ctx.author.voice == None:
            await ctx.send((msg.music.error.you_not_in_vc).format(ctx.author.mention))
            return False

        if not ctx.voice_client == None: #Checks if bot is already in another vc.
            if not ctx.voice_client.channel == ctx.author.voice.channel:
                await ctx.voice_client.disconnect()

        if ctx.voice_client == None:
            await ctx.author.voice.channel.connect()

        return True

    @staticmethod
    async def leave_vc(ctx): #Goldy Bot leaves the vc it is connected to.
        if not ctx.voice_client == None: #Disconnects if goldy bot is in a vc.
            ctx.voice_client.pause()
            await ctx.voice_client.disconnect()
        else:
            await ctx.send((msg.music.error.not_connected_to_vc).format(ctx.author.mention))

    class checks():
        @staticmethod
        async def in_vc(ctx): #Checks if goldy bot is already in a vc in the guild.
            if ctx.voice_client.source == None:
                return False #Goldy is not in vc.
            else:
                return True #Goldy is in vc.

class queue():
    def __init__(self, client):
        self.song_queue = {}

        self.setup(client)

    def setup(self, client): #Create a queue for the guild.
        for guild in client.guilds:
            self.song_queue[guild.id] = []

    async def check(self, ctx): #Checks queue if there's anything else to play.
        if len(self.song_queue[ctx.guild.id]) > 0:
            await player.play_song(ctx, self.song_queue[ctx.guild.id][0])
            self.song_queue.pop(0)

class youtube():

    @staticmethod
    async def search(ctx, client, amount, song, get_url=False):
        async with ctx.typing():
            try:
                info = youtube_dl.YoutubeDL({"format":"bestaudio", "quiet":False}).extract_info(f"ytsearch{amount}:{song}", 
                download=False, ie_key="YoutubeSearch")

                if len(info["entries"]) == 0:
                    return None
                
                if get_url == True:
                    url_list = []
                    for entry in info["entries"]:
                        url_list.append(entry["webpage_url"])

                    return url_list

                else:
                    return info

            except Exception as e:
                await goldy_utility.goldy.log_error(ctx, client, e, None)

class player():
    def __init__(self, client):
        self.client = client
        pass

    class checks():

        @staticmethod
        async def is_playing(ctx): #Checks if a song is already playing.
            if ctx.voice_client.is_playing():
                return True
            else:
                return False

    async def play_next(self, ctx):
        q = queue(self.client)
        if len(q.song_queue[ctx.guild.id]) > 1:
            self.song_queue.pop(0)
            await self.play_song(ctx, q.song_queue[ctx.guild.id][0])

    async def resume_song(self, ctx):
        await goldy.join_vc(ctx)
        ctx.voice_client.resume()

    async def play_song(self, ctx, song_url):
        url = pafy.new(song_url).getbestaudio().url
        q = queue(self.client)
        try:
            await ctx.voice_client.play(nextcord.PCMVolumeTransformer(nextcord.FFmpegPCMAudio(url)), after=lambda e: self.client.loop.create_task(self.play_next(ctx)))
        except TypeError as e:
            pass
        except ClientException:
            q.song_queue[ctx.guild.id].append(song_url)
        except Exception as e:
            await goldy_utility.goldy.log_error(ctx, self.client, e, None)
            return False

        ctx.voice_client.source.volume = 0.2

    