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

pd.options.display.float_format = '{:.2f}%'.format
pd.set_option('mode.chained_assignment', None)

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36 Edg/83.0.478.37",
    "Accept-Language": "en-US,en;q=0.9",
    "Accept-Charset": "application/x-www-form-urlencoded; charset=UTF-8",
    "Origin": "https://developer.riotgames.com",
    "X-Riot-Token": "RGAPI-ba095dc6-6dcb-47dd-b6f2-cf9da197ed22"
}


def getchallengers():
    a = datetime.now()
    db = sqlite3.connect("players.sqlite")
    im = db.cursor()
    im.execute(
        """CREATE TABLE IF NOT EXISTS challenger(id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,puuid, summonerName,region,wins,loses)""")
    im.execute(
        """CREATE TABLE IF NOT EXISTS grandmaster(id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,puuid, summonerName,region,wins,loses)""")
    im.execute(
        """CREATE TABLE IF NOT EXISTS master(id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,puuid, summonerName,region,wins,loses)""")

    count = 0
    regions = ['euw1', 'br1', 'eun1', 'jp1', 'kr', 'la1', 'la2', 'na1', 'oc1', 'ru', 'tr1']
    leagues = ['challenger', 'grandmaster','master']
    for league in leagues:
        for region in regions:
            url = 'https://{}.api.riotgames.com/tft/league/v1/{}'.format(region, league)
            try:
                player_list = requests.get(url, headers=headers, timeout=5)
            except requests.exceptions.HTTPError as errh:
                continue
            except requests.exceptions.ConnectionError as errc:
                continue
            except requests.exceptions.Timeout as errt:
                continue
            except requests.exceptions.RequestException as err:
                continue
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
                if league == 'challenger':
                    im.execute("""INSERT INTO challenger(puuid, summonerName,region,wins,loses) VALUES (?,?,?,?,?)""",
                               data)
                    print("adding new challenger", data[1])
                elif league == 'grandmaster':
                    im.execute("""INSERT INTO grandmaster(puuid, summonerName,region,wins,loses) VALUES (?,?,?,?,?)""",
                               data)
                    print("adding new grandmaster", data[1])

                elif league == 'master':
                    im.execute("""INSERT INTO master(puuid, summonerName,region,wins,loses) VALUES (?,?,?,?,?)""", data)
                    print("adding new master", data[1])

                db.commit()
                count += 1
                # print(count, data)

    b = datetime.now()
    print("getchallengers :", b - a)


def getmatchids(match_count):
    a = datetime.now()
    db = sqlite3.connect('players.sqlite')
    db2 = sqlite3.connect("new_data.sqlite")
    im = db.cursor()
    im3 = db2.cursor()
    im3.execute(
        """CREATE TABLE IF NOT EXISTS matches(matchId)""")
    im.execute("SELECT * FROM challenger")
    counter = 0
    for i in im:
        if counter > 80:
            print('API limit')
            time.sleep(120)
            counter = 0
        if i[3] == 'euw1' or i[3] == 'eun1' or i[3] == 'tr1' or i[3] == 'ru':
            # print('adding new euw player')
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
                im3.execute("""INSERT OR IGNORE INTO matches(matchId) VALUES(?)""", (match,))
                db2.commit()
            counter += 1
        elif i[3] == 'na1' or i[3] == 'br1' or i[3] == 'la1' or i[3] == 'la2' or i[3] == 'oc1':
            # print('adding new na player')
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
                im3.execute("""INSERT OR IGNORE INTO matches(matchId) VALUES(?)""", (match,))
                db2.commit()
            counter += 1
        elif i[3] == 'kr' or i[3] == 'jp1':
            # print('adding new asian player')
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
                im3.execute("""INSERT OR IGNORE INTO matches(matchId) VALUES(?)""", (match,))
                db2.commit()
            counter += 1
    im.close()
    im3.close()
    b = datetime.now()
    print("getmatchids :", b - a)


def getchampinfo():
    a = datetime.now()
    global istopfour, iswin, item1, item3, item2
    db = sqlite3.connect('new_data.sqlite')
    im = db.cursor()
    im2 = db.cursor()
    im.execute(
        """CREATE TABLE IF NOT EXISTS champs(id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,region,champ_name,tier,place,istopfour,iswin,item1,item2,item3,version,game_mode)""")
    im.execute("SELECT * FROM matches")
    counter = 0
    for i in im:
        match_region = i[0].split('_')[0]
        # print(match_region)
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
                        """INSERT OR IGNORE INTO champs(region,champ_name,tier,place,istopfour,iswin,item1,item2,item3,version,game_mode) VALUES(?,?,?,?,?,?,?,?,?,?,?)""",
                        (
                            match_region, unit['character_id'].split('_')[1], unit['tier'], placement, istopfour,
                            iswin,
                            item1, item2, item3,
                            version, variant))
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
                        """INSERT OR IGNORE INTO champs(region,champ_name,tier,place,istopfour,iswin,item1,item2,item3,version,game_mode) VALUES(?,?,?,?,?,?,?,?,?,?,?)""",
                        (
                            match_region, unit['character_id'].split('_')[1], unit['tier'], placement, istopfour,
                            iswin,
                            item1, item2, item3,
                            version, variant))
                    # print(unit['character_id'].split('_')[1], unit['tier'], placement, istopfour, iswin, item1,item2, item3,version)
            db.commit()
            counter += 1
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
                        """INSERT OR IGNORE INTO champs(region,champ_name,tier,place,istopfour,iswin,item1,item2,item3,version,game_mode) VALUES(?,?,?,?,?,?,?,?,?,?,?)""",
                        (
                            match_region, unit['character_id'].split('_')[1], unit['tier'], placement, istopfour,
                            iswin,
                            item1, item2, item3,
                            version, variant))
                    # print(unit['character_id'].split('_')[1], unit['tier'], placement, istopfour, iswin, item1,item2, item3,version)
            db.commit()
            counter += 1
    b = datetime.now()
    print("getchampinfo :", b - a)


def parsechampdata():
    a = datetime.now()
    json_data = dict()
    champ_names = {'Ahri': ['starguardian', 'sorcerer'], 'Annie': ['mechpilot', 'sorcerer'],
                   'Ashe': ['celestial', 'sniper'], 'AurelionSol': ['rebel', 'starship'],
                   'Blitzcrank': ['chrono', 'brawler'], 'Caitlyn': ['chrono', 'sniper'], 'ChoGath': ['void', 'brawler'],
                   'Darius': ['spacepirate', 'manareaver'], 'Ekko': ['cybernetic', 'infiltrator'],
                   'Ezreal': ['chrono', 'blaster'], 'Fiora': ['cybernetic', 'blademaster'],
                   'Fizz': ['mechpilot', 'infiltrator'], 'Gangplank': ['spacepirate', 'mercenary', 'demolitionist'],
                   'Graves': ['spacepirate', 'blaster'], 'Irelia': ['cybernetic', 'manareaver', 'blademaster'],
                   'JarvanIV': ['darkstar', 'protector'], 'Jayce': ['spacepirate', 'vanguard'],
                   'Jhin': ['darkstar', 'sniper'], 'Jinx': ['rebel', 'blaster'], 'KaiSa': ['valkyrie', 'infiltrator'],
                   'Karma': ['darkstar', 'mystic'],
                   'Kassadin': ['celestial', 'manareaver'], 'Kayle': ['valkyrie', 'blademaster'],
                   'KhaZix': ['void', 'infiltrator'], 'Leona': ['cybernetic', 'vanguard'],
                   'Lucian': ['cybernetic', 'blaster'], 'Lulu': ['celestial', 'mystic'],
                   'Lux': ['darkstar', 'sorcerer'], 'Malphite': ['rebel', 'brawler'],
                   'MasterYi': ['rebel', 'blademaster'],
                   'MissFortune': ['valkyrie', 'mercenary', 'blaster'], 'Mordekaiser': ['darkstar', 'vanguard'],
                   'Poppy': ['starguardian', 'vanguard'], 'Rakan': ['celestial', 'protector'],
                   'Rumble': ['mechpilot', 'demolitionist'], 'Shaco': ['darkstar', 'infiltrator'],
                   'Shen': ['chrono', 'blademaster'], 'Sona': ['rebel', 'mystic'],
                   'Syndra': ['starguardian', 'sorcerer'],
                   'Soraka': ['starguardian', 'mystic'], 'Thresh': ['chrono', 'manareaver'],
                   'TwistedFate': ['chrono', 'sorcerer'], 'VelKoz': ['void', 'sorcerer'],
                   'Vi': ['cybernetic', 'brawler'], 'WuKong': ['chrono', 'vanguard'],
                   'Xayah': ['celestial', 'blademaster'], 'Xerath': ['darkstar', 'sorcerer'],
                   'XinZhao': ['celestial', 'protector'], 'Yasuo': ['rebel', 'blademaster'],
                   'Ziggs': ['rebel', 'demolitionist'], 'Zoe': ['starguardian', 'sorcerer']}
    one_cost_units = ['Caitlyn', 'Fiora', 'Graves', 'JarvanIV', 'KhaZix', 'Leona', 'Malphite', 'Poppy', 'TwistedFate',
                      'Xayah',
                      'Ziggs', 'Zoe']
    two_cost_units = ['Ahri', 'Annie', 'Blitzcrank', 'Darius', 'KaiSa', 'Lucian', 'Mordekaiser', 'Rakan', 'Shen',
                      'Sona', 'XinZhao', 'Yasuo']
    three_cost_units = ['Ashe', 'Ezreal', 'Jayce', 'Karma', 'Kassadin', 'Lux', 'MasterYi', 'Neeko', 'Rumble', 'Shaco',
                        'Syndra', 'Vi']
    four_cost_units = ['ChoGath', 'Fizz', 'Irelia', 'Jhin', 'Jinx', 'Kayle', 'Soraka', 'VelKoz', 'WuKong']
    five_cost_units = ['AurelionSol', 'Ekko', 'Gangplank', 'Lulu', 'MissFortune', 'Thresh', 'Xerath']
    db = sqlite3.connect('new_data.sqlite')
    game_modes = ['TFT3_GameVariation_None', 'TFT3_GameVariation_TwoStarCarousels', 'TFT3_GameVariation_MidGameFoN',
                  'TFT3_GameVariation_FreeRerolls', 'TFT3_GameVariation_FourCostFirstCarousel',
                  'TFT3_GameVariation_Bonanza', 'TFT3_GameVariation_BigLittleLegends', 'TFT3_GameVariation_FreeNeekos']
    for game_mode in game_modes:
        if game_mode == 'TFT3_GameVariation_None':
            df = pd.read_sql_query("SELECT * FROM champs WHERE game_mode == 'TFT3_GameVariation_None'", db)
        elif game_mode == 'TFT3_GameVariation_TwoStarCarousels':
            df = pd.read_sql_query("SELECT * FROM champs WHERE game_mode == 'TFT3_GameVariation_TwoStarCarousels'", db)
        elif game_mode == 'TFT3_GameVariation_MidGameFoN':
            df = pd.read_sql_query("SELECT * FROM champs WHERE game_mode == 'TFT3_GameVariation_MidGameFoN'", db)
        elif game_mode == 'TFT3_GameVariation_FreeRerolls':
            df = pd.read_sql_query("SELECT * FROM champs WHERE game_mode == 'TFT3_GameVariation_FreeRerolls'", db)
        elif game_mode == 'TFT3_GameVariation_FourCostFirstCarousel':
            df = pd.read_sql_query("SELECT * FROM champs WHERE game_mode == 'TFT3_GameVariation_FourCostFirstCarousel'",
                                   db)
        elif game_mode == 'TFT3_GameVariation_Bonanza':
            df = pd.read_sql_query("SELECT * FROM champs WHERE game_mode == 'TFT3_GameVariation_Bonanza'", db)
        elif game_mode == 'TFT3_GameVariation_BigLittleLegends':
            df = pd.read_sql_query("SELECT * FROM champs WHERE game_mode == 'TFT3_GameVariation_BigLittleLegends'", db)
        elif game_mode == 'TFT3_GameVariation_FreeNeekos':
            df = pd.read_sql_query("SELECT * FROM champs WHERE game_mode == 'TFT3_GameVariation_FreeNeekos'", db)

        # print(df.count())
        print(game_mode, 'writing into json.')
        champ_counts = df['champ_name']
        champ_counts = champ_counts.value_counts(normalize=True) * 100
        # print(champ_counts)
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
            # print(round(placement_rate,1))
            # print('{:.2f}'.format(level_rate))
            # print('top four rate:', istopfour_rate.to_dict()[1])
            # print('is win rate:', iswin_rate.to_dict()[1])
            avg_item_df = pd.DataFrame(columns=['amount'])
            for i in range(selected_champ['item1'].isna().sum()):
                avg_item_df = avg_item_df.append({'amount': 0}, ignore_index=True)
            for i in range(selected_champ['item1'].count()):
                avg_item_df = avg_item_df.append({'amount': 1}, ignore_index=True)
            for i in range(selected_champ['item2'].count()):
                avg_item_df = avg_item_df.append({'amount': 2}, ignore_index=True)
            for i in range(selected_champ['item3'].count()):
                avg_item_df = avg_item_df.append({'amount': 3}, ignore_index=True)
            # print('Avg Item:', '{:.2f}'.format(avg_item_df['amount'].mean()))
            item_counts = items_df.value_counts(normalize=True) * 100
            counter = 1
            # print("Itemlist for {}".format(champ_name))
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
                # print("Item_id:", int(key), "Percentage: ", "{:.2f}%".format(val))
                json_data["{}".format(champ_name)]["items"]["{}".format(counter)] = {"item_id": int(key),
                                                                                     "percentage": "{:.2f}%".format(
                                                                                         val)}
                counter += 1
            try:
                json_data["{}".format(champ_name)]["win_rate"] = "{:.2f}%".format(iswin_rate.to_dict()[1])
            except KeyError:
                json_data["{}".format(champ_name)]["win_rate"] = 0
            try:
                json_data["{}".format(champ_name)]["top_four_rate"] = "{:.2f}%".format(istopfour_rate.to_dict()[1])
            except KeyError:
                json_data["{}".format(champ_name)]["top_four_rate"] = 0

            json_data["{}".format(champ_name)]["pick_rate"] = pick_rates[champ_name]
            json_data["{}".format(champ_name)]["average_placement"] = round(placement_rate, 1)
            if float("{:.2f}".format(avg_item_df["amount"].mean())) > 1.50:
                json_data["{}".format(champ_name)]["role"] = 'Carry'
            else:
                json_data["{}".format(champ_name)]["role"] = '-'

            # print(champ_name in two_cost_units)
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

        with open('jsons_new/champion_stats_{}.json'.format(game_mode), 'w') as json_file:
            json.dump(json_data, json_file)
    b = datetime.now()
    print("parsechampinfo :", b - a)


