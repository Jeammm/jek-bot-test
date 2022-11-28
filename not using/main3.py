import discord
import os
import requests
import json
import random
from discord.ext import commands
import asyncio
import tweepy
from discord.utils import get as getvoice
from discord import FFmpegPCMAudio
from youtube_dl import YoutubeDL
from discord.ext.commands import Bot


#from cookieRunTweet import go_get_tweets

from keep_alive import keep_alive
from replit import db
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from discord.ext.commands import CommandNotFound

bot = commands.Bot(command_prefix='jek ', help_command = None)

#consumer_key = os.environ['consumer_key']
#consumer_secret = os.environ['consumer_secret']
#callback_uri = "oob"
#auth = tweepy.OAuthHandler(consumer_key, consumer_secret, callback_uri)
#redirect_url = auth.get_authorization_url()
#print(redirect_url)
#user_pint_input = input("pin : ")
#auth.get_access_token(user_pint_input)
#api = tweepy.API(auth)

@bot.event
async def on_ready():
    print(f"ready {bot.user}")
    

    
@bot.command()
async def help(ctx):
    emBed = discord.Embed(title="Jek Bot 2.0 help", description="Available bot command", color=0xeda334)
    
    #get_quote
    emBed.add_field(name="help", value="list all command and how to use", inline=False)
    #test
    emBed.add_field(name="test word", value="response with message you sent", inline=False)
    #hello
    emBed.add_field(name="hello", value="say hello to you!", inline=False)
    #play
    emBed.add_field(name="play url", value="play sound from url", inline=False)
    #leave
    emBed.add_field(name="leave", value="leave voice channel", inline=False)
    #showgame
    emBed.add_field(name="showgame", value="show available games", inline=False)
    #getgame
    emBed.add_field(name="getgame n", value="pick a random game from list that suited for n players", inline=False)
    #addgame
    emBed.add_field(name="addgame game n n n ...", value="add game that suited for n player to game list", inline=False)
    #removegame
    emBed.add_field(name="removegame game n n n ...", value="remove game from n players category", inline=False)
    #join
    emBed.add_field(name="joincookiefam email username", value="Join cookieRun Kingdom Family", inline=False)
    #leave
    emBed.add_field(name="leavecookiefam username/email", value="Leave cookieRun Kingdom Family", inline=False)
    #redeem
    emBed.add_field(name="redeemcode code", value="redeem CookieRun Kingdom code to all family members account", inline=False)
    #cookiefam
    emBed.add_field(name="cookiefam", value="show all CookieRun Kingdom family members", inline=False)


    emBed.set_thumbnail(url="https://www.matichon.co.th/wp-content/uploads/2019/02/%E0%B9%82%E0%B8%A5%E0%B9%82%E0%B8%81%E0%B9%89-%E0%B8%9E%E0%B8%A3%E0%B8%A3%E0%B8%84%E0%B8%AD%E0%B8%99%E0%B8%B2%E0%B8%84%E0%B8%95%E0%B9%83%E0%B8%AB%E0%B8%A1%E0%B9%88.png")
    emBed.set_footer(text="Jek Lord", icon_url="https://s.isanook.com/ca/0/rp/r/w728/ya0xa0m1w0/aHR0cHM6Ly9zLmlzYW5vb2suY29tL2NhLzAvdWQvMjc4LzEzOTQyMjUvNDI4NzUzMjVfMjI0OTUzODEzMTk0OTM0MV8yMTUuanBn.jpg")
    emBed.set_image(url="https://storage.thaipost.net/main/uploads/photos/big/20190331/image_big_5ca0c0f42d6c1.jpg")
    await ctx.channel.send(embed=emBed)

@bot.command()
async def get_quote(ctx):
    response = requests.get("https://zenquotes.io/api/random")
    json_data = json.loads(response.text)
    quote = json_data[0]['q'] + " -" + json_data[0]['a']
    await ctx.channel.send(quote)

@bot.command()
async def test(ctx, *, a=""):
    await ctx.channel.send("you type {0}".format(a))
    
@bot.command()
async def hello(ctx):
    await ctx.channel.send("hello {0}".format(ctx.author.mention))

