import discord
from discord.ext import commands

class Pages(commands.Cog):

    page1 = discord.Embed(title="General", description="It is slow but working I promise", colour=discord.Colour.orange())
    page1.add_field(name="spam [@person]", value="wake up, @person", inline=False)
    page1.add_field(name="แปล [message]", value="translate given message to Thai", inline=False)
    page1.add_field(name="แปลว่า", value="กด reply ข้อความที่ต้องการ แล้วพิมพ์ 'jek แปลว่า'", inline=False)
    page1.add_field(name="clean", value="delete every jek bot related messages", inline=False)
    page1.add_field(name="[key word of currency] [amount]", value="SPECIAL EXCHANGE SYSTEM, calculate any currencies to Thai baht เช่น jek ฮ่องกง 500", inline=False)
    page1.add_field(name="feedback [feedback]", value="อยากได้ไรก็บอก", inline=False)
    page1.add_field(name="gartic", value="Create a Garticphone lobby for you", inline=False)
    page1.set_thumbnail(url="https://www.matichon.co.th/wp-content/uploads/2019/02/%E0%B9%82%E0%B8%A5%E0%B9%82%E0%B8%81%E0%B9%89-%E0%B8%9E%E0%B8%A3%E0%B8%A3%E0%B8%84%E0%B8%AD%E0%B8%99%E0%B8%B2%E0%B8%84%E0%B8%95%E0%B9%83%E0%B8%AB%E0%B8%A1%E0%B9%88.png")


    page2 = discord.Embed(title="Youtube", colour=discord.Colour.orange())
    page2.add_field(name="play [url/search]", value="play music from youtube (can\'t do spotify, please stop)", inline=False)
    page2.add_field(name="pause/resume", value="pause/resume music", inline=False)
    page2.add_field(name="join/leave", value="join/leave voice channel", inline=False)
    page2.add_field(name="queueList", value="show queue list", inline=False)
    page2.add_field(name="skip", value="skip music to next in queue", inline=False)
    page2.add_field(name="stop", value="it is the same as skip, I can\'t fix it", inline=False)
    page2.set_thumbnail(url="https://www.matichon.co.th/wp-content/uploads/2019/02/%E0%B9%82%E0%B8%A5%E0%B9%82%E0%B8%81%E0%B9%89-%E0%B8%9E%E0%B8%A3%E0%B8%A3%E0%B8%84%E0%B8%AD%E0%B8%99%E0%B8%B2%E0%B8%84%E0%B8%95%E0%B9%83%E0%B8%AB%E0%B8%A1%E0%B9%88.png")

    page3 = discord.Embed(title="For the memes", colour=discord.Colour.orange())
    page3.add_field(name="boo", value="summon Taksin", inline=False)
    page3.add_field(name="amogus", value="summon Amogus", inline=False)
    page3.set_thumbnail(url="https://www.matichon.co.th/wp-content/uploads/2019/02/%E0%B9%82%E0%B8%A5%E0%B9%82%E0%B8%81%E0%B9%89-%E0%B8%9E%E0%B8%A3%E0%B8%A3%E0%B8%84%E0%B8%AD%E0%B8%99%E0%B8%B2%E0%B8%84%E0%B8%95%E0%B9%83%E0%B8%AB%E0%B8%A1%E0%B9%88.png")

    page4 = discord.Embed(title="Commands that people give zero fuk", colour=discord.Colour.orange())
    page4.add_field(name="apex_help", value="More commands on Apex Legends", inline=False)
    page4.add_field(name="ping", value="response to your ping with pong", inline=False)
    page4.add_field(name="ว้าว", value="Get a random quote", inline=False)
    page4.add_field(name="random [stuff1 stuff2 stuff3 ....]", value="random from the list given", inline=False)
    page4.add_field(name="ym_trigger [word]", value="คงเคยเห็น ยม เนอะ อันนี้เอาไว้เปลี่ยนคำได้ ถ้าไม่ใส่คำก็คือให้เอาออก", inline=False)
    page4.add_field(name="tag [@person]", value="say hello to @person", inline=False)
    page4.set_thumbnail(url="https://www.matichon.co.th/wp-content/uploads/2019/02/%E0%B9%82%E0%B8%A5%E0%B9%82%E0%B8%81%E0%B9%89-%E0%B8%9E%E0%B8%A3%E0%B8%A3%E0%B8%84%E0%B8%AD%E0%B8%99%E0%B8%B2%E0%B8%84%E0%B8%95%E0%B9%83%E0%B8%AB%E0%B8%A1%E0%B9%88.png")

    def __init__(self, bot):
        self.bot = bot
        self.help_pages = [Pages.page1, Pages.page2, Pages.page3, Pages.page4]
        self.buttons = [u"\u23EA", u"\u2B05", u"\u27A1", u"\u23E9"]
        # skip to           start,      left,     right,       end

    @commands.command()
    async def help3(self, ctx):
        current = 0
        msg = await ctx.send(embed=self.help_pages[current])

        for button in self.buttons:
            await msg.add_reaction(button)

        while True:
            try:
                reaction, user = await self.bot.wait_for("reaction_add", check=lambda reaction, user: user == ctx.author and reaction.emoji in self.buttons, timeout=60.0)

            except asyncio.TimeoutError:
                return print("test")

            else:
                previous_page = current
                if reaction.emoji == u"\u23EA":
                    current = 0

                elif reaction.emoji == u"\u2B05":
                    if current > 0:
                        current -= 1

                elif reaction.emoji == u"\u27A1":
                    if current < len(self.help_pages)-1:
                        current += 1

                elif reaction.emoji == u"\u23E9":
                    current = len(self.help_pages)-1

                for button in self.buttons:
                    await msg.remove_reaction(button, ctx.author)

                if current != previous_page:
                    await msg.edit(embed=self.help_pages[current])

def setup(bot):
    bot.add_cog(Pages(bot))
