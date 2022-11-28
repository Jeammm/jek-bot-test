import discord
from discord.ext import commands
import json
from urllib.request import urlopen

def currency_update():
    with urlopen("http://www.floatrates.com/daily/thb.json") as response:
            source = response.read()
            rate = json.loads(source)
    return rate

# def get_ex(currency,money:int):
#     rate = currency_update()
#     ex = rate[currency.lower()]["inverseRate"]
#     date = rate[currency.lower()]["date"]
#     amount = money*ex
#     emBed = discord.Embed()
#     emBed.add_field(name=f"{money:,.02f} {currency} = {amount:,.02f} บาท", value=f"{date}")
#     return emBed

def get_ex(currency,money:int):
    emBed = discord.Embed()
    emBed.add_field(name="Use `jek trade amount` instead", value=f"This thing is disabled")
    return emBed

class Exchange(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.rate = currency_update()

    #USD
    @commands.command(aliases=["usd", "$", "$USD"])
    async def USD(self, ctx, money:int):
        await ctx.send(embed=get_ex("USD",money))

    #EURO
    @commands.command(aliases=["ยูโร", "eur", "EURO", "euro", "€"])
    async def EUR(self, ctx, money:int):
        await ctx.send(embed=get_ex("EUR",money))

    #GBP
    @commands.command(aliases=["£", "ปอนด์", "gbp", "pound", "POUND"])
    async def GBP(self, ctx, money:int):
        await ctx.send(embed=get_ex("GBP",money))

    #JPY
    @commands.command(aliases=["¥JPY", "Yen", "yen", "เยน"])
    async def JPY(self, ctx, money:int):
        await ctx.send(embed=get_ex("JPY",money))

    #AUD
    @commands.command(aliases=["$AUD", "$aud", "aud", "ออส"])
    async def AUD(self, ctx, money:int):
        await ctx.send(embed=get_ex("AUD",money))

    #CHF
    @commands.command(aliases=["ฟรังก์", "chf", "swiss", "SWISS"])
    async def CHF(self, ctx, money:int):
        await ctx.send(embed=get_ex("CHF",money))

    #CAD
    @commands.command(aliases=["$CAD", "$cad", "แคนาดา", "cad"])
    async def CAD(self, ctx, money:int):
        await ctx.send(embed=get_ex("CAD",money))

    #KHR
    @commands.command(aliases=["กัมพูชา", "khr", "៛"])
    async def KHR(self, ctx, money:int):
        await ctx.send(embed=get_ex("KHR",money))

    #CNY
    @commands.command(aliases=["หยวน", "จีน", "	¥CNY", "cny"])
    async def CNY(self, ctx, money:int):
         await ctx.send(embed=get_ex("CNY",money))

    #HKD
    @commands.command(aliases=["ฮ่องกง", "hongkong", "hkd", "$HKD"])
    async def HKD(self, ctx, money:int):
         await ctx.send(embed=get_ex("HKD",money))

    #INR
    @commands.command(aliases=["อินเดีย", "รูปี", "₹", "inr"])
    async def INR(self, ctx, money:int):
         await ctx.send(embed=get_ex("INR",money))

    #KRW
    @commands.command(aliases=["เกาหลี", "วอน", "krw", "₩"])
    async def KRW(self, ctx, money:int):
         await ctx.send(embed=get_ex("KRW",money))

    #MYR
    @commands.command(aliases=["มาเล", "มาเลเซีย", "RM", "rm", "myr"])
    async def MYR(self, ctx, money:int):
         await ctx.send(embed=get_ex("MYR",money))

    #PHP
    @commands.command(aliases=["ฟิลิปปินส์", "php", "₱"])
    async def PHP(self, ctx, money:int):
         await ctx.send(embed=get_ex("PHP",money))

    #RUB
    @commands.command(aliases=["รัสเซีย", "รูเบิล", "rub", "ruble", "₽"])
    async def RUB(self, ctx, money:int):
         await ctx.send(embed=get_ex("RUB",money))

    #SGD
    @commands.command(aliases=["สิงคโปร์", "$SGD", "$sgd", "sgd"])
    async def SGD(self, ctx, money:int):
         await ctx.send(embed=get_ex("SGD",money))

    #THB
    @commands.command(aliases=["บาท", "ไทย", "฿", "thb", "baht", "Baht"])
    async def THB(self, ctx, money:int):
         await ctx.send("จะแปลงไทยเป็นไทยหรอ")

    #BND
    @commands.command(aliases=["บรูไน", "$BND", "bnd"])
    async def BND(self, ctx, money:int):
         await ctx.send(embed=get_ex("BND",money))

    #LAK
    @commands.command(aliases=["ลาว", "กีบ", "lak", "₭"])
    async def LAK(self, ctx, money:int):
         await ctx.send(embed=get_ex("LAK",money))

    #MMK
    @commands.command(aliases=["จ๊าต", "พม่า", "mmk", "Ks"])
    async def MMK(self, ctx, money:int):
         await ctx.send(embed=get_ex("MMK",money))

    #SAR
    @commands.command(aliases=["ซาอุ", "sar", "﷼"])
    async def SAR(self, ctx, money:int):
         await ctx.send(embed=get_ex("SAR",money))

def setup(bot):
    bot.add_cog(Exchange(bot))
