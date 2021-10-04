import datetime
import nextcord
from nextcord.ext import commands
import asyncio

from src.goldy_func import *
from src.goldy_utility import *
import utility.msg as msg

#Importing cog packages.
import importlib
from .music_cog import audio, config

cog_name = "music"

class music(commands.Cog, name="🧡🎻Music"):
    def __init__(self, client):
        self.client = client
        self.cog_name = cog_name
        self.help_command_index = None #The position this cog will be placed in the help command.

        importlib.reload(audio)
        importlib.reload(config)
        importlib.reload(msg)

    @commands.command(aliases=["connect", "con"], description="Join and play song right away.", cmd_usage="!nick {nick_name}")
    async def join(self, ctx):
        if await can_the_command_run(ctx, cog_name) == True:
            await audio.goldy.join_vc(ctx)
            pass

    @join.error
    async def command_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            await ctx.author.send(msg.error.cooldown.format(datetime.timedelta(seconds=round(error.retry_after))))
        else:
            await goldy.log_error(ctx, self.client, error, f"{cog_name}.join")

    @commands.command()
    async def play(self, ctx, *, song=None):
        if await can_the_command_run(ctx, cog_name) == True:
            await audio.goldy.join_vc(ctx)
            q = audio.queue(self.client)
            if not song == None:
                #Handle songs that aren't already url's.
                for common_url in config.common_url_domains:
                    if not common_url in song: #It's not a URL.
                        
                        #Search for song.
                        result = await audio.youtube.search(ctx, self.client, 1, song, get_url=True)
                        if result == None:
                            await ctx.send((msg.music.error.song_not_found).format(ctx.author.mention))

                        song = result[0]

                if not song == None:
                    queue_len = len(q.song_queue[ctx.guild.id])

                    if queue_len > 0:
                        embed = await music.embed.added_to_queue("test", "https://osu.ppy.sh/users/15032137")
                        await ctx.send(embed=embed)
                    else:
                        embed = await music.embed.playing("test", "https://osu.ppy.sh/users/15032137")
                        await ctx.send(embed=embed)

                    q.song_queue[ctx.guild.id].append(song) #Adds song to queue

                    await audio.player(self.client).play_song(ctx, q.song_queue[ctx.guild.id][0])

                else:
                    await ctx.send((msg.music.error.song_not_found).format(ctx.author.mention))
                    return False

            else:
                await ctx.send((msg.music.error.need_song_name).format(ctx.author.mention))

    @play.error
    async def command_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            await ctx.author.send(msg.error.cooldown.format(datetime.timedelta(seconds=round(error.retry_after))))
        else:
            await goldy.log_error(ctx, self.client, error, f"{cog_name}.play")

    @commands.command()
    async def leave(self, ctx, *, song=None):
        if await can_the_command_run(ctx, cog_name) == True:
            await audio.goldy.leave_vc(ctx)

    class embed():
        @staticmethod
        async def create(title="**__🧡🎻Goldy Music (BETA)__**", description=""):
            embed=nextcord.Embed(title=title, description=description, color=settings.AKI_ORANGE)
            return embed

        @staticmethod
        async def added_to_queue(song_name, song_url):
            embed = await music.embed.create(title="**➕ Added to Queue**", description="tets")
            return embed

        @staticmethod
        async def playing(song_name, song_url):
            embed = await music.embed.create(title="**▶️ Playing Song**", description="test")
            return embed

def setup(client):
    client.add_cog(music(client))

#Need Help? Check out this: {youtube playlist}