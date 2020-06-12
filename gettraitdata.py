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
def get_trait_data(region):
    global istopfour, iswin, item1, item3, item2
    url_region = str()
    db = sqlite3.connect("databases/match_ids.sqlite", )
    db2 = sqlite3.connect("databases/trait_data.sqlite")
    im = db.cursor()
    im2 = db2.cursor()
    im3 = db2.cursor()
    im2.execute(
        """CREATE TABLE IF NOT EXISTS trait_data(id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,region,trait_name,num_units,tier_current,place,istopfour,iswin,version,game_mode)""")
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
            # print(placement, istopfour, iswin)
            for unit in ptc['traits']:
                if unit['name'] == 'Set3_Sorcerer':
                    trait_name = 'Sorcerer'
                elif unit['name'] == 'Set3_Void':
                    trait_name = 'Void'
                elif unit['name'] == 'Set3_Blademaster':
                    trait_name = 'Blademaster'
                elif unit['name'] == 'Set3_Brawler':
                    trait_name = 'Brawler'
                elif unit['name'] == 'Set3_Celestial':
                    trait_name = 'Celestial'
                elif unit['name'] == 'Set3_Mystic':
                    trait_name = 'Mystic'
                else:
                    trait_name = unit['name']
                if str(version).startswith("10.12"):
                    im3.execute(
                    """INSERT OR IGNORE INTO trait_data(region,trait_name,num_units,tier_current,place,istopfour,iswin,version,game_mode) VALUES(?,?,?,?,?,?,?,?,?)""",
                    (
                        match_region, trait_name, unit['num_units'], unit['tier_current'], placement, istopfour,
                        iswin,
                        version, variant))
            db2.commit()


def get_all_trait_data():
    a = datetime.now()
    pool = Pool(processes=10)
    regions = ['euw1', 'br1', 'eun1', 'jp1', 'kr', 'la1', 'la2', 'na1', 'oc1', 'ru', 'tr1']
    for region in regions:
        r1 = pool.apply_async(get_trait_data, [str(region).upper()])
    pool.close()
    pool.join()
    b = datetime.now()
    print("get_all_trait_data",b-a)

