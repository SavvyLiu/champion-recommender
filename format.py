import sqlite3
import pickle

def main():
    # make a connection to the database 

    con = sqlite3.connect('data.db')
    cur = con.cursor()
    player_data = []

    # find the players in the mastery data (group by puuid)
    # make a query in mastery_data to find all the rows (entries) in mastery_data where puuid is the same (to a given target)
    # get the values from each of those rows (champion id and mastery) and make it into an array where the id is the index of the array

    players = cur.execute('SELECT DISTINCT puuid FROM mastery_data').fetchall()
    for player in players:
        champs = cur.execute('SELECT championid, masterypoints FROM mastery_data WHERE puuid =?', player).fetchall()
        mastery_points = {}
        for champ, mastery in champs:
            mastery_points[champ] = mastery
        player_data.append(mastery_points)

    with open('data.pickle', 'wb') as f:
        pickle.dump(player_data, f, pickle.HIGHEST_PROTOCOL)

if __name__ == '__main__':
    main()