def gettraitinfo():
    a = datetime.now()
    global istopfour, iswin, item1, item3, item2
    db = sqlite3.connect('new_data.sqlite')
    im = db.cursor()
    im2 = db.cursor()
    im.execute(
        """CREATE TABLE IF NOT EXISTS traits(id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,region,trait_name,num_units,tier_current,place,istopfour,iswin,version,game_mode)""")
    im.execute("SELECT * FROM matches")
    counter = 0
    for i in im:
        match_region = i[0].split('_')[0]
        # print(match_region)
        if counter > 90:
            print('API limit')
            time.sleep(120)
            counter = 0
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
            # print(request.status_code)
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
                    im2.execute(
                        """INSERT OR IGNORE INTO traits(region,trait_name,num_units,tier_current,place,istopfour,iswin,version,game_mode) VALUES(?,?,?,?,?,?,?,?,?)""",
                        (
                            match_region, trait_name, unit['num_units'], unit['tier_current'], placement, istopfour,
                            iswin,
                            version, variant))
                    # print(unit['character_id'].split('_')[1], unit['tier'], placement, istopfour, iswin, item1,item2, item3,version)
            db.commit()
            counter += 1
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
            # print(request.status_code)
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
                    im2.execute(
                        """INSERT OR IGNORE INTO traits(region,trait_name,num_units,tier_current,place,istopfour,iswin,version,game_mode) VALUES(?,?,?,?,?,?,?,?,?)""",
                        (
                            match_region, trait_name, unit['num_units'], unit['tier_current'], placement, istopfour,
                            iswin,
                            version, variant))
                    # print(unit['character_id'].split('_')[1], unit['tier'], placement, istopfour, iswin, item1,item2, item3,version)
            db.commit()
            counter += 1
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
            # print(request.status_code)
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
                    im2.execute(
                        """INSERT OR IGNORE INTO traits(region,trait_name,num_units,tier_current,place,istopfour,iswin,version,game_mode) VALUES(?,?,?,?,?,?,?,?,?)""",
                        (
                            match_region, trait_name, unit['num_units'], unit['tier_current'], placement, istopfour,
                            iswin,
                            version, variant))
                    # print(unit['character_id'].split('_')[1], unit['tier'], placement, istopfour, iswin, item1,item2, item3,version)
            db.commit()
            counter += 1
    b = datetime.now()
    print("gettraitdata :", b - a)


def parsetraitdata():
    a = datetime.now()
    global df
    json_data = dict()
    trait_names = ['Blademaster', 'Blaster', 'Brawler', 'Celestial', 'Chrono', 'Cybernetic', 'DarkStar',
                   'Demolitionist', 'Infiltrator', 'ManaReaver', 'MechPilot', 'Mercenary', 'Mystic', 'Protector',
                   'Rebel', 'Sniper', 'Sorcerer', 'SpacePirate', 'StarGuardian', 'Starship', 'Valkyrie', 'Vanguard',
                   'Void']
    one_cost_units = ['Caitlyn', 'Fiora', 'Graves', 'JarvanIV', 'KhaZix', 'Leona', 'Malphite', 'Poppy', 'TwistedFate',
                      'Xayah',
                      'Ziggs', 'Zoe']
    two_cost_units = ['Ahri', 'Annie', 'Blitzcrank', 'Darius', 'KaiSa', 'Lucian', 'Mordekaiser', 'Rakan', 'Shen',
                      'Sona', 'XinZhao', 'Yasuo']
    three_cost_units = ['Ashe', 'Ezreal', 'Jayce', 'Karma', 'Kassadin', 'Lux', 'MasterYi', 'Neeko', 'Rumble', 'Shaco',
                        'Syndra', 'Vi']
    four_cost_units = ['ChoGath', 'Fizz', 'Irelia', 'Jhin', 'Jinx', 'Kayle', 'Soraka', 'VelKoz', 'WuKong']
    five_cost_units = ['AurelionSol', 'Ekko', 'Gangplank', 'Lulu', 'MissFortune', 'Thresh', 'Xerath']
    db = sqlite3.connect('new_data.sqlite')
    game_modes = ['TFT3_GameVariation_None', 'TFT3_GameVariation_TwoStarCarousels', 'TFT3_GameVariation_MidGameFoN',
                  'TFT3_GameVariation_FreeRerolls', 'TFT3_GameVariation_FourCostFirstCarousel',
                  'TFT3_GameVariation_Bonanza', 'TFT3_GameVariation_BigLittleLegends', 'TFT3_GameVariation_FreeNeekos']
    for game_mode in game_modes:
        if game_mode == 'TFT3_GameVariation_None':
            df = pd.read_sql_query("SELECT * FROM traits WHERE game_mode == 'TFT3_GameVariation_None'", db)
        elif game_mode == 'TFT3_GameVariation_TwoStarCarousels':
            df = pd.read_sql_query("SELECT * FROM traits WHERE game_mode == 'TFT3_GameVariation_TwoStarCarousels'", db)
        elif game_mode == 'TFT3_GameVariation_MidGameFoN':
            df = pd.read_sql_query("SELECT * FROM traits WHERE game_mode == 'TFT3_GameVariation_MidGameFoN'", db)
        elif game_mode == 'TFT3_GameVariation_FreeRerolls':
            df = pd.read_sql_query("SELECT * FROM traits WHERE game_mode == 'TFT3_GameVariation_FreeRerolls'", db)
        elif game_mode == 'TFT3_GameVariation_FourCostFirstCarousel':
            df = pd.read_sql_query("SELECT * FROM traits WHERE game_mode == 'TFT3_GameVariation_FourCostFirstCarousel'",
                                   db)
        elif game_mode == 'TFT3_GameVariation_Bonanza':
            df = pd.read_sql_query("SELECT * FROM traits WHERE game_mode == 'TFT3_GameVariation_Bonanza'", db)
        elif game_mode == 'TFT3_GameVariation_BigLittleLegends':
            df = pd.read_sql_query("SELECT * FROM traits WHERE game_mode == 'TFT3_GameVariation_BigLittleLegends'", db)
        elif game_mode == 'TFT3_GameVariation_FreeNeekos':
            df = pd.read_sql_query("SELECT * FROM traits WHERE game_mode == 'TFT3_GameVariation_FreeNeekos'", db)

        print(game_mode, 'writing into json.')
        champ_counts = df['trait_name']
        champ_counts = champ_counts.value_counts(normalize=True) * 100
        # print(champ_counts)
        pick_rates = {}
        for key, val in champ_counts.items():
            pick_rates['{}'.format(key)] = "{:.2f}".format(val)
        for champ_name in trait_names:
            # keyerror
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

            json_data["{}".format(champ_name)]["win_rate"] = "{:.2f}%".format(iswin_rate.to_dict()[1])
            json_data["{}".format(champ_name)]["top_four_rate"] = "{:.2f}%".format(istopfour_rate.to_dict()[1])
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

        with open('jsons_new/trait_stats_{}.json'.format(game_mode), 'w') as json_file:
            json.dump(json_data, json_file)
    b = datetime.now()
    print("parsetraitdata", b - a)


