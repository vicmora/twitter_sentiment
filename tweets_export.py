import datetime
import pandas as pd
# https://github.com/Jefferson-Henrique/GetOldTweets-python
from get_old_tweets import got3 as got
from textblob import TextBlob
from textblob import Blobber
from textblob.sentiments import NaiveBayesAnalyzer

# usage:
# import tweets_export as t

# query = '$eem'
# start_date = '2016-09-07'
# end_date = '2016-09-09'

# df = t.query_hist(query, start_date, end_date)
# df.to_csv(query.replace('$','')+'_tweets'+start_date+'to'+end_date+'.csv', encoding='utf-8')

def sentiment(df):
	tb = Blobber(analyzer=NaiveBayesAnalyzer())
	df['polarity'] = df['text'].apply(lambda x: TextBlob(x).sentiment.polarity)
	df['classification'] = df['text'].apply(lambda x: tb(x).sentiment.classification)
	df['p_pos'] = df['text'].apply(lambda x: tb(x).sentiment.p_pos)
	df['p_neg'] = df['text'].apply(lambda x: tb(x).sentiment.p_neg)

def query_hist(query, start_date, end_date):
    tweet_criteria = got.manager.TweetCriteria().setQuerySearch(query).setSince(start_date).setUntil(end_date)
    tweets = got.manager.TweetManager.getTweets(tweet_criteria)

    for i in range(len(tweets)):
        d = {'index':tweets[i].date, 'text':tweets[i].text, 'id':tweets[i].id, 'username':tweets[i].username,
             'retweets':tweets[i].retweets, 'favorites':tweets[i].favorites,  'mentions':tweets[i].mentions,
             'hashtags':tweets[i].hashtags, 'geo':tweets[i].geo, 'permalink':tweets[i].permalink}
        if i == 0:
            df = pd.DataFrame.from_dict(d,orient='index').T
            df.index = df['index']
            df = df.drop('index', axis=1)
        else:
            df2 = pd.DataFrame.from_dict(d,orient='index').T
            df2.index = df2['index']
            df2 = df2.drop('index', axis=1)
            df = df.append(df2)
        #print '{:%Y-%m-%d %H:%M:%S}'.format(datetime.datetime.now()) + ' ' + str(i) + '/' + str(len(tweets) - 1)
    sentiment(df)
    
    return df

# df = query_hist(query, start_date, end_date)

# df.to_csv(query.replace('$','')+'_tweets'+start_date+'to'+end_date+'.csv', encoding='utf-8')