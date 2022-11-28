import discord
from discord.ext import commands
import requests
import json
from datetime import datetime, timedelta
from random import choice
from discord_components import Button, ButtonStyle
import os
import psycopg2

DATABASE_URL = os.environ.get('DATABASE_URL')
USERNAME = os.environ.get('USERNAME')
PASSWORD = os.environ.get('PASSWORD')

class Besic_task(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.con = psycopg2.connect(DATABASE_URL, user=USERNAME, password=PASSWORD)

    #logs
    @commands.Cog.listener()
    async def on_message(self, ctx):


        if ctx.content.startswith(("jek ","Jek ", "JEK ")):
            command_time = datetime.utcnow() + timedelta(hours=7)
            try:
                ref = await ctx.channel.fetch_message(ctx.reference.message_id)
                text = ref.content
            except:
                text = ""
            command_log = f"[command] {ctx.guild.name} | {command_time} | {ctx.author} | {ctx.content} | {text}"
            print(command_log)
            
            try:
                cur = self.con.cursor()
                cur.execute(f"INSERT INTO logs(serverid, id, stamp, command) VALUES ('{ctx.guild.id}', '{ctx.author.id}', {(datetime.utcnow()).timestamp()}, '{ctx.content} | {text}');")
                cur.close()
            except Exception as error:
                print(f"error: {error}")
            finally:
                if self.con is not None:
                    self.con.commit()


    #ping pong!
    @commands.command(aliases=["ping2","ping3"])
    async def ping(self, ctx):
        await ctx.send('Pong!')

    #tag @user message
    @commands.command()
    async def tag(self, ctx, member : discord.Member, *, reason=None):
        await ctx.send("hey! {}, {} say {}".format(member.mention, ctx.author.mention, reason))

    @commands.command(aliases=["ว้าว", "wow"])
    async def get_quote(self, ctx):
        await ctx.trigger_typing()
        response = requests.get("https://zenquotes.io/api/random")
        json_data = json.loads(response.text)
        quote = json_data[0]['q'] + " -" + json_data[0]['a']
        search = json_data[0]['q'].split()
        search_plus = "+".join(search[:5])
        pic_link = f"https://api.giphy.com/v1/gifs/search?api_key=iY1O7Ca0tE1XeTFKmP3rzrWWBfjut0Bc&q={search_plus}&limit=25&offset=0&rating=g&lang=en"
        pic_response = requests.get(pic_link)
        pic_data = json.loads(pic_response.text)
        emBed = discord.Embed()
        emBed.set_image(url=pic_data["data"][choice([0,1,2,3,4,5])]["images"]["original"]["url"])
        await ctx.send(quote, embed=emBed)

    @commands.command()
    async def uwu(self, ctx):
        pic_link = f"https://api.giphy.com/v1/gifs/search?api_key=iY1O7Ca0tE1XeTFKmP3rzrWWBfjut0Bc&q=uwu+anime&limit=25&offset=0&rating=g&lang=en"
        response = requests.get(pic_link)
        pic_data = json.loads(response.text)
        emBed = discord.Embed()
        selected = choice(pic_data["data"][:10])
        emBed.set_image(url=selected["images"]["original"]["url"])
        await ctx.send(embed=emBed)

    @commands.command()
    async def change_game(self, ctx, *, change_to):
        await self.bot.change_presence(status=discord.Status.online, activity=discord.Game(change_to))

    @commands.command()
    async def random(self, ctx, *, random_list):
        random_list = random_list.split()
        await ctx.send(f"||{choice(random_list)}||")

    @commands.command()
    async def server_check(self, ctx):
        emBed = discord.Embed(title="Jek Bot Active Server")
        for guild in self.bot.guilds:
            emBed.add_field(name=guild.name, value = guild.id)
        await ctx.send(embed=emBed)

#     @commands.command()
#     async def ym_trigger(self, ctx, *, word=""):
#         print(word, "set")
#         with open("settings.json") as st:
#             data = json.loads(st.read())
#         if str(ctx.guild.id) not in data:
#             data[str(ctx.guild.id)] = {"ym_trigger": ""}
# 
#         if word == "":
#             data[str(ctx.guild.id)]["ym_trigger"] = ""
#             with open("settings.json", 'w') as st:
#                 json.dump(data, st, indent=4)
#             await ctx.send(f"Trigger no more")
#             del data
# 
#         else:
#             data[str(ctx.guild.id)]["ym_trigger"] = word
#             with open("settings.json", 'w') as st:
#                 json.dump(data, st, indent=4)
#             await ctx.send(f"{word} triggered")
#             del data

    @commands.command()
    async def info(self, ctx, *, word=""):
        invite = "https://discord.com/api/oauth2/authorize?client_id=882277442218250260&permissions=397254589649&scope=bot"
        async def callback(interaction):
            pass
        await ctx.send(
            "ชวนผมเข้าห้อง กดปุ่มนี้งับ",
            components=[
                self.bot.components_manager.add_callback(
                    Button(style=ButtonStyle.URL, label="เผยแพร่เจ๊ก", url=invite),callback
                )
            ],
        )

def setup(bot):
    bot.add_cog(Besic_task(bot))