def getcompinfo():
    a = datetime.now()
    global istopfour, iswin
    db = sqlite3.connect('new_data.sqlite')
    im = db.cursor()
    im2 = db.cursor()
    im.execute(
        """CREATE TABLE IF NOT EXISTS comps(id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,region,version,game_mode,place,iswin,istopfour,trait_info,champ_info)""")
    im.execute("SELECT * FROM matches")
    counter = 0
    for i in im:
        match_region = i[0].split('_')[0]
        # print(match_region)
        if counter > 90:
            print('API Limit')
            time.sleep(120)
            counter = 0
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
                continue
            request = json.loads(request.text)
            try:
                version = request['info']['game_version'].strip('Version ').split('(')[0].strip()
                variant = request['info']['game_variation']
            except KeyError:
                continue
            for ptc in request['info']['participants']:
                trait_template = {'Blademaster': 0, 'Brawler': 0, 'Blaster': 0, 'Celestial': 0, 'Chrono': 0,
                                  'Cybernetic': 0, 'DarkStar': 0, 'Demolitionist': 0, 'Infiltrator': 0, 'ManaReaver': 0,
                                  'MechPilot': 0, 'Mercenary': 0, 'Mystic': 0, 'Protector': 0, 'Rebel': 0, 'Sniper': 0,
                                  'Sorcerer': 0, 'SpacePirate': 0, 'StarGuardian': 0, 'Starship': 0, 'Valkyrie': 0,
                                  'Vanguard': 0, 'Void': 0}
                champ_template = list()
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
                comp = list()
                for i in ptc['traits']:
                    if i['name'] == 'Set3_Sorcerer':
                        trait_name = 'Sorcerer'
                    elif i['name'] == 'Set3_Void':
                        trait_name = 'Void'
                    elif i['name'] == 'Set3_Blademaster':
                        trait_name = 'Blademaster'
                    elif i['name'] == 'Set3_Brawler':
                        trait_name = 'Brawler'
                    elif i['name'] == 'Set3_Celestial':
                        trait_name = 'Celestial'
                    elif i['name'] == 'Set3_Mystic':
                        trait_name = 'Mystic'
                    else:
                        trait_name = i['name']
                    if i['tier_current'] > 0:
                        trait_template['{}'.format(trait_name)] = i['tier_current']
                for i in ptc['units']:
                    champ_template.append(i['character_id'].split('_')[1])

                # print(trait_template)
                im2.execute(
                    """INSERT OR IGNORE INTO comps(region,version,game_mode,place,iswin,istopfour,trait_info,champ_info) VALUES(?,?,?,?,?,?,?,?)""",
                    (match_region, version, variant, placement, iswin, istopfour, str(trait_template),
                     str(champ_template)))
            db.commit()
            counter += 1
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
                trait_template = {'Blademaster': 0, 'Brawler': 0, 'Blaster': 0, 'Celestial': 0, 'Chrono': 0,
                                  'Cybernetic': 0, 'DarkStar': 0, 'Demolitionist': 0, 'Infiltrator': 0, 'ManaReaver': 0,
                                  'MechPilot': 0, 'Mercenary': 0, 'Mystic': 0, 'Protector': 0, 'Rebel': 0, 'Sniper': 0,
                                  'Sorcerer': 0, 'SpacePirate': 0, 'StarGuardian': 0, 'Starship': 0, 'Valkyrie': 0,
                                  'Vanguard': 0, 'Void': 0}
                champ_template = list()
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
                comp = list()
                for i in ptc['traits']:
                    if i['name'] == 'Set3_Sorcerer':
                        trait_name = 'Sorcerer'
                    elif i['name'] == 'Set3_Void':
                        trait_name = 'Void'
                    elif i['name'] == 'Set3_Blademaster':
                        trait_name = 'Blademaster'
                    elif i['name'] == 'Set3_Brawler':
                        trait_name = 'Brawler'
                    elif i['name'] == 'Set3_Celestial':
                        trait_name = 'Celestial'
                    elif i['name'] == 'Set3_Mystic':
                        trait_name = 'Mystic'
                    else:
                        trait_name = i['name']
                    if i['tier_current'] > 0:
                        trait_template['{}'.format(trait_name)] = i['tier_current']
                for i in ptc['units']:
                    champ_template.append(i['character_id'].split('_')[1])

                # print(trait_template)
                im2.execute(
                    """INSERT OR IGNORE INTO comps(region,version,game_mode,place,iswin,istopfour,trait_info,champ_info) VALUES(?,?,?,?,?,?,?,?)""",
                    (match_region, version, variant, placement, iswin, istopfour, str(trait_template),
                     str(champ_template)))
            db.commit()
            counter += 1
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
                trait_template = {'Blademaster': 0, 'Brawler': 0, 'Blaster': 0, 'Celestial': 0, 'Chrono': 0,
                                  'Cybernetic': 0, 'DarkStar': 0, 'Demolitionist': 0, 'Infiltrator': 0, 'ManaReaver': 0,
                                  'MechPilot': 0, 'Mercenary': 0, 'Mystic': 0, 'Protector': 0, 'Rebel': 0, 'Sniper': 0,
                                  'Sorcerer': 0, 'SpacePirate': 0, 'StarGuardian': 0, 'Starship': 0, 'Valkyrie': 0,
                                  'Vanguard': 0, 'Void': 0}
                champ_template = list()
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
                comp = list()
                for i in ptc['traits']:
                    if i['name'] == 'Set3_Sorcerer':
                        trait_name = 'Sorcerer'
                    elif i['name'] == 'Set3_Void':
                        trait_name = 'Void'
                    elif i['name'] == 'Set3_Blademaster':
                        trait_name = 'Blademaster'
                    elif i['name'] == 'Set3_Brawler':
                        trait_name = 'Brawler'
                    elif i['name'] == 'Set3_Celestial':
                        trait_name = 'Celestial'
                    elif i['name'] == 'Set3_Mystic':
                        trait_name = 'Mystic'
                    else:
                        trait_name = i['name']
                    if i['tier_current'] > 0:
                        trait_template['{}'.format(trait_name)] = i['tier_current']
                for i in ptc['units']:
                    champ_template.append(i['character_id'].split('_')[1])

                # print(trait_template)
                im2.execute(
                    """INSERT OR IGNORE INTO comps(region,version,game_mode,place,iswin,istopfour,trait_info,champ_info) VALUES(?,?,?,?,?,?,?,?)""",
                    (match_region, version, variant, placement, iswin, istopfour, str(trait_template),
                     str(champ_template)))
            db.commit()
            counter += 1
    b = datetime.now()
    print("getcompinfo", b - a)


def parsecompdata():
    a = datetime.now()
    global df
    json_data = dict()
    db = sqlite3.connect('new_data.sqlite')
    game_modes = ['TFT3_GameVariation_None', 'TFT3_GameVariation_TwoStarCarousels', 'TFT3_GameVariation_MidGameFoN',
                  'TFT3_GameVariation_FreeRerolls', 'TFT3_GameVariation_FourCostFirstCarousel',
                  'TFT3_GameVariation_Bonanza', 'TFT3_GameVariation_BigLittleLegends', 'TFT3_GameVariation_FreeNeekos']
    for game_mode in game_modes:
        print("Writing json for ", game_mode)
        if game_mode == 'TFT3_GameVariation_None':
            df = pd.read_sql_query("SELECT * FROM comps WHERE game_mode == 'TFT3_GameVariation_None'", db)
        elif game_mode == 'TFT3_GameVariation_TwoStarCarousels':
            df = pd.read_sql_query("SELECT * FROM comps WHERE game_mode == 'TFT3_GameVariation_TwoStarCarousels'", db)
        elif game_mode == 'TFT3_GameVariation_MidGameFoN':
            df = pd.read_sql_query("SELECT * FROM comps WHERE game_mode == 'TFT3_GameVariation_MidGameFoN'", db)
        elif game_mode == 'TFT3_GameVariation_FreeRerolls':
            df = pd.read_sql_query("SELECT * FROM comps WHERE game_mode == 'TFT3_GameVariation_FreeRerolls'", db)
        elif game_mode == 'TFT3_GameVariation_FourCostFirstCarousel':
            df = pd.read_sql_query("SELECT * FROM comps WHERE game_mode == 'TFT3_GameVariation_FourCostFirstCarousel'",
                                   db)
        elif game_mode == 'TFT3_GameVariation_Bonanza':
            df = pd.read_sql_query("SELECT * FROM comps WHERE game_mode == 'TFT3_GameVariation_Bonanza'", db)
        elif game_mode == 'TFT3_GameVariation_BigLittleLegends':
            df = pd.read_sql_query("SELECT * FROM comps WHERE game_mode == 'TFT3_GameVariation_BigLittleLegends'", db)
        elif game_mode == 'TFT3_GameVariation_FreeNeekos':
            df = pd.read_sql_query("SELECT * FROM comps WHERE game_mode == 'TFT3_GameVariation_FreeNeekos'", db)
        champ_counts = df['trait_info']
        champ_counts = champ_counts.value_counts(normalize=True) * 100
        counter = 0
        top_comps = dict()
        for comp, val in champ_counts.items():
            top_comps['{}'.format(comp)] = '{:.2f}'.format(val)
            if counter > 15:
                break
            counter += 1
        for comp, val in top_comps.items():
            dict_comp = json.loads(comp.replace("'", '"'))
            list_comp = []
            clean_dic = dict()
            for champ, trait_number in dict_comp.items():
                if trait_number > 0:
                    list_comp.append(champ)
                    clean_dic[champ] = trait_number
            temp_df = df[df['trait_info'] == comp]['champ_info']
            second_df = df[df['trait_info'] == comp]
            most_common_champs = temp_df.value_counts()[:1].index.tolist()
            maxval = max(dict_comp.values())
            max2 = 0
            for comp, key in dict_comp.items():
                if (key > max2 and key < maxval):
                    second_champ = comp
            # print("Name:", max(dict_comp.items(), key=operator.itemgetter(1))[0] + "-" + second_champ)
            # print("Json format:", clean_dic)
            # print("Traits:", list_comp)
            # print("Champions:", most_common_champs[0])
            most_common_champs = ast.literal_eval(most_common_champs[0])
            # print("Pick Rate:", val)
            iswin_rate = second_df['iswin'].value_counts(normalize=True) * 100
            istopfour_rate = second_df['istopfour'].value_counts(normalize=True) * 100
            try:
                # print("Win rate:", "{:.2f}".format(iswin_rate.to_dict()[1]))
                winrate = "{:.2f}".format(iswin_rate.to_dict()[1])
            except KeyError:
                winrate = 0
            try:
                # print("Top 4 rate:", "{:.2f}".format(istopfour_rate.to_dict()[1]))
                topfourrate = "{:.2f}".format(istopfour_rate.to_dict()[1])
            except KeyError:
                topfourrate = 0
            placement_rate = second_df['place'].mean()
            # print("Placement rate:", "{:.2f}".format(placement_rate))
            json_data['{}'.format(max(dict_comp.items(), key=operator.itemgetter(1))[0] + "-" + second_champ)] = {
                "json_format": clean_dic, "traits:": list_comp, "champions": most_common_champs,
                "pick_rate": val,
                "win_rate": winrate, "top_four_rate": topfourrate, "placement_rate": "{:.2f}".format(placement_rate)}
        with open('jsons_new/comp_stats_{}.json'.format(game_mode), 'w') as json_file:
            json.dump(json_data, json_file)
    b = datetime.now()
    print("parsecompinfo :", b - a)


