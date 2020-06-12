import pandas as pd
import json
import datetime


def getchampscore():
    json_data = {"champions": {
    }}
    json_data2 = {"champions": {
    }}
    df = pd.read_json('json_data/champion_data/None.json').to_dict()
    trait_template = {'blademaster': 0, 'brawler': 0, 'blaster': 0, 'celestial': 0, 'chrono': 0,
                      'cybernetic': 0, 'darkStar': 0, 'demolitionist': 0, 'infiltrator': 0, 'manaReaver': 0,
                      'mechPilot': 0, 'mercenary': 0, 'mystic': 0, 'protector': 0, 'rebel': 0, 'sniper': 0,
                      'sorcerer': 0, 'spacePirate': 0, 'starGuardian': 0, 'starship': 0,
                      'vanguard': 0, 'astro': 0,'paragon':0,'battlecast':0}
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

    with open("json_data/popularity_data/champions/outdated_scores.json", 'w') as json_file:
        json.dump(json_data, json_file)
    with open("json_data/popularity_data/champions/updated_tiers.json", 'w') as json_file:
        json.dump(json_data2, json_file)

def gettraitscore():
    json_data = {"traits": {}}
    json_data2 = {"traits": {
        "Blademaster": {
            "tier": None,
            "champions": ["Fiora", "Xayah", "Shen", "Yasuo", "MasterYi", "Irelia", "Riven"],
            "description": "Blademasters' Basic Attacks have a chance to trigger two additional attacks against their target. These additional attacks deal damage like Basic Attacks and trigger on-hit effects.",
        },
        "Blaster": {
            "tier": None,
            "champions": ["Graves", "Lucian", "Ezreal", "Jinx", "KogMaw"],
            "description": "Every fourth Basic Attack from a Blaster fires additional attacks at random enemies. These additional attacks deal damage like Basic Attacks, trigger on-hit effects and can critically hit.",
        },
        "Brawler": {
            "tier": None,
            "champions": ["Malphite", "Blitzcrank", "Vi", "Illaoi"],
            "description": "Brawlers gain bonus Maximum Health.",
        },
        "Demolitionist": {
            "tier": None,
            "champions": ["Ziggs", "Rumble", "Gangplank"],
            "description": "Damage from Demolitionists' spellcasts stun their for 1.50 seconds. (Once per spellcast)",
        },
        "Infiltrator": {
            "tier": None,
            "champions": ["KhaZix", "Nocturne", "Shaco", "Fizz", "Ekko","Zed"],
            "description": "Innate: At the start of combat, Infiltrators move to the enemy's backline. Infiltrators gain Attack Speed for 6 seconds at the start of combat, refreshes on takedown",
        },
        "Mercenary": {
            "tier": None,
            "champions": ["Gangplank",],
            "description": "Innate: Upgrades for Mercenaries's spells have a chance to appear in the shop.",
        },
        "ManaReaver": {
            "tier": None,
            "champions": ["Darius", "Irelia", "Thresh"],
            "description": "Mana-Reaver attacks increase the mana cost of their target’s next spell by 40%",
        },
        "Mystic": {
            "tier": None,
            "champions": ["Cassiopeia", "Karma", "Soraka", "Lulu",],
            "description": "All allies gain Magic Resistance.",
        },
        "Protector": {
            "tier": None,
            "champions": ["JarvanIV", "Rakan", "XinZhao", "Neeko","Urgot"],
            "description": "Protectors shield themselves for 4 seconds whenever they cast a spell. This shield doesn't stack.",
        },
        "Sniper": {
            "tier": None,
            "champions": ["Caitlyn", "Ashe", "Jhin","Teemo","Vayne"],
            "description": "Snipers deal 15% increased damage for each hex between themselves and their target.",
        },
        "Sorcerer": {
            "tier": None,
            "champions": ["TwistedFate", "Zoe", "Ahri", "Annie", "Syndra", "Xerath","Viktor"],
            "description": "All allies have increased Spell Power.",
        },
        "Vanguard": {
            "tier": None,
            "champions": ["Leona", "Poppy", "Mordekaiser", "Jayce", "WuKong","Nautilus"],
            "description": "Vanguard champions gain bonus Armor.",
        },
        "Celestial": {
            "tier": None,
            "champions": ["Xayah", "Rakan", "XinZhao", "Ashe", "Lulu"],
            "description": "All allies heal for some of the damage they deal with spells and attacks.",
        },
        "Chrono": {
            "tier": None,
            "champions": ["Caitlyn", "TwistedFate", "Blitzcrank", "Shen", "Ezreal", "WuKong", "Thresh","Riven"],
            "description": "All allies gain 15% Attack Speed every some seconds.",
        },
        "Cybernetic": {
            "tier": None,
            "champions": ["Leona", "Fiora", "Lucian", "Vi", "Irelia", "Ekko","Vayne"],
            "description": "Cybernetic champions with at least one item gain Health and Attack Damage.",
        },
        "DarkStar": {
            "tier": None,
            "champions": ["JarvanIV", "Mordekaiser", "Karma", "Shaco", "Jhin", "Xerath"],
            "description": "When a Dark Star Champion dies, all other allied Dark Star Champions gain Attack Damage and Spell Power",
        },
        "MechPilot": {
            "tier": None,
            "champions": ["Annie", "Rumble", "Fizz"],
            "description": "The Super-Mech has the combined Pilots Health, Attack Damage, and Traits of its Pilots, as well as 3 random items from among them. When the Super-Mech dies the Pilots are ejected, continue to fight.",
        },
        "Rebel": {
            "tier": None,
            "champions": ["Ziggs", "Malphite", "Zed", "Yasuo", "MasterYi", "Jinx", "AurelionSol"],
            "description": "At the start of combat, Rebels gain a shield and increased damage for each adjacent Rebel. The shield lasts for 8 seconds.",
        },
        "SpacePirate": {
            "tier": None,
            "champions": ["Graves", "Darius", "Jayce", "Gangplank"],
            "description": "Whenever a Space Pirate lands a killing blow on a Champion there is a chance to drop extra loot.",
        },
        "StarGuardian": {
            "tier": None,
            "champions": ["Poppy", "Zoe", "Ashe", "Neeko", "Syndra", "Soraka","Janna"],
            "description": "Star Guardians' spellcasts grant Mana to other Star Guardians spread among them.",
        },
        "Starship": {
            "tier": None,
            "champions": ["AurelionSol"],
            "description": "Innate: Starships gain 40 Mana per second, maneuver around the board, and are immune to movement impairing effects, but can't Basic Attack.",
        },
        "Battlecast":{
            "tier":None,
            "champions":['Cassiopeia','Illaoi','KogMaw','Nocturne','Urgot','Viktor'],
            'description':"Battlecast champions, upon dealing or taking 10 instances of damage, heal if below half health, or deal magic damage to the nearest enemy if above half."
        },
        "Astro":{
            'tier':None,
            'champions':["Bard",'Gnar','Nautilus','Teemo'],
            'description':'Astro Champions reduce their mana costs by 30',
        },
        "Paragon":{
            'tier':None,
            'champions':['Janna'],
            'description':'Ally Star Guardian basic attacks are converted to true damage.'
        }

    }}
    df = pd.read_json("json_data/trait_data/None.json").to_dict()
    trait_names = ['Blademaster', 'Blaster', 'Brawler', 'Celestial', 'Chrono', 'Cybernetic', 'DarkStar',
                   'Demolitionist', 'Infiltrator', 'ManaReaver', 'MechPilot', 'Mercenary', 'Mystic', 'Protector',
                   'Rebel', 'Sniper', 'Sorcerer', 'SpacePirate', 'StarGuardian', 'Starship', 'Astro', 'Vanguard',
                   'Battlecast','Paragon']
    for name in trait_names:
        win_rate = (float(df['{}'.format(name)]['win_rate']) * 10) * 5 / 100
        top_four_rate = (float(df['{}'.format(name)]['top_four_rate']) * 10) * 5 / 100
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
    with open("json_data/popularity_data/traits/outdated_scores.json", 'w') as json_file:
        json.dump(json_data, json_file)
    with open("json_data/popularity_data/traits/updated_tiers.json", 'w') as json_file:
        json.dump(json_data2, json_file)

