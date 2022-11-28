import discord
from discord.ext import commands
import random
import os

class Game_get(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=["สุ่มเกม"])
    async def get_game(self, ctx, player=3):
        print(player)
        with open("game_list.txt") as fp:
            game_list = {}
            for line in fp.readlines():
                data = line.strip().split() #[n_player, game, game, game]

                if game_list == {} and data == []:
                    await ctx.send("ไม่มีเกมให้เลือกเลยคับ")
                    return
                
                game_list[int(data[0])] = data[1:]

            if player == 1:
                await ctx.send("ไม่มีเพื่อนเล่นอ่อ")
            elif player == 0:
                await ctx.send(random.choice(["อืม", "ครับ", "เค"]))
            elif player in game_list.keys():
                game = random.choice(game_list[int(player)])
                await ctx.send(game)
            else:
                await ctx.send("วาดรูป")
            
    @commands.command(aliases=["เพิ่มเกม"])
    async def add_game(self, ctx, game, *, n):
        target_n = [int(e) for e in n if e.isnumeric()]
        update = 0
        game_row = ""
        with open("game_list.txt", 'r') as fp:
            for line in fp.readlines():
                data = line.strip().split() #[n_player, game, game, game]
                n_player = int(data[0])
                this_row_game = data[1:]

                if (n_player in target_n) and (game not in this_row_game):
                    temp = data.append(game)
                    update = 1
                    game_row += " ".join(temp) + "\n"
                else:
                    game_row += " ".join(data) + "\n"
                print(game_row)

        with open("game_list.txt", "w") as fp:
            fp.write(game_row.strip())

        if update == 1:
            await ctx.send(f"เพิ่มเกม {game} แร้ว")
        else:
            await ctx.send(f"เพิ่มเกมไม่สำเร็จ")

def setup(bot):
    bot.add_cog(Game_get(bot))