import discord
from discord.ext import commands

from footballAPI import matches_request

class Football(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.leagues = {39:"Premier League", 140:"La Liga", 2:"UEFA Champions League"}

    def get_fixture(self, directory, leagues:dict, spec_date):
        return matches_request(directory, leagues, spec_date)

    @commands.command(aliases=["match"])
    async def football(self, ctx, *, spec_date=None):
        leagues_id = self.leagues

        data = self.get_fixture("football_log", self.leagues, spec_date)

        league_sep = {}
        for match in data:
            home = match["teams"]["home"]["name"]
            away = match["teams"]["away"]["name"]
            time = match["fixture"]["date"][11:16]
            if match["league"]["name"] in league_sep:
                league_sep[match["league"]["name"]].append([home, away, time])
            else:
                league_sep[match["league"]["name"]] = [[home, away, time]]

        if spec_date == None:
            emBed = discord.Embed(title="Matches Today", colour=discord.Colour.orange())
        else:
            emBed = discord.Embed(title=f"Matches {spec_date}", colour=discord.Colour.orange())

        for league, matches in league_sep.items():
            info = ""
            for match in matches:
                info += f"{match[0]} VS {match[1]} : {match[2]}\n"
            emBed.add_field(name=league, value=info, inline=False)


        await ctx.send(embed=emBed)


def setup(bot):
    bot.add_cog(Football(bot))
