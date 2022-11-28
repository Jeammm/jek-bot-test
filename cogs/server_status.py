import discord
from discord.ext import commands
import requests
import json
import datetime

def get_player_stat(json_data):
    return_data = {}
    return_data["name"] = json_data["global"]["name"]
    return_data["uid"] = json_data["global"]["uid"]
    return_data["level"] = json_data["global"]["level"]

    return_data["comp_rank_score"] = json_data["global"]["rank"]["rankScore"]
    return_data["comp_rank_name"] = json_data["global"]["rank"]["rankName"]

    return_data["arena_rank_score"] = json_data["global"]["arena"]["rankScore"]
    return_data["arena_rank_name"] = json_data["global"]["arena"]["rankScore"]

    return_data["battlepass"] = json_data["global"]["battlepass"]["level"]

    return_data["avata"] = json_data["global"]["avatar"]

    return return_data


class Server_status(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def apex(self, ctx):
        response = requests.get("https://api.mozambiquehe.re/servers?auth=nUGMrRe0pDgl9vmQVVZ2")
        json_data = json.loads(response.text)
        emBed = discord.Embed(title="Apex Legends server status", color=0xeda334)
        for zone, status in json_data["ApexOauth_Crossplay"].items():
            emBed.add_field(name=zone, value=f"Status : {status['Status']} \nPing : {status['ResponseTime']}")  
        await ctx.send(embed=emBed)

    @commands.command()
    async def rank(self, ctx, origin_name=None):
        
        with open("settings.json") as fp:
            data = json.load(fp)
        
        if "apex_player_data" not in data[str(ctx.guild.id)]:
            data[str(ctx.guild.id)]["apex_player_data"] = {}

        
        if not origin_name:
            search = str(ctx.author.id)
            if search in data[str(ctx.guild.id)]["apex_player_data"]:
                target_name = data[str(ctx.guild.id)]["apex_player_data"][search]
            else:
                await ctx.send("ต้องลงทะเบียนก่อนที่ jek apex_regis *origin_name*")
                return
        
        else:
            target_name = origin_name

        try:
            response = requests.get(f"https://api.mozambiquehe.re/bridge?version=5&platform=PC&player={target_name}&auth=nUGMrRe0pDgl9vmQVVZ2")
            json_data = json.loads(response.text)

            player_stat = get_player_stat(json_data)

            emBed = discord.Embed(title=player_stat["name"], description=player_stat["uid"], color=0xeda334)

            emBed.add_field(name="Level", value=player_stat["level"], inline=False)
            emBed.add_field(name="Rank", value=f"{player_stat['comp_rank_name']} : {player_stat['comp_rank_score']}", inline=False)
            emBed.add_field(name="Arena", value=f"{player_stat['arena_rank_name']} : {player_stat['arena_rank_score']}", inline=False)
            emBed.add_field(name="Battlepass Level", value=player_stat["battlepass"], inline=False)
            emBed.set_thumbnail(url=player_stat["avata"])
            await ctx.send(embed=emBed)
        
        except:
            await ctx.send("Error, check your spelling and try again. *(name given must be Origin account name)*")

    @commands.command()
    async def apex_regis(self, ctx, *, origin_name=None):
        if not origin_name:
            await ctx.send("ใส่ชื่อ id origin ด้วย")
            return

        with open("settings.json") as fp:
            data = json.load(fp)

        if "apex_player_data" not in data[str(ctx.guild.id)]:
            data[str(ctx.guild.id)]["apex_player_data"] = {}

        data[str(ctx.guild.id)]["apex_player_data"][str(ctx.author.id)] = origin_name

        with open("settings.json", 'w') as fp:
            json.dump(data, fp, indent=4)
            await ctx.send(f"ลงทะเบียน {ctx.author.name} ในชื่อ {origin_name}")

    @commands.command()
    async def apex_help(self, ctx):
        emBed = discord.Embed(title="Apex Legends API command", color=0xeda334)

        emBed.add_field(name="rank *origin_name*", value="Show Apex status of player given. If you have registered your name to jek bot, use 'jek rank'(name not required) to see your stats", inline=False)
        emBed.add_field(name="apex_regis *origin_name*", value="Register your origin name to jek bot database so you can you 'jek rank' to see your stats", inline=False)
        
        await ctx.send(embed=emBed)

def setup(bot):
    bot.add_cog(Server_status(bot))