def getchampscore():
    a = datetime.now()
    json_data = {"champions": {
    }}
    json_data2 = {"champions": {
    }}
    df = pd.read_json('jsons_new/champion_stats_TFT3_GameVariation_None.json').to_dict()
    trait_template = {'blademaster': 0, 'brawler': 0, 'blaster': 0, 'celestial': 0, 'chrono': 0,
                      'cybernetic': 0, 'darkStar': 0, 'demolitionist': 0, 'infiltrator': 0, 'manaReaver': 0,
                      'mechPilot': 0, 'mercenary': 0, 'mystic': 0, 'protector': 0, 'rebel': 0, 'sniper': 0,
                      'sorcerer': 0, 'spacePirate': 0, 'starGuardian': 0, 'starship': 0, 'valkyrie': 0,
                      'vanguard': 0, 'void': 0}
    champ_names = {'Ahri': ['starguardian', 'sorcerer'], 'Annie': ['mechpilot', 'sorcerer'],
                   'Ashe': ['celestial', 'sniper'], 'AurelionSol': ['rebel', 'starship'],
                   'Blitzcrank': ['chrono', 'brawler'], 'Caitlyn': ['chrono', 'sniper'], 'ChoGath': ['void', 'brawler'],
                   'Darius': ['spacepirate', 'manareaver'], 'Ekko': ['cybernetic', 'infiltrator'],
                   'Ezreal': ['chrono', 'blaster'], 'Fiora': ['cybernetic', 'blademaster'],
                   'Fizz': ['mechpilot', 'infiltrator'], 'Gangplank': ['spacepirate', 'mercenary', 'demolitionist'],
                   'Graves': ['spacepirate', 'blaster'], 'Irelia': ['cybernetic', 'manareaver', 'blademaster'],
                   'JarvanIV': ['darkstar', 'protector'], 'Jayce': ['spacepirate', 'vanguard'],
                   'Jhin': ['darkstar', 'sniper'], 'Jinx': ['rebel', 'blaster'], 'KaiSa': ['valkyrie', 'infiltrator'],
                   'Karma': ['darkstar', 'mystic'],
                   'Kassadin': ['celestial', 'manareaver'], 'Kayle': ['valkyrie', 'blademaster'],
                   'KhaZix': ['void', 'infiltrator'], 'Leona': ['cybernetic', 'vanguard'],
                   'Lucian': ['cybernetic', 'blaster'], 'Lulu': ['celestial', 'mystic'],
                   'Lux': ['darkstar', 'sorcerer'], 'Malphite': ['rebel', 'brawler'],
                   'MasterYi': ['rebel', 'blademaster'],
                   'MissFortune': ['valkyrie', 'mercenary', 'blaster'], 'Mordekaiser': ['darkstar', 'vanguard'],
                   'Poppy': ['starguardian', 'vanguard'], 'Rakan': ['celestial', 'protector'],
                   'Rumble': ['mechpilot', 'demolitionist'], 'Shaco': ['darkstar', 'infiltrator'],
                   'Shen': ['chrono', 'blademaster'], 'Sona': ['rebel', 'mystic'],
                   'Syndra': ['starguardian', 'sorcerer'],
                   'Soraka': ['starguardian', 'mystic'], 'Thresh': ['chrono', 'manareaver'],
                   'TwistedFate': ['chrono', 'sorcerer'], 'VelKoz': ['void', 'sorcerer'],
                   'Vi': ['cybernetic', 'brawler'], 'WuKong': ['chrono', 'vanguard'],
                   'Xayah': ['celestial', 'blademaster'], 'Xerath': ['darkstar', 'sorcerer'],
                   'XinZhao': ['celestial', 'protector'], 'Yasuo': ['rebel', 'blademaster'],
                   'Ziggs': ['rebel', 'demolitionist'], 'Zoe': ['starguardian', 'sorcerer']}
    for name in champ_names.keys():
        avg = (float(df['{}'.format(name)]['avg']) * 100) * 20 / 100
        win_rate = (float(df['{}'.format(name)]['win_rate'].rstrip('%')) * 10) * 5 / 100
        top_four_rate = (float(df['{}'.format(name)]['top_four_rate'].rstrip('%')) * 10) * 5 / 100
        pick_rate = (float(df['{}'.format(name)]['pick_rate']) * 10) * 70 / 100
        score = avg + win_rate + top_four_rate + pick_rate
        # print(name, '{:.2f}'.format(score))
        json_data["champions"]["{}".format(name)] = "{:.2f}".format(score)
        if score > 85:
            json_data2["champions"]["{}".format(name)] = "S"
        elif score > 70:
            json_data2["champions"]["{}".format(name)] = "A"
        elif score > 60:
            json_data2["champions"]["{}".format(name)] = "B"
        elif score > 50:
            json_data2["champions"]["{}".format(name)] = "C"
        else:
            json_data2["champions"]["{}".format(name)] = "D"

    with open("popularity_scores/champ_scores_new.json", 'w') as json_file:
        json.dump(json_data, json_file)
    with open("popularity_scores/champ_tier_scores.json", 'w') as json_file:
        json.dump(json_data2, json_file)
    b = datetime.now()
    print("getchampscore :", b - a)
    # print(df['Ahri']['avg'])
    # 10% of avg item
    # 10% of winrate
    # 10% of top4
    # 70% of pickrate


def parsechampscore():
    a = datetime.now()
    json_data = {"champions": {}}
    df_new = pd.read_json("popularity_scores/champ_scores_new.json").to_dict()
    df_old = pd.read_json('popularity_scores/champ_scores_old.json').to_dict()
    champ_names = {'Ahri': ['starguardian', 'sorcerer'], 'Annie': ['mechpilot', 'sorcerer'],
                   'Ashe': ['celestial', 'sniper'], 'AurelionSol': ['rebel', 'starship'],
                   'Blitzcrank': ['chrono', 'brawler'], 'Caitlyn': ['chrono', 'sniper'], 'ChoGath': ['void', 'brawler'],
                   'Darius': ['spacepirate', 'manareaver'], 'Ekko': ['cybernetic', 'infiltrator'],
                   'Ezreal': ['chrono', 'blaster'], 'Fiora': ['cybernetic', 'blademaster'],
                   'Fizz': ['mechpilot', 'infiltrator'], 'Gangplank': ['spacepirate', 'mercenary', 'demolitionist'],
                   'Graves': ['spacepirate', 'blaster'], 'Irelia': ['cybernetic', 'manareaver', 'blademaster'],
                   'JarvanIV': ['darkstar', 'protector'], 'Jayce': ['spacepirate', 'vanguard'],
                   'Jhin': ['darkstar', 'sniper'], 'Jinx': ['rebel', 'blaster'], 'KaiSa': ['valkyrie', 'infiltrator'],
                   'Karma': ['darkstar', 'mystic'],
                   'Kassadin': ['celestial', 'manareaver'], 'Kayle': ['valkyrie', 'blademaster'],
                   'KhaZix': ['void', 'infiltrator'], 'Leona': ['cybernetic', 'vanguard'],
                   'Lucian': ['cybernetic', 'blaster'], 'Lulu': ['celestial', 'mystic'],
                   'Lux': ['darkstar', 'sorcerer'], 'Malphite': ['rebel', 'brawler'],
                   'MasterYi': ['rebel', 'blademaster'],
                   'MissFortune': ['valkyrie', 'mercenary', 'blaster'], 'Mordekaiser': ['darkstar', 'vanguard'],
                   'Poppy': ['starguardian', 'vanguard'], 'Rakan': ['celestial', 'protector'],
                   'Rumble': ['mechpilot', 'demolitionist'], 'Shaco': ['darkstar', 'infiltrator'],
                   'Shen': ['chrono', 'blademaster'], 'Sona': ['rebel', 'mystic'],
                   'Syndra': ['starguardian', 'sorcerer'],
                   'Soraka': ['starguardian', 'mystic'], 'Thresh': ['chrono', 'manareaver'],
                   'TwistedFate': ['chrono', 'sorcerer'], 'VelKoz': ['void', 'sorcerer'],
                   'Vi': ['cybernetic', 'brawler'], 'WuKong': ['chrono', 'vanguard'],
                   'Xayah': ['celestial', 'blademaster'], 'Xerath': ['darkstar', 'sorcerer'],
                   'XinZhao': ['celestial', 'protector'], 'Yasuo': ['rebel', 'blademaster'],
                   'Ziggs': ['rebel', 'demolitionist'], 'Zoe': ['starguardian', 'sorcerer']}
    for name in champ_names.keys():
        # print(name)
        difference = "{:.2f}".format(
            float(df_new["champions"]['{}'.format(name)]) - float(df_old["champions"]['{}'.format(name)]))
        # print("Difference", difference)
        json_data["champions"]["{}".format(name)] = float(difference)

    with open("popularity_scores/champ_scores_diff.json", "w") as json_file:
        json.dump(json_data, json_file)
    b = datetime.now()
    print("parsechampscore :", b - a)


