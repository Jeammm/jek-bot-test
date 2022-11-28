import discord
from discord.ext import commands
import json
import psycopg2
import os

DATABASE_URL = os.environ.get('DATABASE_URL')
USERNAME = os.environ.get('USERNAME')
PASSWORD = os.environ.get('PASSWORD')

class Notification_beta(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot
        
        
    def check_permission(self, ctx):
        con = None
        try:
            con = psycopg2.connect(DATABASE_URL, user=USERNAME, password=PASSWORD)
            cur = con.cursor()
            cur.execute(f"SELECT rankid FROM userwallets WHERE id='{ctx.author.id}';")
            data = cur.fetchall()
            cur.close()
        except Exception as error:
            print(f"error: {error}")
        finally:
            if con is not None:
                con.close()
                
        return data[0][0]
        
    #set the channel as notification channel for broadcast
    @commands.command()
    async def setup(self, ctx):
        con = None
        try:
            con = psycopg2.connect(DATABASE_URL, user=USERNAME, password=PASSWORD)
            cur = con.cursor()
            cur.execute(f"SELECT notificationchannel FROM serverlists WHERE serverid='{ctx.guild.id}';")
            data = cur.fetchall()
            
            if len(data) == 1:
                print(f"UPDATE serverlists SET notificationchannel='{ctx.channel.id}' WHERE serverid='{ctx.guild.id}';")
                cur.execute(f"UPDATE serverlists SET notificationchannel='{ctx.channel.id}' WHERE serverid='{ctx.guild.id}';")
            else:
                cur.execute(f"INSERT INTO serverlists(serverid,notificationchannel) VALUES ('{ctx.guild.id}','{ctx.channel.id}')")
            await ctx.send(f"set #{ctx.channel.name} as notification channel")
            
            con.commit()
            cur.close()
        except Exception as error:
            print(f"error: {error}")
        finally:
            if con is not None:
                con.close()

    
    #broadcast to all channel that set as notification channel (one per server)
    @commands.command()
    async def broadcast(self, ctx, *, msg):
        if self.check_permission(ctx) != 0:
            await ctx.send("You don't have permission")
            return
        
        con = None
        try:
            con = psycopg2.connect(DATABASE_URL, user=USERNAME, password=PASSWORD)
            cur = con.cursor()
            cur.execute(f"SELECT notificationchannel FROM serverlists;")
            data = cur.fetchall()
            con.commit()
            cur.close()
        except Exception as error:
            print(f"error: {error}")
        finally:
            if con is not None:
                con.close()
        
        target_channel = []
        for guild in data:
            if guild[0] is not None:
                target_channel.append(int(guild[0])) 
        print("broadcastting to", target_channel)
        
        for guild in self.bot.guilds:
            for channel in guild.text_channels:
                if channel.id in target_channel:
                    try:
                        await channel.send(msg)
                        print(f"Broadcasted {msg} to #{channel.name}; {guild.name}")
                    except Exception as e:
                        print(f"{e} in {channel.name}")

    #remove notification channel from database
    @commands.command() 
    async def recall(self, ctx):
        con = None
        try:
            con = psycopg2.connect(DATABASE_URL, user=USERNAME, password=PASSWORD)
            cur = con.cursor()
            cur.execute(f"SELECT notificationchannel FROM serverlists WHERE serverid='{ctx.guild.id}';")
            data = cur.fetchall()
            
            if len(data) == 1:
                print(f"UPDATE serverlists notificationchannel='{ctx.channel.id}' WHERE serverid='{ctx.guild.id}';")
                cur.execute(f"UPDATE serverlists SET notificationchannel=NULL WHERE serverid='{ctx.guild.id}';")
            else:
                cur.execute(f"INSERT INTO serverlists(serverid) VALUES ('{ctx.guild.id}')")
            await ctx.send(f"Notification channel removed")
            
            con.commit()
            cur.close()
        except Exception as error:
            print(f"error: {error}")
        finally:
            if con is not None:
                con.close()
    
    @commands.command()
    async def emergency(self, ctx, *, msg):
        if self.check_permission(ctx) == 0: #if author is admin
            for guild in self.bot.guilds:
                await guild.text_channels[0].send(msg)
        else:
            await ctx.send("You don't have permission")
            
    @commands.command()
    async def fetch_guild(self, ctx):
        try:
            con = psycopg2.connect(DATABASE_URL, user=USERNAME, password=PASSWORD)
            cur = con.cursor()
            
            cur.execute(f"SELECT serverid FROM serverlists;")
            table = cur.fetchall()
            data = [e[0] for e in table]
            
            def qescape(text):
                if "'" in text:
                    pos = text.find("'")
                    qtext = text[:pos] + "'" + text[pos:]
                    return qtext
                else:
                    return text
            
            command = []
            
            for guild in self.bot.guilds:
                owner_name = await self.bot.fetch_user(int(guild.owner_id))
                owner_name = qescape(owner_name.name)
                server_name = qescape(guild.name)
                
                if str(guild.id) not in data:
                    command.append(f"""INSERT INTO ServerLists(serverid, servername, ownerid, ownername, n_member) VALUES ('{guild.id}', '{server_name}', '{guild.owner_id}', '{owner_name}', {guild.member_count});""")
#                     print(f"""INSERT INTO ServerLists(serverid, servername, ownerid, ownername, n_member) VALUES ('{guild.id}', '{server_name}', '{guild.owner_id}', '{owner_name}', {guild.member_count});""")
                else:
                    command.append(f"""UPDATE ServerLists SET servername='{server_name}', ownerid='{guild.owner_id}', ownername='{owner_name}', n_member={guild.member_count} WHERE serverid='{guild.id}';""")
#                     print(f"""UPDATE ServerLists SET servername='{server_name}', ownerid='{guild.owner_id}', ownername='{owner_name}', n_member={guild.member_count} WHERE serverid='{guild.id}';""")
            
            await ctx.send(f"Updated {len(command)} servers")
            cur.execute("\n".join(command))
            con.commit() 
            cur.close()
        except Exception as error:
            print(f"error: {error}")
        finally:
            if con is not None:
                con.close()
                
    @commands.command()
    async def fetch_member(self, ctx):
        try:
            con = psycopg2.connect(DATABASE_URL, user=USERNAME, password=PASSWORD)
            cur = con.cursor()
        
            def qescape(text):
                if text is None:
                    return None
                elif "'" in text:
                    pos = text.find("'")
                    qtext = text[:pos] + "'" + text[pos:]
                    return qtext
                else:
                    return text
            
            insert_list = []

            for guild in self.bot.guilds:
                for member in guild.members:
                    if member.nick is None:
                        insert_list.append(f"""INSERT INTO userdata(id, serverid, name) VALUES ('{member.id}','{guild.id}', '{qescape(member.name)}');""")
                    else:
                        insert_list.append(f"""INSERT INTO userdata(id, serverid, name, nickname) VALUES ('{member.id}','{guild.id}', '{qescape(member.name)}', '{qescape(member.nick)}');""")

            cur.execute(f"DELETE FROM userdata;")
            cur.execute("\n".join(insert_list))
            
            con.commit()
            await ctx.send(f"Updated {len(insert_list)} users")
            cur.close()
        except Exception as error:
            print(f"error: {error}")
        finally:
            if con is not None:
                con.close()
        
        

def setup(bot):
    bot.add_cog(Notification_beta(bot))