import discord
from discord.ext import commands
import requests
import json
import datetime
from parinya import LINE

class Feedback(commands.Cog):
    line = LINE("7yOmCyjHgoHZRRGdRBVyFhPz0Pg1MZWfJn9sxUL4drk")
    def __init__(self, bot):
        self.bot = bot

    #Feedback
    @commands.command()
    async def feedback(self, ctx, *, msg):
        with open("feedback.txt", 'a') as fp:
            fp.write(f"\n[{ctx.author}, {ctx.guild}] : {msg}")
        await ctx.send("บันทึกเรียบร้อยแล้ว ขอบคุณครับ")
        Feedback.line.sendtext(f"\n[{ctx.author}, {ctx.guild}] :\n{msg}")



def setup(bot):
    bot.add_cog(Feedback(bot))
