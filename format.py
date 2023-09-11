import sqlite3
import csv

def main():
    # make a connection to the database 

    con = sqlite3.connect('data.db')
    cur = con.cursor()
    player_data = []

    # find the players in the mastery data (group by puuid)
    # make a query in mastery_data to find all the rows (entries) in mastery_data where puuid is the same (to a given target)
    # get the values from each of those rows (champion id and mastery) and make it into an array where the id is the index of the array

    with open('data.csv', 'w', newline='') as f:
        writer =  csv.writer(f)
        players = cur.execute('SELECT puuid, championid, masterypoints FROM mastery_data').fetchall()
        writer.writerows(players)

if __name__ == '__main__':
    main()