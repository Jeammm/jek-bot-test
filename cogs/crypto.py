import discord
from discord.ext import commands
from pycoingecko import CoinGeckoAPI
from discord_components import Button, ButtonStyle, Select, SelectOption
import json
import pytz
from datetime import datetime, timedelta
import asyncio
import os
import psycopg2

DATABASE_URL = os.environ.get('DATABASE_URL')
USERNAME = os.environ.get('USERNAME')
PASSWORD = os.environ.get('PASSWORD')

OPTIONS = {
    "✅": 0,
    "❌": 1,
}

SUPPORTED_COIN = ['bitcoin', 'litecoin', 'ethereum', 'dogecoin', 'bitkub-coin', 'shiba-inu', 'binance-usd']
SUPPORTED_COIN_LOWER = ['bitcoin', 'litecoin', 'ethereum', 'dogecoin', 'bitkubcoin', 'shibainu', 'binanceusd']

class Crypto(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.cg = CoinGeckoAPI()
        self.con = psycopg2.connect(DATABASE_URL, user=USERNAME, password=PASSWORD)
        self.con.autocommit = True
        
    def get_price(self, spec=None):
        if spec == None:
            coin_prices = self.cg.get_price(ids=SUPPORTED_COIN, vs_currencies='usd')
            return coin_prices
        else:
            coin_prices = self.cg.get_price(ids=spec, vs_currencies='usd')
            return coin_prices
    
    @commands.command(aliases=["coin", "crypto"])
    async def buy(self, ctx, amount=None):
        if amount == None:
            coin_prices = self.get_price()
            emBed = discord.Embed(title="Current Price!")
            
            for coin, usd in coin_prices.items():
                emBed.add_field(name=coin.upper(), value=f"{usd['usd']} Jek coin", inline=True)
            await ctx.send("`jek buy coin amount` to buy coin", embed=emBed)
            return
        
        elif amount == 0:
            await ctx.send(">0 pls")
            return

        async def callback(interaction):
            if interaction.author.id != ctx.author.id:
                await interaction.send("This panel does not belong to you.")
                return

            def _check(r, u):
                return (
                    r.emoji in OPTIONS.keys()
                    and u == ctx.author
                    and r.message.id == msg.id
                )

            coin_recieve = amount/float(self.get_price(interaction.values[0])[interaction.values[0]]['usd'])

            emBed = discord.Embed(
                title='Confirm order',
                description=f"{amount} Jek coin -> {coin_recieve} {interaction.values[0]}",
                colour=ctx.author.colour,
                timestamp=datetime.utcnow()
            )
            emBed.set_footer(text=f"{ctx.author.display_name}", icon_url=ctx.author.avatar_url)

            msg = await interaction.send(embed=emBed, ephemeral=False)
            for emoji in list(OPTIONS.keys()):
                await msg.add_reaction(emoji)

            try:
                reaction, _ = await self.bot.wait_for("reaction_add", timeout=60.0, check=_check)
            except asyncio.TimeoutError:
                await msg.delete()
                await ctx.message.delete()
                await bet_menu.delete()
            else:
                click = OPTIONS[reaction.emoji]
                if click == 1:
                    await msg.delete()
                else:
                    try:
                        cur = self.con.cursor()
                        coin_name = ''.join([i for i in interaction.values[0] if i.isalpha()])
                        cur.execute(f"SELECT money, {coin_name} FROM userwallets WHERE id='{ctx.author.id}';")
                        data = cur.fetchall()
                        cur.execute(f"UPDATE userwallets SET money={data[0][0]-amount}, {coin_name}={data[0][1]+coin_recieve} WHERE id='{ctx.author.id}';")
                        
                        await buy_menu.delete()
                        await msg.delete()
                        await ctx.message.delete()
                        await ctx.send(f"`{ctx.author.name} : Confirmed {amount} Jek coin -> {coin_recieve} {interaction.values[0]}`")

                    except discord.errors.NotFound:
                        await msg.delete()
                        await ctx.send("ซื้อไปแล้ว อยากซื้อเพิ่มก็กดใหม่")


        if not amount.isnumeric():
            await ctx.send("ใส่ตัวเลขให้ถูกงับ")
            return
        
        else:
            amount = float(amount)
        await ctx.trigger_typing()
        
        try:
            cur = self.con.cursor()
            cur.execute(f"SELECT * FROM userwallets WHERE id='{ctx.author.id}';")
            wallet = cur.fetchall()
            if len(wallet) == 0:
                await ctx.send("`Create an wallet first, `jek wallet` now and get free 1,000 Jek coin`")
                return
            if float(amount) > wallet[0][2]:
                await ctx.send("เงินไม่พออะเตง", delete_after=10)
                return
        except Exception as e:
            await ctx.send(f"[ERROR] {e}")

        emBed = discord.Embed(title="Which one")
        coin_prices = self.get_price()
        for coin, usd in coin_prices.items():
            emBed.add_field(name=coin.upper(), value=f"{usd['usd']} Jek coin", inline=True)
        emBed.set_footer(text=f"{ctx.author.display_name} : {amount} Jek coin", icon_url=ctx.author.avatar_url)

        buy_menu = await ctx.send(
            embed=emBed,
            components=[
                self.bot.components_manager.add_callback(
                    Select(
                        options=[SelectOption(label=coin.upper(), description=f"{usd['usd']} Jek coin", value=coin) for coin, usd in coin_prices.items()]
                    ),callback
                    )
                ],
            )
        
    @commands.command()
    async def sell(self, ctx, amount=None, coin=None):
        if not amount.isnumeric() or float(amount) < 0:
            await ctx.send(">0 pls")
            return
        
        coin = ''.join([i for i in coin.lower() if i.isalpha()])
        if coin != None and coin in SUPPORTED_COIN_LOWER:
            try:
                cur = self.con.cursor()
                cur.execute(f"SELECT {coin}, money FROM userwallets WHERE id='{ctx.author.id}';")
                port = cur.fetchall()
                if port[0][0] < float(amount):
                    await ctx.send(f"`You only have {port[0][0]:,} {coin.upper()}`")
                else:
                    coin_price = self.get_price(coin)
                    recieve_jek = float(amount)*coin_price[coin]['usd'] + port[0][1]
                    cur.execute(f"UPDATE userwallets SET money={recieve_jek}, {coin}={port[0][0]-float(amount)} WHERE id='{ctx.author.id}';")
                    cur.execute(f"SELECT {coin},money FROM userwallets WHERE id='{ctx.author.id}';")
                    data = cur.fetchall()
                    await ctx.send(f"{data[0][0]} {coin} , {data[0][1]} Jek coin")
                
            except Exception as e:
                await ctx.send(f"[ERROR] {e}")
                
        else:        
            coin_prices = self.get_price()
            emBed = discord.Embed(title="Current Price!")
            
            for coin, usd in coin_prices.items():
                emBed.add_field(name=coin.upper(), value=f"{usd['usd']} Jek coin", inline=True)
            await ctx.send("`jek buy coin amount` to buy coin", embed=emBed)

#         port = self.get_portfolio()
#         if str(ctx.author.id) not in port:
#             port[str(ctx.author.id)] = {}
#             with open(self.database, 'w') as ba:
#                 json.dump(port, ba, indent=4)
# 
#         try:
#             coin_prices = self.get_price(list(port[str(ctx.author.id)].keys()))
#         except:
#             await ctx.send("no coin")
#             return
# 
# 
#         emBed = discord.Embed(title="Portfolio")
#         for coin_name, size in port[str(ctx.author.id)].items():
#             emBed.add_field(name=coin_name.upper(), value=f"{size} {coin_name} -> {coin_prices[coin_name]['usd']*size} Jek coin", inline=False)
# 
#         if coin == None or amount == None:
#             await ctx.send("`jek sell amount coin` to sell coin", embed=emBed)
#         else:
#             jek_recieve = float(amount)*coin_prices[coin]['usd']
#             self.update_portfolio(ctx.author.id, coin, float(amount), buying=False)
#             await ctx.send(f"{ctx.author.name} : {self.get_portfolio()[str(ctx.author.id)][coin]} {coin} left and recieve {jek_recieve} Jek coin")
# 
#             wallet = self.get_wallets()
#             wallet[str(ctx.author.id)] += jek_recieve
#             self.update_wallets(wallet)

def setup(bot):
    bot.add_cog(Crypto(bot))

