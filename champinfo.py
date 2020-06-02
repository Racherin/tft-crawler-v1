import sqlite3
import requests
import json
import time
import pandas as pd
from datetime import datetime
import operator
import ast
import copy
from operator import *
import os
from datetime import datetime
import shutil
import requests
import sqlite3
import json
import asyncio
from datetime import datetime
from multiprocessing import Pool


pd.options.display.float_format = '{:.2f}%'.format
pd.set_option('mode.chained_assignment', None)

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36 Edg/83.0.478.37",
    "Accept-Language": "en-US,en;q=0.9",
    "Accept-Charset": "application/x-www-form-urlencoded; charset=UTF-8",
    "Origin": "https://developer.riotgames.com",
    "X-Riot-Token": "RGAPI-ba095dc6-6dcb-47dd-b6f2-cf9da197ed22"
}


def getchampdata(region):
    a = datetime.now()
    global istopfour, iswin, item1, item3, item2
    db = sqlite3.connect('new_tft.sqlite')
    im = db.cursor()
    im2 = db.cursor()
    im.execute(
        """CREATE TABLE IF NOT EXISTS champion_data(id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,region,champ_name,tier,place,istopfour,iswin,item1,item2,item3,version,game_mode)""")
    im.execute("SELECT * FROM match_ids")
    counter = 0
    for i in im:
        match_region = i[0].split('_')[0]
        if region ==  match_region :
            if match_region == 'EUW1' or match_region == 'TR1' or match_region == 'EUN1' or match_region == 'RU':
                url = 'https://europe.api.riotgames.com/tft/match/v1/matches/{}'.format(i[0])
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
                    print(request.status_code)
                request = json.loads(request.text)
                try:
                    version = request['info']['game_version'].strip('Version ').split('(')[0].strip()
                    variant = request['info']['game_variation']
                except KeyError:
                    continue
                for ptc in request['info']['participants']:
                    placement = ptc['placement']
                    if int(placement) > 4:
                        istopfour = False
                    else:
                        istopfour = True
                    if int(placement) == 1:
                        iswin = True
                    else:
                        iswin = False
                    # print(placement, istopfour, iswin)
                    for unit in ptc['units']:
                        item1 = None
                        item2 = None
                        item3 = None
                        try:
                            item1 = unit['items'][0]
                            item2 = unit['items'][1]
                            item3 = unit['items'][2]
                        except:
                            pass
                        im2.execute(
                            """INSERT OR IGNORE INTO champion_data(region,champ_name,tier,place,istopfour,iswin,item1,item2,item3,version,game_mode) VALUES(?,?,?,?,?,?,?,?,?,?,?)""",
                            (
                                match_region, unit['character_id'].split('_')[1], unit['tier'], placement, istopfour,
                                iswin,
                                item1, item2, item3,
                                version, variant))
                        print('adding',region,'player')
                        # print(unit['character_id'].split('_')[1], unit['tier'], placement, istopfour, iswin, item1,item2, item3,version)
                db.commit()
            elif match_region == 'NA1' or match_region == 'BR1' or match_region == 'LA1' or match_region == 'LA2' or match_region == 'OC1':
                url = 'https://americas.api.riotgames.com/tft/match/v1/matches/{}'.format(i[0])
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
                request = json.loads(request.text)
                try:
                    version = request['info']['game_version'].strip('Version ').split('(')[0].strip()
                    variant = request['info']['game_variation']
                except KeyError:
                    continue
                for ptc in request['info']['participants']:

                    placement = ptc['placement']
                    if int(placement) > 4:
                        istopfour = False
                    else:
                        istopfour = True
                    if int(placement) == 1:
                        iswin = True
                    else:
                        iswin = False
                    # print(placement, istopfour, iswin)
                    for unit in ptc['units']:
                        item1 = None
                        item2 = None
                        item3 = None
                        try:
                            item1 = unit['items'][0]
                            item2 = unit['items'][1]
                            item3 = unit['items'][2]
                        except:
                            pass
                        im2.execute(
                            """INSERT OR IGNORE INTO champion_data(region,champ_name,tier,place,istopfour,iswin,item1,item2,item3,version,game_mode) VALUES(?,?,?,?,?,?,?,?,?,?,?)""",
                            (
                                match_region, unit['character_id'].split('_')[1], unit['tier'], placement, istopfour,
                                iswin,
                                item1, item2, item3,
                                version, variant))
                        print('adding',region,'player')

                    # print(unit['character_id'].split('_')[1], unit['tier'], placement, istopfour, iswin, item1,item2, item3,version)
                db.commit()
            elif match_region == 'KR' or match_region == 'JP1':
                url = 'https://asia.api.riotgames.com/tft/match/v1/matches/{}'.format(i[0])
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
                request = json.loads(request.text)
                try:
                    version = request['info']['game_version'].strip('Version ').split('(')[0].strip()
                    variant = request['info']['game_variation']
                except KeyError:
                    continue
                for ptc in request['info']['participants']:

                    placement = ptc['placement']
                    if int(placement) > 4:
                        istopfour = False
                    else:
                        istopfour = True
                    if int(placement) == 1:
                        iswin = True
                    else:
                        iswin = False
                    # print(placement, istopfour, iswin)
                    for unit in ptc['units']:
                        item1 = None
                        item2 = None
                        item3 = None
                        try:
                            item1 = unit['items'][0]
                            item2 = unit['items'][1]
                            item3 = unit['items'][2]
                        except:
                            pass
                        im2.execute(
                            """INSERT OR IGNORE INTO champion_data(region,champ_name,tier,place,istopfour,iswin,item1,item2,item3,version,game_mode) VALUES(?,?,?,?,?,?,?,?,?,?,?)""",
                            (
                                match_region, unit['character_id'].split('_')[1], unit['tier'], placement, istopfour,
                                iswin,
                                item1, item2, item3,
                                version, variant))
                        print('adding',region,'player')

                    # print(unit['character_id'].split('_')[1], unit['tier'], placement, istopfour, iswin, item1,item2, item3,version)
                db.commit()

def get_all_champ_data():
    a = datetime.now()
    pool = Pool(processes=10)
    regions = ['EUW1', 'BR1', 'EUN1', 'JP1', 'KR', 'LA1', 'LA2', 'NA1', 'OC1', 'RU', 'TR1']
    for region in regions:
        r1 = pool.apply_async(getchampdata, [region])
    pool.close()
    pool.join()
    b = datetime.now()
    print("get_all_champ_data",b-a)

if __name__ == '__main__':
    print('sa')