import nextcord
from nextcord.ext import commands
import asyncio

from goldy_func import *
from goldy_utility import *
import config.msg as msg

#Change 'your_cog' to the name you wish to call your cog. ('your_cog' is just a placeholder.)
cog_name = "music"

class music(commands.Cog, name="🧡🎻Music"):
    def __init__(self, client):
        self.client = client
        self.cog_name = cog_name
        self.help_command_index = None #The position this cog will be placed in the help command.

    @commands.command()
    async def play(self, ctx):
        if await can_the_command_run(ctx, cog_name) == True:
            pass

def setup(client):
    client.add_cog(music(client))

#Need Help? Check out this: {youtube playlist}