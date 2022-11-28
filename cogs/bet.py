import discord
from discord.ext import commands
from discord_components import Button, ButtonStyle, Select, SelectOption
import json
import pytz
from datetime import datetime, timedelta
import os
import asyncio
import asyncpg

USERNAME = os.environ.get('USERNAME')
PASSWORD = os.environ.get('PASSWORD')
DATABASE_URL = os.environ.get('DATABASE_URL')
LEAGUE = {39:"Premier League", 140:"La Liga", 2:"UEFA Champions League"}

OPTIONS = {
    "🏠": 0,
    "🤝": 1,
    "🚌": 2,
    "❌": 3,
}

class Bet(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    def get_str_today_date(self):
        today = datetime.now(pytz.timezone('Asia/Bangkok'))
        today_str = str(today).split()[0]
        return today_str

    def get_str_tomorrow_date(self):
        tomorrow = datetime.now(pytz.timezone('Asia/Bangkok')) + timedelta(days=1)
        tomorrow_str = str(tomorrow).split()[0]
        return tomorrow_str

    def get_teams_from_id(self, match_id:list, days:list):
        match_name = {}
        directory = "football_log"
        for day in days:
            matches = matches_request(directory, self.leagues, day)

            for number in match_id:
                for match in matches:
                    if match["fixture"]["id"] == number:
                        match_name[number] = f'{match["teams"]["home"]["name"]} VS {match["teams"]["away"]["name"]}'
                        break
        return match_name

    def get_matches(self):
        match_odd = {}
        days = [self.get_str_today_date(), self.get_str_tomorrow_date()]
        for day in days:
            data = self.get_fixture("bet_log", self.leagues, day)
            for match in data:
                match_odd[match["fixture"]["id"]] = match["bookmakers"][0]["bets"][0]["values"] + [match["fixture"]["timestamp"]]
        return match_odd

    def get_fixture(self, directory, leagues:dict, spec_date):
        return odds_request(directory, leagues, spec_date)

    @commands.command()
    async def bet(self, ctx, amount = "0"):
        if not amount.isnumeric() or float(amount)<0:
            await ctx.send("ใส่ตัวเลขให้ถูกงับ")
            return
        else:
            amount = float(amount)

        await ctx.trigger_typing()

        try:
            con = await asyncpg.connect(DATABASE_URL, user=USERNAME, password=PASSWORD)
            wallet = await con.fetch(f"SELECT money FROM userwallets WHERE id='{ctx.author.id}';")
            if len(wallet) == 0:
                await ctx.send("Create wallet first, `jek wallet` now and get free 1000 Jek coin")
                return
            elif amount > wallet[0][0]:
                await ctx.send("เงินไม่พออะเตง")
                return
        except Exception as e:
            await ctx.send(f"[ERROR] {e}")
        finally:
            await con.close()


        # async def callback(interaction):
        #     if interaction.author.id != ctx.author.id:
        #         await interaction.send("This panel does not belong to you.")
        #         return
        #
        #     def _check(r, u):
        #         return (
        #             r.emoji in OPTIONS.keys()
        #             and u == ctx.author
        #             and r.message.id == msg.id
        #         )
        #
        #     name = match_name[int(interaction.values[0].split()[0])]
        #     odd = data[int(interaction.values[0].split()[0])]
        #     home = odd[0]["odd"]
        #     draw = odd[1]["odd"]
        #     away = odd[2]["odd"]
        #
        #     emBed = discord.Embed(
        #         title=f"{name} {amount} coin",
        #         description=f"Home : {home}\nDraw : {draw}\nAway : {away}",
        #         colour=ctx.author.colour,
        #         timestamp=datetime.utcnow()
        #     )
        #     emBed.set_footer(text=f"{ctx.author.display_name}", icon_url=ctx.author.avatar_url)
        #
        #     msg = await interaction.send(embed=emBed, ephemeral=False)
        #     for emoji in list(OPTIONS.keys()):
        #         await msg.add_reaction(emoji)
        #
        #     try:
        #         reaction, _ = await self.bot.wait_for("reaction_add", timeout=60.0, check=_check)
        #     except asyncio.TimeoutError:
        #         await msg.delete()
        #         await ctx.message.delete()
        #         await bet_menu.delete()
        #     else:
        #         click = OPTIONS[reaction.emoji]
        #         if click == 3:
        #             await msg.delete()
        #         else:
        #             bet_on = odd[click]["value"]
        #             try:
        #                 await bet_menu.delete()
        #                 await ctx.send(f"**{name}** : {interaction.author.name} bet __{amount}__ on __{bet_on}__")
        #                 await msg.delete()
        #                 await ctx.message.delete()
        #                 with open("jek-better.txt", 'a') as fp:
        #                     fp.write(f"{datetime.now(pytz.timezone('Asia/Bangkok'))} // {int(interaction.values[0].split()[0])} // {interaction.values[0].split()[1]} // {interaction.author.id} // {amount}*{[home,draw,away][click]} // {bet_on}\n")
        #
        #                 accounts[str(interaction.author.id)] -= float(amount)
        #
        #                 with open("bet-account.txt", 'w') as ba:
        #                     json.dump(accounts, ba, indent=4)
        #
        #             except discord.errors.NotFound:
        #                 await msg.delete()
        #                 await ctx.send("ลงไปแล้ว อยากลงเพิ่มก็กดใหม่")

        # leagues_id = self.leagues
        # data = self.get_matches()

        try:
            con = await asyncpg.connect(DATABASE_URL, user=USERNAME, password=PASSWORD)
            matches = await con.fetch(f"SELECT date,league,home,away, odd FROM FootballMatches WHERE league IN (SELECT id FROM leagues;);")
        except Exception as e:
            await ctx.send(f"[ERROR] {e}")
        finally:
            await con.close()

        emBed = discord.Embed(title="Today Selection")

        match_name = self.get_teams_from_id(data.keys(), [self.get_str_today_date(), self.get_str_tomorrow_date()])

        for match_id, match_info in data.items():

            home = match_info[0]["odd"]
            draw = match_info[1]["odd"]
            away = match_info[2]["odd"]
            info = f"Home : {home}\nDraw : {draw}\nAway : {away}"
            emBed.add_field(name = f"{match_name[match_id]}\n{str(datetime.fromtimestamp(data[match_id][3], pytz.timezone('Asia/Bangkok')))[:16]}", value=info)

        if amount != 0:
            try:
                emBed.set_footer(text=f"{ctx.author.display_name} : {amount} coin", icon_url=ctx.author.avatar_url)
                bet_menu = await ctx.send(
                    embed=emBed,
                    components=[
                        self.bot.components_manager.add_callback(
                            Select(
                                options=[SelectOption(label=match_name[match_id], description=f"ID : {match_id}", value=f"{match_id} {str(datetime.fromtimestamp(data[match_id][3], pytz.timezone('Asia/Bangkok')))[:10]}") for match_id in data.keys() if data[match_id][3] > datetime.timestamp(datetime.now())]
                            ),callback
                            )
                        ],
                    )
            except Exception:
                emBed.set_footer(text="No available match", icon_url=ctx.author.avatar_url)
                await ctx.send(embed=emBed)
        else:
            await ctx.send("`jek bet amount` to place bet",embed=emBed)

    def football_result(self, days:list):
        matches = []
        directory = "football_result"
        for day in days:
            match = matches_request(directory, self.leagues, day)
            matches += match
        return matches

    @commands.command()
    async def claim(self, ctx):
        await ctx.trigger_typing()
        with open("bet-account.txt") as ba:
            account = json.loads(ba.read())
            if str(ctx.author.id) not in account:
                await ctx.send("Create account first, `jek wallet` now and get free 1000 coin")
                return

        with open("jek-better.txt") as fp:
            bet_data = fp.readlines()

        emBed = discord.Embed(title=ctx.author.name, color=0xff0000)
        change = False
        total_reward = 0
        bets = []
        matches_date = []

        for i in range(len(bet_data)):
            try:
                date, match_id, match_date, user_id, odd, predict = bet_data[i].split(" // ")
                predict = predict.strip()
            except ValueError:
                continue

            if user_id == str(ctx.author.id):
                match_result = get_match_from_id("football_result", match_id)
                if match_result["fixture"]["status"]["short"] == "FT":
                    bet_data[i] = []
                    change = True
                    if match_result["goals"]["home"] > match_result["goals"]["away"]:
                        winner = "Home"
                    elif match_result["goals"]["home"] < match_result["goals"]["away"]:
                        winner = "Away"
                    else:
                        winner = "Draw"

                    pay = odd.split("*")
                    if predict == winner:
                        reward = float(pay[0]) * float(pay[1])
                        total_reward += reward
                    else:
                        reward = 0

                    if winner == "Home":
                        match_name_highlight = f'__{match_result["teams"]["home"]["name"]}__ VS {match_result["teams"]["away"]["name"]}'
                    elif winner == "Away":
                        match_name_highlight = f'{match_result["teams"]["home"]["name"]} VS __{match_result["teams"]["away"]["name"]}__'
                    else:
                        match_name_highlight = f'{match_result["teams"]["home"]["name"]} VS {match_result["teams"]["away"]["name"]}'

                    if reward == 0:
                        emBed.add_field(name=f"{match_name_highlight}", value=f"reward : -{pay[0]}", inline = False)
                    else:
                        emBed.add_field(name=f"{match_name_highlight}", value=f"reward : +{reward}", inline = False)
                else:
                    match_name_highlight = f'{match_result["teams"]["home"]["name"]} VS {match_result["teams"]["away"]["name"]}'
                    emBed.add_field(name=f"{match_name_highlight}", value="The game is not over yet", inline = False)


        emBed.set_footer(text=f"Wallet : {account[str(ctx.author.id)]+total_reward} (+{total_reward})", icon_url=ctx.author.avatar_url)
        if total_reward >= 1500:
            emBed.set_image(url="https://cdn.substack.com/image/fetch/f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fbucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com%2Fpublic%2Fimages%2Fa4b8647a-09e8-4576-95de-e622dcc38d72_1280x720.jpeg")
        await ctx.send(embed=emBed)

        if change:
            with open("bet-account.txt") as ba:
                account = json.loads(ba.read())
                account[str(ctx.author.id)] += total_reward

            with open("bet-account.txt", 'w') as ba:
                json.dump(account, ba, indent=4)

        with open("jek-better.txt", 'w') as fp:
            for line in bet_data:
                if line != [] and line != "" and line != "\n":
                    fp.write(f"{line}")


    @commands.command()
    async def mybet(self, ctx):
        with open("jek-better.txt") as fp:
            data = fp.readlines()
        mybet_dict = {}
        match_name = {}
        for line in data:
            if line == "":
                break
            bet = line.split(" // ")
            place_date = bet[0][:16]
            match_id = bet[1]
            match_date = bet[2]
            holder = bet[3]
            odd = bet[4].split("*")
            side = bet[5].strip()

            if holder == str(ctx.author.id):
                if match_date not in mybet_dict:
                    mybet_dict[match_date] = [{"match_id":int(match_id), "place_date":place_date, "price":odd[0], "odd":odd[1], "side":side}]
                else:
                    mybet_dict[match_date].append({"match_id":int(match_id), "place_date":place_date, "price":odd[0], "odd":odd[1], "side":side})

        info = ""
        for match_date, bets in mybet_dict.items():
            matches_id = [bet["match_id"] for bet in bets]
            matches_name = self.get_teams_from_id(matches_id, [match_date])
            for bet in bets:
                match_name = matches_name[bet["match_id"]].split(" VS ")
                if bet["side"] == "Home":
                    match_name[0] = f"**{match_name[0]}**"
                elif bet["side"] == "Away":
                    match_name[1] = f"**{match_name[1]}**"

                info += f'`{bet["place_date"]}` : {match_name[0]} VS {match_name[1]} : {bet["price"]} * {bet["odd"]}\n'

        emBed = discord.Embed(title=f"{ctx.author.name}'s bet", description=info, color=0x006eff)
        await ctx.send(embed=emBed)


def setup(bot):
    bot.add_cog(Bet(bot))