def getitemscore():
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
            "name": "Battlecast Hex Core",
            "components": [3, 8],
            "description": "Wearer is also a Battlecast.",
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
            "name": "Blue Sentiel",
            "components": [4, 4],
            "description": "Set's holder mana to 20 after each cast.",
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
            "name": "Chalice of Power",
            "components": [4, 6],
            "description": "At start of combat, the holder and their left and right neighbors gain 30AP for 20 seconds.",
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
    df = pd.read_json("json_data/item_data/None.json").to_dict()
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
    with open("json_data/popularity_data/items/outdated_scores.json", 'w') as json_file:
        json.dump(json_data, json_file)
    with open("json_data/popularity_data/items/updated_tiers.json", 'w') as json_file:
        json.dump(json_data2, json_file)

def getchampdiff():
    json_data = {"champions": {}}
    df_new = pd.read_json("json_data/popularity_data/champions/outdated_scores.json").to_dict()
    df_old = pd.read_json("json_data/popularity_data/champions/outdated_scores.json").to_dict()
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
    for name in champ_names.keys():
        difference = "{:.2f}".format(
            float(df_new["champions"]['{}'.format(name)]) - float(df_old["champions"]['{}'.format(name)]))
        json_data["champions"]["{}".format(name)] = float(difference)

    with open("json_data/popularity_data/champions/difference_scores.json", "w") as json_file:
        json.dump(json_data, json_file)

