# Import required libraries
import os
import requests
import pandas as pd
import numpy as np
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime

#--------------------------------------------------------------

# Change directory to data directory
work_dir = os.getcwd()
if not 'data' in work_dir.split("/"):
    os.chdir('./data')

#--------------------------------------------------------------

#Create function to unpack arrays in timeline fields
def using_repeat(df):
    lens = [len(item) for item in df['timeline']]
    return pd.DataFrame( {"name" : np.repeat(df['name'].values,lens),
                          "coordinates" : np.repeat(df['coordinates'].values,lens),
                          "code" : np.repeat(df['code'].values,lens),
                          "population": np.repeat(df['population'].values,lens),
                          "timeline" : np.concatenate(df['timeline'].values)})

#--------------------------------------------------------------

def timeline_raw_data():
    # URL Link construction
    timeline_url = "https://corona-api.com/timeline"

    # Request to endpoint
    raw_timeline = requests.request("GET", timeline_url)
    raw_timeline = raw_timeline.json()

    # Transform data into pandas dataframe
    df_timeline = pd.DataFrame(raw_timeline['data'])
    df_timeline['updated_at'] = df_timeline['updated_at'].astype('datetime64')
    df_timeline['date'] = df_timeline['date'].astype('datetime64')

    # Create timestamp and name
    timestamp = datetime.today().strftime('%Y_%m_%d')
    name = 'df_timeline_{}.parquet.snappy'.format(timestamp)

    # Delete previous file
    for filename in os.listdir():
        if 'df_timeline_' in filename:
            os.remove(filename)

    # Save data to parquet format
    df_timeline.to_parquet(
        name,
        compression='snappy'
    )

    # Return pandas data frame
    return df_timeline

#--------------------------------------------------------------

def country_raw_data():
    # URL Link construction
    country_url = "https://corona-api.com/countries"

    # API call
    raw_country = requests.request("GET", country_url)
    raw_country = raw_country.json()
    
    # Transform data into pandas dataframe and unpack array fields
    df_country = pd.DataFrame(raw_country['data'])
    df_country = df_country.join(pd.json_normalize(df_country["today"].tolist()).add_prefix("today.")).drop(["today"], axis=1)
    df_country = df_country.join(pd.json_normalize(df_country["latest_data"].tolist()).add_prefix("latest_data.")).drop(["latest_data"], axis=1)
    df_country = df_country.join(pd.json_normalize(df_country["coordinates"].tolist()).add_prefix("coordinates.")).drop(["coordinates"], axis=1)

    # Create timestamp and name
    timestamp = datetime.today().strftime('%Y_%m_%d')
    name = 'df_country_{}.parquet.snappy'.format(timestamp)

    # Delete previous file
    for filename in os.listdir():
        if 'df_country_20' in filename:
            os.remove(filename)

    # Save data to parquet format
    df_country.to_parquet(
        name,
        compression='snappy'
    )

    # Return pandas data frame
    return df_country

#--------------------------------------------------------------


def download_file(url, mylist):
    try:
        resp = requests.get(url)
        resp_json = resp.json()
        mylist.append(resp_json['data'])
        return resp.status_code
    except requests.exceptions.RequestException as e:
       return e

#--------------------------------------------------------------

def multi_url_get(urls):
    threads= []
    mylist = []
    with ThreadPoolExecutor(max_workers=20) as executor:
        for url in urls:
            threads.append(executor.submit(download_file, url, mylist))
    return mylist

#--------------------------------------------------------------

def country_timeline_raw_data():
    # URL Link construction
    country_url = country_raw_data()

    # Unique country list
    country_code = list(country_url.code.unique())

    country_endpoint = []
    for i in country_code:
        url = 'https://corona-api.com/countries/' + i
        country_endpoint.append(url)

    # Multi URL get to speed up execution¡
    df_country = pd.DataFrame(multi_url_get(country_endpoint))

    df_country = using_repeat(df_country)
    df_country = df_country.join(pd.json_normalize(df_country["timeline"].tolist()).add_prefix("timeline.")).drop(["timeline"], axis=1)
    df_country = df_country.join(pd.json_normalize(df_country["coordinates"].tolist()).add_prefix("coordinates.")).drop(["coordinates"], axis=1)
    df_country['timeline.date']=pd.to_datetime(df_country['timeline.date'])

    # Create timestamp and name
    timestamp = datetime.today().strftime('%Y_%m_%d')
    name = 'df_country_flatten_{}.parquet.snappy'.format(timestamp)

    # Delete previous file
    for filename in os.listdir():
        if 'df_country_flatten' in filename:
            os.remove(filename)

    # Save data to parquet format
    df_country.to_parquet(
        name,
        compression='snappy'
    )

    # Return pandas data frame
    return df_country

#--------------------------------------------------------------

def get_country_prediction(id_country):
    if not id_country:
        return 0
    else:
        url = 'https://covid19-api.org/api/prediction/{}'.format(id_country)
        url2 = 'https://covid19-api.org/api/status/{}'.format(id_country)
        resp = requests.get(url)
        resp2 = requests.get(url2)
        data = resp.json()
        data2 = resp2.json()
        data = data[0]['cases']
        data2 = data2['cases']
        return  data - data2