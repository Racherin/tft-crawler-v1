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
    "X-Riot-Token": ""
}


def getchampdata(region):
    global istopfour, iswin, item1, item3, item2
    url_region = str()
    db = sqlite3.connect("databases/match_ids.sqlite", )
    db2 = sqlite3.connect("databases/champion_data.sqlite")
    im = db.cursor()
    im2 = db2.cursor()
    im3 = db2.cursor()
    im2.execute(
        """CREATE TABLE IF NOT EXISTS champion_data(id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,region,champ_name,tier,place,istopfour,iswin,item1,item2,item3,version,game_mode)""")
    if region == 'EUW1':
        im.execute("SELECT * FROM match_ids WHERE matchId LIKE 'EUW1%'")
        url_region = "europe"
    elif region == 'BR1':
        im.execute("SELECT * FROM match_ids WHERE matchId LIKE 'BR1%'")
        url_region = "americas"
    elif region == 'LA1':
        im.execute("SELECT * FROM match_ids WHERE matchId LIKE 'LA1%'")
        url_region = "americas"
    elif region == 'LA2':
        im.execute("SELECT * FROM match_ids WHERE matchId LIKE 'LA2%'")
        url_region = "americas"
    elif region == 'NA1':
        im.execute("SELECT * FROM match_ids WHERE matchId LIKE 'NA1%'")
        url_region = "americas"
    elif region == 'OC1':
        im.execute("SELECT * FROM match_ids WHERE matchId LIKE 'OC1%'")
        url_region = "americas"
    elif region == 'TR1':
        im.execute("SELECT * FROM match_ids WHERE matchId LIKE 'TR1%'")
        url_region = "europe"
    elif region == 'RU':
        im.execute("SELECT * FROM match_ids WHERE matchId LIKE 'RU%'")
        url_region = "europe"
    elif region == 'EUN1':
        im.execute("SELECT * FROM match_ids WHERE matchId LIKE 'EUN1%'")
        url_region = "europe"
    elif region == 'KR':
        im.execute("SELECT * FROM match_ids WHERE matchId LIKE 'KR%'")
        url_region = "asia"
    elif region == 'JP1':
        im.execute("SELECT * FROM match_ids WHERE matchId LIKE 'JP1%'")
        url_region = "asia"
    counter = 0;
    for i in im:
        match_region = i[0].split('_')[0]
        url = 'https://{}.api.riotgames.com/tft/match/v1/matches/{}'.format(url_region, i[0])
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
                if str(version).startswith("10.15"):
                    im3.execute(
                        """INSERT INTO champion_data(region,champ_name,tier,place,istopfour,iswin,item1,item2,item3,version,game_mode) VALUES(?,?,?,?,?,?,?,?,?,?,?)""",
                        (
                            match_region, unit['character_id'].split('_')[1], unit['tier'], placement, istopfour,
                            iswin,
                            item1, item2, item3,
                            version, variant))
            db2.commit()


