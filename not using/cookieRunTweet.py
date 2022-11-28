import discord
from discord.ext import commands, tasks
import tweepy
from replit import db
import json
from notification_beta import Notification_beta
import os

def go_get_tweets(api):
    if "recent_cr_tweet_id" not in db.keys():
        db["recent_cr_tweet_id"] = 1433414408340918279

    tweets = api.user_timeline(screen_name="auuathicha", since_id=int(db["recent_cr_tweet_id"])) #CRKingdomEN
    for tweet in tweets:
        if tweet.author.screen_name == "auuathicha":
            if db["recent_cr_tweet_id"] != tweet.id:
                db["recent_cr_tweet_id"] = tweet.id
                print(api.get_status(tweet.id).text)
                return api.get_status(tweet.id).text

def most_recent(api):
    with open("settings.json") as fp:
        data = json.loads(fp)
    if "lastest_tweet" not in data:
        data["lastest_tweet"] = 1433414408340918279
    
    tweets = api.user_timeline(screen_name="auuathicha", since_id=int(data["lastest_tweet"])) #CRKingdomEN
    for tweet in tweets:
        if tweet.author.screen_name == "auuathicha":
            if int(data["lastest_tweet"]) != int(tweet.id):
                data["lastest_tweet"] = int(tweet.id)
                print(api.get_status(tweet.id).text)
                with open("settings.json", 'w') as fp:
                    json.dump(data, fp, indent=4)

                return api.get_status(tweet.id).text


    return None


class Cookie_tweet(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

        consumer_key = os.environ['consumer_key']
        consumer_secret = os.environ['consumer_secret']
        callback_uri = "oob"
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret, callback_uri)
        redirect_url = auth.get_authorization_url()
        print(redirect_url)
        user_pint_input = input("pin : ")
        auth.get_access_token(user_pint_input)
        self.api = tweepy.API(auth)
        
    @tasks.loop(seconds=10)
    async def check_new_tweet(self):
        tweet = most_recent(self.api)
        if tweet != None:
            print(tweet)
            Notification_beta.broadcast(tweet)
        print("test")

    @commands.Cog.listener()
    async def on_message(self, ctx):
        self.check_new_tweet.start()


def setup(bot):
    bot.add_cog(Cookie_tweet(bot))
        
