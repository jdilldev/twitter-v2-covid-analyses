# -*- coding: utf-8 -*-
"""twarc.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1PfPIbaQDx_36hJgJKXmAM6WOaQBrka1R
"""

# import the libraries
import scipy.stats as st
from collections import Counter
from textblob import TextBlob

from wordcloud import WordCloud
import pandas as pd
import numpy as np
import re
import plotly.graph_objects as go
import plotly.express as px
import random


states = {
    'Alabama': 'AL',
    'Alaska': 'AK',
    'Arizona': 'AZ',
    'Arkansas': 'AR',
    'California': 'CA',
    'Colorado': 'CO',
    'Connecticut': 'CT',
    'Delaware': 'DE',
    'District Of Columbia': 'DC',
    'Florida': 'FL',
    'Georgia': 'GA',
    'Hawaii': 'HI',
    'Idaho': 'ID',
    'Illinois': 'IL',
    'Indiana': 'IN',
    'Iowa': 'IA',
    'Kansas': 'KS',
    'Kentucky': 'KY',
    'Louisiana': 'LA',
    'Maine': 'ME',
    'Maryland': 'MD',
    'Massachusetts': 'MA',
    'Michigan': 'MI',
    'Minnesota': 'MN',
    'Mississippi': 'MS',
    'Missouri': 'MO',
    'Montana': 'MT',
    'Nebraska': 'NE',
    'Nevada': 'NV',
    'New Hampshire': 'NH',
    'New Jersey': 'NJ',
    'New Mexico': 'NM',
    'New York': 'NY',
    'North Carolina': 'NC',
    'North Dakota': 'ND',
    'Ohio': 'OH',
    'Oklahoma': 'OK',
    'Oregon': 'OR',
    'Pennsylvania': 'PA',
    'Rhode Island': 'RI',
    'South Carolina': 'SC',
    'South Dakota': 'SD',
    'Tennessee': 'TN',
    'Texas': 'TX',
    'Utah': 'UT',
    'Vermont': 'VT',
    'Virgin Islands': 'VI',
    'Virginia': 'VA',
    'Washington': 'WA',
    'West Virginia': 'WV',
    'Wisconsin': 'WI',
    'Wyoming': 'WY',
}

print('reading CSV')
df= pd.read_csv('./pre-tweets.csv3.csv', usecols=["created_at", "text", "geo.full_name",'author.location'])

df.columns=['Created Date','Tweet','Tweet Location','User Location']

def retrieve_location(location):
    if ("," in location):
        location_set= set(i.lower().strip().replace(',','') for i in location.split())
        state_abbrv_set = set(i.lower() for i in states.values())
        state_name_set = set(i.lower() for i in states.keys())

        if (len(state_abbrv_set&location_set)==0):
            if (len(state_abbrv_set&location_set)==0):
                if (len(state_name_set&location_set)==1):
                    return states.get(list(state_name_set&location_set)[0].title().strip())
                else:
                    location_set_2 = set(i.lower().strip() for i in location.split(','))
                    if (len(location_set_2&state_name_set)==1):
                        return states.get(list(state_name_set&location_set_2)[0].title().strip())
                    elif (len(location_set_2&state_abbrv_set)==1):
                        return list(state_abbrv_set&location_set_2)[0].upper().strip()
                    else:
                        return 'Unknown'
        else:
            return (location.split(',')[-1]).upper().strip()
    elif (location in states.keys()):
        return states.get(location)
    elif (location in states.values()):
        return location.strip()
    else:
        return 'Unknown'

def extract_place_helper(location):
    if ("," in location):
        return True
    elif (location in states.keys()):
        return True
    elif (location in states.values()):
        return True
    else:
        return False

#Store the tweets for pre; full-text returned by default
def extract_place(tweet_location, user_location):
    if (isinstance(tweet_location, str)):
        if (extract_place_helper(tweet_location)):
            return retrieve_location(tweet_location)
        elif (isinstance(user_location, str)):
            if (extract_place_helper(user_location)):
                return retrieve_location(user_location)
            else: return 'Unknown'
        else:
            return 'Unknown'
    elif (isinstance(user_location, str)):
        if (extract_place_helper(user_location)):
            return retrieve_location(user_location)
        else:
            return 'Unknown'
    else:
        return 'Unknown'

df['Location'] = df.apply(lambda x: extract_place(x['Tweet Location'], x['User Location']), axis=1)

print('finished applying locations to tweets')

def deEmojify(text):
    return text

#Create a function to clean the tweets
def cleanTwt(twt):
    if(isinstance(twt, str)):
        twt = re.sub('#Covid', 'Covid', twt) # Removes the '#' from covid19
        twt = re.sub('#COVID', 'COVID', twt) # Removes the '#' from covid19
        twt = re.sub('#covid', 'covid', twt) # Removes the '#' from covid19
        twt = re.sub('#covid19', 'covid19', twt) # Removes the '#' from covid19
        twt = re.sub('#Covid19', 'Covid19', twt) # Removes the '#' from Covid19
        twt = re.sub('#Covid-19', 'Covid-19', twt) # Removes the '#' from Covid19
        twt = re.sub('#covid19', 'covid-19', twt) # Removes the '#' from Covid19
        twt = re.sub('#Coronavirus', 'Coronavirus', twt) # Removes the '#' from Covid19
        twt = re.sub('#coronavirus', 'coronavirus', twt) # Removes the '#' from Covid19
        twt = re.sub('#[A-Za-z0-9]+', '', twt) #Removes any string with a '#'
        twt = re.sub('\\n', '', twt) #Removes the '\n' string
        twt = re.sub('https?:\/\/\S+', '', twt) #Removes any hyperlinks
        return twt
    else:
        return ""

#Clean the tweets
df['Cleaned_Tweet'] = df['Tweet'].apply(lambda x:cleanTwt(x))
print('finished cleaning tweets')

#Create a function to get the subjectivity
def getSubjectivity(twt):
    # Applying the NaiveBayesAnalyzer
    blob_object = TextBlob(twt, analyzer=NaiveBayesAnalyzer())
    # Running sentiment analysis
    analysis = blob_object.sentiment
    print(analysis)
    return TextBlob(twt).sentiment.subjectivity
#Create a function to get the polarity
def getPolarity(twt):
    return TextBlob(twt).sentiment.polarity

#Create two new columns called 'Subjectivity' & 'Polarity
df['Polarity'] = df['Cleaned_Tweet'].apply(getPolarity)

df['Subjectivity'] = df['Cleaned_Tweet'].apply(getSubjectivity)

print('finished getting subjectivity and polarity')

#Create a function to get the  text sentiment
def getSentiment(score):
    if score < 0:
        return 'Negative'
    elif score == 0:
        return 'Neutral'
    else:
        return 'Positive'

#Create a column to store the text sentiment
df['Sentiment'] = df['Polarity'].apply(getSentiment)

print('finished getting sentiment')

df.to_html('./pre3.html')


print('ending processing')
