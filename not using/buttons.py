import discord
from discord.ext import commands
from discord_components import Button, ButtonStyle, Select, SelectOption

class Butt(commands.Cog):

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
        self.help_pages = [Butt.page1, Butt.page2, Butt.page3, Butt.page4]
        self.current = 0

    @commands.command()
    async def buttons(self, ctx):
        await ctx.channel.send(
            "test1",
            components = [
                Button(style=ButtonStyle.blue, label="butt1"),
                Button(style=ButtonStyle.red, label="butt2"),
                Button(style=ButtonStyle.URL, label="butt3", url="https://www.google.com")
            ]
        )

        res = await self.bot.wait_for("button_click")
        if res.channel == ctx.channel:
            await res.respond(
                type=5,
                content=f"{res.component.label} clicked"
            )

        res2 = await self.bot.wait_for("button_click")
        if res2.channel == ctx.channel:
            await res2.respond(
                type=5,
                content=f"{res2.component.label} clicked"
            )

    @commands.command()
    async def butt(self, ctx):
        one = Button(style=ButtonStyle.blue, label="11", id="first")
        two = Button(style=ButtonStyle.red, label="22", id="second")
        three = Button(style=ButtonStyle.green, label="33", id="third")
        four = Button(style=ButtonStyle.grey, label="44", id="fourth")
        google = Button(style=ButtonStyle.URL, label="go google", url="https://www.google.com")

        page1 = Butt.page1
        page2 = Butt.page2
        page3 = Butt.page3
        page4 = Butt.page4

        await ctx.send(
            "help test",
            components=[
                [one, two, three, four],
                [google]
            ]
        )

        buttons = {
            "first": page1,
            "second": page2,
            "third": page3,
            "fourth": page4
        }

        while True:
            event = await self.bot.wait_for("button_click")
            if event.channel is not ctx.channel:
                return
            if event.channel == ctx.channel:
                response = buttons.get(event.component.id)
                if response is None:
                    await event.channel.send(
                        "Something went wrong, Please try again"
                    )
                else:
                    await event.respond(
                        type=4,
                        embed=response
                    )
    @commands.command()
    async def selection(self, ctx):

        one = Button(style=ButtonStyle.blue, label="11", id="first")
        two = Button(style=ButtonStyle.red, label="22", id="second")
        three = Button(style=ButtonStyle.green, label="33", id="third")
        four = Button(style=ButtonStyle.grey, label="44", id="fourth")
        google = Button(style=ButtonStyle.URL, label="go google", url="https://www.google.com")

        buttons = {
            "first": Butt.page1,
            "second": Butt.page2,
            "third": Butt.page3,
            "fourth": Butt.page4
        }


        await ctx.send(
            "testing1",
            components=[
                Select(placeholder="Choose fom here",
                    options=[
                        SelectOption(
                            label="page1",
                            value="option1",
                            description="see option 1",
                            emoji="😊"
                        ),
                        SelectOption(
                            label="page2",
                            value="option2",
                            description="see option 2",
                            emoji="😊"
                        ),
                        SelectOption(
                            label="page3",
                            value="option3",
                            description="see option 3",
                            emoji="😊"
                        ),
                        SelectOption(
                            label="page4",
                            value="option4",
                            description="see option 4",
                            emoji="😊"
                        ),
                    ]

                ),[one, two, three, four],
                [google]

            ]
        )

        e1 = Butt.page1
        e2 = Butt.page2
        e3 = Butt.page3
        e4 = Butt.page4

        while True:
            try:
                event = await self.bot.wait_for("select_option", check=None)
                label = event.component[0].label

                if label == "Option 1":
                    await event.respond(
                        type=4,
                        ephemeral=True,
                        embed=e1
                    )
                elif label == "Option 2":
                    await event.respond(
                        type=4,
                        ephemeral=True,
                        embed=e2
                    )
                elif label == "Option 3":
                    await event.respond(
                        type=4,
                        ephemeral=True,
                        embed=e3
                    )
                elif label == "Option 4":
                    await event.respond(
                        type=4,
                        ephemeral=False,
                        embed=e4
                    )
            except discord.NotFound:
                print("error")

def setup(bot):
    bot.add_cog(Butt(bot))
