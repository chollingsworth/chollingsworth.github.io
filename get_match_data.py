from urllib.request import urlopen 
import requests
import json
import time
import os

from pathlib import Path

import pandas as pd


def saveOutput(data, leagueslug, season_name):

    current_dir = os.getcwd()

    path = current_dir + f"/data/matchdata/{leagueslug}/"
    Path(path).mkdir(parents=True, exist_ok=True)

 
    # Save as JSON
    fname = path + f'{season_name}.json'
    save_file = open(fname, "w")  
    json.dump(data, save_file, indent = 6)  
    save_file.close() 

    # Save as EXCEL
    excelpath = fname.replace('.json', '.xlsx')
    df = pd.json_normalize(data)
    df_home = pd.json_normalize(data, record_path=['home_stats'], record_prefix='home_', meta=['id'])
    df_away = pd.json_normalize(data, record_path=['away_stats'], record_prefix='away_', meta=['id'])
    df = (df.merge(df_home, on='id').merge(df_away, on='id').drop(['home_stats', 'away_stats'], axis=1))
    df.to_excel(excelpath)


def getHistoricData(my_api_token, season_id):

    url = f'https://futstats.net/api/matchesdata/season/{season_id}/'
    headers={"Authorization": f"Token {my_api_token}"}
    response = requests.get(url, headers=headers)
    status_code = int(response.status_code)

    if status_code == 200:
        print(f'Status Code: 200.  Successfully retrieved data from server!')    
        resp = response.json()
        return resp
    else:
        print(f'Houston we have a problem.  Error code is: {status_code}')
        return []
    

def main():

    #my_api_token = os.getenv("APIKEY") - doesn't work. path issue??

    my_api_token = 'fff933f9aaa4a86c2e9159ddf120999dd11440be'

    leagueseasons = None

    # GET LIST OF LEAGUES AND SEASONS FROM API
    url = 'https://futstats.net/api/leaguesdata/'
    headers={"Authorization": f"Token {my_api_token}"}

    response = requests.get(url, headers=headers)
    status_code = int(response.status_code)

    if status_code == 200:
        print(f'Status Code: 200.  Successfully retrieved data from server!')    
        leagueseasons = response.json()
        
    else:
        print(f'Houston we have a problem.  Error code is: {status_code}')


    # for item in leagueseasons:
    #     print(item)

    for league in leagueseasons:

        print(f"Getting data for league: {league['name']}")
        leagueslug = league['slug']

        for season in league['pseasons']:
            print(f"Getting historic data for season {season['year']}")
            data = getHistoricData(my_api_token, season['id'])
            time.sleep(3)

            season_year = season['year']
            season_name = season_year.replace("/", "-" )
            saveOutput(data, leagueslug, season_name)

if __name__ == '__main__':
    main()



