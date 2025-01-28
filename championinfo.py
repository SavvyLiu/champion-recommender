import sqlite3
import json

def setup():
    con = sqlite3.connect('data.db')
    cur = con.cursor()
    cur.execute('''CREATE TABLE champion_info(
                champion_id PRIMARY KEY, 
                name,
                attack,
                defense,
                magic,
                difficulty
                )''') # champion data

def main():

    con = sqlite3.connect('data.db')
    cur = con.cursor()

    with open('champion.json', encoding="utf-8") as user_file:
        file_contents = json.load(user_file)

    champs = file_contents.get('data')
    for k,v in champs.items():
        cur.execute('INSERT INTO champion_info VALUES(?,?,?,?,?,?)', (v['key'], k, v['info']['attack'], v['info']['defense'], v['info']['magic'], v['info']['difficulty']))
        con.commit()


if __name__ == '__main__':
    main()