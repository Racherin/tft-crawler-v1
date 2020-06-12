import pandas as pd
import datetime
import json
import sqlite3
def get_last_update():
    df = pd.read_json('C:\\Users\\merta\\Documents\\google_sync\\TFTSheets\\last_datetime.json').to_dict()
    epoch = df['last_datetime'][0]
    print(epoch)
    ts = datetime.datetime.fromtimestamp(epoch/1000).strftime('%Y-%m-%d %H:%M')
    ts = {'last_update':ts}
    with open('json_data/other_data/last_update.json', "w") as json_file:
        json.dump(ts, json_file)


def get_total_matches():
    db = sqlite3.connect('databases/match_ids.sqlite')
    cursor = db.cursor()
    cursor.execute("SELECT * FROM match_ids")
    mc = {
        'match_count':int(len(cursor.fetchall())),
    }
    with open('json_data/other_data/match_count.json', "w") as json_file:
        json.dump(mc, json_file)


if __name__ == '__main__':
    get_total_matches()