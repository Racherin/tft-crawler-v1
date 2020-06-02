import sqlite3
from multiprocessing import Pool
import pandas as pd
from datetime import datetime
import requests
import time
import json


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
    global istopfour, iswin, item1, item3, item2
    url_region = str()
    db = sqlite3.connect("new_tft.sqlite")
    im = db.cursor()
    im2 = db.cursor()
    im.execute(
        """CREATE TABLE IF NOT EXISTS champion_data(id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,region,champ_name,tier,place,istopfour,iswin,item1,item2,item3,version,game_mode)""")
    if region == 'EUW1' :
        im2.execute("SELECT * FROM match_ids WHERE matchId LIKE 'EUW1%'")
        url_region = "europe"
    elif region == 'BR1':
        im2.execute("SELECT * FROM match_ids WHERE matchId LIKE 'BR1%'")
        url_region = "americas"

    for i in im2 :
        match_region = i[0].split('_')[0]
        url = 'https://{}.api.riotgames.com/tft/match/v1/matches/{}'.format(url_region,i[0])
        print(url)
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
            return
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
                print(
                            match_region, unit['character_id'].split('_')[1], unit['tier'], placement, istopfour,
                            iswin,
                            item1, item2, item3,
                            version, variant)
                im.execute(
                        """INSERT INTO champion_data(region,champ_name,tier,place,istopfour,iswin,item1,item2,item3,version,game_mode) VALUES(?,?,?,?,?,?,?,?,?,?,?)""",
                        (
                            match_region, unit['character_id'].split('_')[1], unit['tier'], placement, istopfour,
                            iswin,
                            item1, item2, item3,
                            version, variant))
    db.commit()
    im.close()
    im2.close()



def get_all_champ_data():
    a = datetime.now()
    pool = Pool(processes=10)
    regions = ['euw1', 'br1']
    for region in regions:
        r1 = pool.apply_async(getchampdata, [str(region).upper()])
    pool.close()
    pool.join()
    b = datetime.now()
    print("get_all_champ_data",b-a)

if __name__ == '__main__':
    get_all_champ_data()