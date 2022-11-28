import discord
from discord.ext import commands

class help(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def help2(self, ctx):
        emBed = discord.Embed(title="Jek Bot 2.0 help", description="Available bot command", color=0xeda334)

        #get_quote
        emBed.add_field(name="help", value="list all command and how to use", inline=False)
        #ping
        emBed.add_field(name="ping", value="response your ping with pong", inline=False)
        #tag
        emBed.add_field(name="tag [@person]", value="say hello to @person", inline=False)
        #play
        emBed.add_field(name="play [url/search]", value="play sound from youtube", inline=False)
        #pause
        emBed.add_field(name="pause/resume", value="pause/resume sound", inline=False)
        #join/leave
        emBed.add_field(name="join/leave", value="join/leave voice channel", inline=False)
        #queuelist
        emBed.add_field(name="queueList", value="show queue list", inline=False)
        #skip
        emBed.add_field(name="skip", value="skip sound to next in queue", inline=False)
        #stop
        emBed.add_field(name="stop", value="stop sound", inline=False)
        #clean
        emBed.add_field(name="clean", value="delete every jek bot command messages", inline=False)
        #exchange
        emBed.add_field(name="[key word of currency] [amount]", value="SPECIAL EXCHANGE SYSTEM, calculate any currencies to Thai baht เช่น jek ฮ่องกง 500", inline=False)
        #spam
        emBed.add_field(name="spam [@person]", value="wake the fuck up @person", inline=False)
        #boo
        emBed.add_field(name="boo", value="boo", inline=False)
        #amogus
        emBed.add_field(name="amogus", value="amogus", inline=False)
        #feedback
        emBed.add_field(name="feedback [feedback]", value="Send feedback to developer.", inline=False)
        #apex command
        emBed.add_field(name="apex_help", value="More command on Apex Legends", inline=False)
        #gartic
        emBed.add_field(name="gartic", value="Create a Garticphone lobby for ya", inline=False)

        emBed.set_thumbnail(url="https://www.matichon.co.th/wp-content/uploads/2019/02/%E0%B9%82%E0%B8%A5%E0%B9%82%E0%B8%81%E0%B9%89-%E0%B8%9E%E0%B8%A3%E0%B8%A3%E0%B8%84%E0%B8%AD%E0%B8%99%E0%B8%B2%E0%B8%84%E0%B8%95%E0%B9%83%E0%B8%AB%E0%B8%A1%E0%B9%88.png")
        emBed.set_footer(text="Jek Lord", icon_url="https://s.isanook.com/ca/0/rp/r/w728/ya0xa0m1w0/aHR0cHM6Ly9zLmlzYW5vb2suY29tL2NhLzAvdWQvMjc4LzEzOTQyMjUvNDI4NzUzMjVfMjI0OTUzODEzMTk0OTM0MV8yMTUuanBn.jpg")
        emBed.set_image(url="https://storage.thaipost.net/main/uploads/photos/big/20190331/image_big_5ca0c0f42d6c1.jpg")
        await ctx.channel.send(embed=emBed)

def setup(bot):
    bot.add_cog(help(bot))
