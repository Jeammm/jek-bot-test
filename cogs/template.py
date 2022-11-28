import discord
from discord.ext import commands

class Test_Linux(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def template(self, ctx):
        await ctx.send("template")

def setup(bot):
    bot.add_cog(Test_Linux(bot))