def parse_trait_data(game_mode):
    a = datetime.now()
    global df
    json_data = dict()
    trait_names = ['Astro','Battlecast','Blademaster', 'Blaster', 'Brawler', 'Celestial', 'Chrono', 'Cybernetic', 'DarkStar',
                   'Demolitionist', 'Infiltrator', 'ManaReaver', 'MechPilot', 'Mercenary', 'Mystic', 'Protector',
                   'Rebel', 'Sniper', 'Sorcerer', 'SpacePirate', 'StarGuardian', 'Starship', 'Vanguard','Paragon',
                  ]
    one_cost_units = ['Caitlyn', 'Fiora', 'Graves', 'JarvanIV', 'Leona', 'Malphite', 'Poppy', 'TwistedFate',
                      'Xayah',
                      'Ziggs', 'Zoe', 'Illaoi', 'Nocturne']
    two_cost_units = ['Ahri', 'Annie', 'Blitzcrank', 'Darius', 'Lucian', 'Mordekaiser', 'Rakan', 'Shen',
                      'XinZhao', 'Yasuo', 'KogMaw', 'Nautilus', 'Zed']
    three_cost_units = ['Ashe', 'Ezreal', 'Jayce', 'Karma', 'MasterYi', 'Neeko', 'Rumble', 'Shaco',
                        'Syndra', 'Vi', 'Bard', 'Cassiopeia', 'Vayne']
    four_cost_units = ['Fizz', 'Irelia', 'Jhin', 'Jinx', 'Soraka', 'WuKong', 'Gnar', 'Riven', 'Teemo', 'Viktor']
    five_cost_units = ['Gangplank', 'Lulu', 'Thresh', 'Xerath', 'Janna', 'Urgot']
    db = sqlite3.connect('databases/trait_data.sqlite')
    game_modes = ['TFT3_GameVariation_None', 'TFT3_GameVariation_TwoStarCarousels', 'TFT3_GameVariation_MidGameFoN',
                  'TFT3_GameVariation_FreeRerolls',
                  'TFT3_GameVariation_Bonanza', 'TFT3_GameVariation_BigLittleLegends', 'TFT3_GameVariation_FreeNeekos']
    if game_mode == 'TFT3_GameVariation_None':
        df = pd.read_sql_query("SELECT * FROM trait_data WHERE game_mode == 'TFT3_GameVariation_None'", db)
    elif game_mode == 'TFT3_GameVariation_TwoStarCarousels':
        df = pd.read_sql_query("SELECT * FROM trait_data WHERE game_mode == 'TFT3_GameVariation_TwoStarCarousels'", db)
    elif game_mode == 'TFT3_GameVariation_MidGameFoN':
        df = pd.read_sql_query("SELECT * FROM trait_data WHERE game_mode == 'TFT3_GameVariation_MidGameFoN'", db)
    elif game_mode == 'TFT3_GameVariation_FreeRerolls':
        df = pd.read_sql_query("SELECT * FROM trait_data WHERE game_mode == 'TFT3_GameVariation_FreeRerolls'", db)
    elif game_mode == 'TFT3_GameVariation_Bonanza':
        df = pd.read_sql_query("SELECT * FROM trait_data WHERE game_mode == 'TFT3_GameVariation_Bonanza'", db)
    elif game_mode == 'TFT3_GameVariation_BigLittleLegends':
        df = pd.read_sql_query("SELECT * FROM trait_data WHERE game_mode == 'TFT3_GameVariation_BigLittleLegends'", db)
    elif game_mode == 'TFT3_GameVariation_FreeNeekos':
        df = pd.read_sql_query("SELECT * FROM trait_data WHERE game_mode == 'TFT3_GameVariation_FreeNeekos'", db)
    elif game_mode == 'TFT3_GameVariation_StartingItems':
        df = pd.read_sql_query("SELECT * FROM trait_data WHERE game_mode == 'TFT3_GameVariation_StartingItems'",db)
    elif game_mode == 'TFT3_GameVariation_LittlerLegends':
        df = pd.read_sql_query("SELECT * FROM trait_data WHERE game_mode == 'TFT3_GameVariation_LittlerLegends'",db)

    #print(game_mode, 'writing into json.')
    champ_counts = df['trait_name']
    champ_counts = champ_counts.value_counts(normalize=True) * 100
    # print(champ_counts)
    pick_rates = {}
    for key, val in champ_counts.items():
        pick_rates['{}'.format(key)] = "{:.2f}".format(val)
    for champ_name in trait_names:
        try:
            selected_champ = df[df['trait_name'] == '{}'.format(champ_name)]
            istopfour_rate = selected_champ['istopfour'].value_counts(normalize=True) * 100
            iswin_rate = selected_champ['iswin'].value_counts(normalize=True) * 100
            num_units_rate = selected_champ['num_units'].mean()
            tier_current_rate = selected_champ['tier_current'].mean()
            placement_rate = selected_champ['place'].mean()
            # print(round(placement_rate,1))
            # print('{:.2f}'.format(level_rate))
            # print('top four rate:', istopfour_rate.to_dict()[1])
            # print('is win rate:', iswin_rate.to_dict()[1])

            # print('Avg Item:', '{:.2f}'.format(avg_item_df['amount'].mean()))
            counter = 1
            # print("Itemlist for {}".format(champ_name))
            now = datetime.now()

            json_data["{}".format(champ_name)] = {"win_rate": None, "top_four_rate": None,
                                                  "pick_rate": None,
                                                  "average_units": "{:.2f}".format(num_units_rate),
                                                  "average_tier": "{:.2f}".format(tier_current_rate),
                                                  "average_placement": None, }

            json_data["{}".format(champ_name)]["win_rate"] = "{:.2f}".format(iswin_rate.to_dict()[1])
            json_data["{}".format(champ_name)]["top_four_rate"] = "{:.2f}".format(istopfour_rate.to_dict()[1])
            json_data["{}".format(champ_name)]["pick_rate"] = pick_rates[champ_name]
            json_data["{}".format(champ_name)]["average_placement"] = round(placement_rate, 1)

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
        except:
            continue

    with open('json_data/trait_data/{}.json'.format(str(game_mode).split('_')[2]), 'w') as json_file:
        json.dump(json_data, json_file)

def parse_all_trait_data():
    a = datetime.now()
    pool2 = Pool(processes=10)
    game_modes = ['TFT3_GameVariation_None', 'TFT3_GameVariation_TwoStarCarousels', 'TFT3_GameVariation_MidGameFoN',
                  'TFT3_GameVariation_FreeRerolls',
                  'TFT3_GameVariation_Bonanza', 'TFT3_GameVariation_BigLittleLegends', 'TFT3_GameVariation_FreeNeekos',
                  'TFT3_GameVariation_StartingItems','TFT3_GameVariation_LittlerLegends']
    for mode in game_modes :
        r1 = pool2.apply_async(parse_trait_data, [mode])
    pool2.close()
    pool2.join()
    b = datetime.now()
    print('parse_all_champs',b-a)

if __name__ == '__main__':
    get_all_trait_data()
    parse_all_trait_data()