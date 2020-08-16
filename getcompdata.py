from sqlite3 import dbapi2 as sqlite3
from multiprocessing import Pool
from datetime import datetime
import requests
import time
import json
import pandas as pd
from operator import *
import copy
import operator

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36 Edg/83.0.478.37",
    "Accept-Language": "en-US,en;q=0.9",
    "Accept-Charset": "application/x-www-form-urlencoded; charset=UTF-8",
    "Origin": "https://developer.riotgames.com",
    "X-Riot-Token": ""
}


def get_all_comp_data():
    a = datetime.now()
    json_data = {}
    game_modes = ['AllGalaxies']
    indicators = {
        "Ahri": "None",
        "Annie": "None",
        "Ashe": "None",
        "AurelionSol": "None",
        "Bard": "Nerf",
        "Blitzcrank": "None",
        "Caitlyn": "None",
        "Cassiopeia": "None",
        "Ezreal": "None",
        "Ekko": "None",
        "Darius": "None",
        "Fiora": "None",
        "Fizz": "Nerf",
        "Gangplank": "Buff",
        "Graves": "None",
        "Gnar": "None",
        "Illaoi": "None",
        "Irelia": "None",
        "Janna": "None",
        "JarvanIV": "None",
        "Jayce": "None",
        "Jhin": "Nerf",
        "Jinx": "Buff",
        "Karma": "None",
        "KogMaw": "None",
        "Leona": "None",
        "Lucian": "None",
        "Lulu": "None",
        "Malphite": "None",
        "MasterYi": "None",
        "Mordekaiser": "None",
        "Nautilus": "None",
        "Neeko": "None",
        "Nocturne": "None",
        "Poppy": "None",
        "Rakan": "None",
        "Rumble": "None",
        "Shaco": "None",
        "Shen": "None",
        "Syndra": "None",
        "Soraka": "None",
        "Riven": "None",
        "Teemo": "Nerf",
        "Thresh": "None",
        "TwistedFate": "None",
        "Urgot": "None",
        "Vayne": "None",
        "Vi": "None",
        "Viktor": "None",
        "WuKong": "None",
        "Xayah": "None",
        "Xerath": "None",
        "XinZhao": "None",
        "Yasuo": "None",
        "Zed": "None",
        "Ziggs": "None",
        "Zoe": "None"

    }
    item_name_list = {"1": "B.F Sword", "2": "Recurve Bow", "3": "Needlessly Large Rod", "4": "Tear of the Goddess",
                      "5": "Chain Vest", "6": "Negatron Cloak", "7": "Giant's Belt", "8": "Spatula",
                      "9": "Sparring Gloves", "11": "Deathblade", "12": "Giant Slayer", "13": "Hextech Gunblade",
                      "14": "Spear of Shojin", "15": "Guardian Angel", "16": "Bloodthirster", "17": "Zeke's Herald",
                      "18": "Blade of the Ruined King", "19": "Infinity Edge", "22": "Rapid Firecannon",
                      "23": "Guinsoo's Rageblade", "24": "Statikk Shiv", "25": "Titan's Resolve",
                      "26": "Runaan's Hurricane", "27": "Zz'Rot Portal", "28": "Infiltrator's Talons",
                      "29": "Last Whisper", "33": "Rabadon's Deathcap", "34": "Luden's Echo",
                      "35": "Locket of the Iron Solari", "36": "Ionic Spark", "37": "Morellonomicon",
                      "38": "Battlecast Hex Core", "39": "Jeweled Gauntlet", "44": "Blue Buff",
                      "45": "Frozen Heart", "46": "Chalice of Favor", "47": "Redemption", "48": "Star Guardian's Charm",
                      "49": "Hand of Justice", "55": "Bramble Vest", "56": "Sword Breaker", "57": "Red Buff",
                      "58": "Rebel Medal", "59": "Shroud of Stillness", "66": "Dragon's Claw", "67": "Zephyr",
                      "68": "Celestial Orb", "69": "Quicksilver", "77": "Warmog's Armor",
                      "78": "Protector's Chestguard", "79": "Trap Claw", "88": "Force of Nature",
                      "89": "Dark Star's Heart", "99": "Thief's Gloves"}
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
                   'KogMaw': ['battlecast', 'blaster'],
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
    trait_template = {'blademaster': 0, 'brawler': 0, 'blaster': 0, 'celestial': 0, 'chrono': 0,
                      'cybernetic': 0, 'darkstar': 0, 'demolitionist': 0, 'infiltrator': 0, 'manareaver': 0,
                      'mechpilot': 0, 'mercenary': 0, 'mystic': 0, 'protector': 0, 'rebel': 0, 'sniper': 0,
                      'sorcerer': 0, 'spacepirate': 0, 'starguardian': 0, 'starship': 0,
                      'vanguard': 0, 'astro': 0, 'paragon': 0, 'battlecast': 0}
    inv_map = {v: k for k, v in item_name_list.items()}

    for mode in game_modes:
        df = pd.read_json('C:\\Users\\merta\\Documents\\google_sync\\TFTSheets\\{}.json'.format(mode))
        current_df_columns = df.columns.to_list()
        max_col = 0
        for column in current_df_columns:
            if max_col < int(column[0]):
                max_col = int(column[0])
        for column in range(1, max_col + 1):
            json_data["team_comp_{}".format(column)] = {"comp_name": str(), "Thumbnail_picture": None, "Count": None,
                                                        "Placement": None, "WinRate": None, "Top4Rate": None,
                                                        "PickPct": None,
                                                        "Traits": {'blademaster': 0, 'brawler': 0, 'blaster': 0,
                                                                   'celestial': 0, 'chrono': 0,
                                                                   'cybernetic': 0, 'darkstar': 0, 'demolitionist': 0,
                                                                   'infiltrator': 0, 'manareaver': 0,
                                                                   'mechpilot': 0, 'mercenary': 0, 'mystic': 0,
                                                                   'protector': 0, 'rebel': 0, 'sniper': 0,
                                                                   'sorcerer': 0, 'spacepirate': 0, 'starguardian': 0,
                                                                   'starship': 0,
                                                                   'vanguard': 0, 'astro': 0, 'battlecast': 0,
                                                                   'paragon': 0}, "Trait_tiers": None,
                                                        "Champions": {},
                                                        "first_row": {
                                                            "a1": "None",
                                                            "a2": "None",
                                                            "a3": "None",
                                                            "a4": "None",
                                                            "a5": "None",
                                                            "a6": "None",
                                                            "a7": "None",
                                                        },
                                                        "second_row": {

                                                            "b1": "None",
                                                            "b2": "None",
                                                            "b3": "None",
                                                            "b4": "None",
                                                            "b5": "None",
                                                            "b6": "None",
                                                            "b7": "None",

                                                        },
                                                        "third_row": {

                                                            "c1": "None",
                                                            "c2": "None",
                                                            "c3": "None",
                                                            "c4": "None",
                                                            "c5": "None",
                                                            "c6": "None",
                                                            "c7": "None",

                                                        },
                                                        "fourth_row": {
                                                            "d1": "None",
                                                            "d2": "None",
                                                            "d3": "None",
                                                            "d4": "None",
                                                            "d5": "None",
                                                            "d6": "None",
                                                            "d7": "None",
                                                        },
                                                        "first_item_priortiy": {
                                                            "first": "None",
                                                            "second": "None",
                                                            "third": "None"
                                                        },
                                                        "item_priority": {
                                                            "first": "None",
                                                            "second": "None",
                                                            "third": "None"
                                                        }
                                                        }
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
                            '{}'.format(str(key).strip("TFT3").strip("_"))] = {"Count": int(df_col2[val]), "Items": [],
                                                                               "Indicator": indicators['{}'.format(str(key).strip("TFT3").strip("_"))]}
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
                elif key == "WinRate":
                    json_data["team_comp_{}".format(column)][key] = df_col2[val]
                elif key == "Top4Rate":
                    json_data["team_comp_{}".format(column)][key] = df_col2[val]
                elif key == "PickPct":
                    json_data["team_comp_{}".format(column)][key] = df_col2[val]
            traits_copy = copy.deepcopy(json_data)
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
                    traits_copy["team_comp_{}".format(column)]['Trait_tiers'][val] = key // 2
                elif val == 'astro' and key > 2:
                    traits_copy["team_comp_{}".format(column)]['Trait_tiers'][val] = 1
                elif val == 'battlecast' and key > 1:
                    traits_copy["team_comp_{}".format(column)]['Trait_tiers'][val] = key // 2
                elif val == 'paragon' and key > 0:
                    traits_copy["team_comp_{}".format(column)]['Trait_tiers'][val] = 1
                else:
                    traits_copy["team_comp_{}".format(column)]['Trait_tiers'].pop(val)
            json_data["team_comp_{}".format(column)]['Trait_tiers'] = traits_copy["team_comp_{}".format(column)][
                'Trait_tiers']
            inc_champions = dict(
                sorted(json_data["team_comp_{}".format(column)]["Traits"].items(), key=operator.itemgetter(1),
                       reverse=True)[:2])
            comp_name_list = list()
            for val, key in inc_champions.items():
                comp_name_list.append(val)
            json_data["team_comp_{}".format(column)]["comp_name"] = str(
                comp_name_list[0].title() + " & " + comp_name_list[1].title())
            json_data["team_comp_{}".format(column)].pop("Traits")
        json_data_sorted = sorted(json_data.items(), key=lambda x: getitem(x[1], 'Placement'), reverse=False)
        with open('json_data/comp_data/None.json', "w") as json_file:
            json.dump(dict(json_data_sorted), json_file)
    b = datetime.now()
    print('get_comp_data', b - a)


if __name__ == '__main__':
    get_all_comp_data()
