import discord
from discord.ext import commands
import json
import os
import asyncpg
import asyncio
from discord_components import Button, ButtonStyle

DATABASE_URL = os.environ.get('DATABASE_URL')
USERNAME = os.environ.get('USERNAME')
PASSWORD = os.environ.get('PASSWORD')

class hbd(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
    
    @commands.command()
    async def hbd_pp(self, ctx, memberid, *, nickname):
        con = await asyncpg.connect(DATABASE_URL, user=USERNAME, password=PASSWORD)
        data = await con.fetch(f"SELECT serverid FROM userdata WHERE id='{memberid}';")
        await con.close()
        data = [e[0] for e in data]
        user_object = await self.bot.fetch_user(memberid)
        
        async def callback(interaction):
            await interaction.edit_origin()
            await interaction.channel.send(f"{(interaction.author).mention} said HBD {nickname}!")
        
        for guild in self.bot.guilds:
            if str(guild.id) in data:                
                await guild.text_channels[0].send(
                            f"Today is {user_object.mention}'s birthday! click here to say HBD to {nickname}.",
                            components=[[
                                self.bot.components_manager.add_callback(
                                    Button(style=ButtonStyle.green, label=f"HBD {nickname}!", custom_id="hbd"),callback
                                ),
                            ]]
                        )

def setup(bot):
    bot.add_cog(hbd(bot))