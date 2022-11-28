import discord
import os
import requests
import json
import random
from keep_alive import keep_alive
from replit import db
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException



client = discord.Client()

def get_quote():
    response = requests.get("https://zenquotes.io/api/random")
    json_data = json.loads(response.text)
    quote = json_data[0]['q'] + " -" + json_data[0]['a']
    return quote

def get_game(player):
    game_list = db["game_list"]
    if player == "1":
        return 'ไม่มีเพื่อนเล่นอ่อ'
    elif player == "0":
        return 'อืม'
    elif player not in game_list:
        return "วาดรูป"
    target_game = game_list[player]
    return random.choice(target_game)

def update_game_list(game, n):
    if "game_list" in db.keys():
        game_list = db["game_list"]
        game_list.setdefault(n,[])
        game_list[n].append(game)
        db["game_list"] = game_list
    else:
        db["game_list"] = {n,[game]}

def delete_game_list(game, n):
    game_list = db["game_list"]
    if n == "0":
        for e in game_list.keys():
            game_list[e].remove(game)
    else:
        game_list[n].remove(game)
    db["game_list"] = game_list

def joinCookieFam(email, username):
    if "cookierun_email" in db.keys():
        cookierun_email = db["cookierun_email"]
        cookierun_email.append([email, username]) #[email, username]
        db["cookierun_email"] = cookierun_email
        return "done"
    else:
        db["cookierun_email"] = [[email, username]]

def leaveCookieFam(leaver):
    target = ''
    cookierun_email = db["cookierun_email"] 
    for i in range(len(cookierun_email)):
        if any(leaver == e for e in cookierun_email[i]):
            target = cookierun_email[i][1]
            del cookierun_email[i]
            break
    db["cookierun_email"] = cookierun_email

    if target != '':
        return "bye {username}".format(username = target)
    else:
        return "มั่วละ"


@client.event
async def on_ready():
    print('หิวเล้ง {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    msg = message.content

    if msg.startswith('jek'):
        input_cmd = msg.split()

        if len(input_cmd) == 1:
            await message.channel.send(random.choice(["ไรครับเจ๊ก","อืม","ครับ","หิวเล้ง","เจ๊ก"]))
            await message.channel.send("jek help เพื่อดูวิธีใช้")

        elif input_cmd[1] == "help":
            await message.channel.send("""คำสั่ง
jek leaw - ขอคำคมบาดใจ
jek เล่นไร *จำนวนคน* - สุ่มเกมจากจำนวนคน
jek เพิ่มเกม ชื่อเกม จำนวนคน - เพิ่มเกมในรายชื่อสุ่มตามจำนวนคน
jek ลบเกม ชื่อเกม *จำนวนคน* - ลบเกมออกจากรายชื่อสุ่ม ระบุจำนวนคนได้
jek joincookiefam email username - จอย CookieRun Family
jek leavecookiefam email/username - ออกจาก CookieRun Family
jek เติมโค้ด code - เติมโค้ดให้คนใน CookieRun Family ทั้งหมด
jek cookiefam - เช็ครายชื่อ Family *[ไม่ให้ดูแล้ว]* """)

        elif input_cmd[1] == "leaw":
            quote = get_quote()
            await message.channel.send(quote)
    
        elif input_cmd[1] == "เล่นไร":
            if len(input_cmd) >= 3:
                n = input_cmd[2]
            else:
                n = "3"
            random_game = get_game(n)
            await message.channel.send(random_game)

        elif input_cmd[1] == "เพิ่มเกม":
            game = input_cmd[2]
            n = input_cmd[3]
            update_game_list(game, n)

        elif input_cmd[1] == "ลบเกม":
            game = input_cmd[2]
            if len(input_cmd) < 4:
                n = "0"
            else:
                n = input_cmd[3]
            delete_game_list(game, n)

        elif input_cmd[1] == "joincookiefam":
            await message.channel.send(joinCookieFam(input_cmd[2], input_cmd[3]))

        elif input_cmd[1] == "leavecookiefam":
            await message.channel.send(leaveCookieFam(input_cmd[2]))
            
        elif input_cmd[1] == "เติมโค้ด":
            await message.channel.send("รอเจ๊กทำงานแปป")
            successful_redeem = []
            driver = webdriver.Firefox()
            driver.get("https://game.devplay.com/coupon/ck/en")
            for email in db["cookierun_email"]:
                driver.find_element_by_id('code-box').send_keys(input_cmd[2])
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
                    await message.channel.send("{username} redeemed".format(username = email[1]))
                elif alert_msg == "Please enter all 16 characters of a coupon code!":
                    await message.channel.send("code ไม่ถูก")
                    code_error = 1; break
                elif alert_msg == "Please check your DevPlay account!":
                    await message.channel.send("id/email ไม่ถูก : {email}".format(email = email[0]))
                elif alert_msg == "This coupon code has expired!":
                    await message.channel.send("หมดอายุ")
                    code_error = 1
                    break
                elif alert_msg == "Please check the coupon code!":
                    await message.channel.send("code ไม่ถูก")
                    code_error = 1; break
                elif alert_msg == "You have already used this coupon code on this account!":
                    await message.channel.send("ใช้ไปแล้ว")
                elif alert_msg == "This coupon code has already been used!":
                    await message.channel.send("code หมดโควตา")
                    code_error = 1; break
                elif alert_msg == "Unknown server error! Please try again later.":
                    await message.channel.send("เว็บล่มอยู่ ค่อยเติมใหม่")
                else:
                    await message.channel.send("เป็นไรไม่รู้ ต้องแก้ก่อนงับ")
                alert.accept()
                driver.get("https://game.devplay.com/coupon/ck/en")
                driver.refresh()
            if code_error != 1:
                await message.channel.send("เติมโค้ด {code} ให้ {n} คน เรียบร้อย".format(code = input_cmd[2], n=len(successful_redeem)))
                #await message.channel.send("{e}".format(e = "\n".join(successful_redeem)))
            else:
                alert.accept()
                await message.channel.send("เติมโค้ดไม่สำเร็จ")
            driver.close()
#        elif input_cmd[1] == "cookiefam":
#            for e in db["cookierun_email"]:
#                await message.channel.send("{e2}: {e1}".format(e2 = e[1], e1 = e[0]))
        
        else:
            await message.channel.send("อ่าน help ไม่ออกเหรอ")

my_secret = os.environ['botToken']

a = keep_alive()
client.run(my_secret)