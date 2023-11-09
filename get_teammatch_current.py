from urllib.request import urlopen 
import requests
import json
import time
import os

from pathlib import Path

import pandas as pd


""" 
Pull current seasons teammatchstats and append to saved historic data.

Required historic data to have been brought down and saved as json.
"""

   

def getCurrentSeasonsData(my_api_token):
    """ 
    This endpoint returns data for all current leagues.

    """
    url = f'http://127.0.0.1:8000/api/teammatchdata/current/'

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

    """ 
    # get historic data from file.   Load to data frame, get current, contatenate and save.
    
    """
    #my_api_token = os.getenv("APIKEY") - doesn't work. path issue??
    #my_api_token = 'fff933f9aaa4a86c2e9159ddf120999dd11440be' # online
    my_api_token =  '1c814017131711c6b5541bc50040c00f6ed76130'   # local extra@test

    current_dir = os.getcwd()
    path = current_dir + f"/data/teammatchdata/"
    Path(path).mkdir(parents=True, exist_ok=True)
    fname = path + f'historic_combined.json'
    f = open(fname)

    historic = json.load(f)
    df = pd.json_normalize(historic)


    print('Historic DF from file :', df.head())

    # get latest and combine with historic.
    data = getCurrentSeasonsData(my_api_token)

    if data:
        print('have data from current seasons')

        dframe = pd.json_normalize(data)

        if not dframe.empty:
            print('concatenating historic with current....')
            df = pd.concat([df, dframe], ignore_index=True)

            # Save as JSON
            current_dir = os.getcwd()
            fname = path + f'cur_hist_combined.json'
            df.to_json(fname, orient = 'records', compression = 'infer')

            print('All Done! - should have combined Json file....')


    else:
        print('error with data....')


if __name__ == '__main__':
    main()