@bot.command()
async def play(ctx, url):
    voice_client = getvoice(bot.voice_clients, guild=ctx.guild)
    
    if voice_client == None:
        if ctx.author.voice == None:
            await ctx.channel.send("เข้าห้องก่อนครับ")
            return
        await ctx.author.voice.channel.connect()
        voice_client = getvoice(bot.voice_clients, guild=ctx.guild)
        
    YDL_OPTIONS = {'format' : 'bestaudio', 'noplaylist' : 'False'}
    FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
    
    if not voice_client.is_playing():
        with YoutubeDL(YDL_OPTIONS) as ydl:
            info = ydl.extract_info(url, download=False)
        URL = info['formats'][0]['url']
        voice_client.play(discord.FFmpegPCMAudio(URL, **FFMPEG_OPTIONS))
        voice_client.is_playing()
    else:
        await ctx.channel.send("Already playing")
        return
            
@bot.command()
async def leave(ctx):
    await ctx.voice_client.disconnect()

@bot.command()
async def getgame(ctx, *, n="3"):
    if len(n.split()) > 1:
        await ctx.channel.send("ใส่เลขตัวเดียวพอ")
        return
    else:
        n = n[0]
    game_list = db["game_list"]
    if n == "0":
        await ctx.channel.send("อืม")
    elif n == "1":
        await ctx.channel.send("ไม่มีเพื่อนเล่นอ่อ")
    elif n in game_list:
        available_game = game_list[n]
        await ctx.channel.send(random.choice(available_game))
    else:
        await ctx.channel.send("วาดรูป")

@bot.command()
async def addgame(ctx, *, par):
    detail = par.split()
    if len(detail) == 1:
        await ctx.channel.send("ใส่จำนวนคนเล่นด้วยจ้ะ")
        return
    game_name = detail[0]
    game_n = detail[1:]
    game_list = db["game_list"]
    emBed = discord.Embed(title="Game Added")
    for n in game_n:
        game_list.setdefault(n, [])
        game_list[n].append(game_name)
        emBed.add_field(name=game_name, value="Added to {0}".format(n), inline=False)
    db["game_list"] = game_list
    await ctx.channel.send(embed=emBed)
    
@bot.command()
async def removegame(ctx, *, par):
    detail = par.split()
    game_name = detail[0]
    game_n = detail[1:]
    game_list = db["game_list"]
    emBed = discord.Embed(title="Game Removed")
    for n in game_n:
        game_list[n].remove(game_name)
        emBed.add_field(name=game_name, value="Removed from {0}".format(n), inline=False)
    db["game_list"] = game_list
    await ctx.channel.send(embed=emBed)

@bot.command()
async def showgame(ctx):
    game_list = db["game_list"]
    emBed = discord.Embed(title="All game")
    emBed.set_thumbnail(url="https://cdnb.artstation.com/p/assets/images/images/016/574/671/original/roman-boichuk-ezgif-com-optimize-1.gif?1552655919")
    for n, game in sorted(game_list.items(), key=lambda x:int(x[0])):
        if game == []:
            del game_list[n]
        else:
            emBed.add_field(name="{0} player".format(n), value=" ".join(game), inline=True)
    await ctx.channel.send(embed=emBed)

@bot.command()
async def joincookiefam(ctx, *, par):
    detail = par.split()
    email = detail[0]
    username = detail[1]
    cookierun_email = db["cookierun_email"]
    cookierun_email.append(detail)
    db["cookierun_email"] = cookierun_email
    emBed = discord.Embed(title="Added to Cookie Run Kingdom Family")
    emBed.set_thumbnail(url="https://playpost.gg/wp-content/uploads/2021/01/Review-Cookie-Run-Kingdom-ICON.jpg")
    emBed.add_field(name=username, value=email)
    await ctx.channel.send(embed=emBed)

@bot.command()
async def leavecookiefam(ctx, leaver):
    cookierun_email = db["cookierun_email"]
    for i in range(len(cookierun_email)):
        if leaver in cookierun_email[i]:
            await ctx.channel.send(embed=discord.Embed(title="Removed", description="{0} : {1}".format(cookierun_email[i][1], cookierun_email[i][0])))
            del cookierun_email[i]
            db["cookierun_email"] = cookierun_email
            return
    await ctx.channel.send("Remove Failed")
        