def gettraitscore():
    a = datetime.now()
    json_data = {"traits": {}}
    json_data2 = {"traits": {
        "Blademaster": {
            "tier": None,
            "champions": ["Fiora", "Xayah", "Shen", "Yasuo", "MasterYi", "Irelia", "Kayle"],
            "description": "Blademasters' Basic Attacks have a chance to trigger two additional attacks against their target. These additional attacks deal damage like Basic Attacks and trigger on-hit effects.",
        },
        "Blaster": {
            "tier": None,
            "champions": ["Graves", "Lucian", "Ezreal", "Jinx", "MissFortune"],
            "description": "Every fourth Basic Attack from a Blaster fires additional attacks at random enemies. These additional attacks deal damage like Basic Attacks, trigger on-hit effects and can critically hit.",
        },
        "Brawler": {
            "tier": None,
            "champions": ["Malphite", "Blitzcrank", "Vi", "ChoGath"],
            "description": "Brawlers gain bonus Maximum Health.",
        },
        "Demolitionist": {
            "tier": None,
            "champions": ["Ziggs", "Rumble", "Gangplank"],
            "description": "Damage from Demolitionists' spellcasts stun their for 1.50 seconds. (Once per spellcast)",
        },
        "Infiltrator": {
            "tier": None,
            "champions": ["KhaZix", "KaiSa", "Shaco", "Fizz", "Ekko"],
            "description": "Innate: At the start of combat, Infiltrators move to the enemy's backline. Infiltrators gain Attack Speed for 6 seconds at the start of combat, refreshes on takedown",
        },
        "Mercenary": {
            "tier": None,
            "champions": ["Gangplank", "MissFortune"],
            "description": "Innate: Upgrades for Mercenaries's spells have a chance to appear in the shop.",
        },
        "ManaReaver": {
            "tier": None,
            "champions": ["Darius", "Kassadin", "Irelia", "Thresh"],
            "description": "Mana-Reaver attacks increase the mana cost of their target’s next spell by 40%",
        },
        "Mystic": {
            "tier": None,
            "champions": ["Sona", "Karma", "Soraka", "Lulu"],
            "description": "All allies gain Magic Resistance.",
        },
        "Protector": {
            "tier": None,
            "champions": ["JarvanIV", "Rakan", "XinZhao", "Neeko"],
            "description": "Protectors shield themselves for 4 seconds whenever they cast a spell. This shield doesn't stack.",
        },
        "Sniper": {
            "tier": None,
            "champions": ["Caitlyn", "Ashe", "Jhin"],
            "description": "Snipers deal 15% increased damage for each hex between themselves and their target.",
        },
        "Sorcerer": {
            "tier": None,
            "champions": ["TwistedFate", "Zoe", "Ahri", "Annie", "Lux", "Syndra", "VelKoz", "Xerath"],
            "description": "All allies have increased Spell Power.",
        },
        "Vanguard": {
            "tier": None,
            "champions": ["Leona", "Poppy", "Mordekaiser", "Jayce", "WuKong"],
            "description": "Vanguard champions gain bonus Armor.",
        },
        "Celestial": {
            "tier": None,
            "champions": ["Xayah", "Rakan", "XinZhao", "Ashe", "Kassadin", "Lulu"],
            "description": "All allies heal for some of the damage they deal with spells and attacks.",
        },
        "Chrono": {
            "tier": None,
            "champions": ["Caitlyn", "TwistedFate", "Blitzcrank", "Shen", "Ezreal", "WuKong", "Thresh"],
            "description": "All allies gain 15% Attack Speed every some seconds.",
        },
        "Cybernetic": {
            "tier": None,
            "champions": ["Leona", "Fiora", "Lucian", "Vi", "Irelia", "Ekko"],
            "description": "Cybernetic champions with at least one item gain Health and Attack Damage.",
        },
        "DarkStar": {
            "tier": None,
            "champions": ["JarvanIV", "Mordekaiser", "Karma", "Lux", "Shaco", "Jhin", "Xerath"],
            "description": "When a Dark Star Champion dies, all other allied Dark Star Champions gain Attack Damage and Spell Power",
        },
        "MechPilot": {
            "tier": None,
            "champions": ["Annie", "Rumble", "Fizz"],
            "description": "The Super-Mech has the combined Pilots Health, Attack Damage, and Traits of its Pilots, as well as 3 random items from among them. When the Super-Mech dies the Pilots are ejected, continue to fight.",
        },
        "Rebel": {
            "tier": None,
            "champions": ["Ziggs", "Malphite", "Sona", "Yasuo", "MasterYi", "Jinx", "AurelionSol"],
            "description": "At the start of combat, Rebels gain a shield and increased damage for each adjacent Rebel. The shield lasts for 8 seconds.",
        },
        "SpacePirate": {
            "tier": None,
            "champions": ["Graves", "Darius", "Jayce", "Gangplank"],
            "description": "Whenever a Space Pirate lands a killing blow on a Champion there is a chance to drop extra loot.",
        },
        "StarGuardian": {
            "tier": None,
            "champions": ["Poppy", "Zoe", "Ashe", "Neeko", "Syndra", "Soraka"],
            "description": "Star Guardians' spellcasts grant Mana to other Star Guardians spread among them.",
        },
        "Valkyrie": {
            "tier": None,
            "champions": ["KaiSa", "Kayle", "MissFortune"],
            "description": " Valkyrie attacks and spells always critically hit targets below 40% health.",
        },
        "Void": {
            "tier": None,
            "champions": ["KhaZix", "ChoGath", "VelKoz"],
            "description": "Attacks and spells from Void champions deal true damage.",
        },
        "Starship": {
            "tier": None,
            "champions": ["AurelionSol"],
            "description": "Innate: Starships gain 40 Mana per second, maneuver around the board, and are immune to movement impairing effects, but can't Basic Attack.",
        },

    }}
    df = pd.read_json("jsons_new/trait_stats_TFT3_GameVariation_None.json").to_dict()
    trait_names = ['Blademaster', 'Blaster', 'Brawler', 'Celestial', 'Chrono', 'Cybernetic', 'DarkStar',
                   'Demolitionist', 'Infiltrator', 'ManaReaver', 'MechPilot', 'Mercenary', 'Mystic', 'Protector',
                   'Rebel', 'Sniper', 'Sorcerer', 'SpacePirate', 'StarGuardian', 'Starship', 'Valkyrie', 'Vanguard',
                   'Void']
    for name in trait_names:
        win_rate = (float(df['{}'.format(name)]['win_rate'].rstrip('%')) * 10) * 5 / 100
        top_four_rate = (float(df['{}'.format(name)]['top_four_rate'].rstrip('%')) * 10) * 5 / 100
        pick_rate = (float(df['{}'.format(name)]['pick_rate']) * 10) * 90 / 100
        score = win_rate + top_four_rate + pick_rate
        json_data["traits"]["{}".format(name)] = "{:.2f}".format(score)
        if score > 85:
            json_data2["traits"]["{}".format(name)]["tier"] = "S"
        elif score > 70:
            json_data2["traits"]["{}".format(name)]["tier"] = "A"
        elif score > 60:
            json_data2["traits"]["{}".format(name)]["tier"] = "B"
        elif score > 50:
            json_data2["traits"]["{}".format(name)]["tier"] = "C"
        else:
            json_data2["traits"]["{}".format(name)]["tier"] = "D"
    with open("popularity_scores/trait_scores_new.json", 'w') as json_file:
        json.dump(json_data, json_file)
    with open("popularity_scores/trait_tier_scores.json", 'w') as json_file:
        json.dump(json_data2, json_file)
    b = datetime.now()
    print("gettraitscore :", b - a)


def parsetraitscore():
    a = datetime.now()
    json_data = {"traits": {}}
    df_new = pd.read_json("popularity_scores/trait_scores_new.json").to_dict()
    df_old = pd.read_json('popularity_scores/trait_scores_old.json').to_dict()
    trait_names = ['Blademaster', 'Blaster', 'Brawler', 'Celestial', 'Chrono', 'Cybernetic', 'DarkStar',
                   'Demolitionist', 'Infiltrator', 'ManaReaver', 'MechPilot', 'Mercenary', 'Mystic', 'Protector',
                   'Rebel', 'Sniper', 'Sorcerer', 'SpacePirate', 'StarGuardian', 'Starship', 'Valkyrie', 'Vanguard',
                   'Void']
    for name in trait_names:
        difference = "{:.2f}".format(
            float(df_new["traits"]['{}'.format(name)]) - float(df_old["traits"]['{}'.format(name)]))
        json_data["traits"]["{}".format(name)] = float(difference)

    with open("popularity_scores/trait_scores_diff.json", "w") as json_file:
        json.dump(json_data, json_file)
    b = datetime.now()
    print("parsetraitscore :", b - a)


def getcompscore():
    a = datetime.now()
    global score
    json_data = {"comps": {}}
    df = pd.read_json("jsons_new/comp_stats_TFT3_GameVariation_None.json").to_dict()
    for val, key in df.items():
        try:
            win_rate = (float(df['{}'.format(val)]['win_rate'].rstrip('%')) * 10) * 5 / 100
            top_four_rate = (float(df['{}'.format(val)]['top_four_rate'].rstrip('%')) * 10) * 5 / 100
            pick_rate = (float(df['{}'.format(val)]['pick_rate']) * 10) * 90 / 100
            score = win_rate + top_four_rate + pick_rate
            json_data["comps"]["{}".format(val)] = "{:.2f}".format(score)
        except:
            json_data["comps"]["{}".format(val)] = 0

    with open("popularity_scores/comp_scores_new.json", 'w') as json_file:
        json.dump(json_data, json_file)
    b = datetime.now()
    print("getcompscore :", b - a)


def parsecompscore():
    a = datetime.now()
    json_data = {"comps": {}}
    df_new = pd.read_json("popularity_scores/comp_scores_new.json").to_dict()
    df_old = pd.read_json('popularity_scores/comp_scores_old.json').to_dict()
    df = pd.read_json("jsons_new/comp_stats_TFT3_GameVariation_None.json").to_dict()

    for val, key in df.items():
        try:
            difference = "{:.2f}".format(
                float(df_new["comps"]['{}'.format(val)]) - float(df_old["comps"]['{}'.format(val)]))
            json_data["comps"]["{}".format(val)] = float(difference)
        except KeyError:
            json_data["comps"]["{}".format(val)] = 0

    with open("popularity_scores/comp_scores_diff.json", "w") as json_file:
        json.dump(json_data, json_file)
    b = datetime.now()
    print("parsecompscore :", b - a)


