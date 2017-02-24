import pandas as pd
import requests
import cfg
from requests_oauthlib import OAuth1
from pandas.io.json import json_normalize

# usage:
# import twitter_api as ta
# un_list=['potus', 'realdonaldtrump']
# df = ta.username_lookup(un_list)

def username_lookup(un_list):
    df = pd.DataFrame()

    for i in range(0,len(un_list),100):
        working_list = un_list[i:i+100]
        usernames = ''
        for name in working_list:
            if name == working_list[-1]:
                usernames = usernames + name
                break
            else:
                string = name + '%2C'
                usernames = usernames + string

        url = 'https://api.twitter.com/1.1/users/lookup.json?screen_name=%s' % usernames
        auth = OAuth1(cfg.API_KEY, cfg.API_SECRET, cfg.ACCESS_TOKEN, cfg.ACCESS_TOKEN_SECRET)
        r = requests.get(url, auth=auth)
        for i in range(len(working_list)):
            try:
                name_df = json_normalize(r.json()[i])
                df = df.append(name_df)
            except:
                pass
    return df

    # df.to_csv('twitter_usernames.csv', encoding='utf-8')