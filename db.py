import sqlite3

def setup():
    '''Sets up the database with the required tables'''
    con = sqlite3.connect("data.db")
    cur = con.cursor()
    cur.execute('CREATE TABLE player_queue(puuid)') # queue
    cur.execute('CREATE TABLE champion(puuid, championid, masterypoints)') # champion
    cur.execute('CREATE TABLE visited_players(puuid)') # visited players
    return

setup()