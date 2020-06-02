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
    "X-Riot-Token": "RGAPI-ba095dc6-6dcb-47dd-b6f2-cf9da197ed22"
}

def get_match_ids(region):
    db = sqlite3.connect('players.sqlite')
    db2 = sqlite3.connect("new_tft.sqlite")
    im = db.cursor()
    im2 = db2.cursor()
    im2.execute(
        """CREATE TABLE IF NOT EXISTS match_ids(matchId)""")
    if region == 'euw1' :
        im.execute("SELECT * FROM players WHERE region='euw1'")
    elif region == 'br1':
        im.execute("SELECT * FROM players WHERE region='br1'")
    elif region == 'eun1':
        im.execute("SELECT * FROM players WHERE region='eun1'")
    elif region == 'tr1':
        im.execute("SELECT * FROM players WHERE region='tr1'")
    elif region == 'ru':
        im.execute("SELECT * FROM players WHERE region='ru'")
    elif region == 'na1':
        im.execute("SELECT * FROM players WHERE region='na1'")
    elif region == 'la1':
        im.execute("SELECT * FROM players WHERE region='la1'")
    elif region == 'la2':
        im.execute("SELECT * FROM players WHERE region='la2'")
    elif region == 'oc1':
        im.execute("SELECT * FROM players WHERE region='oc1'")
    elif region == 'kr':
        im.execute("SELECT * FROM players WHERE region='kr'")
    elif region == 'jp1':
        im.execute("SELECT * FROM players WHERE region='jp1'")


    for i in im:
        if i[3] == 'euw1' or i[3] == 'eun1' or i[3] == 'tr1' or i[3] == 'ru':
            print('adding new euw player')
            url = 'https://europe.api.riotgames.com/tft/match/v1/matches/by-puuid/{}/ids?count={}'.format(i[1], 10)
            try:
                request = requests.get(url, headers=headers, timeout=5)
            except requests.exceptions.HTTPError as errh:
                continue
            except requests.exceptions.ConnectionError as errc:
                continue
            except requests.exceptions.Timeout as errt:
                continue
            except requests.exceptions.RequestException as err:
                continue
            if request.status_code != 200:
                continue
            # print(counter, request.text)
            request = json.loads(request.text)
            for match in request:
                im2.execute("""INSERT OR IGNORE INTO match_ids(matchId) VALUES(?)""", (match,))
                db2.commit()
        elif i[3] == 'na1' or i[3] == 'br1' or i[3] == 'la1' or i[3] == 'la2' or i[3] == 'oc1':
            print('adding new na player')
            url = 'https://americas.api.riotgames.com/tft/match/v1/matches/by-puuid/{}/ids?count={}'.format(i[1], 10)
            try:
                request = requests.get(url, headers=headers, timeout=5)
            except requests.exceptions.HTTPError as errh:
                continue
            except requests.exceptions.ConnectionError as errc:
                continue
            except requests.exceptions.Timeout as errt:
                continue
            except requests.exceptions.RequestException as err:
                continue
            if request.status_code != 200:
                continue
            # print(counter, request.text)
            request = json.loads(request.text)
            for match in request:
                im2.execute("""INSERT OR IGNORE INTO match_ids(matchId) VALUES(?)""", (match,))
                db2.commit()
        elif i[3] == 'kr' or i[3] == 'jp1':
            print('adding new asian player')
            url = 'https://asia.api.riotgames.com/tft/match/v1/matches/by-puuid/{}/ids?count={}'.format(i[1], 10)
            try:
                request = requests.get(url, headers=headers, timeout=5)
            except requests.exceptions.HTTPError as errh:
                continue
            except requests.exceptions.ConnectionError as errc:
                continue
            except requests.exceptions.Timeout as errt:
                continue
            except requests.exceptions.RequestException as err:
                continue
            if request.status_code != 200:
                continue
            # print(counter, request.text)
            request = json.loads(request.text)
            for match in request:
                im2.execute("""INSERT OR IGNORE INTO match_ids(matchId) VALUES(?)""", (match,))
                db2.commit()
    im.close()
    im2.close()

def get_all_match_ids():
    a = datetime.now()
    pool = Pool(processes=10)
    regions = ['euw1', 'br1', 'eun1', 'jp1', 'kr', 'la1', 'la2', 'na1', 'oc1', 'ru', 'tr1']
    for region in regions:
        r1 = pool.apply_async(get_match_ids, [region])
    pool.close()
    pool.join()
    b = datetime.now()
    print("get_all_match_ids",b-a)


if __name__ == '__main__':
        get_all_match_ids()
        db =sqlite3.connect("new_tft.sqlite")
        im = db.cursor()
        im.execute("CREATE TABLE temp_table as SELECT DISTINCT * FROM match_ids;")
        im.execute("DELETE FROM match_ids;")
        im.execute("INSERT INTO match_ids SELECT * FROM temp_table")
        db.commit()
        im.close()