@bot.command()
async def redeemcode(ctx, code):
    await ctx.channel.send("รอเจ๊กทำงานแปป")
    successful_redeem = []
    driver = webdriver.Firefox()
    driver.get("https://game.devplay.com/coupon/ck/en")
    for email in db["cookierun_email"]:
        driver.find_element_by_id('code-box').send_keys(code)
        driver.find_element_by_id('email-box').send_keys(email[0])
        driver.find_element_by_xpath("/html/body/div/div[1]/div[2]/form/div[4]/div").click()
        code_error = 0
        try:
            WebDriverWait(driver, 10).until(EC.alert_is_present(),"  ")
            alert = driver.switch_to.alert
            alert_msg = alert.text
            print("alert accepted")
            print(alert_msg)
        except TimeoutException:
            alert_msg = "Unknown server error! Please try again later."
            print("no alert")
        if alert_msg == "Done! Log in to the game to claim your reward!":
            successful_redeem.append(email[1])
            await ctx.channel.send("{username} redeemed".format(username = email[1]))
        elif alert_msg == "Please enter all 16 characters of a coupon code!":
            await ctx.channel.send("code ไม่ถูก")
            code_error = 1; break
        elif alert_msg == "Please check your DevPlay account!":
            await ctx.channel.send("id/email ไม่ถูก : {email}".format(email = email[0]))
        elif alert_msg == "This coupon code has expired!":
            await ctx.channel.send("หมดอายุ")
            code_error = 1
            break
        elif alert_msg == "Please check the coupon code!":
            await ctx.channel.send("code ไม่ถูก")
            code_error = 1; break
        elif alert_msg == "You have already used this coupon code on this account!":
            await ctx.channel.send("ใช้ไปแล้ว")
        elif alert_msg == "This coupon code has already been used!":
            await ctx.channel.send("code หมดโควตา")
            code_error = 1; break
        elif alert_msg == "Unknown server error! Please try again later.":
            await ctx.channel.send("เว็บล่มอยู่ ค่อยเติมใหม่")
        else:
            await ctx.channel.send("เป็นไรไม่รู้ ต้องแก้ก่อนงับ")
        alert.accept()
        driver.get("https://game.devplay.com/coupon/ck/en")
        driver.refresh()
    if code_error != 1:
        await ctx.channel.send("เติมโค้ด {code} ให้ {n} คน เรียบร้อย".format(code = code, n=len(successful_redeem)))
        #await ctx.channel.send("{e}".format(e = "\n".join(successful_redeem)))
    else:
        alert.accept()
        await ctx.channel.send("เติมโค้ดไม่สำเร็จ")
    driver.close()

@bot.command()
async def cookiefam(ctx):
    emBed = discord.Embed(title="Cookie Run Family", description="use 'jek joincookiefam' to join family", color = 0x08b5ff)
    emBed.set_thumbnail(url="https://playpost.gg/wp-content/uploads/2021/01/Review-Cookie-Run-Kingdom-ICON.jpg")
    cookierun_email = db["cookierun_email"]
    for info in cookierun_email:
        email = info[0]
        username = info[1]
        emBed.add_field(name=username, value=email, inline=False)
    await ctx.channel.send(embed=emBed)

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    elif "ยม" in message.content:
        await message.channel.send("ยม.{0}".format(message.author.mention))
    elif message.content == "jek":
        await message.channel.send("jek help เพื่อดูรายละเอียดคับ")
    
    await bot.process_commands(message)

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, CommandNotFound):
        await ctx.channel.send("jek help เพื่อดูรายละเอียดคับ")
        return
    raise error

#async def get_tweets(ctx):
#    while True:
#        try:
#            new_tweet = go_get_tweets(api)
#            for target in db["cookie_news_update_channel"]:
#                print(f"target channel : {target}")
#                channel = bot.get_channel(int(target))
#                print(channel)
#                await channel.send(new_tweet)
#                
#        except Exception:
#            pass
#        await asyncio.sleep(5)
#
#@bot.command()
#async def setup(ctx):
#    if "cookie_news_update_channel" in db.keys():
#       target = db["cookie_news_update_channel"].get(str(ctx.guild.id), 0)
#    else:
#        db["cookie_news_update_channel"] = {}
#        target = 0
#    
#
#    if target == 0:
#        target = ctx.channel
#        cookie_news_update_channel = dict(db["cookie_news_update_channel"])
#        cookie_news_update_channel[str(ctx.guild.id)] = str(ctx.channel.id)
#        db["cookie_news_update_channel"] = cookie_news_update_channel
#        await ctx.channel.send("K")
#    bot.loop.create_task(get_tweets(ctx))

@bot.command()
async def refresh_setup(ctx):
    db["cookie_news_update_channel"] = {}
    await ctx.channel.send(db["cookie_news_update_channel"])

@bot.command()
async def clear(ctx):
    #mgs = [] #Empty list to put all the messages in the log
    async for x in ctx.channel.history():
        if x.author == bot.user or x.content.startswith("jek"):
            await x.delete()

keep_alive()
my_secret = os.environ['botToken']
bot.run(my_secret)