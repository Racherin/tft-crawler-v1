from sqlite3 import dbapi2 as sqlite3
from multiprocessing import Pool
from datetime import datetime
import requests
import time
import json
import pandas as pd


headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36 Edg/83.0.478.37",
    "Accept-Language": "en-US,en;q=0.9",
    "Accept-Charset": "application/x-www-form-urlencoded; charset=UTF-8",
    "Origin": "https://developer.riotgames.com",
    "X-Riot-Token": "RGAPI-1bab49fb-e3cd-446b-a751-d96d562ecdc7"
}

def get_item_data():
    global istopfour, iswin, item1, item3, item2
    db = sqlite3.connect("databases/champion_data.sqlite", )
    db2 = sqlite3.connect("databases/item_data.sqlite")
    im = db.cursor()
    im2 = db2.cursor()
    im3 = db2.cursor()
    im2.execute("""CREATE TABLE IF NOT EXISTS item_data(id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,region,item_name,place,istopfour,iswin,version,game_mode)""")
    df = pd.read_sql_query("SELECT * FROM champion_data WHERE item1 IS NOT NULL", db)
    for id, val in df.iterrows():
        if str(val['version']).startswith("10.12"):

            im3.execute(
            """INSERT INTO item_data(region,item_name,place,istopfour,iswin,version,game_mode) VALUES(?,?,?,?,?,?,?)""",
            (val['region'], val['item1'], val['place'], val['istopfour'], val['iswin'], val['version'],
             val['game_mode']))
    df = pd.read_sql_query("SELECT * FROM champion_data WHERE item2 IS NOT NULL", db)
    for id, val in df.iterrows():
        if str(val['version']).startswith("10.12"):
            im3.execute(
            """INSERT INTO item_data(region,item_name,place,istopfour,iswin,version,game_mode) VALUES(?,?,?,?,?,?,?)""",
            (val['region'], val['item2'], val['place'], val['istopfour'], val['iswin'], val['version'],
             val['game_mode']))
    df = pd.read_sql_query("SELECT * FROM champion_data WHERE item3 IS NOT NULL", db)
    for id, val in df.iterrows():
        if str(val['version']).startswith("10.12"):
            im3.execute(
            """INSERT INTO item_data(region,item_name,place,istopfour,iswin,version,game_mode) VALUES(?,?,?,?,?,?,?)""",
            (val['region'], val['item3'], val['place'], val['istopfour'], val['iswin'], val['version'],
             val['game_mode']))
    db2.commit()



def parse_item_data(game_mode):
    db = sqlite3.connect('databases/item_data.sqlite')
    json_data = dict()
    df = pd.read_sql_query("SELECT * FROM item_data", db)
    df_none = df[df['game_mode'] == game_mode]
    item_counts = df_none['item_name'].value_counts(normalize=True) * 100
    # print(item_counts)
    for item, val in item_counts.items():
        pick_rate = '{:.2f}'.format(val)
        selected_item = df[df['item_name'] == item]
        istopfour_rate = selected_item['istopfour'].value_counts(normalize=True) * 100
        iswin_rate = selected_item['iswin'].value_counts(normalize=True) * 100

        json_data["{}".format(item)] = {"win_rate": None, "top_four_rate": None,
                                        "pick_rate": pick_rate, }
        json_data["{}".format(item)]['win_rate'] = "{:.2f}".format(iswin_rate.to_dict()[1])
        json_data["{}".format(item)]['top_four_rate'] = "{:.2f}".format(istopfour_rate.to_dict()[1])
    with open('json_data/item_data/{}.json'.format(str(game_mode).split('_')[2]), "w") as json_file:
        json.dump(json_data, json_file)

def parse_all_item_data():
    a = datetime.now()
    pool2 = Pool(processes=10)
    game_modes = ['TFT3_GameVariation_None', 'TFT3_GameVariation_TwoStarCarousels', 'TFT3_GameVariation_MidGameFoN',
                  'TFT3_GameVariation_FreeRerolls',
                  'TFT3_GameVariation_Bonanza', 'TFT3_GameVariation_BigLittleLegends', 'TFT3_GameVariation_FreeNeekos',
                  'TFT3_GameVariation_StartingItems','TFT3_GameVariation_LittlerLegends']
    for mode in game_modes :
        r1 = pool2.apply_async(parse_item_data, [mode])
    pool2.close()
    pool2.join()
    b = datetime.now()
    print('parse_all_champs',b-a)

if __name__ == '__main__':
    get_item_data()