import discord
from discord.ext import commands
from googletrans import Translator
import os

#os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = "astute-quarter-328109-051769b1a5e4.json"

class Trans(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.translator = Translator()

    @commands.command(aliases=["แปลว่า", "พูดไร", "แปล", "trans"])
    async def what(self, ctx, *, msg=None):
        if msg == None:
            text = await ctx.channel.fetch_message(ctx.message.reference.message_id)
            output = self.translator.translate(text.content, dest="th")
            await text.reply(output.text)
            await ctx.message.delete()
        else:
            output = self.translator.translate(msg, dest="th")
            await ctx.reply(output.text)

    @commands.command()
    async def china(self, ctx, *, msg=None):
        if msg == None:
            text = await ctx.channel.fetch_message(ctx.message.reference.message_id)
            output = self.translator.translate(text.content, dest="zh")
            await text.reply(output.text)
            await ctx.message.delete()
        else:
            output = self.translator.translate(msg, dest="zh")
            await ctx.reply(output.text)


def setup(bot):
    bot.add_cog(Trans(bot))
