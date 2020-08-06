# Import required libraries
import requests
import pandas as pd
import numpy as np
from concurrent.futures import ThreadPoolExecutor, as_completed

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

    # Return pandas data frame
    return df_country