def parsechampdata(game_mode):
    a = datetime.now()
    json_data = dict()
    champ_names = {'Ahri': ['starguardian', 'sorcerer'],
                   'Annie': ['mechpilot', 'sorcerer'],
                   'Ashe': ['celestial', 'sniper'],
                   'AurelionSol': ['rebel', 'starship'],
                   'Bard': ['astro', 'mystic'],
                   'Blitzcrank': ['chrono', 'brawler'],
                   'Caitlyn': ['chrono', 'sniper'],
                   'Cassiopeia': ['battlecast', 'mystic'],
                   'Ezreal': ['chrono', 'blaster'],
                   'Ekko': ['cybernetic', 'infiltrator'],
                   'Darius': ['spacepirate', 'manareaver'],
                   'Fiora': ['cybernetic', 'blademaster'],
                   'Fizz': ['mechpilot', 'infiltrator'],
                   'Gangplank': ['spacepirate', 'mercenary', 'demolitionist'],
                   'Graves': ['spacepirate', 'blaster'],
                   'Gnar': ['astro', 'brawler'],
                   'Illaoi': ['battlecast', 'brawler'],
                   'Irelia': ['cybernetic', 'manareaver', 'blademaster'],
                   'Janna': ['starguardian', 'paragon'],
                   'JarvanIV': ['darkstar', 'protector'],
                   'Jayce': ['spacepirate', 'vanguard'],
                   'Jhin': ['darkstar', 'sniper'],
                   'Jinx': ['rebel', 'blaster'],
                   'Karma': ['darkstar', 'mystic'],
                   'KogMaw': ['battlecast', 'brawler'],
                   'Leona': ['cybernetic', 'vanguard'],
                   'Lucian': ['cybernetic', 'blaster'],
                   'Lulu': ['celestial', 'mystic'],
                   'Malphite': ['rebel', 'brawler'],
                   'MasterYi': ['rebel', 'blademaster'],
                   'Mordekaiser': ['darkstar', 'vanguard'],
                   'Nautilus': ['astro', 'vanguard'],
                   'Neeko': ['starguardian', 'protector'],
                   'Nocturne': ['battlecast', 'infiltrator'],
                   'Poppy': ['starguardian', 'vanguard'],
                   'Rakan': ['celestial', 'protector'],
                   'Rumble': ['mechpilot', 'demolitionist'],
                   'Shaco': ['darkstar', 'infiltrator'],
                   'Shen': ['chrono', 'blademaster'],
                   'Syndra': ['starguardian', 'sorcerer'],
                   'Soraka': ['starguardian', 'mystic'],
                   'Riven': ['chrono', 'blademaster'],
                   'Teemo': ['astro', 'sniper'],
                   'Thresh': ['chrono', 'manareaver'],
                   'TwistedFate': ['chrono', 'sorcerer'],
                   'Urgot': ['battlecast', 'protector'],
                   'Vayne': ['cybernetic', 'sniper'],
                   'Vi': ['cybernetic', 'brawler'],
                   'Viktor': ['battlecast', 'sorcerer'],
                   'WuKong': ['chrono', 'vanguard'],
                   'Xayah': ['celestial', 'blademaster'],
                   'Xerath': ['darkstar', 'sorcerer'],
                   'XinZhao': ['celestial', 'protector'],
                   'Yasuo': ['rebel', 'blademaster'],
                   'Zed': ['rebel', 'infiltrator'],
                   'Ziggs': ['rebel', 'demolitionist'],
                   'Zoe': ['starguardian', 'sorcerer']}
    one_cost_units = ['Caitlyn', 'Fiora', 'Graves', 'JarvanIV', 'Leona', 'Malphite', 'Poppy', 'TwistedFate',
                      'Xayah',
                      'Ziggs', 'Zoe', 'Illaoi', 'Nocturne']
    two_cost_units = ['Ahri', 'Annie', 'Blitzcrank', 'Darius', 'Lucian', 'Mordekaiser', 'Rakan', 'Shen',
                      'XinZhao', 'Yasuo', 'KogMaw', 'Nautilus', 'Zed']
    three_cost_units = ['Ashe', 'Ezreal', 'Jayce', 'Karma', 'MasterYi', 'Neeko', 'Rumble', 'Shaco',
                        'Syndra', 'Vi', 'Bard', 'Cassiopeia', 'Vayne']
    four_cost_units = ['Fizz', 'Irelia', 'Jhin', 'Jinx', 'Soraka', 'WuKong', 'Gnar', 'Riven', 'Teemo', 'Viktor']
    five_cost_units = ['Gangplank', 'Lulu', 'Thresh', 'Xerath', 'Janna', 'Urgot', 'AurelionSol','Ekko']
    db = sqlite3.connect('databases/champion_data.sqlite')
    if game_mode == 'TFT3_GameVariation_None':
        df = pd.read_sql_query("SELECT * FROM champion_data WHERE game_mode == 'TFT3_GameVariation_None'", db)
    elif game_mode == 'TFT3_GameVariation_TwoStarCarousels':
        df = pd.read_sql_query("SELECT * FROM champion_data WHERE game_mode == 'TFT3_GameVariation_TwoStarCarousels'",
                               db)
    elif game_mode == 'TFT3_GameVariation_MidGameFoN':
        df = pd.read_sql_query("SELECT * FROM champion_data WHERE game_mode == 'TFT3_GameVariation_MidGameFoN'", db)
    elif game_mode == 'TFT3_GameVariation_FreeRerolls':
        df = pd.read_sql_query("SELECT * FROM champion_data WHERE game_mode == 'TFT3_GameVariation_FreeRerolls'", db)
    elif game_mode == 'TFT3_GameVariation_Bonanza':
        df = pd.read_sql_query("SELECT * FROM champion_data WHERE game_mode == 'TFT3_GameVariation_Bonanza'", db)
    elif game_mode == 'TFT3_GameVariation_TwoItemMax':
        df = pd.read_sql_query("SELECT * FROM champion_data WHERE game_mode == 'TFT3_GameVariation_TwoItemMax'",
                               db)
    elif game_mode == 'TFT3_GameVariation_Dreadnova':
        df = pd.read_sql_query("SELECT * FROM champion_data WHERE game_mode == 'TFT3_GameVariation_Dreadnova'", db)
    elif game_mode == 'TFT3_GameVariation_StartingItems':
        df = pd.read_sql_query("SELECT * FROM champion_data WHERE game_mode == 'TFT3_GameVariation_StartingItems'", db)
    elif game_mode == 'TFT3_GameVariation_SmallerBoards':
        df = pd.read_sql_query("SELECT * FROM champion_data WHERE game_mode == 'TFT3_GameVariation_SmallerBoards'", db)

    champ_counts = df['champ_name']
    champ_counts = champ_counts.value_counts(normalize=True) * 100
    pick_rates = {}
    for key, val in champ_counts.items():
        pick_rates['{}'.format(key)] = "{:.2f}".format(val)
    for champ_name in champ_names:
        selected_champ = df[df['champ_name'] == '{}'.format(champ_name)]
        items_df = pd.concat([selected_champ['item1'], selected_champ['item2'], selected_champ['item3']],
                             ignore_index=True)
        istopfour_rate = selected_champ['istopfour'].value_counts(normalize=True) * 100
        iswin_rate = selected_champ['iswin'].value_counts(normalize=True) * 100
        level_rate = selected_champ['tier'].mean()
        placement_rate = selected_champ['place'].mean()
        avg_item_df = pd.DataFrame(columns=['amount'])
        for i in range(selected_champ['item1'].isna().sum()):
            avg_item_df = avg_item_df.append({'amount': 0}, ignore_index=True)
        for i in range(selected_champ['item1'].count()):
            avg_item_df = avg_item_df.append({'amount': 1}, ignore_index=True)
        for i in range(selected_champ['item2'].count()):
            avg_item_df = avg_item_df.append({'amount': 2}, ignore_index=True)
        for i in range(selected_champ['item3'].count()):
            avg_item_df = avg_item_df.append({'amount': 3}, ignore_index=True)
        item_counts = items_df.value_counts(normalize=True) * 100
        counter = 1
        now = datetime.now()
        json_data["{}".format(champ_name)] = {"avg": "{:.2f}".format(avg_item_df["amount"].mean()),
                                              "items": {},
                                              "win_rate": None, "top_four_rate": None,
                                              "pick_rate": None,
                                              "price": None,
                                              "average_level": '{:.2f}'.format(float(level_rate)),
                                              "average_placement": None, "role": None,
                                              "traits": champ_names[champ_name]}
        for key, val in item_counts.items():
            if counter > 7:
                break
            json_data["{}".format(champ_name)]["items"]["{}".format(counter)] = {"item_id": int(key),
                                                                                 "percentage": "{:.2f}%".format(
                                                                                     val)}
            counter += 1
        try:
            json_data["{}".format(champ_name)]["win_rate"] = "{:.2f}".format(iswin_rate.to_dict()[1])
        except KeyError:
            json_data["{}".format(champ_name)]["win_rate"] = 0
        try:
            json_data["{}".format(champ_name)]["top_four_rate"] = "{:.2f}".format(istopfour_rate.to_dict()[1])
        except KeyError:
            json_data["{}".format(champ_name)]["top_four_rate"] = 0

        json_data["{}".format(champ_name)]["pick_rate"] = pick_rates[champ_name]
        json_data["{}".format(champ_name)]["average_placement"] = round(placement_rate, 1)
        if float("{:.2f}".format(avg_item_df["amount"].mean())) > 1.50:
            json_data["{}".format(champ_name)]["role"] = 'Carry'
        else:
            json_data["{}".format(champ_name)]["role"] = '-'

        if champ_name in one_cost_units:
            json_data["{}".format(champ_name)]["price"] = 1
        elif champ_name in two_cost_units:
            json_data["{}".format(champ_name)]["price"] = 2
        elif champ_name in three_cost_units:
            json_data["{}".format(champ_name)]["price"] = 3
        elif champ_name in four_cost_units:
            json_data["{}".format(champ_name)]["price"] = 4
        elif champ_name in five_cost_units:
            json_data["{}".format(champ_name)]["price"] = 5
    with open('json_data/champion_data/{}.json'.format(str(game_mode).split('_')[2]), 'w') as json_file:
        json.dump(json_data, json_file)
    b = datetime.now()


def parse_all_champ_data():
    a = datetime.now()
    pool2 = Pool(processes=10)
    game_modes = ['TFT3_GameVariation_None', 'TFT3_GameVariation_TwoStarCarousels', 'TFT3_GameVariation_MidGameFoN',
                  'TFT3_GameVariation_FreeRerolls',
                  'TFT3_GameVariation_Bonanza', 'TFT3_GameVariation_TwoItemMax', 'TFT3_GameVariation_Dreadnova',
                  'TFT3_GameVariation_StartingItems', 'TFT3_GameVariation_SmallerBoards']
    for mode in game_modes:
        r1 = pool2.apply_async(parsechampdata, [mode])
    pool2.close()
    pool2.join()
    b = datetime.now()
    print('parse_all_champs', b - a)


def get_all_champ_data():
    a = datetime.now()
    pool = Pool(processes=10)
    regions = ['euw1', 'br1', 'eun1', 'jp1', 'kr', 'la1', 'la2', 'na1', 'oc1', 'ru', 'tr1']
    for region in regions:
        r1 = pool.apply_async(getchampdata, [str(region).upper()])
    pool.close()
    pool.join()
    b = datetime.now()
    print("get_all_champdata", b - a)


if __name__ == '__main__':
    get_all_champ_data()