def gettraitdiff():
    json_data = {"traits": {}}
    df_new = pd.read_json("json_data/popularity_data/traits/outdated_scores.json").to_dict()
    df_old = pd.read_json("json_data/popularity_data/traits/outdated_scores.json").to_dict()
    trait_names = ['Blademaster', 'Blaster', 'Brawler', 'Celestial', 'Chrono', 'Cybernetic', 'DarkStar',
                   'Demolitionist', 'Infiltrator', 'ManaReaver', 'MechPilot', 'Mercenary', 'Mystic', 'Protector',
                   'Rebel', 'Sniper', 'Sorcerer', 'SpacePirate', 'StarGuardian', 'Starship','Vanguard',"Battlecast","Astro","Paragon"]
    for name in trait_names:
        difference = "{:.2f}".format(
            float(df_new["traits"]['{}'.format(name)]) - float(df_old["traits"]['{}'.format(name)]))
        json_data["traits"]["{}".format(name)] = float(difference)

    with open("json_data/popularity_data/traits/difference_scores.json", "w") as json_file:
        json.dump(json_data, json_file)

def getitemdiff():
    json_data = {"items": {}}
    df_new = pd.read_json("json_data/popularity_data/items/outdated_scores.json").to_dict()
    df_old = pd.read_json("json_data/popularity_data/items/outdated_scores.json").to_dict()
    df = pd.read_json("json_data/item_data/None.json").to_dict()

    for val, key in df.items():
        try:
            difference = "{:.2f}".format(
                float(df_new["items"][val]) - float(df_old["items"][val]))
            json_data["items"][val] = float(difference)
        except KeyError:
            json_data["items"][val] = 0

    with open("json_data/popularity_data/items/difference_scores.json", "w") as json_file:
        json.dump(json_data, json_file)

if __name__ == '__main__':
    getchampscore()
    gettraitscore()
    getitemscore()
    getchampdiff()
    gettraitdiff()
    getitemdiff()
