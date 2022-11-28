import discord
from discord.ext import commands
import asyncio

class Help2(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        self.page_0 = discord.Embed(title="test1")
        self.page_0.add_field(name="page1", value="work")

        self.page_1 = discord.Embed(title="test2")
        self.page_1.add_field(name="page2", value="work")

        self.page_2 = discord.Embed(title="test3")
        self.page_2.add_field(name="page3", value="work")

        self.current = 0
        self.bot.pages = [self.page_0, self.page_1, self.page_2]
        self.buttons = [u"\u23EA", u"\u25C0", u"\u25B6", u"\u23E9"]

    @commands.command()
    async def help2(self, ctx):

        self.help_message = await ctx.send(embed=self.page_0)

        for button in self.buttons:
            await self.help_message.add_reaction(button)

        while True:
            try: 
                reaction, user = await self.bot.wait_for("reaction_add", check=lambda reaction, user: user == ctx.author and reaction.emoji in self.buttons, timeout=60.0)
                print(reaction.emoji == u"\u23EA", user)

            except asyncio.TimeoutError:
                emBed = self.bot.pages[self.current]
                emBed.set_footer(text="Timed Out.")
                await self.help_message.clear_reactions()

            else:
                self.previous_page = self.current

                if reaction.emoji == u"\u23EA":
                    self.current = 0

                elif reaction.emoji == u"\u25C0":
                    if self.current > 0:
                        self.current -= 1

                elif reaction.emoji == u"\u25B6":
                    if self.current > 0:
                        self.current += 1
                    
                elif reaction.emoji == u"\u23E9":
                    if self.current < len(self.bot.pages)-1:
                        self.current = len(self.bot.pages)-1

                for button in self.buttons:
                    await self.help_message.remove_reaction(button, ctx.author)

                if self.current != self.previous_page:
                    await self.help_message.edit(embed=self.bot.pages[self.current])

def setup(bot):
    bot.add_cog(Help2(bot))