def getiteminfo():
    a = datetime.now()
    global istopfour, iswin, item1, item3, item2
    db = sqlite3.connect('new_data.sqlite')
    im = db.cursor()
    im2 = db.cursor()
    im.execute(
        """CREATE TABLE IF NOT EXISTS items(id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,region,item_name,place,istopfour,iswin,version,game_mode)""")
    im.execute("SELECT * FROM champs WHERE item1 IS NOT NULL")
    df = pd.read_sql_query("SELECT * FROM champs WHERE item1 IS NOT NULL", db)
    for id, val in df.iterrows():
        im2.execute(
            """INSERT OR IGNORE INTO items(region,item_name,place,istopfour,iswin,version,game_mode) VALUES(?,?,?,?,?,?,?)""",
            (val['region'], val['item1'], val['place'], val['istopfour'], val['iswin'], val['version'],
             val['game_mode']))
    df = pd.read_sql_query("SELECT * FROM champs WHERE item2 IS NOT NULL", db)
    for id, val in df.iterrows():
        im2.execute(
            """INSERT OR IGNORE INTO items(region,item_name,place,istopfour,iswin,version,game_mode) VALUES(?,?,?,?,?,?,?)""",
            (val['region'], val['item2'], val['place'], val['istopfour'], val['iswin'], val['version'],
             val['game_mode']))
    df = pd.read_sql_query("SELECT * FROM champs WHERE item3 IS NOT NULL", db)
    for id, val in df.iterrows():
        im2.execute(
            """INSERT OR IGNORE INTO items(region,item_name,place,istopfour,iswin,version,game_mode) VALUES(?,?,?,?,?,?,?)""",
            (val['region'], val['item3'], val['place'], val['istopfour'], val['iswin'], val['version'],
             val['game_mode']))
    db.commit()


def parseitemdata():
    a = datetime.now()
    global df
    json_data = dict()
    db = sqlite3.connect('new_data.sqlite')
    game_modes = ['TFT3_GameVariation_None', 'TFT3_GameVariation_TwoStarCarousels', 'TFT3_GameVariation_MidGameFoN',
                  'TFT3_GameVariation_FreeRerolls', 'TFT3_GameVariation_FourCostFirstCarousel',
                  'TFT3_GameVariation_Bonanza', 'TFT3_GameVariation_BigLittleLegends', 'TFT3_GameVariation_FreeNeekos']

    df = pd.read_sql_query("SELECT * FROM items", db)
    for mode in game_modes:
        df_none = df[df['game_mode'] == mode]
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
        with open('jsons_new/item_stats_{}.json'.format(mode), "w") as json_file:
            json.dump(json_data, json_file)

    b = datetime.now()
    print("parsecompinfo :", b - a)


def parsecompinfonew():
    json_data = {}
    game_modes = ['TFT3_GameVariation_None', 'TFT3_GameVariation_TwoStarCarousels', 'TFT3_GameVariation_MidGameFoN',
                  'TFT3_GameVariation_FreeRerolls', 'TFT3_GameVariation_FourCostFirstCarousel',
                  'TFT3_GameVariation_Bonanza', 'TFT3_GameVariation_BigLittleLegends', 'TFT3_GameVariation_FreeNeekos']
    item_name_list = {"1": "B.F Sword", "2": "Recurve Bow", "3": "Needlessly Large Rod", "4": "Tear of the Goddess",
                      "5": "Chain Vest", "6": "Negatron Cloak", "7": "Giant's Belt", "8": "Spatula",
                      "9": "Sparring Gloves", "11": "Deathblade", "12": "Giant Slayer", "13": "Hextech Gunblade",
                      "14": "Spear of Shojin", "15": "Guardian Angel", "16": "Bloodthirster", "17": "Zeke's Herald",
                      "18": "Blade of the Ruined King", "19": "Infinity Edge", "22": "Rapid Firecannon",
                      "23": "Guinsoo's Rageblade", "24": "Statikk Shiv", "25": "Titan's Resolve",
                      "26": "Runaan's Hurricane", "27": "Zz'Rot Portal", "28": "Infiltrator's Talons",
                      "29": "Last Whisper", "33": "Rabadon's Deathcap", "34": "Luden's Echo",
                      "35": "Locket of the Iron Solari", "36": "Ionic Spark", "37": "Morellonomicon",
                      "38": "Demolitionist's Charge", "39": "Jeweled Gauntlet", "44": "Seraph's Embrace",
                      "45": "Frozen Heart", "46": "Chalice of Favor", "47": "Redemption", "48": "Star Guardian's Charm",
                      "49": "Hand of Justice", "55": "Bramble Vest", "56": "Sword Breaker", "57": "Red Buff",
                      "58": "Rebel Medal", "59": "Shroud of Stillness", "66": "Dragon's Claw", "67": "Zephyr",
                      "68": "Celestial Orb", "69": "Quicksilver", "77": "Warmog's Armor",
                      "78": "Protector's Chestguard", "79": "Trap Claw", "88": "Force of Nature",
                      "89": "Dark Star's Heart", "99": "Thief's Gloves"}
    champ_names = {'Ahri': ['starguardian', 'sorcerer'], 'Annie': ['mechpilot', 'sorcerer'],
                   'Ashe': ['celestial', 'sniper'], 'AurelionSol': ['rebel', 'starship'],
                   'Blitzcrank': ['chrono', 'brawler'], 'Caitlyn': ['chrono', 'sniper'], 'ChoGath': ['void', 'brawler'],
                   'Darius': ['spacepirate', 'manareaver'], 'Ekko': ['cybernetic', 'infiltrator'],
                   'Ezreal': ['chrono', 'blaster'], 'Fiora': ['cybernetic', 'blademaster'],
                   'Fizz': ['mechpilot', 'infiltrator'], 'Gangplank': ['spacepirate', 'mercenary', 'demolitionist'],
                   'Graves': ['spacepirate', 'blaster'], 'Irelia': ['cybernetic', 'manareaver', 'blademaster'],
                   'JarvanIV': ['darkstar', 'protector'], 'Jayce': ['spacepirate', 'vanguard'],
                   'Jhin': ['darkstar', 'sniper'], 'Jinx': ['rebel', 'blaster'], 'KaiSa': ['valkyrie', 'infiltrator'],
                   'Karma': ['darkstar', 'mystic'],
                   'Kassadin': ['celestial', 'manareaver'], 'Kayle': ['valkyrie', 'blademaster'],
                   'KhaZix': ['void', 'infiltrator'], 'Leona': ['cybernetic', 'vanguard'],
                   'Lucian': ['cybernetic', 'blaster'], 'Lulu': ['celestial', 'mystic'],
                   'Lux': ['darkstar', 'sorcerer'], 'Malphite': ['rebel', 'brawler'],
                   'MasterYi': ['rebel', 'blademaster'],
                   'MissFortune': ['valkyrie', 'mercenary', 'blaster'], 'Mordekaiser': ['darkstar', 'vanguard'],
                   'Neeko': ['starguardian', 'protector'],
                   'Poppy': ['starguardian', 'vanguard'], 'Rakan': ['celestial', 'protector'],
                   'Rumble': ['mechpilot', 'demolitionist'], 'Shaco': ['darkstar', 'infiltrator'],
                   'Shen': ['chrono', 'blademaster'], 'Sona': ['rebel', 'mystic'],
                   'Syndra': ['starguardian', 'sorcerer'],
                   'Soraka': ['starguardian', 'mystic'], 'Thresh': ['chrono', 'manareaver'],
                   'TwistedFate': ['chrono', 'sorcerer'], 'VelKoz': ['void', 'sorcerer'],
                   'Vi': ['cybernetic', 'brawler'], 'WuKong': ['chrono', 'vanguard'],
                   'Xayah': ['celestial', 'blademaster'], 'Xerath': ['darkstar', 'sorcerer'],
                   'XinZhao': ['celestial', 'protector'], 'Yasuo': ['rebel', 'blademaster'],
                   'Ziggs': ['rebel', 'demolitionist'], 'Zoe': ['starguardian', 'sorcerer']}
    trait_template = {'blademaster': 0, 'brawler': 0, 'blaster': 0, 'celestial': 0, 'chrono': 0,
                      'cybernetic': 0, 'darkstar': 0, 'demolitionist': 0, 'infiltrator': 0, 'manareaver': 0,
                      'mechpilot': 0, 'mercenary': 0, 'mystic': 0, 'protector': 0, 'rebel': 0, 'sniper': 0,
                      'sorcerer': 0, 'spacepirate': 0, 'starguardian': 0, 'starship': 0, 'valkyrie': 0,
                      'vanguard': 0, 'void': 0}
    inv_map = {v: k for k, v in item_name_list.items()}

    for mode in game_modes:
        df = pd.read_json('comp_jsons/{}.json'.format(mode))
        current_df_columns = df.columns.to_list()
        max_col = 0
        for column in current_df_columns:
            if max_col < int(column[0]):
                max_col = int(column[0])
        for column in range(1, max_col + 1):
            json_data["team_comp_{}".format(column)] = {"comp_name": str(), "Thumbnail_picture": None, "Count": None,
                                                        "Placement": None,
                                                        "Traits": {'blademaster': 0, 'brawler': 0, 'blaster': 0,
                                                                   'celestial': 0, 'chrono': 0,
                                                                   'cybernetic': 0, 'darkstar': 0, 'demolitionist': 0,
                                                                   'infiltrator': 0, 'manareaver': 0,
                                                                   'mechpilot': 0, 'mercenary': 0, 'mystic': 0,
                                                                   'protector': 0, 'rebel': 0, 'sniper': 0,
                                                                   'sorcerer': 0, 'spacepirate': 0, 'starguardian': 0,
                                                                   'starship': 0, 'valkyrie': 0,
                                                                   'vanguard': 0, 'void': 0}, "Trait_tiers": None,
                                                        "Champions": {}}
        for column in range(1, max_col + 1):
            df_col1 = df['{}_character'.format(column)].to_dict()
            for val, key in df_col1.items():
                df_col2 = df['{}_pct'.format(column)].to_dict()
                if len(str(key).split("_")) == 2:
                    if df_col2[val] > 40:
                        if len(json_data["team_comp_{}".format(column)]['Champions']) == 0:
                            json_data["team_comp_{}".format(column)]['Thumbnail_picture'] = str(key).strip(
                                "TFT3").strip("_")
                        json_data["team_comp_{}".format(column)]['Champions'][
                            '{}'.format(str(key).strip("TFT3").strip("_"))] = {"Count": int(df_col2[val]), "Items": []}
                        for trait in range(len(champ_names['{}'.format(str(key).strip("TFT3").strip("_"))])):
                            # print(champ_names['{}'.format(str(key).strip("TFT3").strip("_"))][trait])
                            json_data["team_comp_{}".format(column)]['Traits'][
                                '{}'.format(champ_names['{}'.format(str(key).strip("TFT3").strip("_"))][trait])] += 1
                    non_zero_traits = {x: y for x, y in json_data["team_comp_{}".format(column)]["Traits"].items() if
                                       y != 0}
                    # print(non_zero_traits)
                    # json_data["team_comp_{}".format(column)]['Traits'] = {}
                    json_data["team_comp_{}".format(column)]['Trait_tiers'] = non_zero_traits

                elif len(str(key).split("_")) == 3:
                    splitted_version = str(key).split("_")
                    champ_name = splitted_version[1]
                    item_name = splitted_version[2]
                    try:
                        json_data["team_comp_{}".format(column)]["Champions"][champ_name]["Items"].append(
                            inv_map['{}'.format(item_name)])
                        if len(json_data["team_comp_{}".format(column)]["Champions"][champ_name]["Items"]) > 3:
                            json_data["team_comp_{}".format(column)]["Champions"][champ_name]["Items"].pop()
                            json_data["team_comp_{}".format(column)]["Champions"][champ_name]["isCarry"] = True
                    except KeyError:
                        continue
                elif key == "Count":
                    json_data["team_comp_{}".format(column)][key] = df_col2[val]
                elif key == "Placement":
                    json_data["team_comp_{}".format(column)][key] = df_col2[val]
            # print(json_data["team_comp_{}".format(column)]['Traits'])
            # print(json_data["team_comp_{}".format(column)]['Trait_tiers'])
            traits_copy = copy.deepcopy(json_data)
            # print(traits_copy)
            for val, key in json_data["team_comp_{}".format(column)]["Trait_tiers"].items():
                # print(val,key)
                if val == 'blademaster' and key > 2:
                    traits_copy["team_comp_{}".format(column)]['Trait_tiers'][val] = key // 3
                elif val == 'brawler' and key > 1:
                    traits_copy["team_comp_{}".format(column)]['Trait_tiers'][val] = key // 2
                elif val == 'blaster' and key > 1:
                    traits_copy["team_comp_{}".format(column)]['Trait_tiers'][val] = key // 2
                elif val == 'celestial' and key > 1:
                    traits_copy["team_comp_{}".format(column)]['Trait_tiers'][val] = key // 2
                elif val == 'chrono' and key > 1:
                    traits_copy["team_comp_{}".format(column)]['Trait_tiers'][val] = key // 2
                elif val == 'cybernetic' and key > 2:
                    traits_copy["team_comp_{}".format(column)]['Trait_tiers'][val] = key // 3
                elif val == 'darkstar' and key > 2:
                    traits_copy["team_comp_{}".format(column)]['Trait_tiers'][val] = key // 3
                elif val == 'demolitionist' and key > 1:
                    traits_copy["team_comp_{}".format(column)]['Trait_tiers'][val] = key // 2
                elif val == 'infiltrator' and key > 1:
                    traits_copy["team_comp_{}".format(column)]['Trait_tiers'][val] = key // 2
                elif val == 'manareaver' and key > 1:
                    traits_copy["team_comp_{}".format(column)]['Trait_tiers'][val] = key // 2
                elif val == 'mechpilot' and key > 2:
                    traits_copy["team_comp_{}".format(column)]['Trait_tiers'][val] = 1
                elif val == 'mercenary' and key > 0:
                    traits_copy["team_comp_{}".format(column)]['Trait_tiers'][val] = 1
                elif val == 'mystic' and key > 1:
                    traits_copy["team_comp_{}".format(column)]['Trait_tiers'][val] = key // 2
                elif val == 'protector' and key > 1:
                    traits_copy["team_comp_{}".format(column)]['Trait_tiers'][val] = key // 2
                elif val == 'rebel' and key > 2:
                    traits_copy["team_comp_{}".format(column)]['Trait_tiers'][val] = key // 3
                elif val == 'sniper' and key > 1:
                    traits_copy["team_comp_{}".format(column)]['Trait_tiers'][val] = key // 2
                elif val == 'sorcerer' and key > 1:
                    traits_copy["team_comp_{}".format(column)]['Trait_tiers'][val] = key // 2
                elif val == 'spacepirate' and key > 1:
                    traits_copy["team_comp_{}".format(column)]['Trait_tiers'][val] = key // 2
                elif val == 'starguardian' and key > 2:
                    traits_copy["team_comp_{}".format(column)]['Trait_tiers'][val] = key // 3
                elif val == 'starship' and key > 0:
                    traits_copy["team_comp_{}".format(column)]['Trait_tiers'][val] = 1
                elif val == 'valkyrie' and key > 1:
                    traits_copy["team_comp_{}".format(column)]['Trait_tiers'][val] = key // 2
                elif val == 'vanguard' and key > 1:
                    traits_copy["team_comp_{}".format(column)]['Trait_tiers'][val] = 1
                elif val == 'void' and key > 2:
                    traits_copy["team_comp_{}".format(column)]['Trait_tiers'][val] = 1
                else:
                    traits_copy["team_comp_{}".format(column)]['Trait_tiers'].pop(val)
            json_data["team_comp_{}".format(column)]['Trait_tiers'] = traits_copy["team_comp_{}".format(column)][
                'Trait_tiers']
            # print(json_data["team_comp_{}".format(column)]["Traits"])
            inc_champions = dict(
                sorted(json_data["team_comp_{}".format(column)]["Traits"].items(), key=operator.itemgetter(1),
                       reverse=True)[:2])
            comp_name_list = list()
            for val, key in inc_champions.items():
                comp_name_list.append(val)
            json_data["team_comp_{}".format(column)]["comp_name"] = str(
                comp_name_list[0].title() + " & " + comp_name_list[1].title())
            json_data["team_comp_{}".format(column)].pop("Traits")
        json_data_sorted = sorted(json_data.items(), key=lambda x: getitem(x[1], 'Count'),reverse=True)
        with open('comp_jsons/comp_{}.json'.format(mode), "w") as json_file:
            json.dump(dict(json_data_sorted), json_file)


