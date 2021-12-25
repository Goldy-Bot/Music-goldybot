import datetime
import nextcord
from nextcord import voice_client
from nextcord import embeds
from nextcord.ext import commands
import asyncio
import importlib

from src import goldy_error, goldy_func, goldy_cache, goldy_utility
from src.utility import cmds, members
import src.utility.msg as msg
import settings

#Importing cog packages.
from .music_cog import config, msg as music_msg
from .music_cog.audio import goldy, player, queue
from .music_cog.platforms import youtube

cog_name = "music"
ver = "1.0[alpha]"

class music(commands.Cog, name="🧡🎻Music"):
    def __init__(self, client):
        self.client = client
        self.cog_name = cog_name
        self.github_repo = "https://github.com/Goldy-Bot/Music-goldybot"
        self.version = ver
        self.help_command_index = None #The position this cog will be placed in the help command.

        importlib.reload(msg)
        importlib.reload(queue)
        importlib.reload(goldy)
        importlib.reload(config)
        importlib.reload(player)
        importlib.reload(music_msg)

    @commands.command(aliases=["connect", "con"], description="Join and play song right away.", cmd_usage="!nick {nick_name}")
    async def join(self, ctx):
        if await cmds.can_the_command_run(ctx, cog_name) == True:
            await goldy.join_vc(ctx)

    @join.error
    async def command_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            await ctx.author.send(msg.error.cooldown.format(datetime.timedelta(seconds=round(error.retry_after))))
        else:
            await goldy_error.log(ctx, self.client, error, f"{cog_name}.join")

    @commands.command()
    async def play(self, ctx, *, song=None):
        if await cmds.can_the_command_run(ctx, cog_name) == True:
            if await goldy.play(ctx, self.client, song) == False:
                await ctx.send(msg.help.command_usage.format(ctx.author.mention, "!play {song name/link}"))

    @play.error
    async def command_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            await ctx.author.send(msg.error.cooldown.format(datetime.timedelta(seconds=round(error.retry_after))))
        else:
            await goldy_error.log(ctx, self.client, error, f"{cog_name}.play")

    @commands.command()
    async def pause(self, ctx):
        if await cmds.can_the_command_run(ctx, cog_name) == True:
            try:
                player_:player.player = goldy_cache.main_cache_object["goldy_music"][ctx.guild.id]["player_instance"]
                await player_.pause()
                embed = await music.embed.paused(ctx)
                await ctx.send(embed=embed)
            except KeyError:
                await ctx.send(music_msg.error.nothing_playing.format(ctx.author.mention)) #I'm not playing anything.

    @pause.error
    async def command_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            await ctx.author.send(msg.error.cooldown.format(datetime.timedelta(seconds=round(error.retry_after))))
        else:
            await goldy_error.log(ctx, self.client, error, f"{cog_name}.pause")

    @commands.command()
    async def skip(self, ctx):
        if await cmds.can_the_command_run(ctx, cog_name) == True:
            try:
                player_:player.player = goldy_cache.main_cache_object["goldy_music"][ctx.guild.id]["player_instance"]
                embed = await music.embed.skipped(await player_.song_object)
                await ctx.send(embed=embed)
                await player_.skip()
            except KeyError:
                await ctx.send(music_msg.error.nothing_playing.format(ctx.author.mention)) #I'm not playing anything.

    @skip.error
    async def command_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            await ctx.author.send(msg.error.cooldown.format(datetime.timedelta(seconds=round(error.retry_after))))
        else:
            await goldy_error.log(ctx, self.client, error, f"{cog_name}.skip")

    @commands.command()
    async def clear(self, ctx):
        if await cmds.can_the_command_run(ctx, cog_name) == True:
            song_queue:queue.queue = await queue.get(ctx)
            if await song_queue.remove_all():
                embed = await music.embed.clear(ctx)
                await ctx.send(embed=embed)

    @clear.error
    async def command_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            await ctx.author.send(msg.error.cooldown.format(datetime.timedelta(seconds=round(error.retry_after))))
        else:
            await goldy_error.log(ctx, self.client, error, f"{cog_name}.clear")


    @commands.command()
    async def queue(self, ctx, option=None, song_num_or_name=None):
        if await cmds.can_the_command_run(ctx, cog_name) == True:
            if option == None:
                try:
                    song_queue:queue.queue = await queue.get(ctx)
                    embed = await music.embed._queue(ctx, self.client, await song_queue.get())
                    await ctx.send(embed=embed)
                except IndexError:
                    await ctx.send(music_msg.error.nothing_playing.format(ctx.author.mention)) #I'm not playing anything.

                except Exception:
                    await goldy_error.log(ctx, self.client)
            
            if not option == None:
                if option.lower() == "remove":
                    if not song_num_or_name == None:
                        if not int(song_num_or_name) <= 1:
                            song_queue:queue.queue = await queue.get(ctx)
                            (x, song_object) = await song_queue.remove.by_queue_num(int(song_num_or_name))
                            embed = await music.embed.queue_remove(song_object)
                            await ctx.send(embed=embed)
                        else:
                            embed = await music.embed.queue_song_is_playing(ctx)
                            await ctx.send(embed=embed)
                        return True
                    else:
                        await ctx.send(msg.help.command_usage.format(ctx.author.mention, "!queue remove {song queue number}"))
                        return

                if option.lower() == "clear":
                    await music.clear(ctx)

    @queue.error
    async def command_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            await ctx.author.send(msg.error.cooldown.format(datetime.timedelta(seconds=round(error.retry_after))))
        else:
            await goldy_error.log(ctx, self.client, error, f"{cog_name}.queue")

    @commands.command()
    async def leave(self, ctx):
        if await cmds.can_the_command_run(ctx, cog_name) == True:
            await goldy.leave_vc(ctx)

    @leave.error
    async def command_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            await ctx.author.send(msg.error.cooldown.format(datetime.timedelta(seconds=round(error.retry_after))))
        else:
            await goldy_error.log(ctx, self.client, error, f"{cog_name}.leave")

    class embed():
        @staticmethod
        async def create(title="**__🧡🎻Goldy Music (BETA)__**", description="", colour=settings.AKI_ORANGE):
            embed=nextcord.Embed(title=title, description=description, colour=colour)
            return embed

        @staticmethod
        async def added_to_queue(song_object:queue.song):
            embed = await music.embed.create(title=music_msg.add_to_queue.embed.title, 
            description=music_msg.add_to_queue.embed.des.format(song_object.name, song_object.ctx.author.mention, song_object.duration.formated, song_object.bitrate), 
            colour=settings.GREY)
            embed.set_footer(text=music_msg.add_to_queue.embed.footer.format(song_object.platform.name, music_msg.footer.type_1.format(ver)), 
            icon_url=song_object.platform.icon)
            return embed

        @staticmethod
        async def added_to_queue_playlist(playlist):
            song_object = playlist[0]
            embed = await music.embed.create(title=music_msg.add_to_queue_playlist.embed.title, 
            description=music_msg.add_to_queue_playlist.embed.des.format(len(playlist), song_object.ctx.author.mention), 
            colour=settings.YELLOW)
            embed.set_footer(text=music_msg.add_to_queue.embed.footer.format(song_object.platform.name, music_msg.footer.type_1.format(ver)), 
            icon_url=song_object.platform.icon)
            return embed

        @staticmethod
        async def playing(song_object:queue.song):
            embed = await music.embed.create(title=music_msg.playing.embed.title, 
            description=music_msg.playing.embed.des.format(song_object.name, song_object.ctx.author.mention, song_object.duration.formated, song_object.bitrate), 
            colour=settings.AKI_BLUE)
            embed.set_footer(text=music_msg.playing.embed.footer.format(song_object.platform.name, music_msg.footer.type_1.format(ver)), 
            icon_url=song_object.platform.icon)
            return embed

        @staticmethod
        async def crossed_out_playing(song_object:queue.song):
            embed = await music.embed.create(title=music_msg.playing.crossed_out_embed.title, 
            description=music_msg.playing.crossed_out_embed.des.format(song_object.name, song_object.ctx.author.mention, song_object.duration.formated, song_object.bitrate), 
            colour=settings.AKI_BLUE)
            embed.set_footer(text=music_msg.playing.crossed_out_embed.footer.format(song_object.platform.name, music_msg.footer.type_1.format(ver)), 
            icon_url=song_object.platform.icon)
            return embed

        @staticmethod
        async def paused(ctx):
            embed = await music.embed.create(title=music_msg.paused.embed.title, description=music_msg.paused.embed.des.format(ctx.author.mention), colour=settings.BLUE)
            embed.set_footer(text=f"{music_msg.footer.type_1.format(ver)}")
            return embed

        @staticmethod
        async def skipped(song_object:queue.song):
            embed = await music.embed.create(title=music_msg.skipped.embed.title, description=music_msg.skipped.embed.des.format(song_object.short_name), colour=settings.BLUE)
            embed.set_footer(text=f"{music_msg.footer.type_1.format(ver)}")
            return embed

        @staticmethod
        async def _queue(ctx, client, song_queue:list):
            song:queue.song
            embed_context = ""
            num = 0
            for song in song_queue:
                num += 1
                embed_context += f"• ``{num}``┃``{song.short_name}`` **__Req By {song.ctx.author.mention}__**\n"

            embed = await music.embed.create(title=music_msg.queue.embed.title, description=embed_context, colour=settings.GREY)
            
            embed.add_field(name="**▶️ Now Playing:**", value=f"``{song_queue[0].name}``", inline=True)

            player_:player.player = goldy_cache.main_cache_object["goldy_music"][ctx.guild.id]["player_instance"]
            embed.add_field(name="**🔊 Playing in VC:**", value=f"{player_.voice_client.channel.mention}", inline=True)

            embed.set_thumbnail(url=await goldy_utility.servers.get_icon(ctx, client))
            embed.set_footer(text=f"{music_msg.footer.type_1.format(ver)}")

            return embed

        @staticmethod
        async def queue_remove(song_object:queue.song):
            embed = await music.embed.create(title=music_msg.queue_remove.embed.title, description=music_msg.queue_remove.embed.des.format(song_object.name), colour=settings.RED)
            embed.set_footer(text=f"{music_msg.footer.type_1.format(ver)}")
            return embed

        @staticmethod
        async def queue_song_is_playing(ctx):
            embed = await music.embed.create(title=music_msg.queue_song_is_playing.embed.title, description=music_msg.queue_song_is_playing.embed.des.format(ctx.author.mention), colour=settings.AKI_ORANGE)
            embed.set_footer(text=f"{music_msg.footer.type_1.format(ver)}")
            return embed

        @staticmethod
        async def clear(ctx):
            embed = await music.embed.create(title=music_msg.clear.embed.title, description=music_msg.clear.embed.des.format(ctx.author.mention), colour=settings.WHITE)
            embed.set_footer(text=f"{music_msg.footer.type_1.format(ver)}")
            return embed

def setup(client):
    client.add_cog(music(client))

#Need Help? Check out this: {youtube playlist}