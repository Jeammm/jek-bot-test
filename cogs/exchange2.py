import discord
from discord.ext import commands
from discord_components import Button, ButtonStyle, Select, SelectOption
from urllib.request import urlopen
import json


def currency_update():
    with urlopen("http://www.floatrates.com/widget/00001504/0e72d886cbf1a57a7897d25c49095a40/thb.json") as response:
            source = response.read()
            rate = json.loads(source)
    return rate

class Exchange2(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.rate = currency_update()
        self.options = self.rate.keys()
        with open("flag_emoji.txt", encoding="utf8") as fp:
            self.data = json.loads(fp.read())

    def get_ex(self, currency, money):
        rate = currency_update()
        ex = rate[currency.lower()]["inverseRate"]
        date = rate[currency.lower()]["date"]
        amount = money*ex
        emBed = discord.Embed()
        emBed.add_field(name=f"{self.data[currency.lower()]} {money:,.02f} {currency.upper()} = {amount:,.02f} บาท 🇹🇭", value=f"{date}")
        return emBed

    @commands.command(aliases=['ex'])
    async def trade(self, ctx, amount):

        async def callback(interaction):
            currency, amount = interaction.values[0].split()
            await interaction.edit_origin(embed=self.get_ex(currency, int(amount)))#embed=get_ex("USD",amount)

        await ctx.send(
            embed=self.get_ex("USD",int(amount)),
            components=[
                self.bot.components_manager.add_callback(
                    Select(
                        options=[SelectOption(label=currency.upper(), description=self.rate[currency]["name"], emoji=self.data[currency], value=f"{currency} {amount}") for currency in self.options]
                    ),callback
                )
            ],
        )



def setup(bot):
    bot.add_cog(Exchange2(bot))