def getitemscore():
    a = datetime.now()
    global score
    json_data = {"items": {}}
    json_data2 = {"items": {
        "1": {
            "name": "B.F Sword",
            "components": None,
            "description": "15 Attack damage.",
            "tier": str(),
            "powers": {
                "ad": 15
            }
        },
        "2": {
            "name": "Recurve Bow",
            "components": None,
            "description": "20% Attack speed.",
            "tier": str(),
            "powers": {
                "sp": 20
            }

        },
        "3": {
            "name": "Needlessly Large Rod",
            "components": None,
            "description": "20 Spell power.",
            "tier": str(),
            "powers": {
                "md": 20
            }
        },
        "4": {
            "name": "Tear of the Goddess",
            "components": None,
            "description": "15 Mana.",
            "tier": str(),
            "powers": {
                "mn": 15
            }
        },
        "5": {
            "name": "Chain Vest",
            "components": None,
            "description": "25 Armor.",
            "tier": str(),
            "powers": {
                "ar": 25
            }
        },
        "6": {
            "name": "Negatron Cloak",
            "components": None,
            "description": "25 Magic resists.",
            "tier": str(),
            "powers": {
                "mr": 25
            }
        },
        "7": {
            "name": "Giant's Belt",
            "components": None,
            "description": "200 Healt.",
            "tier": str(),
            "powers": {
                "hp": 200
            }
        },
        "8": {
            "name": "Spatula",
            "components": None,
            "description": "It must do something...",
            "tier": str(),
            "powers": {
            }

        },
        "9": {
            "name": "Sparring Gloves",
            "components": None,
            "description": "10% Crit and 10% Dodge chance.",
            "tier": str(),
            "powers": {
                "cr": 10,
                "dg": 10
            }
        },
        "11": {
            "name": "Deathblade",
            "components": [1, 1],
            "description": "Contributing to a kill grants +30 Attack Damage for the remainder of combat. This effect can stack any number of times.",
            "tier": str(),
            "powers": {
                "ad": 30
            }
        },
        "12": {
            "name": "Giant Slayer",
            "components": [1, 2],
            "description": "Attacks deal an additional 12% enemy current Health as Physical Damage.",
            "tier": str(),
            "powers": {
                "ad": 15,
                "sp": 15
            }
        },
        "13": {
            "name": "Hextech Gunblade",
            "components": [1, 3],
            "description": "Heal for 25% of all damage dealt.",
            "tier": str(),
            "powers": {
                "ad": 15,
                "md": 20
            }
        },
        "14": {
            "name": "Spear of the Shojin",
            "components": [1, 4],
            "description": "After casting, wearer gains 18% of its max Mana per attack.",
            "tier": str(),
            "powers": {
                "ad": 15,
                "mn": 15
            }
        },
        "15": {
            "name": "Guardian Angel",
            "components": [1, 5],
            "description": "Wearer revives with 400 HP.",
            "tier": str(),
            "powers": {
                "ad": 15,
                "ar": 25
            }

        },
        "16": {
            "name": "Bloodthirster",
            "components": [1, 6],
            "description": "Basic Attacks heal the wearer for 35% of the damage dealt.",
            "tier": str(),
            "powers": {
                "ad": 15,
                "mr": 20
            }
        },
        "17": {
            "name": "Zeke's Herald",
            "components": [1, 7],
            "description": "When combat begins, the wearer and all allies within 1 hex in the same row gain +30% Attack Speed for the rest of combat.",
            "tier": str(),
            "powers": {
                "ad": 15,
                "hp": 200
            }
        },
        "18": {
            "name": "Blade of the Ruined King",
            "components": [1, 8],
            "description": "Wearer is also a Blademaster.",
            "tier": str(),
            "powers": {
                "ad": 15
            }
        },
        "19": {
            "name": "Infinity Edge",
            "components": [1, 9],
            "description": "100% critical strike damage",
            "tier": str(),
            "powers": {
                "ad": 15,
                "cr": 20,
            }
        },
        "22": {
            "name": "Rapid Firecannon",
            "components": [2, 2],
            "description": "Attack Range is tripled.",
            "tier": str(),
            "powers": {
                "sp": 30
            }
        },
        "23": {
            "name": "Guinsoo's Rageblade",
            "components": [2, 3],
            "description": "Basic Attacks grant +5% bonus Attack Speed for the rest of combat. No stacking limit.",
            "tier": str(),
            "powers": {
                "md": 20,
                "sp": 15
            }

        },
        "24": {
            "name": "Statikk Shiv",
            "components": [2, 4],
            "description": "Every third Basic Attack from the wearer deals 80 magic damage to 3/4/5 enemies.",
            "tier": str(),
            "powers": {
                "sp": 15,
                "mn": 15
            }
        },
        "25": {
            "name": "Titan's Resolve",
            "components": [2, 5],
            "description": "When the wearer takes damage or inflicts a critical hit, they gain a 2% stacking damage bonus. Stacks up to 50 times, at which point the wearer gains 25 Armor and Magic Resistance, and increases in size.",
            "tier": str(),
            "powers": {
                "sp": 15,
                "ar": 25
            }
        },
        "26": {
            "name": "Runaan's Hurricane",
            "components": [2, 6],
            "description": "Basic Attacks fire a bolt at another nearby enemy, dealing 70% of the wearer's Attack Damage and applying on-hit effects.",
            "tier": str(),
            "powers": {
                "mr": 25,
                "sp": 15
            }
        },
        "27": {
            "name": "Zz'Rot Portal",
            "components": [2, 7],
            "description": "When the wearer dies, a Construct with 1000/2000/3000 ★ Health aries to continue the fight.",
            "tier": str(),
            "powers": {
                "hp": 200,
                "sp": 15
            }
        },
        "28": {
            "name": "Infiltrator's Talons",
            "components": [2, 8],
            "description": "Wearer is also an Infiltrator.",
            "tier": str(),
            "powers": {
                "sp": 15
            }
        },
        "29": {
            "name": "Last Whisper",
            "components": [2, 9],
            "description": "Critical hits reduce the target’s Armor by 90% for 3 seconds. This effect does not stack.",
            "tier": str(),
            "powers": {
            }

        },
        "33": {
            "name": "Rabadon's Deathcap",
            "components": [3, 3],
            "description": "Wearer's Spell Power stat is amplified by 50%.",
            "tier": str(),
            "powers": {
                "md": 40,
            }
        },
        "34": {
            "name": "Luden's Echo",
            "components": [3, 4],
            "description": "When the wearer casts their spell, the first target dealt magic damage and up to 3 nearby enemies are dealt an additional 150 / 175 / 225 magic damage.",
            "tier": str(),
            "powers": {
                "md": 20,
                "mn": 15
            }
        },
        "35": {
            "name": "Locket of the Iron Solari",
            "components": [3, 5],
            "description": "Shields allies within two hexes in the same row for 250 / 275 / 350 damage for 8 seconds (scales with wearer’s Star Level).",
            "tier": str(),
            "powers": {
                "md": 20,
                "ar": 25
            }
        },
        "36": {
            "name": "Ionic Spark",
            "components": [3, 6],
            "description": "Enemies within 2 hexes have their Magic Resist reduced by 50% (does not stack). When they cast a spell, they are zapped taking magic damage equal to 225% of their max Mana.",
            "tier": str(),
            "powers": {
                "md": 20,
                "mr": 25
            }
        },
        "37": {
            "name": "Morellonomicon",
            "components": [3, 7],
            "description": "When the wearer deals damage with their spell, they burn the target, dealing 25% of the target's Maximum Health as true damage over 10 seconds and reducing healing by 50% for the duration of the burn.",
            "tier": str(),
            "powers": {
                "md": 20,
                "hp": 200
            }
        },
        "38": {
            "name": "Demolitionist's Charge",
            "components": [3, 8],
            "description": "Wearer is also a Demolitionist.",
            "tier": str(),
            "powers": {
                "md": 20,
            }
        },
        "39": {
            "name": "Jeweled Gauntlet",
            "components": [3, 9],
            "description": "The wearer's spells can critically strike.",
            "tier": str(),
            "powers": {
                "md": 20,
                "cr": 20
            }
        },
        "44": {
            "name": "Seraph's Embrace",
            "components": [4, 4],
            "description": "Wearer regains 20 mana after spellcast.",
            "tier": str(),
            "powers": {
                "mn": 30,
            }
        },
        "45": {
            "name": "Frozen Heart",
            "components": [4, 5],
            "description": "Adjacent enemies lose 50% Attack Speed. (Stacking increases the radius of this effect, not the amount of the slow).",
            "tier": str(),
            "powers": {
                "ar": 25,
                "mn": 15
            }
        },
        "46": {
            "name": "Chalice of Favor",
            "components": [4, 6],
            "description": "When the wearer casts a spell, restores 8 mana to allies within 2 hexes.",
            "tier": str(),
            "powers": {
                "mr": 25,
                "mn": 15
            }
        },
        "47": {
            "name": "Redemption",
            "components": [4, 7],
            "description": "When the wearer dies, allies are healed for 800 Health.",
            "tier": str(),
            "powers": {
                "hp": 200,
                "mn": 15
            }
        },
        "48": {
            "name": "Star Guardian's Charm",
            "components": [4, 8],
            "description": "Wearer is also a Star Guardian.",
            "tier": str(),
            "powers": {
                "mn": 15
            }
        },
        "49": {
            "name": "Hand of Justice",
            "components": [4, 9],
            "description": "Each planning phase, gain one: Deal +50% more damage / Basic Attack heal 50 health on Hit.",
            "tier": str(),
            "powers": {
                "mn": 15,
                "cr": 10,
                "dg": 10
            }
        },
        "55": {
            "name": "Bramble Vest",
            "components": [5, 5],
            "description": "Negates bonus damage from incoming critical hits. On being hit by a Basic Attack, deal 100 / 140 / 200 magic damage to all nearby enemies (once every 2.5 second maximum). Scales with wearer’s Star Level.",
            "tier": str(),
            "powers": {
                "ar": 50
            }
        },
        "56": {
            "name": "Sword Breaker",
            "components": [5, 6],
            "description": "25% chance to disarm for 3 seconds.",
            "tier": str(),
            "powers": {
                "mr": 25,
                "ar": 25
            }
        },
        "57": {
            "name": "Red Buff",
            "components": [5, 7],
            "description": "Wearer's Basic Attacks burn the target on-hit, dealing 25% of the target's Maximum Health as true damage over 10 seconds and reducing healing by 50% for the duration of the burn.",
            "tier": str(),
            "powers": {
                "hp": 200,
                "ar": 25
            }
        },
        "58": {
            "name": "Rebel Medal",
            "components": [5, 8],
            "description": "Wearer is also a Rebel.",
            "tier": str(),
            "powers": {
                "ar": 25
            }
        },
        "59": {
            "name": "Shroud of Stillness",
            "components": [5, 9],
            "description": "When combat begins, shoots a beam straight ahead that delays affected enemies' first spellcast, increasing their max Mana by 40% until they cast.",
            "tier": str(),
            "powers": {
                "ar": 25
            }
        },
        "66": {
            "name": "Dragon's Claw",
            "components": [6, 6],
            "description": "Reduces incoming magic damage by 50%.",
            "tier": str(),
            "powers": {
                "mr": 50
            }
        },
        "67": {
            "name": "Zephyr",
            "components": [6, 7],
            "description": "When combat begins, the wearer summons a whirlwind on the opposite side of the arena that removes the closest enemy from combat for 5 seconds.",
            "tier": str(),
            "powers": {
                "mr": 25,
                "hp": 200
            }
        },
        "68": {
            "name": "Celestial Orb",
            "components": [6, 8],
            "description": "The wearer gains the Celestial trait.",
            "tier": str(),
            "powers": {
                "mr": 25
            }
        },
        "69": {
            "name": "Quicksilver",
            "components": [6, 9],
            "description": "The wearer is immute to croud control for the first 10 seconds of combat.",
            "tier": str(),
            "powers": {
                "mr": 25,
                "dg": 20
            }
        },
        "77": {
            "name": "Warmog's Armor",
            "components": [7, 7],
            "description": "The wearer regenerates 5% of their missing Health per second. (max of 150 HP/tick).",
            "tier": str(),
            "powers": {
                "hp": 400,
            }
        },
        "78": {
            "name": "Protector's Chestguard",
            "components": [7, 8],
            "description": "Wearer is also a Protector.",
            "tier": str(),
            "powers": {
                "hp": 200
            }
        },
        "79": {
            "name": "Trap Claw",
            "components": [7, 9],
            "description": "Start combat with a spell shield. Stun the champion that breaks it for 4 sec.",
            "tier": str(),
            "powers": {
                "hp": 200,
                "dg": 20
            }
        },
        "88": {
            "name": "Force of Nature",
            "components": [8, 8],
            "description": "Gain +1 team size.",
            "tier": str(),
            "powers": {
            }
        },
        "89": {
            "name": "Dark Star's Heart",
            "components": [8, 9],
            "description": "Wearer is also a Dark Star.",
            "tier": str(),
            "powers": {
                "cr": 10,
                "dg": 10
            }
        },
        "99": {
            "name": "Thief's Gloves",
            "components": [9, 9],
            "description": "Each planning phase, fetch two temporary items, quality based upon your player level. [Consumes Three item Slots]",
            "tier": str(),
            "powers": {
                "cr": 20,
                "dg": 20
            }
        },
    }}
    df = pd.read_json("jsons_new/item_stats_TFT3_GameVariation_None.json").to_dict()
    print(df[15])
    for val, key in df.items():
        try:
            win_rate = (float(df[val]['win_rate']) * 10) * 5 / 100
            top_four_rate = (float(df[val]['top_four_rate']) * 10) * 5 / 100
            pick_rate = (float(df[val]['pick_rate']) * 10) * 90 / 100
            score = win_rate + top_four_rate + pick_rate
            json_data["items"]["{}".format(val)] = "{:.2f}".format(score)
            if score > 85:
                json_data2["items"]["{}".format(val)]["tier"] = "S"
            elif score > 70:
                json_data2["items"]["{}".format(val)]["tier"] = "A"
            elif score > 60:
                json_data2["items"]["{}".format(val)]["tier"] = "B"
            elif score > 50:
                json_data2["items"]["{}".format(val)]["tier"] = "C"
            else:
                json_data2["items"]["{}".format(val)]["tier"] = "D"
        except:
            json_data["items"]["{}".format(val)] = 0
    with open("popularity_scores/item_scores_new.json", 'w') as json_file:
        json.dump(json_data, json_file)
    with open("popularity_scores/item_tier_scores.json", 'w') as json_file:
        json.dump(json_data2, json_file)
    b = datetime.now()
    print("getitemscore :", b - a)


