import requests
import sqlite3
import json
import asyncio
from datetime import datetime
from multiprocessing import Pool

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36 Edg/83.0.478.37",
    "Accept-Language": "en-US,en;q=0.9",
    "Accept-Charset": "application/x-www-form-urlencoded; charset=UTF-8",
    "Origin": "https://developer.riotgames.com",
    "X-Riot-Token": "RGAPI-1bab49fb-e3cd-446b-a751-d96d562ecdc7"
}
def get_challengers(region):
    db = sqlite3.connect("databases/players.sqlite")
    im = db.cursor()
    url = 'https://{}.api.riotgames.com/tft/league/v1/{}'.format(region, 'challenger')
    im.execute(
        """CREATE TABLE IF NOT EXISTS players(id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,puuid, summonerName,region,wins,loses)""")
    try:
        player_list = requests.get(url, headers=headers, timeout=5)
    except requests.exceptions.HTTPError as errh:
        pass
    except requests.exceptions.ConnectionError as errc:
        pass
    except requests.exceptions.Timeout as errt:
        pass
    except requests.exceptions.RequestException as err:
        pass
    if player_list.status_code != 200:
        player_list.raise_for_status()
        return
    player_list = json.loads(player_list.text)['entries']
    for player in player_list:
        url2 = 'https://{}.api.riotgames.com/tft/summoner/v1/summoners/{}'.format(region, player['summonerId'])
        try:
            player_data = requests.get(url2, headers=headers, timeout=5)
        except requests.exceptions.HTTPError as errh:
            continue
        except requests.exceptions.ConnectionError as erer:
            continue
        except requests.exceptions.Timeout as ere:
            continue
        except requests.exceptions.RequestException as gfv:
            continue
        if player_data.status_code != 200:
            player_data.raise_for_status()
            return
        player_data = json.loads(player_data.text)
        data = (player_data['puuid'], player['summonerName'], region, player['wins'], player['losses'])
        im.execute("""INSERT INTO players(puuid, summonerName,region,wins,loses) VALUES (?,?,?,?,?)""",
                   data)
        #print("adding new", region, "challenger", data[1])
        db.commit()

def get_all_challengers():
    a = datetime.now()
    pool = Pool(processes=10)
    regions = ['euw1', 'br1', 'eun1', 'jp1', 'kr', 'la1', 'la2', 'na1', 'oc1', 'ru', 'tr1']
    for region in regions:
        r1 = pool.apply_async(get_challengers, [region])
    pool.close()
    pool.join()
    b = datetime.now()
    print("get_all_challengers",b-a)

def get_grandmasters(region):
    db = sqlite3.connect("databases/players.sqlite")
    im = db.cursor()
    url = 'https://{}.api.riotgames.com/tft/league/v1/{}'.format(region, 'grandmaster')
    im.execute(
        """CREATE TABLE IF NOT EXISTS players(id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,puuid, summonerName,region,wins,loses)""")
    try:
        player_list = requests.get(url, headers=headers, timeout=5)
    except requests.exceptions.HTTPError as errh:
        pass
    except requests.exceptions.ConnectionError as errc:
        pass
    except requests.exceptions.Timeout as errt:
        pass
    except requests.exceptions.RequestException as err:
        pass
    if player_list.status_code != 200:
        player_list.raise_for_status()
        return
    player_list = json.loads(player_list.text)['entries']
    for player in player_list:
        url2 = 'https://{}.api.riotgames.com/tft/summoner/v1/summoners/{}'.format(region, player['summonerId'])
        try:
            player_data = requests.get(url2, headers=headers, timeout=5)
        except requests.exceptions.HTTPError as errh:
            continue
        except requests.exceptions.ConnectionError as erer:
            continue
        except requests.exceptions.Timeout as ere:
            continue
        except requests.exceptions.RequestException as gfv:
            continue
        if player_data.status_code != 200:
            player_data.raise_for_status()
            return
        player_data = json.loads(player_data.text)
        data = (player_data['puuid'], player['summonerName'], region, player['wins'], player['losses'])
        im.execute("""INSERT INTO players(puuid, summonerName,region,wins,loses) VALUES (?,?,?,?,?)""",
                   data)
        #print("adding new", region, "grandmaster", data[1])
        db.commit()

def get_all_grandmasters():
    a = datetime.now()
    pool = Pool(processes=10)
    regions = ['euw1', 'br1', 'eun1', 'jp1', 'kr', 'la1', 'la2', 'na1', 'oc1', 'ru', 'tr1']
    for region in regions:
        r1 = pool.apply_async(get_grandmasters, [region])
    pool.close()
    pool.join()
    b = datetime.now()
    print("get_all_grandmasters",b-a)

def get_masters(region):
    db = sqlite3.connect("databases/players.sqlite")
    im = db.cursor()
    url = 'https://{}.api.riotgames.com/tft/league/v1/{}'.format(region, 'master')
    im.execute(
        """CREATE TABLE IF NOT EXISTS players(id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,puuid, summonerName,region,wins,loses)""")
    try:
        player_list = requests.get(url, headers=headers, timeout=5)
    except requests.exceptions.HTTPError as errh:
        pass
    except requests.exceptions.ConnectionError as errc:
        pass
    except requests.exceptions.Timeout as errt:
        pass
    except requests.exceptions.RequestException as err:
        pass
    if player_list.status_code != 200:
        player_list.raise_for_status()
        return
    player_list = json.loads(player_list.text)['entries']
    for player in player_list:
        url2 = 'https://{}.api.riotgames.com/tft/summoner/v1/summoners/{}'.format(region, player['summonerId'])
        try:
            player_data = requests.get(url2, headers=headers, timeout=5)
        except requests.exceptions.HTTPError as errh:
            continue
        except requests.exceptions.ConnectionError as erer:
            continue
        except requests.exceptions.Timeout as ere:
            continue
        except requests.exceptions.RequestException as gfv:
            continue
        if player_data.status_code != 200:
            player_data.raise_for_status()
            return
        player_data = json.loads(player_data.text)
        data = (player_data['puuid'], player['summonerName'], region, player['wins'], player['losses'])
        im.execute("""INSERT INTO players(puuid, summonerName,region,wins,loses) VALUES (?,?,?,?,?)""",
                   data)
        #print("adding new", region, "master", data[1])
        db.commit()

def get_all_masters():
    a = datetime.now()
    pool = Pool(processes=10)
    regions = ['euw1', 'br1', 'eun1', 'jp1', 'kr', 'la1', 'la2', 'na1', 'oc1', 'ru', 'tr1']
    for region in regions:
        r1 = pool.apply_async(get_masters, [region])
    pool.close()
    pool.join()
    b = datetime.now()
    print("get_all_masters",b-a)


if __name__ == '__main__':
    get_all_masters()
