from collections import Counter
from flask import Flask, request, render_template, jsonify
import pickle
import pandas as pd
import numpy as np
import requests
import re
from bs4 import BeautifulSoup
import argparse
import time
from splinter import Browser
import time
from collections import defaultdict
import json
import re
import requests
import boto3
from boto3.dynamodb.conditions import Key, Attr
import json
from decimal import Decimal

from cleaner import Cleaner
import fantasy_scoring as fs

if __name__ == '__main__':
    f = open('.env','r')
    env = {}
    print('reading env variables')
    for line in f.readlines():
        env[line.strip().split("=")[0]]=line.strip().split("=")[1]
    dynamodb = boto3.resource('dynamodb', region_name='us-east-1',aws_access_key_id = env['aws_access_key_id'],
        aws_secret_access_key = env['aws_secret_access_key'])
    table = dynamodb.Table('nba_bbref')
    print("env")
    print(env)

    data1 = pd.read_csv("data/bb_reference/2016to2019Data_merged.csv", encoding = 'latin-1')
    data2 = pd.read_csv("data/bb_reference/2013to2015Data_merged.csv", encoding = 'latin-1')
    data = data1.append(data2)
    data = data.drop(['Unnamed: 0_y','Unnamed: 0'], axis = 1)
    data = data.rename(columns={'Unnamed: 0_x':'gamescore_rank'})
    clnr = Cleaner()
    data = clnr.transform(data)

    pe = "slug, #dt, minutes_07_sum"
    ea = {"#dt":"date"}

    data['date']=data['dt'].apply(lambda x: x.strftime("%Y-%m-%d"))
    players = data['slug'].unique()
    names = data['player'].unique()
    slug_names = {}
    name_slugs = {}
    for row in data[['slug','player']].groupby('slug').agg('first').iterrows():
        slug_names[row[0]]=row[1]['player']
        name_slugs[row[1]['player']]=row[0]
    lags = [7]
    data = data.sort_values(by='date',axis = 0)
    for player in players[0:200]:
        kce = Key('slug').eq(player)
        resp = table.query(IndexName = 'slug-date-index', KeyConditionExpression = kce,
                ExpressionAttributeNames =ea,
                ProjectionExpression = pe,
                ScanIndexForward = False,
                Limit = 1
                )['Items']
        if len(resp)==0:
            print("{} messed up".format(slug_names[player]))
        elif 'minutes_07_sum' in resp[0].keys():
            print("{} already done".format(slug_names[player]))
        else:
            print("working on {}".format(slug_names[player]))
            now = time.time()
            for lag in lags:
                single = data[data['slug']==player]
                lag_df = clnr.time_stats(single,lag = lag)
                if len(lag_df)>0:

                    lag_df['date']=single['date'].values
                    lag_df['slug']=single['slug'].values
                    lag_df['id']= lag_df['date']+lag_df['slug']
                    lag_df =lag_df.drop(labels = ['dt'],axis = 1)
                    lag_df['name']=slug_names[player]
                    for ind, elem in enumerate(lag_df.iloc[0,:]):
                        if (str(type(elem))=="<class 'numpy.float64'>"):
                            lag_df.iloc[:,ind] = lag_df.iloc[:,ind].apply(lambda x : Decimal(x).quantize(Decimal('.001')))
                    dict_row = lag_df.iloc[0,:].to_dict()
                    key  = dict_row.pop('id')
                    ean = {"#"+key : key for key in dict_row.keys()}
                    ue = "SET " + ', '.join(["#"+key +" = :"+key for key in dict_row.keys()])
                    with table.batch_writer() as batch:
                        for row in lag_df.iterrows():
                            dict_row = row[1].to_dict()
                            key  = dict_row.pop('id')
                            eav = {":"+key : dict_row[key] for key in dict_row.keys()}
                            table.update_item(Key={'id':key},
                                     ExpressionAttributeNames = ean,
                                     ExpressionAttributeValues = eav,
                                     UpdateExpression = ue)
                print("done with {} lag ({})".format(lag,len(lag_df)))
            print("Done with {} in {:.01f}".format(slug_names[player],(time.time()-now)/60))
