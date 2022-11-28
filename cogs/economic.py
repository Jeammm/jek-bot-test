import discord
from discord.ext import commands
import json
from discord_components import Button, ButtonStyle, Select, SelectOption
from datetime import datetime, timedelta
import psycopg2
import os

USERNAME = os.environ.get('USERNAME')
PASSWORD = os.environ.get('PASSWORD')
DATABASE_URL = os.environ.get('DATABASE_URL')
DAILY_REWARD = 100

class Economic(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.con = psycopg2.connect(DATABASE_URL, user=USERNAME, password=PASSWORD)
        self.con.autocommit = True

    @commands.command()
    async def wallet(self, ctx):
        try:
            cur = self.con.cursor()
            cur.execute(f"SELECT money FROM userwallets WHERE id='{ctx.author.id}';")
            data = cur.fetchall()
            if len(data) == 0:
                cur.execute(f"INSERT INTO userwallets(id, rankid, money) VALUES ('{ctx.author.id}', 2, 1000);")
                await ctx.send("`Wallet created! 1000.- jek coin received.`")
                cur.execute(f"SELECT money FROM userwallets WHERE id='{ctx.author.id}'")
                data = cur.fetchall()
            await ctx.send(f"`{ctx.author.name}'s wallet : {int(data[0][0]):,}`")
        except Exception as e:
            print(f"[ERROR] : {e}")

    @commands.command(name="give")
    async def give_command(self, ctx, member:discord.Member=None, amount=0.0):
        if amount < 0:
            await ctx.send("Bro, stop")
            return
        elif ctx.author == member:
            await ctx.send("Bro, stop")
            return

        async def callback(interaction):
            if interaction.author.id != ctx.author.id:
                await interaction.send("Go away you little kid")
            else:
                if interaction.custom_id == "confirm":
                    try:
                        cur = self.con.cursor()
                        cur.execute(f"SELECT id, money FROM userwallets WHERE id='{ctx.author.id}' OR id='{member.id}';")
                        data = cur.fetchall()
                        for row in data:
                            if row[0] == str(ctx.author.id):
                                cur.execute(f"UPDATE userwallets SET money={row[1]-amount} WHERE id='{row[0]}';")
                            else:
                                cur.execute(f"UPDATE userwallets SET money={row[1]+amount} WHERE id='{row[0]}';")
                        cur.execute(f"SELECT money FROM userwallets WHERE id='{ctx.author.id}';")
                        data=cur.fetchall()
                        emBed = discord.Embed(title="Transaction Confirmed", description=f"**From** : {ctx.author}\n**Amount** : {amount}\n**To** : {member}" , color=0xfbff00, timestamp=datetime.utcnow())
                        emBed.set_footer(text=f"Balance : {data[0][0]:,} coin", icon_url=ctx.author.avatar_url)
                        await interaction.edit_origin(embed=emBed, components=[])

                    except Exception as e:
                        await ctx.send(f"[ERROR] {e}")


                elif interaction.custom_id == "cancel":
                    emBed = discord.Embed(title="Transaction Canceled", color=0xfbff00)
                    await interaction.edit_origin(embed=emBed, components=[])

        try:
            cur = self.con.cursor()
            cur.execute(f"SELECT id, money FROM userwallets WHERE id='{ctx.author.id}' OR id='{member.id}';")
            wallet = cur.fetchall()
        except Exception as e:
            await ctx.send(f"[ERROR] {e}")


        if len(wallet) == 2:
            for row in wallet:
                if row[0] == str(ctx.author.id):
                    if amount > row[1]:
                        emBed=discord.Embed(title=f"{ctx.author.name}'s Account", description=f"**Balance** : {row[1]} coin", color=0x00ff62)
                        await ctx.send("You Broke Bro", embed=emBed)
                    else:
                        emBed=discord.Embed(title="Confirm Transaction", description=f"**From** : {ctx.author}\n**Amount** : {amount}\n**To** : {member}", color=0xfbff00)
                        transaction = await ctx.send(
                            embed=emBed,
                            components=[[
                                self.bot.components_manager.add_callback(
                                    Button(style=ButtonStyle.green, label="CONFIRM", custom_id="confirm"),callback
                                ),
                                self.bot.components_manager.add_callback(
                                    Button(style=ButtonStyle.red, label="CANCEL", custom_id="cancel"),callback
                                )
                            ]]
                        )

        elif len(wallet) == 1:
            if wallet[0][0] == str(ctx.author.id):
                await ctx.send("Reciever has no wallet, `jek wallet` now and get free 1,000 Jek coin")
            else:
                await ctx.send("Create wallet first, `jek wallet` now and get free 1,000 Jek coin")


    @give_command.error
    async def give_command_error(self, ctx, exc):
        if isinstance(exc, discord.ext.commands.errors.MemberNotFound):
            await ctx.send("Receiver not correct")
        else:
            await ctx.send(exc)

    @commands.command()
    async def checkin(self, ctx):
        datenow = datetime.utcnow() + timedelta(hours=7)
        datenow = datenow.strftime("%Y-%m-%d")
        try:
            cur = self.con.cursor()
            cur.execute(f"SELECT * FROM userwallets WHERE id='{ctx.author.id}';")
            if len(cur.fetchall()) == 0:
                await ctx.send("Create wallet first, `jek wallet` now and get free 1,000 Jek coin") 
                return
            cur.execute(f"SELECT * FROM checkins WHERE id='{ctx.author.id}' AND serverid='{ctx.guild.id}';")
            data = cur.fetchall()
            if len(data) == 0:
                cur.execute(f"INSERT INTO checkins(id, serverid, checkdate) VALUES ('{ctx.author.id}','{ctx.guild.id}','{datenow}');")
                cur.execute(f"""UPDATE userwallets
                                SET money=(SELECT money FROM userwallets WHERE id='{ctx.author.id}')+{DAILY_REWARD};""")
                await ctx.send(f"Wow, this is your first check in!. Take this {DAILY_REWARD} Jek coin <3")
            else:
                print(type(data[0][2]))
                print(str(data[0][2]) == datenow)
                if str(data[0][2]) == datenow:
                    await ctx.send("Come back tomorrow na")
                else:
                    cur.execute(f"UPDATE checkins SET checkdate='{datenow}' WHERE id='{ctx.author.id}';")
                    cur.execute(f"""UPDATE userwallets
                                    SET money=(SELECT money FROM userwallets WHERE id='{ctx.author.id}')+{DAILY_REWARD};""")
                    await ctx.send(f"Here is your free {DAILY_REWARD} Jek coin.")
            cur.close()
        except Exception as e:
            await ctx.send(f"[ERROR] {e}")

def setup(bot):
    bot.add_cog(Economic(bot))
