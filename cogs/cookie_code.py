import discord
from discord.ext import commands
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.firefox import GeckoDriverManager
import json
import os
import psycopg2

USERNAME = os.environ.get('USERNAME')
PASSWORD = os.environ.get('PASSWORD')
DATABASE_URL = os.environ.get('DATABASE_URL')

class CookieCode(commands.Cog):

    def __init__(self, bot):
        self.bot = bot        
        self.con = psycopg2.connect(DATABASE_URL, user=USERNAME, password=PASSWORD)

    @commands.command()
    async def reg(self, ctx, email):
        try:
            cur = self.con.cursor()
            cur.execute(f"SELECT email FROM emails WHERE id='{ctx.author.id}' AND email='{email}';")
            data = cur.fetchall()
            if len(data) == 0:
                cur.execute(f"INSERT INTO emails(id,email) VALUES ('{ctx.author.id}','{email}')")
                con.commit()
                await ctx.send(f"Added {email} to redeeming list.")
            else:
                await ctx.send(f"{email} already on the list.")
            cur.close()
        except Exception as error:
            print(f"error: {error}")
    
    @commands.command()
    async def redeem(self, ctx, *, code=None):
        if code == None:
            try:
                replyed = await ctx.channel.fetch_message(ctx.message.reference.message_id)
                code = replyed.content
            except AttributeError:
                await ctx.send("jek redeem `code`")
                return
        
        try:
            cur = self.con.cursor()
            cur.execute(f"SELECT email FROM emails WHERE id='{ctx.author.id}';")
            data = cur.fetchall()
            cur.close()
        except Exception as error:
            print(f"error: {error}")
        
        if len(data) == 0:
            await ctx.send("Can't find your accounts in the database")
            return
        
        emails = [e[0] for e in data]
        print(len(emails))

        waiting = await ctx.channel.send(f"Redeeming {len(emails)} accounts")
        
        chrome_options = webdriver.ChromeOptions()
        chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--no-sandbox")
        
        driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), chrome_options=chrome_options)
#         driver = webdriver.Firefox(executable_path=GeckoDriverManager().install())
        driver.set_window_position(0, 0)
        driver.set_window_size(500, 500)
        driver.get("https://game.devplay.com/coupon/ck/en")
        for count, email in enumerate(emails):
            email_box = WebDriverWait(driver, 60).until(EC.visibility_of_element_located((By.XPATH, "/html/body/div/div[1]/div[2]/form/div[1]/input")))
            code_box = WebDriverWait(driver, 60).until(EC.visibility_of_element_located((By.XPATH, "/html/body/div/div[1]/div[2]/form/div[2]/input")))
            button = WebDriverWait(driver, 60).until(EC.visibility_of_element_located((By.XPATH, "/html/body/div/div[1]/div[2]/form/div[4]/div")))

            email_box.send_keys(email)
            code_box.send_keys(code)
            button.click()

            try:
                WebDriverWait(driver, 10).until(EC.alert_is_present(),"  ")
                alert = driver.switch_to.alert
                alert_msg = alert.text
            except TimeoutException:
                alert_msg = "Unknown error. Please try again later."
                driver.close()
                return

            if alert_msg == "Done! Log in to the game to claim your reward!":
                await ctx.channel.send(f"{count+1} : Successfully redeemed : {code}")
            elif alert_msg == "Please check your DevPlay account!":
                await ctx.channel.send(f"{count+1} : id/email ไม่ถูก")
            elif alert_msg == "You have already used this coupon code on this account!":
                await ctx.channel.send(f"{count+1} : ใช้ไปแล้ว")

            elif alert_msg == "Please enter all 16 characters of a coupon code!":
                await ctx.channel.send("code ไม่ครบ")
            elif alert_msg == "This coupon code has expired!":
                await ctx.channel.send("หมดอายุแน้ว")
            elif alert_msg == "Please check the coupon code!":
                await ctx.channel.send("code ไม่ถูก")
            elif alert_msg == "This coupon code has already been used!":
                await ctx.channel.send("code หมดโควตา")
            elif alert_msg == "Unknown server error! Please try again later.":
                await ctx.channel.send("เว็บล่มอยู่ ค่อยเติมใหม่")
            else:
                await ctx.channel.send("เป็นไรไม่รู้ ต้องแก้ก่อนงับ")
            alert.accept()
            driver.refresh()
            if alert_msg in ["Please enter all 16 characters of a coupon code!", "This coupon code has expired!", "Please check the coupon code!", "This coupon code has already been used!", "Unknown server error! Please try again later."]:
                break
        driver.close()
        await waiting.delete()


def setup(bot):
    bot.add_cog(CookieCode(bot))
