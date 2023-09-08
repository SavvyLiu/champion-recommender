from typing import List
import json
import requests
from dotenv import dotenv_values

API_KEY = dotenv_values()['API_KEY']

def getPlayerPUUID(summoner_name: str) -> str:
    req = requests.get(f'https://na1.api.riotgames.com/lol/summoner/v4/summoners/by-name/{summoner_name}?api_key={API_KEY}')
    if req.status_code != 200:
        print(f'[Error] issue getting player puuid {req.status_code}')
        return
    puuid = json.loads(req.text)['puuid']
    return puuid

def getPlayers(seed_puuid: str) -> List[str]:
    req = requests.get(f'https://americas.api.riotgames.com/lol/match/v5/matches/by-puuid/{seed_puuid}/ids?start=0&count=1&api_key={API_KEY}')
    if req.status_code != 200:
        print(f'[Error] issue getting player infomation {req.status_code}')
        return
    match_id = json.loads(req.text)[0]

    req = requests.get(f'https://americas.api.riotgames.com/lol/match/v5/matches/{match_id}?api_key={API_KEY}')
    if req.status_code != 200:
        print(f'[Error] issue getting player infomation {req.status_code}')
        return
    return json.loads(req.text)['metadata']['participants'] 

def getPlayerMastery(puuid: str) -> List[tuple[int, int]]:
    req = requests.get(f'https://na1.api.riotgames.com/lol/champion-mastery/v4/champion-masteries/by-puuid/{puuid}/top?api_key={API_KEY}')
    if req.status_code != 200:
        print(f'[Error] issue getting player infomation {req.status_code}')
        return
    body = json.loads(req.text)
    return [(champ['championId'], champ['championPoints']) for champ in body]

def main():
    puuid = getPlayerPUUID('SavageCabb')
    print(puuid)
    print(getPlayerMastery(puuid))

if __name__ == '__main__':
    main()


