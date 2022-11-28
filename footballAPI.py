import requests
import json
import pytz
from datetime import datetime, timedelta
import os

def matches_request(directory, leagues:dict, spec_date):
    if spec_date != None:
          today_str = spec_date
    else:
      today = datetime.now(pytz.timezone('Asia/Bangkok'))
      today_str = str(today).split()[0]

    if f"{today_str}.txt" in os.listdir(f'./{directory}'):
      with open(f"{directory}/{today_str}.txt") as fp:
          matches = json.loads(fp.read())

    else:
      matches = []
      url = "https://api-football-v1.p.rapidapi.com/v3/fixtures"
      querystring = {"date":f"{today_str}", "timezone":"Asia/Bangkok"}
      headers = {
          'x-rapidapi-host': "api-football-v1.p.rapidapi.com",
          'x-rapidapi-key': "999ba1e36cmshdb9a22b0a52d227p1180bcjsn778b41c652cc"
          }
      response = requests.request("GET", url, headers=headers, params=querystring)
      data = json.loads(response.text)
      data = data["response"]
      for match in data:
          if match["league"]["id"] in leagues:
              matches += [match]

      with open(f"{directory}/{today_str}.txt", 'w') as fp:
          json.dump(matches, fp, indent=4)

    return matches

def odds_request(directory, leagues:dict, spec_date):
    today_str = spec_date
    matches = []
    if f"{today_str}.txt" in os.listdir(f'./{directory}'):
        with open(f"{directory}/{today_str}.txt") as fp:
            data = json.loads(fp.read())
            matches = data

    else:
        i = 1
        print("bets loading",end="")
        while True:
            url = "https://api-football-v1.p.rapidapi.com/v3/odds"
            querystring = {"date":spec_date,"timezone":"Asia/Bangkok","page":f"{i}","bookmaker":"5"}
            headers = {
                'x-rapidapi-host': "api-football-v1.p.rapidapi.com",
                'x-rapidapi-key': "999ba1e36cmshdb9a22b0a52d227p1180bcjsn778b41c652cc"
                }
            response = requests.request("GET", url, headers=headers, params=querystring)
            raw = json.loads(response.text)
            data = raw["response"]
            for match in data:
                print(".",end="")
                if match["league"]["id"] in leagues:
                    matches += [match]
            i += 1
            if i > raw["paging"]["total"]:
                break

        with open(f"{directory}/{today_str}.txt", 'w') as fp:
            json.dump(matches, fp, indent=4)
    return matches

def get_match_from_id(directory, match_id):
    if f"{match_id}.txt" in os.listdir(f'./{directory}'):
        with open(f"{directory}/{match_id}.txt") as fp:
            data = json.loads(fp.read())
        if data["fixture"]["status"]["short"] == "FT":
            return data
        elif data["fixture"]["timestamp"] > datetime.timestamp(datetime.now()):
            return data

    url = "https://api-football-v1.p.rapidapi.com/v3/fixtures"
    querystring = {"id":f"{match_id}"}
    headers = {
        'x-rapidapi-host': "api-football-v1.p.rapidapi.com",
        'x-rapidapi-key': "999ba1e36cmshdb9a22b0a52d227p1180bcjsn778b41c652cc"
        }
    response = requests.request("GET", url, headers=headers, params=querystring)
    raw = json.loads(response.text)
    data = raw["response"][0]
    with open(f"{directory}/{match_id}.txt", 'w') as fp:
        json.dump(data, fp, indent=4)
    return data
