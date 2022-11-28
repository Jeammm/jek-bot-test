import discord
from discord.ext import commands
import requests
import json
import time

class Spam(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def spam(self, ctx, target:discord.Member = None):
        if target == None:
            await ctx.send("who")
        else:
            for i in range(10):
                await ctx.send(target.mention)
                time.sleep(0.05)
        
def setup(bot):
    bot.add_cog(Spam(bot))