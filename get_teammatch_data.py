from urllib.request import urlopen 
import requests
import json
import time
import os

from pathlib import Path

import pandas as pd


""" 
To get histotic teammatch data.  

"""

PANDAS_LIST = []                                    # save pandas data frame from each call so can concatenate them

LEAGUES_TO_GET = ['england-premier-league', 'spain-la-liga', 'germany-bundesliga', 'italy-serie-a', 'france-ligue-1']  # just get big 5


def saveOutput(data, leagueslug):

    current_dir = os.getcwd()

    path = current_dir + f"/data/teammatchdata/{leagueslug}/"
    Path(path).mkdir(parents=True, exist_ok=True)

    # Save as JSON
    fname = path + f'{leagueslug}.json'
    save_file = open(fname, "w")  
    json.dump(data, save_file, indent = 6)  
    save_file.close() 

    # Save as EXCEL
    excelpath = fname.replace('.json', '.xlsx')
    df = pd.json_normalize(data)
    
    df.to_excel(excelpath)


def getHistoricData(my_api_token, leagueslug):

    """ 
    This endpoint returns all data for a given league.

    """

    url = f'http://127.0.0.1:8000/api/teammatchdata/{leagueslug}/'

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

    my_api_token = 'fff933f9aaa4a86c2e9159ddf120999dd11440be' # online

    my_api_token =  '1c814017131711c6b5541bc50040c00f6ed76130'   # local extra@test

    leagueseasons = None

    df=pd.DataFrame()

    if LEAGUES_TO_GET:


        for league in LEAGUES_TO_GET:

            print(f"Getting data for league: {league}")
            leagueslug = league

            data = getHistoricData(my_api_token, leagueslug)
            #time.sleep(3)

            if data:
                dframe = pd.json_normalize(data)

            if dframe.empty:
                print("DF is empty")
            else:
                df = pd.concat([df, dframe], ignore_index=True)



        # Save the outputs
        current_dir = os.getcwd()
        path = current_dir + f"/data/teammatchdata/"
        Path(path).mkdir(parents=True, exist_ok=True)


        # Save as JSON
        fname = path + f'combined.json'
        df.to_json(fname, orient = 'records', compression = 'infer')


    else:

        # GET LIST OF LEAGUES AND SEASONS FROM API
        
        url = 'http://127.0.0.1:8000/api/leaguesdata/'
        #url = 'https://futstats.net/api/leaguesdata/'
        headers={"Authorization": f"Token {my_api_token}"}

        response = requests.get(url, headers=headers)
        status_code = int(response.status_code)

        if status_code == 200:
            print(f'Status Code: 200.  Successfully retrieved data from server!')    
            leagueseasons = response.json()
            
        else:
            print(f'Houston we have a problem.  Error code is: {status_code}')



        for league in leagueseasons[:2]:

            print(f"Getting data for league: {league['name']}")
            leagueslug = league['slug']

            data = getHistoricData(my_api_token, leagueslug)
            time.sleep(3)
            saveOutput(data, leagueslug)

if __name__ == '__main__':
    main()



