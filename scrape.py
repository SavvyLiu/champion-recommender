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
    cur.execute('CREATE TABLE visited_accounts(puuid)') # visited players
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
        try:
            time.sleep(2.5)
            queue_length = cur.execute('SELECT COUNT(*) FROM player_queue').fetchone()[0]
            puuid = cur.execute('SELECT * FROM player_queue').fetchone()[0]
            if queue_length < QUEUE_BUFFER:
                accounts = req.getPlayers(puuid)
                for account in accounts:
                    is_present = cur.execute('SELECT * FROM visited_accounts WHERE puuid=?', (account,)).fetchone()
                    if not is_present:
                        cur.execute('INSERT INTO player_queue VALUES(?)', (account,))

            player_mastery = req.getPlayerMastery(puuid)
            for mastery in player_mastery:
                print(f'Writting mastery data ({count + 1}/10000)')
                cur.execute('INSERT INTO mastery_data VALUES(?, ?, ?)', (puuid, *mastery,))

            cur.execute('INSERT INTO visited_accounts VALUES(?)', (puuid,))
            cur.execute('DELETE FROM player_queue WHERE puuid=?', (puuid,))
            count = cur.execute('SELECT COUNT(*) FROM mastery_data').fetchone()[0]
            con.commit()
        except KeyboardInterrupt:
            print('Exiting program')
            con.commit()
            cur.close()
            con.close()    
    cur.close()
    con.close()

if __name__ == '__main__':
    main()