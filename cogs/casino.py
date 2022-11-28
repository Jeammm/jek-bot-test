import discord
from discord.ext import commands
import random
import asyncio
from discord_components import Button, ButtonStyle, Select, SelectOption
from async_timeout import timeout


class Card:
    def __init__(self, value, color):
        self.value = value
        self.color = color
        self.name  = f"{value}{color}"
        self.secret= "__"
        if value == "A":
            self.num = 11
        elif value in ['J', 'Q', 'K']:
            self.num = 10
        else:
            self.num = int(value)

class Casino(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.guild_deck = {}

    def create_deck(self):
        colors = ['♡', '♢', '♤', '♧']
        values = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']
        deck = [Card(value, color) for value in values for color in colors]
        random.shuffle(deck)
        return deck

    @commands.command()
    async def deck(self, ctx):
        if ctx.guild.id not in self.guild_deck:
            self.guild_deck[ctx.guild.id] = self.create_deck()
            await ctx.send("Deck shuffled", delete_after=10)
        elif len(self.guild_deck[ctx.guild.id]) == 0:
            self.guild_deck[ctx.guild.id] = self.create_deck()
            await ctx.send("Deck shuffled", delete_after=10)
        else:
            await ctx.send(f"{len(self.guild_deck[ctx.guild.id])} cards left in the deck")

    @commands.command()
    async def draw(self, ctx, amount=1):
        if ctx.guild.id not in self.guild_deck:
            self.guild_deck[ctx.guild.id] = self.create_deck()
            await ctx.send("Deck shuffled", delete_after=10)
        elif len(self.guild_deck[ctx.guild.id]) == 0:
            await ctx.send("No more card")
            return

        if amount > len(self.guild_deck[ctx.guild.id]):
            await ctx.send(f"only {len(self.guild_deck[ctx.guild.id])} cards left in the deck")
            return

        cards = []
        for i in range(amount):
            cards.append(self.guild_deck[ctx.guild.id].pop(0).name)
        await ctx.reply(" | ".join(cards))



def setup(bot):
    bot.add_cog(Casino(bot))