def parseitemscore():
    a = datetime.now()
    json_data = {"items": {}}
    df_new = pd.read_json("popularity_scores/item_scores_new.json").to_dict()
    df_old = pd.read_json('popularity_scores/item_scores_old.json').to_dict()
    df = pd.read_json("jsons_new/item_stats_TFT3_GameVariation_None.json").to_dict()

    for val, key in df.items():
        try:
            difference = "{:.2f}".format(
                float(df_new["items"][val]) - float(df_old["items"][val]))
            json_data["items"][val] = float(difference)
        except KeyError:
            json_data["items"][val] = 0

    with open("popularity_scores/item_scores_diff.json", "w") as json_file:
        json.dump(json_data, json_file)
    b = datetime.now()
    print("parsecompscore :", b - a)


def getfirstcomp():
    a = datetime.now()

    json_data = dict()
    df = pd.read_json("comp_jsons/comp_TFT3_GameVariation_None.json").to_dict()
    max_count = 0
    for val, key in df.items():
        if key["Count"] > max_count:
            max_count = float(key["Count"])

    for val, key in df.items():
        if key["Count"] == max_count:
            json_data = key

    with open("popularity_scores/first_comp.json", "w") as json_file:
        json.dump(json_data, json_file)
    b = datetime.now()
    print("parsecompscore :", b - a)


getchallengers()