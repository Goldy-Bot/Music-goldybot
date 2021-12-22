import datetime
import nextcord
from nextcord import voice_client
from nextcord import embeds
from nextcord.ext import commands
import asyncio
import importlib

from src.goldy_func import *
from src.goldy_utility import *
import src.utility.msg as msg

#Importing cog packages.
from .music_cog import audio, config, msg as music_msg

cog_name = "music"
ver = "1.0[alpha]"

class music(commands.Cog, name="🧡🎻Music"):
    def __init__(self, client):
        self.client = client
        self.cog_name = cog_name
        self.github_repo = "https://github.com/Goldy-Bot/Music-goldybot"
        self.version = ver
        self.help_command_index = None #The position this cog will be placed in the help command.

        importlib.reload(audio)
        importlib.reload(config)
        importlib.reload(msg)

    @commands.command(aliases=["connect", "con"], description="Join and play song right away.", cmd_usage="!nick {nick_name}")
    async def join(self, ctx):
        if await can_the_command_run(ctx, cog_name) == True:
            await audio.goldy.join_vc(ctx)

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
            song_queue = audio.queue(ctx)
            player = audio.player(ctx, self.client, ctx.voice_client, song_queue)

            if not song == None:
                url = await audio.youtube.search(ctx, self.client, song)
                stream_object = await audio.youtube.stream(ctx, self.client, url).create()
                song_object = audio.song(ctx, url, stream_object)

                await song_queue.add(song_object) #Adds song to guild's music queue.

                if song_queue.length > 1:
                    embed = await music.embed.added_to_queue(song_object)
                    await ctx.send(embed=embed)
                    return True
                else: 
                    #Plays song now.
                    await player.play(stream_object)
                    message = await ctx.send(embed=await music.embed.playing(song_object))
                    setattr(song_object, "np_msg", message)
                    return True
            
            else:
                if song_queue.length >= 1:
                    if await (player.old_instance).checks.is_playing():
                        message = await ctx.send(embed=await music.embed.playing(await (player.old_instance).song_object))
                        setattr(await (player.old_instance).song_object, "np_msg", message)
                        return True

            await ctx.send(msg.help.command_usage.format(ctx.author.mention, "!play {song name/link}"))

    @play.error
    async def command_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            await ctx.author.send(msg.error.cooldown.format(datetime.timedelta(seconds=round(error.retry_after))))
        else:
            await goldy.log_error(ctx, self.client, error, f"{cog_name}.play")

    @commands.command()
    async def pause(self, ctx):
        if await can_the_command_run(ctx, cog_name) == True:
            try:
                player = goldy_cache.main_cache_object["goldy_music"][ctx.guild.id]["player_instance"]
                await player.pause()
                embed = await music.embed.paused(ctx)
                await ctx.send(embed=embed)
            except KeyError:
                await ctx.send(music_msg.error.nothing_playing.format(ctx.author.mention)) #I'm not playing anything.

    @pause.error
    async def command_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            await ctx.author.send(msg.error.cooldown.format(datetime.timedelta(seconds=round(error.retry_after))))
        else:
            await goldy.log_error(ctx, self.client, error, f"{cog_name}.pause")

    @commands.command()
    async def leave(self, ctx):
        if await can_the_command_run(ctx, cog_name) == True:
            await audio.goldy.leave_vc(ctx)

    @leave.error
    async def command_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            await ctx.author.send(msg.error.cooldown.format(datetime.timedelta(seconds=round(error.retry_after))))
        else:
            await goldy.log_error(ctx, self.client, error, f"{cog_name}.leave")

    class embed():
        @staticmethod
        async def create(title="**__🧡🎻Goldy Music (BETA)__**", description="", colour=settings.AKI_ORANGE):
            embed=nextcord.Embed(title=title, description=description, colour=colour)
            return embed

        @staticmethod
        async def added_to_queue(song_object:audio.song):
            embed = await music.embed.create(title=music_msg.add_to_queue.embed.title, 
            description=music_msg.add_to_queue.embed.des.format(song_object.name, song_object.ctx.author.mention, song_object.duration.formated), 
            colour=settings.GREY)
            embed.set_footer(text=music_msg.add_to_queue.embed.footer.format(song_object.platform.name, music_msg.footer.type_1.format(ver)), 
            icon_url=song_object.platform.icon)
            return embed

        @staticmethod
        async def playing(song_object:audio.song):
            embed = await music.embed.create(title=music_msg.playing.embed.title, 
            description=music_msg.playing.embed.des.format(song_object.name, song_object.ctx.author.mention, song_object.duration.formated), 
            colour=settings.AKI_BLUE)
            embed.set_footer(text=music_msg.playing.embed.footer.format(song_object.platform.name, music_msg.footer.type_1.format(ver)), 
            icon_url=song_object.platform.icon)
            return embed

        @staticmethod
        async def crossed_out_playing(song_object:audio.song):
            embed = await music.embed.create(title=music_msg.playing.crossed_out_embed.title, 
            description=music_msg.playing.crossed_out_embed.des.format(song_object.name, song_object.ctx.author.mention, song_object.duration.formated), 
            colour=settings.AKI_BLUE)
            embed.set_footer(text=music_msg.playing.crossed_out_embed.footer.format(song_object.platform.name, music_msg.footer.type_1.format(ver)), 
            icon_url=song_object.platform.icon)
            return embed

        @staticmethod
        async def paused(ctx):
            embed = await music.embed.create(title=music_msg.paused.embed.title, description=music_msg.paused.embed.des.format(ctx.author.mention), colour=settings.BLUE)
            embed.set_footer(text=f"{music_msg.footer.type_1.format(ver)}")
            return embed


def setup(client):
    client.add_cog(music(client))

#Need Help? Check out this: {youtube playlist}