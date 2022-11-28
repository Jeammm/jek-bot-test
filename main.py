import os
import discord
from discord.ext import commands, tasks
from itertools import cycle
import json
import datetime
from discord_components.client import DiscordComponents
import psycopg2


BOT_TOKEN = os.environ.get('BOT_TOKEN')
DATABASE_URL = os.environ.get('DATABASE_URL')
USERNAME = os.environ.get('USERNAME')
PASSWORD = os.environ.get('PASSWORD')

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    def disable(self):
        self.HEADER = ''
        self.OKBLUE = ''
        self.OKGREEN = ''
        self.WARNING = ''
        self.FAIL = ''
        self.ENDC = ''

print(f"{bcolors.OKGREEN}{DATABASE_URL[:10]}{bcolors.ENDC}")

intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(intents=intents, command_prefix=["jek ", "Jek ", "JEK "], help_command = None)

#load specifig extension
@bot.command()
async def load(ctx, extension):
    bot.load_extension(f'cogs.{extension}')
    print(f'{extension} successfully loaded')
    await ctx.send(f'{extension} successfully loaded')
    await ctx.message.delete()

#unload specific extension
@bot.command()
async def unload(ctx, extension):
    bot.unload_extension(f'cogs.{extension}')
    print(f'{extension} successfully un-loaded')
    await ctx.send(f'{extension} successfully un-loaded')
    await ctx.message.delete()

@bot.command()
async def reload(ctx, extension):
    bot.reload_extension(f'cogs.{extension}')
    print(f'{bcolors.OKGREEN}{extension} successfully re-loaded{bcolors.ENDC}')
    await ctx.send(f'{extension} successfully re-loaded')
    await ctx.message.delete()

#load all extention in cogs to start
for filename in os.listdir('./cogs'):
    try:
        if filename.endswith('.py'):
            print(f"{bcolors.OKGREEN}LOADED : {filename}{bcolors.ENDC}")
            bot.load_extension(f'cogs.{filename[:-3]}')
    except Exception as error:
        print(f"{bcolors.FAIL}{error}{bcolors.ENDC}")


#start
@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")
    await bot.change_presence(status=discord.Status.online, activity=discord.Activity(type=discord.ActivityType.listening, name="your shits"))
    DiscordComponents(bot)

@bot.event
async def on_guild_join(guild):
    con = None
    try:
        con = psycopg2.connect(DATABASE_URL, user=USERNAME, password=PASSWORD)
        cur = con.cursor()
        cur.execute(f"INSERT INTO serverlists(serverid) VALUES ('{guild.id}');")
        cur.execute(f"INSERT INTO logs VALUES ({guild.id}, NULL, {(datetime.datetime.now()).timestamp()}, 'Guild Join');")
        cur.close()
    except Exception as error:
        print(f"error: {error}")
    finally:
        if con is not None:
            con.commit()
            con.close()

@bot.command(aliases=["clean"])
async def clear(ctx):
    async for x in ctx.channel.history():
        if x.author == bot.user or x.content.startswith("jek") or x.content.startswith("Jek"):
            await x.delete()

@bot.command()
async def gartic(ctx):
    return

#handle unknown command error
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("งงอะ ไปดูวิธีใช้ที่ jek help")
    else:
        print(error)
        await ctx.send(f"```[error] {error}```", delete_after=20)

################################### create loop จดไว้เผื่อใช้
#say.start()
to_say = cycle(["1", "2", "3"])
@tasks.loop(seconds=10)
async def say():
    await bot.change_presence(activity=discord.Game(next(to_say)))
###################################


#keep_alive()
bot.run(BOT_TOKEN)
