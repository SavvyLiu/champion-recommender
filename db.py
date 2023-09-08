import sqlite3
import sys
import os
import req
import time

QUEUE_BUFFER = 100

def setup():
    '''Sets up the database with the required tables'''
    con = sqlite3.connect('data.db')
    cur = con.cursor()
    cur.execute('CREATE TABLE player_queue(puuid)') # queue
    cur.execute('CREATE TABLE mastery_data(puuid, championid, masterypoints)') # champion
    cur.execute('CREATE TABLE visited_players(puuid)') # visited players
    cur.close()
    con.close()
    return

def main():
    # check if data.db is in directory
    cwd = os.path.dirname(os.path.realpath(__file__))
    if not os.path.isfile(cwd + '/data.db'):
        setup()

    con = sqlite3.connect('data.db')
    cur = con.cursor()

    queue_length = cur.execute('SELECT COUNT(*) FROM player_queue').fetchone()[0]
    if queue_length == 0:
        summoner_name = input('Enter a summoner name: ')
        puuid = req.getPlayerPUUID(summoner_name)
        cur.execute('INSERT INTO player_queue VALUES(?)', (puuid,))
        con.commit()

    count = cur.execute('SELECT COUNT(*) FROM mastery_data').fetchone()[0]
    while count < 10000:
        time.sleep(1/10)
        try:
            puuid = cur.execute('SELECT * FROM player_queue').fetchone()[0]
            queue_length = cur.execute('SELECT COUNT(*) FROM player_queue').fetchone()[0]
            if queue_length < QUEUE_BUFFER:
                players = req.getPlayers(puuid)
                for player in players:
                    is_present = cur.execute('SELECT * FROM visited_players WHERE puuid=?', (player,)).fetchone()
                    if not is_present:
                        cur.execute('INSERT INTO player_queue VALUES(?)', (puuid,))
            player_mastery = req.getPlayerMastery(puuid)
            print(player_mastery)
            cur.execute('INSERT INTO mastery_data VALUES(?, ?, ?)', (puuid, *player_mastery,))
            cur.execute('INSERT INTO visited_accounts VALUES(?)', (puuid,))

            count = cur.execute('SELECT COUNT(*) FROM mastery_data').fetchone()[0]
        except KeyboardInterrupt:
            con.commit()
            cur.close()
            con.close()    
    cur.close()
    con.close()

if __name__ == '__main__':
    main()