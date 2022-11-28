import discord
from discord.ext import commands
from discord_components import Button, ButtonStyle, Select, SelectOption


class Paginator(commands.Cog):

    description1 = """**[spam `@person`](https://www.google.com)**
    :point_right: wake up, @person

    **[แปล `message`](https://www.google.com)**
    :point_right: translate given message to Thai

    **[แปลว่า](https://www.google.com)**
    :point_right: กด reply ข้อความที่ต้องการ แล้วพิมพ์ 'jek แปลว่า'

    **[clean](https://www.google.com)**
    :point_right: delete every jek bot related messages

    **[trade `amount`](https://www.google.com)**
    :point_right: Any curreny to THB

    **[feedback `feedback`](https://www.google.com)**
    :point_right: อยากได้ไรก็บอก

    **[gartic](https://garticphone.com/)**
    :point_right: ส่ง Jek ไปจองห้อง Garticphone
    """
    page1 = discord.Embed(title="**Page 1 :** General", description=description1, colour=discord.Colour.orange())

    description2 ="""**[play `url/search`](https://www.youtube.com)**
    :point_right: play music from youtube (can\'t do spotify, please stop)

    **[pause/resume](https://www.youtube.com)**
    :point_right: pause/resume music

    **[join/leave](https://www.youtube.com)**
    :point_right: join/leave voice channel

    **[queueList](https://www.youtube.com)**
    :point_right: show music queue

    **[skip](https://www.youtube.com)**
    :point_right: skip to next music in queue

    **[stop](https://www.youtube.com)**
    :point_right: It is suppose to stop the music but..
    """
    page2 = discord.Embed(title="**Page 2 :** Youtube", description=description2, colour=discord.Colour.orange())

    description3 ="""**[boo](https://www.youtube.com)**
    :point_right: summon Wazowski to the chat

    **[amogus](https://www.youtube.com)**
    :point_right: Summon Amogus to the chat

    **[thomas](https://www.youtube.com)**
    :point_right: Summon Thomas to the chat

    **[alarm](https://www.youtube.com)**
    :point_right: Alarm triggering
    """
    page3 = discord.Embed(title="**Page 3 :** For the memes", description=description3, colour=discord.Colour.orange())
    page3.set_footer(text="**Volume warning**", icon_url="https://media.istockphoto.com/vectors/sound-icon-volume-icon-speaker-icon-vector-id1034246176?k=20&m=1034246176&s=170667a&w=0&h=z3d33zrTM9FeDy-kdel_QxrM-GIGZqcZ49r-9Vl8Ysg=")

    description4 ="""**[tag `@person`](https://www.google.com)**
    :point_right: say hello to @person

    **[ym_trigger `word`](https://www.google.com)**
    :point_right: คงเคยเห็น ยม เนอะ อันนี้เอาไว้เปลี่ยนคำได้ ถ้าไม่ใส่คำก็คือให้เอาออก

    **[random `stuff_1` `stuff_2` `stuff3` `...`](https://www.google.com)**
    :point_right: pick a random stuff from the list

    **[ว้าว](https://www.google.com)**
    :point_right: Get a random quote

    **[ping](https://www.google.com)**
    :point_right: check ping with pong!

    **[apex_help](https://www.google.com)**
    :point_right: More commands on Apex Legends
    """
    page4 = discord.Embed(title="**Page 4 :** Commands that people give zero fuk", description=description4, colour=discord.Colour.orange())

    description5 ="""**[match `yyyy-mm-dd`](https://www.youtube.com)**
    :point_right: โชว์ตารางการแข่งตามวันที่ใส่ ถ้าไม่ใส่=โชว์ของวันนี้

    **[bet `amount`](https://www.youtube.com)**
    :point_right: ลงพนัน ถ้าไม่ใส่จำนวน=เช็คคู่ที่ลงได้

    **[claim](https://www.youtube.com)**
    :point_right: รับตังพนันบอล

    **[mybet](https://www.youtube.com)**
    :point_right: ลงไรไว้บ้าง
    """
    page5 = discord.Embed(title="**Page 5 :** Football และอบายมุข", description=description5, colour=discord.Colour.orange())

    description6 ="""**[wallet](https://www.youtube.com)**
    :point_right: สร้างเป๋าตัง/เช็คเงิน รับฟรี 1000 coin

    **[checkin](https://www.youtube.com)**
    :point_right: เช็คอินวันละครั้ง/server รับฟรี 50 Jek coin

    **[give `receiver` `amount`](https://www.youtube.com)**
    :point_right: โอนตังให้ @receiver

    **[buy `amount`](https://www.youtube.com)**
    :point_right: เช็คราคา Crypto Currencies และซื้อด้วย Jek Coin

    **[sell `amount` `coin name`](https://www.youtube.com)**
    :point_right: เช็ค Portfolio และขายเหรียญเป็น Jek coin
    """
    page6 = discord.Embed(title="**Page 6 :** การเงินและการลงทุน (Beta)", description=description6, colour=discord.Colour.orange())


    pages = {
        1:page1,
        2:page2,
        3:page3,
        4:page4,
        5:page5,
        6:page6,
    }

    def __init__(self, bot):
        self.bot = bot
        self.current = {}

    @commands.command()
    async def help(self, ctx):
        self.current[ctx.author.id] = 1
        async def callback(interaction):
            previous = self.current[ctx.author.id]

            if interaction.author.id != ctx.author.id:
                await interaction.send("This panel does not belong to you")
                return

            if interaction.custom_id == "first":
                self.current[ctx.author.id] = 1
            elif interaction.custom_id == "before":
                if self.current[ctx.author.id] >= 2:
                    self.current[ctx.author.id] -= 1
            elif interaction.custom_id == "next":
                if self.current[ctx.author.id] < len(Paginator.pages):
                    self.current[ctx.author.id] += 1
            elif interaction.custom_id == "last":
                self.current[ctx.author.id] = len(Paginator.pages)

            #if self.current[ctx.author.id] != previous:
            if True:
                await interaction.edit_origin(
                    embed = Paginator.pages[self.current[ctx.author.id]],
                    components=[[
                        self.bot.components_manager.add_callback(
                            Button(style=ButtonStyle.green, label="<<", custom_id="first"),callback
                        ),
                        self.bot.components_manager.add_callback(
                            Button(style=ButtonStyle.blue, label="<", custom_id="before"),callback
                        ),
                        self.bot.components_manager.add_callback(
                            Button(style=ButtonStyle.blue, label=">", custom_id="next"),callback
                        ),
                        self.bot.components_manager.add_callback(
                            Button(style=ButtonStyle.green, label=">>", custom_id="last"),callback
                        ),
                    ]],
                )
            else:
                await interaction.send("Maximum Reached")

        await ctx.send(
            embed = Paginator.page1,
            components=[[
                self.bot.components_manager.add_callback(
                    Button(style=ButtonStyle.green, label="<<", custom_id="first"),callback
                ),
                self.bot.components_manager.add_callback(
                    Button(style=ButtonStyle.blue, label="<", custom_id="before"),callback
                ),
                self.bot.components_manager.add_callback(
                    Button(style=ButtonStyle.blue, label=">", custom_id="next"),callback
                ),
                self.bot.components_manager.add_callback(
                    Button(style=ButtonStyle.green, label=">>", custom_id="last"),callback
                ),
            ]],
        )

def setup(bot):
    bot.add_cog(Paginator(bot))
